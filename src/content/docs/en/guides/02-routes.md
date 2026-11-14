---
title: "Browse by role, failure, or interest"
sidebar:
  order: 2
---

## Role requirements

| Capability | Sections | Evidence to demonstrate |
| --- | --- | --- |
| VLA/VLM training and deployment | 2.1, 6.1–6.4 | Interface contract and offline replay |
| CT/SFT/RL | 2.1–2.2, 6.3 | Loss masks and stage timing |
| Distributed training | 3.1–3.4 | DDP logs and batch accounting |
| IO and checkpoints | 2.3–2.4 | Input-supply comparisons and recovery checks |
| Graphs, memory, overlap | 4.1–4.4, 3.4 | Traces, memory budgets, controlled comparisons |
| Export, quantization, TensorRT | 5.2–5.3 | Output alignment and quality/performance table |
| Serving and end-to-end work | 1.4, 5.4, 6.4 | p50/p95, throughput, queue time |
| Kernel/Plugin bonus | 4.4 | Correctness and timing across shapes |
| Attention/KV bonus | 5.1 | Capacity estimate and concurrency experiment |

## Start from a failure

- **OOM on the first step:** read the [memory budget](/Infra/en/01-foundations/03/) and [memory/graphs](/Infra/en/04-performance/03/).
- **GPU keeps waiting:** inspect [data IO](/Infra/en/02-training/03/) and [profiling](/Infra/en/04-performance/01/).
- **Multiple cards hang:** read [DDP](/Infra/en/03-distributed/01/) and [NCCL](/Infra/en/03-distributed/04/); locate the earliest failed rank.
- **Slow first token or limited concurrency:** inspect [KV caching](/Infra/en/05-inference/01/) and [serving](/Infra/en/05-inference/04/).
- **Fast model, slow robot:** examine the [end-to-end budget](/Infra/en/06-embodied/04/), observation age, queues, and stale results.

## Similar names, different responsibilities

Triton the language writes GPU kernels. Triton Inference Server deploys models. TensorRT optimizes and executes inference on target hardware. TRT-LLM focuses on language models and should not be assumed to cover an arbitrary embodied network.

FSDP and Megatron provide different training-system components or approaches. verl organizes LLM RL data flows and can integrate training/inference backends. Choose from the task and bottleneck, not from the acronym list.
