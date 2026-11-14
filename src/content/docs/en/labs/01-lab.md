---
title: "Lab A: time inference and compare batches"
sidebar:
  order: 1
---

## Purpose and environment

Requires Python and PyTorch. CPU is sufficient. CUDA requires a compatible NVIDIA GPU, driver, and PyTorch build. Choose your installation from the [official PyTorch instructions](https://pytorch.org/get-started/locally/), rather than copying hardware-specific commands blindly. See the repository README for the environment actually validated.

Run from the repository root in PowerShell or a Linux shell. No model/data download or robot connection is needed.

~~~bash
python labs/benchmark.py --device cpu --batch 1 --output lab-results/b1.json
python labs/benchmark.py --device cpu --batch 32 --output lab-results/b32.json
~~~

With a compatible GPU:
~~~bash
python labs/benchmark.py --device cuda --batch 8 --trace --output lab-results/gpu.json
~~~

## What to observe

Output contains raw timings, p50/p95, throughput, versions, and a correctness check. CUDA additionally reports peak allocated memory, which is not the same as total process memory in nvidia-smi.

After warm-up, each call is timed with synchronization at the boundaries. This is a small MLP with resident inputs, excluding IO, networking, queueing, and a complete policy. Its throughput is not VLA performance, nor is serialized synchronized timing the maximum throughput of an asynchronous service.

Compare per-batch latency and amortized per-sample time as batch grows. Repeat configurations independently and record system load. Short CPU timings depend on thread pools and scheduling.

## Optional compilation and traces

Add --compile to compare compiled steady-state performance. The platform must support the chosen torch.compile backend. Initial compilation is excluded from timing, not claimed to cost zero. Record unsupported environments rather than inventing results.

--trace captures five additional calls after measurement so profiler overhead does not contaminate the benchmark. Open the .json.trace file in a compatible viewer. Local results default to the Git-ignored lab-results directory.
