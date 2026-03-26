# Source Notes: Path Integral and Generating Functionals

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `path integral and generating functionals` should be understood in the standard QFT sense:

- functional integration over field configurations,
- source-coupled generating functionals,
- correlators obtained from source derivatives,
- and the functional identities that arise from shifts or symmetries of the path integral.

This batch is intended to support textbook, lecture-note, and paper reading in the QFT foundation setting, not a full effective-action or renormalization treatment.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize the functional-integral setup,
- follow the source-dependent notation used to generate correlators,
- and use the standard functional identities that show up in perturbative QFT discussions.

The batch is not trying to capture:

- all of perturbation theory,
- the 1PI or effective-action branch as the main story,
- renormalization and RG,
- or gauge-fixing structure unless a source passage makes it unavoidable.

## Likely High-Value Node Candidates

The most likely node candidates are:

- classical action functional, when the exponentiated weight is being written
- functional measure
- source-coupled path integral
- generating functional
- connected generating functional
- Gaussian functional integral
- fermionic path integral
- source-derivative rule for correlators
- Schwinger-Dyson equation
- Ward-Takahashi identity
- `i epsilon`-related reuse when the source is Minkowski-signature and causal contour choices matter

## Likely Edge Patterns

High-value dependency patterns probably include:

- action functional into the source-coupled path integral
- functional measure into the source-coupled path integral
- Gaussian free-theory evaluation into the generating functional
- source derivatives of the generating functional into correlator identities
- source shifts or symmetry transformations into Schwinger-Dyson or Ward-Takahashi statements
- fermionic path integrals into the source-coupled and identity-level branches

## Source Guidance

Prioritize introductory QFT and functional-method passages that explicitly define the source-coupled integral and then derive correlators or identities from it.

Prefer a small source set with stable terminology over broad secondary references or an immediate jump to effective-action language.

## Anti-Patterns

Avoid:

- collapsing the batch into perturbation theory by default,
- turning the generating functional into an effective-action node too early,
- importing renormalization or RG machinery without direct evidence,
- and treating symmetry identities as generic algebra rather than as functional statements about the integral.

## Evidence Guidance

Use evidence that shows:

- how the source-dependent integral is written,
- which terms are treated as part of the exponent or measure,
- how source derivatives produce correlators,
- and which symmetry or shift argument generates a functional identity.

If a candidate feels like it belongs in the later effective-action or renormalization branches, flag it rather than forcing it into this first-pass slice.
