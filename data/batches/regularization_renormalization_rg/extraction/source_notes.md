# Source Notes: Regularization, Renormalization, and RG

These notes are batch-specific extraction context, not canonical graph facts.

## Intended Reading of the Topic

For this batch, `regularization, renormalization, and RG` should be understood in the standard perturbative-QFT sense:

- ultraviolet divergences in loop amplitudes or Green functions,
- a regulator that makes the intermediate expressions well-defined,
- counterterms that absorb the regulator dependence,
- renormalized perturbation theory with finite observables,
- and the flow of parameters with renormalization scale.

This batch is intended to support textbook, lecture-note, and paper reading in the QFT foundation setting, not a full EFT or nonperturbative renormalization program.

## What the Batch Is Trying to Capture

This batch should identify the smallest defensible prerequisite slice needed to:

- recognize UV-divergence language,
- follow regularization and subtraction steps,
- and use the standard RG equations that describe running parameters and operator dimensions.

The batch is not trying to capture:

- EFT matching and operator bases as the main story,
- gauge-fixing subtleties as a separate branch,
- infrared resummation,
- or nonperturbative renormalization.

## Likely High-Value Node Candidates

The most likely node candidates are:

- ultraviolet divergence
- dimensional regularization
- counterterm Lagrangian
- renormalized perturbation theory
- renormalization scale
- beta function
- anomalous dimension
- renormalization-group equation
- Wilsonian RG
- Callan-Symanzik equation

## Likely Edge Patterns

High-value dependency patterns probably include:

- UV-divergence recognition into regularization language
- dimensional regularization into renormalized perturbation theory
- counterterm Lagrangians into renormalized perturbation theory
- renormalization scale into beta functions and anomalous dimensions
- beta functions and anomalous dimensions into RG equations
- RG equations into Callan-Symanzik or Wilsonian flow statements

## Source Guidance

Prioritize perturbative-QFT passages that explicitly introduce the regulator, subtract divergences, define renormalized parameters, and then derive flow equations.

Prefer a small source set with stable terminology over scheme-specific overfitting or a premature shift into EFT matching language.

## Anti-Patterns

Avoid:

- treating the regularization choice as identical to the renormalization scheme,
- using counterterms without an explicit divergence problem,
- collapsing the batch into EFT or gauge-theory details,
- and reading RG equations as a generic pedagogical "things depend on scale" slogan rather than as concrete functional statements.

## Evidence Guidance

Use evidence that shows:

- where divergences are isolated,
- how the regulator is introduced,
- how counterterms cancel the divergent pieces,
- how renormalized parameters depend on scale,
- and how beta functions or anomalous dimensions are extracted.

If a candidate is really part of a later EFT, gauge-theory, or infrared branch, flag it rather than forcing it into this first-pass slice.
