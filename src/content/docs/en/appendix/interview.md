---
title: "Interview self-check and project template"
sidebar:
  order: 3
---

## Answer in your own words

| Question | Important points |
| --- | --- |
| How do you diagnose low GPU utilization? | Timeline, data supply, CPU, copies, synchronization, isolated baselines |
| Is a larger batch always better? | Throughput, memory, latency, and convergence |
| How do DDP and FSDP differ? | Replicas versus sharded state, communication timing, peaks |
| Does TP=4 multiply effective batch by four? | No; the cards cooperate on the same samples |
| How do you address OOM? | Identify live state, activations, or workspace before choosing a remedy |
| Does empty_cache fix every OOM? | No; it cannot release referenced live tensors |
| How do you time CUDA? | Asynchrony, boundary synchronization, Events, warm-up, measurement scope |
| How do you identify communication bottlenecks? | Rank consistency, topology baseline, timeline, exposed communication |
| Why are weights insufficient for recovery? | Optimizer, scheduler, RNG, sampling position, versions |
| Why may quantization not accelerate inference? | Kernels, dequantization, hardware, actual bottleneck |
| How do prefill and decode differ? | Parallel prompt processing versus iterative generation; caches and workloads |
| What is distinctive about VLA optimization? | Vision, action heads, timestamps, observation age, action semantics |
| How is RL training organized? | Rollout, rewards/environments, updates, weight sync, policy lag |
| What makes an optimization credible? | Controlled baseline, correctness threshold, raw results, limitations |

## A three-minute project explanation

“On [hardware, versions, model, inputs], I observed [specific problem]. Using [logs/trace/control experiment], I located [bottleneck]. I changed only [mechanism], compared against the baseline, and obtained [measured metrics, sample count, quality]. The cost was [memory/compilation/quality/maintenance], and it did not help under [conditions].”

Fill brackets from actual records. Write “not measured” where appropriate. Teaching assumptions are not personal résumé achievements.

## Reusable report structure

1. Problem and quality threshold: model, inputs, intended use, acceptable error.
2. Environment: hardware, OS, driver, CUDA, PyTorch, backend versions, commit.
3. Baseline: commands, warm-up, repetitions, p50/p95, throughput, peak memory.
4. Evidence: timeline or logs explaining the diagnosis.
5. Change: one mechanism and why it should help.
6. Results: raw data, numerical/task correctness, performance comparison.
7. Limits: untested hardware/inputs, negative results, rollback conditions.

## Choose a manageable next project

Complete one reproducible project rather than listing ten frameworks. Single-GPU vision IO optimization, recoverable training, a small kernel validated across sizes, or policy replay latency can be credible starting points. Distinguish reading about a system, running it, and independently optimizing it.
