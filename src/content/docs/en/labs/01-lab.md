---
title: "Lab A: measure, repeat, and interpret"
sidebar:
  order: 1
---

## Prepare and run

Complete [Lab 0](/Infra/en/labs/00-training/) and read [latency and throughput](/Infra/en/01-foundations/04/). Run from the repository root in a Python environment with PyTorch. CPU is sufficient; no model/data downloads are needed.

~~~bash
python labs/benchmark.py --device cpu --batch 1 --threads 1 --output lab-results/b1.json
python labs/benchmark.py --device cpu --batch 32 --threads 1 --output lab-results/b32.json
python labs/compare_benchmarks.py lab-results/b1.json lab-results/b32.json
~~~

Fix threads to avoid different default pools between runs. Record versions, device, thread count, shapes, and background load. This is a synthetic 256→512→64 MLP with resident inputs, not a trained VLA.

## Interpret the fields

| Field | Meaning |
| --- | --- |
| p50_ms, p95_ms | Whole-call, whole-batch latency percentiles in milliseconds |
| samples_per_second | Total samples divided by total measured duration |
| raw_ms | Individual timings saved in JSON |
| peak_allocated_bytes | Peak CUDA live-tensor allocation; null on CPU, not zero |
| correctness | Output comparison, not task accuracy |

Throughput = batch×measured calls/total seconds. **Do not estimate measured throughput using batch/p50**: a percentile is not the mean duration. Total time/total samples gives amortized sample cost, not online request latency.

## Interpret existing records

These values come from validation/b1.json and validation/b32.json: Windows, PyTorch 2.11.0+cpu, 14 threads, 20 warm-ups, 100 measurements. They are historical single runs, **not expected results for the one-thread commands above**.

| Batch | p50 ms/batch | p95 ms/batch | Samples/s |
| --- | --- | --- | --- |
| 1 | 0.09155 | 0.10931 | 7984.92 |
| 32 | 0.14520 | 0.19217 | 231469.76 |

Supported conclusion: these records show higher whole-batch percentile latency and higher sample throughput at the larger batch. Unsupported conclusions: faster online responses, the same VLA speedup, or established reproducibility. Tiny CPU calls are sensitive to scheduling and thread pools.

## Repeat in independent processes

~~~bash
python labs/repeat_benchmark.py --batch 1 --runs 3 --threads 1 --output-dir lab-results/repeat-b1
python labs/repeat_benchmark.py --batch 32 --runs 3 --threads 1 --output-dir lab-results/repeat-b32
~~~

Inspect individual records and summary.json for between-run variation. Three runs are a beginner exercise, not a significance guarantee. If variation approaches the claimed gain, investigate load, warm-up, and sample count instead of selecting the best run.

## Optional branches and troubleshooting

With compatible CUDA, change a single-run command to --device cuda. Boundary synchronization measures serialized wall time, including host overhead, not maximum asynchronous serving throughput. --compile requires a supported backend; compilation is excluded from steady-state timing and cold start must be reported separately.

| Symptom | Action |
| --- | --- |
| Script not found | Return to the repository root containing labs |
| No module named torch | Install PyTorch in the active Python environment |
| CUDA unavailable | Complete CPU first; verify hardware/build without relabeling CPU data |
| Unsupported compiler backend | Keep the eager baseline and record the limitation |
| Numerical assertion fails | Investigate dtype, inputs, and backend before reporting speed |

--trace captures extra calls after timing. Continue to [Lab G](/Infra/en/labs/07-profiler/) for stage-level interpretation.

Pass when you can explain a JSON record, compare configurations, retain all repeats, and identify at least two unsupported conclusions.
