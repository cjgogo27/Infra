---
title: "Start here: a four-week learning route"
sidebar:
  order: 1
---

Complete one explicit CPU path before adding GPUs, multiple cards, or robots. The default project uses repository models and synthetic data: no model selection, weight search, or GPU rental is required. Plan 8–12 hours weekly as a suggestion; acceptance criteria matter more than pages read.

## Week 1: one training update and one measurement

Follow [1.1 overview](/Infra/en/01-foundations/01/) → [Lab 0](/Infra/en/labs/00-training/) → [1.2 host/GPU](/Infra/en/01-foundations/02/) → [1.3 memory](/Infra/en/01-foundations/03/) → [1.4 metrics](/Infra/en/01-foundations/04/) → [Lab A](/Infra/en/labs/01-lab/).

Deliver parameter/gradient observations and two batch-size JSON records. Explain batch latency, amortized sample cost, and throughput before moving to FSDP or kernels.

## Week 2: correctness and performance evidence

Read [2.2 accumulation](/Infra/en/02-training/02/) and run [Lab E](/Infra/en/labs/05-accumulation/); read [2.4 checkpoints](/Infra/en/02-training/04/) and run [Lab B](/Infra/en/labs/02-resume/). Continue through [2.3 IO](/Infra/en/02-training/03/), [4.1 profiling](/Infra/en/04-performance/01/), [4.3 memory/graphs](/Infra/en/04-performance/03/), and [Lab G](/Infra/en/labs/07-profiler/).

Deliver an explanation of incorrect weighting, recovery verification, and a CPU trace-based hypothesis checked with an unprofiled baseline. Preserve negative results.

## Week 3: deploy a fixed model

Read [3.1 DDP](/Infra/en/03-distributed/01/) and [3.2 FSDP](/Infra/en/03-distributed/02/) for replication/sharding. Read [5.1 KV](/Infra/en/05-inference/01/) and [5.2 export](/Infra/en/05-inference/02/), then complete [Lab D](/Infra/en/labs/04-project/) using the fixed batch-eight MLP and ONNX/ORT CPU.

Deliver an exported file, numerical comparison, and backend performance table. Explain why export success does not guarantee acceleration. If export is blocked, record the limitation; reading documentation is not deployment experience.

## Week 4: embodied interfaces and interviews

Read [6.1 interfaces](/Infra/en/06-embodied/01/), [6.2 chunks](/Infra/en/06-embodied/02/), and [6.4 project evidence](/Infra/en/06-embodied/04/). Run [Lab F](/Infra/en/labs/06-replay/) with valid, wrong-unit, wrong-shape, and stale samples.

Deliver the contract, rejection records, a CPU project report, and answers to the [progressive interview cases](/Infra/en/appendix/interview/). Explain the problem, evidence, change, result, and limitation in three minutes. Synthetic replay is neither VLA training nor demonstrated robot control.

## Hardware and advanced branches

| Available environment | Additional exercise | Otherwise |
| --- | --- | --- |
| Compatible CUDA GPU | CUDA timing and memory in Lab A | Keep CPU findings; do not infer GPU speed |
| Linux, two GPUs, NCCL | [Lab C](/Infra/en/labs/03-ddp/) | Trace replicas/communication on paper; report no measured scaling |
| Completed CPU export, compatible TensorRT | GPU backend extension to Lab D | Stop at ORT CPU; retain numerical checks |
| Appropriate open model/data and resources | Offline vision/policy replay | Finish the synthetic LabBot contract first |

Skim advanced CP/EP, kernels, and complex RL on the first pass. Return in a second pass to [3.3](/Infra/en/03-distributed/03/), [3.4](/Infra/en/03-distributed/04/), [4.2](/Infra/en/04-performance/02/), [4.4](/Infra/en/04-performance/04/), [2.1](/Infra/en/02-training/01/), [5.3](/Infra/en/05-inference/03/), [5.4](/Infra/en/05-inference/04/), and [6.3](/Infra/en/06-embodied/03/). They are relevant without all becoming simultaneous projects.

## Interview tomorrow?

Read the problems and core explanations in 1.1, 1.3, 1.4, 2.2, 3.1, 3.2, 4.1, 5.1, and 6.1. Personally run Labs 0 and A, then attempt the three interview cases. Distinguish reading, execution, and independent optimization.
