# Source Notes: Gauge Invariance and Ward/BRST Structure

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `gauge invariance and Ward/BRST structure` should be understood as the standard
QFT gauge-redundancy slice:

- local gauge invariance as the redundancy that makes gauge fixing necessary,
- Ward and Ward-Takahashi identities as the symmetry constraints on correlators or generating
  functionals,
- Faddeev-Popov gauge fixing as the measure/Jacobian correction to the gauge orbit,
- BRST symmetry as the nilpotent symmetry of the gauge-fixed theory,
- and BRST cohomology / Slavnov-Taylor identities as the reusable downstream language.

This batch is intended to support textbook, lecture-note, and paper reading in the QFT and
Schwartz settings, not a full anomaly or lattice-gauge-fixing program.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize gauge invariance as a property of the Yang-Mills action and the gauge-field
  transformation language,
- read the Ward-Takahashi family as functional identities rather than generic symmetry slogans,
- and use the gauge-fixed BRST/Faddeev-Popov machinery when a source passage moves beyond the
  invariant classical action.

The batch is not trying to capture:

- all non-Abelian gauge theory,
- anomaly cancellation,
- renormalization-group machinery,
- or a full classification of gauge choices beyond the first reusable families.

## Likely High-Value Node Candidates

The most likely node candidates are:

- gauge invariance
- Ward-Takahashi identity, using the existing canonical node rather than a duplicate Ward node
- Faddeev-Popov determinant
- BRST symmetry
- BRST cohomology
- Slavnov-Taylor identity
- Lorenz gauge
- Coulomb gauge
- `R_xi` gauge

Likely reuse nodes that should stay canonical rather than be cloned:

- `qft.yang_mills_action`
- `qft.non_abelian_gauge_symmetry`
- `qft.gauge_fixing`
- `qft.ghost_field`
- `qft.path_integral_and_generating_functionals`
- `qft.ward_takahashi_identity`

## Likely Edge Patterns

High-value dependency patterns probably include:

- Yang-Mills action or local gauge symmetry into gauge-invariance language
- gauge invariance into Ward-Takahashi identities
- path-integral / source-functional machinery into the Ward identity branch
- gauge invariance into gauge fixing
- gauge fixing into the Faddeev-Popov determinant
- the Faddeev-Popov determinant into the ghost-field branch
- gauge fixing into BRST symmetry
- BRST symmetry into BRST cohomology and Slavnov-Taylor identities
- gauge fixing into the standard Lorenz/Coulomb/`R_xi` choice families

## Source Guidance

Prioritize introductory QFT and gauge-theory passages that explicitly:

- write the gauge transformation on the fields,
- impose a gauge condition,
- introduce the Faddeev-Popov determinant or ghost sector,
- derive Ward or Ward-Takahashi identities from the symmetry,
- and state BRST as the symmetry of the gauge-fixed action.

Prefer a small source set with stable terminology over broad gauge-theory surveys or a premature
jump into anomaly and renormalization discussions.

## Anti-Patterns

Avoid:

- creating a separate Ward node when the existing Ward-Takahashi node already carries the
  reusable role,
- splitting Faddeev-Popov ghosts away from the existing ghost-field node without a real dependency
  distinction,
- collapsing the gauge-fixing families into one generic gauge-choice bucket,
- importing anomalies too early,
- and treating BRST as a decorative label rather than the symmetry that organizes the gauge-fixed
  theory.

## Evidence Guidance

Use evidence that shows:

- where the gauge redundancy is stated,
- how the gauge condition is imposed,
- how the Faddeev-Popov determinant arises,
- how ghosts are introduced to represent it,
- how the Ward identity is derived,
- and how BRST or Slavnov-Taylor language is introduced in the gauge-fixed setting.

If a candidate feels like it belongs in later anomaly or gauge-fixing refinement batches, flag it
rather than forcing it into this first-pass slice.
