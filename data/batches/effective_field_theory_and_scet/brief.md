# Batch Brief: Effective Field Theory and SCET

## Goal

Build a first-pass reusable neighborhood for effective field theory, heavy-quark effective theory, and SCET-style scale separation.

This batch should stay disciplined around the core EFT workflow, reuse the classical-field action language where helpful, and avoid expanding into a full renormalization or factorization-proof atlas.

## Target Topic

- `effective field theory and SCET`

## Batch Purpose

This batch is meant to capture the minimum defensible structure needed to read later Schwartz-style EFT material:

- scale separation,
- operator expansion and power counting,
- matching and RG flow,
- HQET-style heavy-quark language,
- and SCET-style mode scaling with hard/jet/soft structure.

## In Scope

Likely high-value topics include:

- effective field theory as a scale-separated description
- operator expansions and higher-dimensional operators
- power counting
- matching between theories
- renormalization-group running and large-log resummation
- heavy-quark effective theory and heavy-quark symmetry
- SCET, mode scaling, collinear modes, and soft modes
- hard, jet, and soft functions where they clearly support the branch structure

## Explicitly Out of Scope

- full factorization proofs
- detailed resummation derivations
- flavor EFT and SMEFT unless a source passage forces them in
- lattice EFT
- broad QCD or renormalization umbrellas that do not sharpen the EFT slice

## Task Model

- `literature_reading`

## Target Mastery Modes

- `recognize`
- `use`

## Audience/Profile Assumption

- `hep_th_grad`
- subfield focus: `effective_field_theory`

## Expected Batch Size

- approximately 12 to 18 nodes
- approximately 14 to 20 dependency edges
- a modest branch structure centered on EFT, HQET, and SCET

## Review Risks

- turning EFT into a generic renormalization batch
- losing the distinction between HQET and SCET branches
- importing factorization proof machinery too early
- treating mode scaling as a free-standing buzzword instead of a reusable branch

## Deliverable for This Batch

A clean first-pass EFT neighborhood that can support later renormalization, QCD, and factorization work without overcommitting to detailed proof machinery.
