#include <algorithm>
#include <cfloat>
#include <cmath>
#include <iostream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include <arbor/assert.hpp>
#include <arbor/common_types.hpp>
#include <arbor/constants.hpp>
#include <arbor/fvm_types.hpp>
#include <arbor/math.hpp>
#include <arbor/simd/simd.hpp>

#include "backends/event.hpp"
#include "io/sepval.hpp"
#include "util/index_into.hpp"
#include "util/padded_alloc.hpp"
#include "util/rangeutil.hpp"

#include "multi_event_stream.hpp"
#include "multicore_common.hpp"
#include "shared_state.hpp"

namespace arb {
namespace multicore {

constexpr unsigned vector_length = (unsigned) simd::simd_abi::native_width<fvm_value_type>::value;
using simd_value_type = simd::simd<fvm_value_type, vector_length, simd::simd_abi::default_abi>;
using simd_index_type = simd::simd<fvm_index_type, vector_length, simd::simd_abi::default_abi>;
const int simd_width  = simd::width<simd_value_type>();

// Pick alignment compatible with native SIMD width for explicitly
// vectorized operations below.
//
// TODO: Is SIMD use here a win? Test and compare; may be better to leave
// these up to the compiler to optimize/auto-vectorize.

inline unsigned min_alignment(unsigned align) {
    unsigned simd_align = sizeof(fvm_value_type)*simd_width;
    return math::next_pow2(std::max(align, simd_align));
}

using pad = util::padded_allocator<>;

// ion_state methods:

ion_state::ion_state(
    int charge,
    const fvm_ion_config& ion_data,
    unsigned align
):
    alignment(min_alignment(align)),
    node_index_(ion_data.cv.begin(), ion_data.cv.end(), pad(alignment)),
    iX_(ion_data.cv.size(), NAN, pad(alignment)),
    eX_(ion_data.init_revpot.begin(), ion_data.init_revpot.end(), pad(alignment)),
    Xi_(ion_data.cv.size(), NAN, pad(alignment)),
    Xo_(ion_data.cv.size(), NAN, pad(alignment)),
    init_Xi_(ion_data.init_iconc.begin(), ion_data.init_iconc.end(), pad(alignment)),
    init_Xo_(ion_data.init_econc.begin(), ion_data.init_econc.end(), pad(alignment)),
    reset_Xi_(ion_data.reset_iconc.begin(), ion_data.reset_iconc.end(), pad(alignment)),
    reset_Xo_(ion_data.reset_econc.begin(), ion_data.reset_econc.end(), pad(alignment)),
    init_eX_(ion_data.init_revpot.begin(), ion_data.init_revpot.end(), pad(alignment)),
    charge(1u, charge, pad(alignment))
{
    arb_assert(node_index_.size()==init_Xi_.size());
    arb_assert(node_index_.size()==init_Xo_.size());
    arb_assert(node_index_.size()==eX_.size());
    arb_assert(node_index_.size()==init_eX_.size());
}

void ion_state::init_concentration() {
    std::copy(init_Xi_.begin(), init_Xi_.end(), Xi_.begin());
    std::copy(init_Xo_.begin(), init_Xo_.end(), Xo_.begin());
}

void ion_state::zero_current() {
    util::fill(iX_, 0);
}

void ion_state::reset() {
    zero_current();
    std::copy(reset_Xi_.begin(), reset_Xi_.end(), Xi_.begin());
    std::copy(reset_Xo_.begin(), reset_Xo_.end(), Xo_.begin());
    std::copy(init_eX_.begin(), init_eX_.end(), eX_.begin());
}

// istim_state methods:

istim_state::istim_state(const fvm_stimulus_config& stim, unsigned align):
    alignment(min_alignment(align)),
    accu_to_cv_(stim.cv_unique.begin(), stim.cv_unique.end(), pad(alignment)),
    frequency_(stim.frequency.begin(), stim.frequency.end(), pad(alignment)),
    phase_(stim.phase.begin(), stim.phase.end(), pad(alignment))
{
    using util::assign;

    // Translate instance-to-CV index from stim to istim_state index vectors.
    assign(accu_index_, util::index_into(stim.cv, accu_to_cv_));
    accu_stim_.resize(accu_to_cv_.size());

    std::size_t n = accu_index_.size();
    std::vector<fvm_value_type> envl_a, envl_t;
    std::vector<fvm_index_type> edivs;

    arb_assert(n==frequency_.size());
    arb_assert(n==stim.envelope_time.size());
    arb_assert(n==stim.envelope_amplitude.size());

    edivs.reserve(n+1);
    edivs.push_back(0);

    for (auto i: util::make_span(n)) {
        arb_assert(stim.envelope_time[i].size()==stim.envelope_amplitude[i].size());
        arb_assert(util::is_sorted(stim.envelope_time[i]));

        util::append(envl_a, stim.envelope_amplitude[i]);
        util::append(envl_t, stim.envelope_time[i]);
        edivs.push_back(fvm_index_type(envl_t.size()));
    }

    assign(envl_amplitudes_, envl_a);
    assign(envl_times_, envl_t);
    assign(envl_divs_, edivs);
    envl_index_.assign(edivs.data(), edivs.data()+n);
}

void istim_state::zero_current() {
    util::fill(accu_stim_, 0);
}

void istim_state::reset() {
    zero_current();

    std::size_t n = envl_index_.size();
    std::copy(envl_divs_.data(), envl_divs_.data()+n, envl_index_.begin());
}

void istim_state::add_current(const array& time, const iarray& cv_to_intdom, array& current_density) {
    constexpr double two_pi = 2*math::pi<double>;

    // Consider vectorizing...
    for (auto i: util::count_along(accu_index_)) {
        // Advance index into envelope until either
        // - the next envelope time is greater than simulation time, or
        // - it is the last valid index for the envelope.

        fvm_index_type ei_left = envl_divs_[i];
        fvm_index_type ei_right = envl_divs_[i+1];

        fvm_index_type ai = accu_index_[i];
        fvm_index_type cv = accu_to_cv_[ai];
        double t = time[cv_to_intdom[cv]];

        if (ei_left==ei_right || t<envl_times_[ei_left]) continue;

        fvm_index_type& ei = envl_index_[i];
        while (ei+1<ei_right && envl_times_[ei+1]<=t) ++ei;

        double J = envl_amplitudes_[ei]; // current density (A/m²)
        if (ei+1<ei_right) {
            // linearly interpolate:
            arb_assert(envl_times_[ei]<=t && envl_times_[ei+1]>t);
            double J1 = envl_amplitudes_[ei+1];
            double u = (t-envl_times_[ei])/(envl_times_[ei+1]-envl_times_[ei]);
            J = math::lerp(J, J1, u);
        }

        if (frequency_[i]) {
            J *= std::sin(two_pi*frequency_[i]*t + phase_[i]);
        }

        accu_stim_[ai] += J;
        current_density[cv] -= J;
    }
}

// shared_state methods:

shared_state::shared_state(
    fvm_size_type n_intdom,
    fvm_size_type n_cell,
    fvm_size_type n_detector,
    const std::vector<fvm_index_type>& cv_to_intdom_vec,
    const std::vector<fvm_index_type>& cv_to_cell_vec,
    const std::vector<fvm_gap_junction>& gj_vec,
    const std::vector<fvm_value_type>& init_membrane_potential,
    const std::vector<fvm_value_type>& temperature_K,
    const std::vector<fvm_value_type>& diam,
    const std::vector<fvm_index_type>& src_to_spike,
    unsigned align
):
    alignment(min_alignment(align)),
    alloc(alignment),
    n_intdom(n_intdom),
    n_detector(n_detector),
    n_cv(cv_to_intdom_vec.size()),
    n_gj(gj_vec.size()),
    cv_to_intdom(math::round_up(n_cv, alignment), pad(alignment)),
    cv_to_cell(math::round_up(cv_to_cell_vec.size(), alignment), pad(alignment)),
    gap_junctions(math::round_up(n_gj, alignment), pad(alignment)),
    time(n_intdom, pad(alignment)),
    time_to(n_intdom, pad(alignment)),
    dt_intdom(n_intdom, pad(alignment)),
    dt_cv(n_cv, pad(alignment)),
    voltage(n_cv, pad(alignment)),
    current_density(n_cv, pad(alignment)),
    conductivity(n_cv, pad(alignment)),
    init_voltage(init_membrane_potential.begin(), init_membrane_potential.end(), pad(alignment)),
    temperature_degC(n_cv, pad(alignment)),
    diam_um(diam.begin(), diam.end(), pad(alignment)),
    time_since_spike(n_cell*n_detector, pad(alignment)),
    src_to_spike(src_to_spike.begin(), src_to_spike.end(), pad(alignment)),
    deliverable_events(n_intdom)
{
    // For indices in the padded tail of cv_to_intdom, set index to last valid intdom index.
    if (n_cv>0) {
        std::copy(cv_to_intdom_vec.begin(), cv_to_intdom_vec.end(), cv_to_intdom.begin());
        std::fill(cv_to_intdom.begin() + n_cv, cv_to_intdom.end(), cv_to_intdom_vec.back());
    }
    if (cv_to_cell_vec.size()) {
        std::copy(cv_to_cell_vec.begin(), cv_to_cell_vec.end(), cv_to_cell.begin());
        std::fill(cv_to_cell.begin() + n_cv, cv_to_cell.end(), cv_to_cell_vec.back());
    }
    if (n_gj>0) {
        std::copy(gj_vec.begin(), gj_vec.end(), gap_junctions.begin());
        std::fill(gap_junctions.begin()+n_gj, gap_junctions.end(), gj_vec.back());
    }

    util::fill(time_since_spike, -1.0);
    for (unsigned i = 0; i<n_cv; ++i) {
        temperature_degC[i] = temperature_K[i] - 273.15;
    }
}

void shared_state::add_ion(
    const std::string& ion_name,
    int charge,
    const fvm_ion_config& ion_info)
{
    ion_data.emplace(std::piecewise_construct,
        std::forward_as_tuple(ion_name),
        std::forward_as_tuple(charge, ion_info, alignment));
}

void shared_state::configure_stimulus(const fvm_stimulus_config& stims) {
    stim_data = istim_state(stims, alignment);
}

void shared_state::reset() {
    std::copy(init_voltage.begin(), init_voltage.end(), voltage.begin());
    util::fill(current_density, 0);
    util::fill(conductivity, 0);
    util::fill(time, 0);
    util::fill(time_to, 0);
    util::fill(time_since_spike, -1.0);

    for (auto& i: ion_data) {
        i.second.reset();
    }

    stim_data.reset();
}

void shared_state::zero_currents() {
    util::fill(current_density, 0);
    util::fill(conductivity, 0);
    for (auto& i: ion_data) {
        i.second.zero_current();
    }
    stim_data.zero_current();
}

void shared_state::ions_init_concentration() {
    for (auto& i: ion_data) {
        i.second.init_concentration();
    }
}

void shared_state::update_time_to(fvm_value_type dt_step, fvm_value_type tmax) {
    using simd::assign;
    using simd::indirect;
    using simd::add;
    using simd::min;
    for (fvm_size_type i = 0; i<n_intdom; i+=simd_width) {
        simd_value_type t;
        assign(t, indirect(time.data()+i, simd_width));
        t = min(add(t, dt_step), tmax);
        indirect(time_to.data()+i, simd_width) = t;
    }
}

void shared_state::set_dt() {
    using simd::assign;
    using simd::indirect;
    using simd::sub;
    for (fvm_size_type j = 0; j<n_intdom; j+=simd_width) {
        simd_value_type t, t_to;
        assign(t, indirect(time.data()+j, simd_width));
        assign(t_to, indirect(time_to.data()+j, simd_width));

        auto dt = sub(t_to,t);
        indirect(dt_intdom.data()+j, simd_width) = dt;
    }

    for (fvm_size_type i = 0; i<n_cv; i+=simd_width) {
        simd_index_type intdom_idx;
        assign(intdom_idx, indirect(cv_to_intdom.data()+i, simd_width));

        simd_value_type dt;
        assign(dt, indirect(dt_intdom.data(), intdom_idx, simd_width));
        indirect(dt_cv.data()+i, simd_width) = dt;
    }
}

void shared_state::add_gj_current() {
    for (unsigned i = 0; i < n_gj; i++) {
        auto gj = gap_junctions[i];
        auto curr = gj.weight *
                    (voltage[gj.loc.second] - voltage[gj.loc.first]); // nA

        current_density[gj.loc.first] -= curr;
    }
}

void shared_state::add_stimulus_current() {
     stim_data.add_current(time, cv_to_intdom, current_density);
}

std::pair<fvm_value_type, fvm_value_type> shared_state::time_bounds() const {
    return util::minmax_value(time);
}

std::pair<fvm_value_type, fvm_value_type> shared_state::voltage_bounds() const {
    return util::minmax_value(voltage);
}

void shared_state::take_samples(
    const sample_event_stream::state& s,
    array& sample_time,
    array& sample_value)
{
    for (fvm_size_type i = 0; i<s.n_streams(); ++i) {
        auto begin = s.begin_marked(i);
        auto end = s.end_marked(i);

        // Null handles are explicitly permitted, and always give a sample of zero.
        // (Note: probably not worth explicitly vectorizing this.)
        for (auto p = begin; p<end; ++p) {
            sample_time[p->offset] = time[i];
            sample_value[p->offset] = p->handle? *p->handle: 0;
        }
    }
}

// (Debug interface only.)
std::ostream& operator<<(std::ostream& out, const shared_state& s) {
    using io::csv;

    out << "n_intdom     " << s.n_intdom << "\n";
    out << "n_cv         " << s.n_cv << "\n";
    out << "cv_to_intdom " << csv(s.cv_to_intdom) << "\n";
    out << "time         " << csv(s.time) << "\n";
    out << "time_to      " << csv(s.time_to) << "\n";
    out << "dt_intdom    " << csv(s.dt_intdom) << "\n";
    out << "dt_cv        " << csv(s.dt_cv) << "\n";
    out << "voltage      " << csv(s.voltage) << "\n";
    out << "init_voltage " << csv(s.init_voltage) << "\n";
    out << "temperature  " << csv(s.temperature_degC) << "\n";
    out << "diameter     " << csv(s.diam_um) << "\n";
    out << "current      " << csv(s.current_density) << "\n";
    out << "conductivity " << csv(s.conductivity) << "\n";
    for (const auto& ki: s.ion_data) {
        auto& kn = ki.first;
        auto& i = ki.second;
        out << kn << "/current_density        " << csv(i.iX_) << "\n";
        out << kn << "/reversal_potential     " << csv(i.eX_) << "\n";
        out << kn << "/internal_concentration " << csv(i.Xi_) << "\n";
        out << kn << "/external_concentration " << csv(i.Xo_) << "\n";
        out << kn << "/intconc_initial        " << csv(i.init_Xi_) << "\n";
        out << kn << "/extconc_initial        " << csv(i.init_Xo_) << "\n";
        out << kn << "/revpot_initial         " << csv(i.init_eX_) << "\n";
        out << kn << "/node_index             " << csv(i.node_index_) << "\n";
    }

    return out;
}

} // namespace multicore
} // namespace arb
