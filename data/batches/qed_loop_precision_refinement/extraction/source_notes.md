# Source Notes: QED Loop Precision Refinement

Primary Schwartz coverage pressure for this batch comes from:

- the extracted index entry `electron self-energy, 322–338`
- the extracted index entry `g-factor, 315`
- the extracted index entry `Uehling potential, 311`
- page 864 triage, where `electron self-energy` remained a direct candidate-new-node item

Observed overlap anchors already in the authored graph:

- `qft.renormalized_perturbation_theory`
- `qft.spinor_lorentz_dirac_foundations`
- `qft.free_dirac_field`
- `sm.precision.gauge_boson_self_energy`

Batch-shaping decisions:

- use a compact dedicated QED loop-precision slice rather than trying to force these payoff
  nodes under the tree-level QED process root
- keep `qed.electron_self_energy` as the electron-sector loop correction node that anchors
  the batch
- use `qed.anomalous_magnetic_moment` as the main precision payoff node and absorb the
  `g-factor` pressure there as adjacent aliasing language rather than creating a separate
  generic `g_factor` node
- reuse the existing `sm.precision.gauge_boson_self_energy` node as the vacuum-polarization
  bridge for `qed.uehling_potential`, instead of minting a duplicate QED-only
  vacuum-polarization node
