# Source Notes: Effective Actions and Background Fields

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `effective actions and background fields` should be understood in the standard QFT sense:

- the 1PI effective action as the source-dependent functional that organizes quantum corrections,
- background-field methods as a way to compute or organize that effective action,
- effective potentials as the constant-background specialization,
- and one-loop functional techniques such as determinants and Schwinger-style representations.

This batch is intended to support paper, lecture-note, and textbook reading in the QFT foundation setting, not a full renormalization or gauge-fixing reconstruction.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize the effective-action and 1PI vocabulary,
- follow background-field calculations without losing the underlying functional picture,
- and use the one-loop and effective-potential machinery when the source expects it.

The batch is not trying to capture:

- the whole path-integral formalism again,
- a full RG or subtraction theory,
- detailed BRST or gauge-fixing structure,
- or SM-specific Higgs potential work unless a source passage explicitly narrows the discussion there.

## Likely High-Value Node Candidates

The most likely node candidates are:

- effective actions and background fields
- effective action
- 1PI effective action as an alias of the same canonical node
- connected generating functional reuse from the path-integral batch
- background field
- background-field method
- one-loop effective action
- effective potential
- functional determinant
- Schwinger proper-time method
- Schwinger parameter
- renormalized perturbation theory when the source makes the effective-potential branch scale-sensitive

## Likely Edge Patterns

High-value dependency patterns probably include:

- connected generating functional into the effective-action node
- action-functional background into the effective-action branch
- background field into the background-field method
- background-field method into the one-loop effective-action branch
- functional determinant into the one-loop effective-action branch
- Schwinger proper-time or Schwinger-parameter language into the determinant branch
- effective action into effective potential
- renormalized perturbation theory into effective potential

## Source Guidance

Prioritize Schwartz-style passages that explicitly define the effective action, introduce the background-field split, and then compute or approximate the effective potential.

Prefer a small source set with stable terminology over broad secondary references or a premature jump into later Higgs-sector specializations.

## Anti-Patterns

Avoid:

- collapsing the batch into generic path-integral language,
- turning effective action into a duplicate of the source-coupled generating functional,
- forcing a dedicated Higgs-potential node when the source only says `effective potential`,
- importing full gauge-fixing or renormalization machinery without direct evidence,
- and treating Schwinger proper-time and Schwinger parameter as more different than the source actually does.

## Evidence Guidance

Use evidence that shows:

- how the effective action is introduced from the connected generating functional,
- which background field or background split is being used,
- how the one-loop determinant is written,
- and where the effective potential is read off from a constant background.

If a candidate feels like it belongs in a later Standard Model, EFT, or RG branch, flag it instead of forcing it into this first-pass slice.
