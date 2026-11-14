---
title: "Lab G: turn a CPU timeline into a testable hypothesis"
sidebar:
  order: 7
---

## Capture semantically labeled work

Complete [Lab A](/Infra/en/labs/01-lab/) and read [Section 4.1](/Infra/en/04-performance/01/). This captures actual CPU work, not CUDA computation or communication.

~~~bash
python labs/profile_pipeline.py --output-dir lab-results/profile
~~~

Outputs are pipeline.json.trace and summary.json. Named ranges are prepare_inputs, policy_forward, and postprocess. validation/profile-summary.json records one actual capture, not timings your machine must reproduce.

## One actual CPU capture, not a steady-state benchmark

Environment: Windows, PyTorch 2.11.0+cpu, one thread, ten calls per range. Inclusive time includes children; self time excludes them. All times below are microseconds.

| Range | Calls | Inclusive total μs | Inclusive mean/call μs | Self total μs |
| --- | --- | --- | --- | --- |
| prepare_inputs | 10 | 1445.7 | 144.57 | 700.5 |
| policy_forward | 10 | 1888.6 | 188.86 | 506.4 |
| postprocess | 10 | 330.8 | 33.08 | 293.9 |

Means are totals divided by ten, **not unprofiled model latency**, p50, or p95. Input generation matters in this capture, but is not actual image decoding. Test whether reusing inputs reduces unprofiled overall time.

Download the [actual CPU trace](https://raw.githubusercontent.com/cjgogo27/Infra/main/validation/profile-pipeline.json.trace) and [summary](https://github.com/cjgogo27/Infra/blob/main/validation/profile-summary.json).

## Open the local trace in Perfetto

Open the [official Perfetto UI](https://ui.perfetto.dev/), choose **Open trace file**, and select pipeline.json.trace. Search for a named range, expand its process/thread track, select an interval to inspect its duration, and zoom into one invocation to see stage relationships.

If the UI fails to load, retain the trace and inspect summary.json. State that graphical inspection was not completed rather than implying a screenshot was checked. Do not upload traces to unknown viewers.

## From observation to hypothesis

| Observation | Provisional interpretation | Next check |
| --- | --- | --- |
| Large prepare_inputs total | Input preparation deserves investigation in this capture | Reuse fixed inputs and compare unprofiled elapsed time |
| Large policy_forward total | Model execution contributes substantially here | Fix threads/input and compare batches |
| One unusually slow invocation | A tail event exists | Compare neighbors, repeat, and inspect system load |

Distinguish inclusive range duration from self time. Parent ranges and child operators overlap; summing every row does not give wall time. Profiling adds overhead, so validate improvement with an unprofiled benchmark.

## Two GPU-related tracks: teaching diagram, not measurement

~~~text
Time →
CPU: [prepare][submit A][submit B]........[synchronize]
GPU:          [copy] [compute A][compute B]...........
~~~

The diagram illustrates why a returned CPU submission does not imply completed GPU work. It does not mean this CPU lab captured CUDA events or demonstrated communication overlap.

Self-check: does fast CPU submission establish short GPU execution? No. Does a GPU gap alone prove slow IO? No; inspect CPU work, dependencies, and supply. Design an isolating control before rewriting kernels.

Pass when you select one actual CPU range, record evidence, propose a hypothesis and control, and identify at least one conclusion unsupported by this trace.
