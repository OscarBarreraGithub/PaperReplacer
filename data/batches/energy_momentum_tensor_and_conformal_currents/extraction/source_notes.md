# Source Notes: Energy-Momentum Tensor and Conformal Currents

Primary Schwartz coverage pressure for this batch comes from:

- page 869 triage, where `energy-momentum tensor` and `canonical` were marked as
  candidate-batch-expansion items
- the follow-on queue after the Stage 6 checkpoint, which identified energy-momentum tensor
  cleanup as a high-yield next refinement

Observed overlap anchors already in the authored graph:

- `classical_fields.noether_theorem`
- `qft.scale_invariance`
- `qft.conformal_invariance`
- `qft.weyl_invariance`

Batch-shaping decisions:

- keep the tensor nodes in the `classical_fields.*` namespace because they arise first as
  Noether-current objects and connect cleanly to the existing variational trunk
- keep the batch centered on current language rather than opening a full trace-anomaly or
  conformal-field-theory branch
- use scale, conformal, and Weyl invariance as reused endpoints rather than rederiving the
  whole critical-phenomena batch
