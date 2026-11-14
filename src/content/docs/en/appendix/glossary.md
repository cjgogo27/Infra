---
title: "Terminology at a glance"
sidebar:
  order: 1
---

| Term | Meaning | Section |
| --- | --- | --- |
| Infra | Infrastructure for training, inference, and operation | 1.1 |
| Tensor / Activation | Multidimensional array / intermediate result | 1.3 |
| SLO / p95 | Service-level objective / 95th percentile | 1.4 |
| CT / SFT / RL | Continued training / supervised fine-tuning / reinforcement learning | 2.1 |
| AMP / BF16 / FP16 | Mixed precision / two 16-bit float formats | 2.2 |
| Microbatch / Accumulation | Small batch per pass / accumulated gradients | 2.2 |
| Prefetch / Pinned memory | Preparing data ahead / page-locked host memory | 2.3 |
| Checkpoint | Saved training state, or activation recomputation depending on context | 2.4, 4.3 |
| Rank / World size | Process identifier / group size | 3.1 |
| DDP / FSDP | Distributed data parallel / fully sharded data parallel | 3.1, 3.2 |
| TP / PP / CP / EP | Tensor / pipeline / context / expert parallelism | 3.3 |
| NCCL | NVIDIA collective communication library | 3.4 |
| Roofline | Performance model combining compute and bandwidth limits | 4.2 |
| Kernel / Fusion | Device program / combining operations | 4.4 |
| Prefill / Decode | Prompt processing / iterative generation | 5.1 |
| KV cache / GQA | Key-value cache / grouped-query Attention | 5.1 |
| ONNX / Engine | Model interchange representation / compiled execution artifact | 5.2 |
| PTQ / QAT | Post-training quantization / quantization-aware training | 5.3 |
| Backpressure | Limiting pending work entering a system | 5.4 |
| VLM / VLA | Vision-language / vision-language-action model | 6.1 |
| Action chunk | A sequence of future actions | 6.2 |
| Rollout / Policy lag | Policy sampling / policy-version staleness | 6.3 |

Search an unfamiliar term, then revisit its engineering scenario. Identical acronyms may have different meanings across teams and frameworks.
