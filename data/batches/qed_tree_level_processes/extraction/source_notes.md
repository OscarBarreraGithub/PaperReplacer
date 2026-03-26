# Source Notes: QED Tree-Level Processes

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `qed tree-level processes` should be understood as the standard QED exemplar neighborhood used throughout Schwartz-style QFT examples:

- Bhabha scattering
- Moller scattering
- Compton scattering
- electron-positron to muon-antimuon scattering
- light-by-light scattering
- equivalent photon approximation
- Mott formula

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize the named QED exemplar processes and result-like nodes when they appear,
- follow the process-sensitive logic behind them,
- and keep them distinct from generic scattering machinery that belongs in the cross-section and phase-space batch.

The batch is not trying to capture:

- cross sections or phase-space formulas,
- decay rates,
- renormalization or loop corrections,
- scalar QED as a separate branch,
- gauge-fixing or Ward-identity machinery,
- or a complete QED foundations chapter.

## Likely Reuse Candidates

Reuse the canonical ids that already do real work in the earlier batches instead of minting duplicates:

- `qft.free_fields_and_quantization`
- `qft.free_dirac_field`
- `qft.free_vector_field`
- `qft.spinor_lorentz_dirac_foundations`
- `qft.correlators_propagators_lsz`
- `qft.feynman_rules`

These should be treated as shared background or prerequisite anchors, not as new tree-level QED-only topic nodes.

## Likely New Node Candidates

The most likely new node candidates are:

- `qft.qed_tree_level_processes`
- `qed.bhabha_scattering`
- `qed.moller_scattering`
- `qed.compton_scattering`
- `qed.electron_positron_to_muon_antimuon`
- `qed.light_by_light_scattering`
- `qed.equivalent_photon_approximation`
- `qed.mott_formula`

## Deliberate Non-Additions

Do not fold generic cross-section machinery into this batch just because a source uses it in the same chapter neighborhood.
Likewise, do not spin up separate nodes for formula labels, historical names, or low-level textbook variants when the same process is already captured by a stable canonical node.

## Likely Edge Patterns

High-value dependency patterns probably include:

- free Dirac or vector field vocabulary into the named process examples
- Feynman rules into the tree-level amplitude calculations
- correlator/LSZ vocabulary into the scattering interpretation of the process neighborhood

The batch should own process-sensitive formulas or approximations when the meaning changes with the external particle content or channel, for example the Mott formula or the equivalent photon approximation.

## Source Guidance

Prioritize introductory QFT passages that explicitly name the tree-level QED examples and write them in the standard scattering-language and channel notation.

Prefer a small source set with stable terminology over broad secondary references or a loop-heavy discussion that would blur the tree-level boundary.

## Anti-Patterns

Avoid:

- drifting into cross-section or decay formulas,
- importing gauge-fixing or Ward-identity machinery too early,
- duplicating the same scattering example under several near-synonymous labels,
- and turning the batch into a chapter mirror instead of a reusable process neighborhood.

## Evidence Guidance

Use evidence that shows:

- which named processes recur as standard tree-level examples,
- how the amplitude is written in terms of the usual QED rules,
- where the shared kinematic invariants are introduced,
- and which examples are only low-energy or classical limits of the same scattering logic.

If a candidate feels like a generic cross-section batch item or a notation-only variant, defer it instead of forcing it into this first-pass process slice.
