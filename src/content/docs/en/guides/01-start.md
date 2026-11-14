---
title: "Start here: a four-week learning route"
sidebar:
  order: 1
---

You do not need every framework at once. First explain where data and computation go, then measure them, then improve them. Budget 8–12 hours per week as a planning suggestion, not a guarantee.

## Week 1: make the single-machine system understandable

Read Chapters 1 and 2; run Labs A and B. Review Python context managers, iterators, processes, Linux memory, and tensor shapes. Work out how a linear layer transforms [B,S,H].

Deliverables: draw one training update, distinguish RAM from GPU memory, calculate effective batch, and actually save and resume training. Keep environment details, logs, and a page of questions.

## Week 2: move from measurement to one change

Read Chapter 4 and compare batch=1 with batch=32. With a GPU, record peak memory and a profiler trace. Without one, report CPU measurements only; do not infer CUDA performance.

Deliverables: identify one bottleneck supported by evidence, propose one change, and compare identical inputs on the same device. Preserve unsuccessful results too.

## Week 3: understand multiple GPUs and deployment

Read Chapters 3 and 5. Run Lab C if two suitable GPUs are available; otherwise trace communication and sharded-state lifetimes by hand. Choose one backend from its official tutorial, verify outputs before timing, and avoid installing every CUDA framework merely to list them.

Deliverables: explain DDP/FSDP memory differences, TP/DP batch accounting, prefill/decode workloads, and quantization quality thresholds.

## Week 4: transfer the method to embodied systems

Read Chapter 6. Replay inputs through an open vision model or policy offline. Specify image format, action meanings, and timestamps, and build an end-to-end latency table. Real robot hardware is not a prerequisite for a beginner project.

Deliverables: submit code, raw results, correctness checks, one negative result, and limitations using the project template. Explain the bottleneck, evidence, change, and cost in three minutes.

## Interview tomorrow?

Read 1.1, 1.3, 1.4, 2.2, 3.1, 3.2, 4.1, 5.1, and 6.1. Focus on each problem, terms, and first explanation, then answer the interview questions aloud. This establishes vocabulary; it is not equivalent to practical distributed-systems experience.
