---
title: "Terminology at a glance"
sidebar:
  order: 1
---

| Term | Meaning | Section |
| --- | --- | --- |
| Infra | Infrastructure for training, inference, and operation | [1.1](/Infra/en/01-foundations/01/) |
| Tensor / Activation | Multidimensional array / intermediate result | [1.3](/Infra/en/01-foundations/03/) |
| SLO / p95 | Service-level objective / 95th percentile | [1.4](/Infra/en/01-foundations/04/) |
| CT / SFT / RL | Continued training / supervised fine-tuning / reinforcement learning | [2.1](/Infra/en/02-training/01/) |
| AMP / BF16 / FP16 | Mixed precision / two 16-bit float formats | [2.2](/Infra/en/02-training/02/) |
| Microbatch / Accumulation | Small batch per pass / accumulated gradients | [2.2](/Infra/en/02-training/02/) |
| Prefetch / Pinned memory | Preparing data ahead / page-locked host memory | [2.3](/Infra/en/02-training/03/) |
| Checkpoint | Saved training state, or activation recomputation depending on context | [2.4](/Infra/en/02-training/04/), [4.3](/Infra/en/04-performance/03/) |
| Rank / World size | Process identifier / group size | [3.1](/Infra/en/03-distributed/01/) |
| DDP / FSDP | Distributed data parallel / fully sharded data parallel | [3.1](/Infra/en/03-distributed/01/), [3.2](/Infra/en/03-distributed/02/) |
| TP / PP / CP / EP | Tensor / pipeline / context / expert parallelism | [3.3](/Infra/en/03-distributed/03/) |
| NCCL | NVIDIA collective communication library | [3.4](/Infra/en/03-distributed/04/) |
| Roofline | Performance model combining compute and bandwidth limits | [4.2](/Infra/en/04-performance/02/) |
| Kernel / Fusion | Device program / combining operations | [4.4](/Infra/en/04-performance/04/) |
| Prefill / Decode | Prompt processing / iterative generation | [5.1](/Infra/en/05-inference/01/) |
| KV cache / GQA | Key-value cache / grouped-query Attention | [5.1](/Infra/en/05-inference/01/) |
| ONNX / Engine | Model interchange representation / compiled execution artifact | [5.2](/Infra/en/05-inference/02/) |
| PTQ / QAT | Post-training quantization / quantization-aware training | [5.3](/Infra/en/05-inference/03/) |
| Backpressure | Limiting pending work entering a system | [5.4](/Infra/en/05-inference/04/) |
| VLM / VLA | Vision-language / vision-language-action model | [6.1](/Infra/en/06-embodied/01/) |
| Action chunk | A sequence of future actions | [6.2](/Infra/en/06-embodied/02/) |
| Rollout / Policy lag | Policy sampling / policy-version staleness | [6.3](/Infra/en/06-embodied/03/) |

Search an unfamiliar term, then revisit its engineering scenario. Identical acronyms may have different meanings across teams and frameworks.
