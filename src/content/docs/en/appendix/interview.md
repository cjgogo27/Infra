---
title: "Interviews: progressive cases, code, and project evidence"
sidebar:
  order: 3
---

## How to use these questions

The three cases are teaching scenarios, not production incidents. Read the initial evidence, explain what you would request next, then reveal more. The goal is a defensible diagnostic process, not guessing the answer immediately.

## Case 1: low GPU utilization

Initial evidence: utilization is approximately 30%; a colleague proposes doubling DataLoader workers.

Ask about environment, input distribution, and timing boundaries. What evidence would justify changing workers?

<details>
<summary>Additional evidence and follow-up</summary>

The complete input path takes 120 ms/step; same-shaped resident GPU tensors take 40 ms. The real path waits before forward. These numbers are assumptions for this question.

Can you conclude that the disk is slow? Choose one next control.

Suggested reasoning: verify comparable compute/shapes, then suspect upstream supply without yet distinguishing reading, decoding, augmentation, or transfer. Add an in-memory-sample control retaining preprocessing/transfers and mark stages. Workers also consume RAM and scheduling resources. Validate with unprofiled end-to-end throughput and preserved quality.

</details>

## Case 2: long-sequence OOM

Initial evidence: short sequences train; long sequences fail on the first step. empty_cache does not help.

What memory, shape, and execution-stage information do you request? Why not immediately add data-parallel replicas?

<details>
<summary>Additional evidence and follow-up</summary>

Weights and optimizer settings are unchanged. The peak occurs around backward, and a smaller microbatch works. Obtain actual allocated/reserved memory, live-tensor information, and peak timing rather than inventing numbers.

Would you first try recomputation, FSDP, or cache clearing? How would you validate the choice?

Suggested reasoning: activation pressure becomes a priority hypothesis, not a proven diagnosis; workspaces and retained references remain alternatives. Establish a smaller-microbatch baseline and separately evaluate recomputation's memory/time cost. Consider sharding if persistent state dominates. DDP replicates model state. Compare fixed effective batch with correct loss weighting and quality checks.

</details>

## Case 3: NCCL timeout

Initial evidence: rank zero reports a timeout; rank one's logs have not been examined.

What do you inspect first? Would you immediately increase the timeout?

<details>
<summary>Additional evidence and follow-up</summary>

Rank one encountered an earlier sample-shape error and exited; rank zero subsequently waited in a collective.

Why does an NCCL error not necessarily establish a network fault? What constitutes a fix?

Suggested reasoning: ordering suggests a secondary timeout. Preserve earliest per-rank errors and input summaries, repair the data contract/error propagation, and verify batch counts and collective order. A controlled bad-sample test should produce a clear error and terminate all processes; valid data should finish with matching parameters. Persistent timeouts then justify topology, collective-baseline, and network investigation. This scenario does not rule out all network faults.

</details>

## Code question 1: is this GPU execution time?

Assume model and x are already on CUDA:

~~~python
start = time.perf_counter()
y = model(x)
elapsed = time.perf_counter() - start
print(elapsed)
~~~

Explain asynchrony and choose either a device interval or a complete call boundary.

<details>
<summary>Answer criteria</summary>

This can mostly measure submission. Warm up, synchronize before/after a complete wall-time interval, and repeat measurements. Move input preparation outside only if excluded from the intended scope. Correctly recorded/synchronized CUDA Events can measure device intervals. Synchronizing after every operator changes overlap. Lab A's serialized timing is not maximum online serving throughput.

</details>

## Code question 2: independent updates were intended

~~~python
for x, target in loader:
    loss = loss_fn(model(x), target)
    loss.backward()
    optimizer.step()
~~~

<details>
<summary>Answer and follow-up</summary>

Clear gradients before each independent update using optimizer.zero_grad; gradients accumulate by default. Clearing gradients does not zero model weights.

For intentional accumulation, define windows and valid-element weighting, clear at window start, backpropagate multiple microbatches, and step at the end. Handle partial windows correctly. Verify against the full-batch objective in [Lab E](/Infra/en/labs/05-accumulation/), rather than memorizing division by the planned accumulation count.

</details>

## Scoring

Score each of three cases and two code questions from 0 to 3, for 15 points total:

| Score | Evidence of understanding |
| --- | --- |
| 0 | Cannot explain the issue, or ignores correctness while claiming speed |
| 1 | Lists relevant terms/causes without priorities or evidence |
| 2 | Proposes a plausible hypothesis, requests evidence, and designs an isolating control |
| 3 | Also states alternative explanations, correctness criteria, acceptance, and limits |

This identifies study gaps; it does not predict interview outcomes. A short answer should still explain how its hypothesis will be tested.

## Three-minute project narrative

“On [hardware, versions, model, inputs], I observed [problem]. [Logs/trace/control] identified [bottleneck]. Changing only [mechanism] produced [measured result and variation] while meeting [correctness threshold]. The cost was [trade-off], and [conditions] remain untested.”

Retain environment/commands, baseline, raw data, correctness checks, one change, results, negative findings, and limitations. Write “not measured” when appropriate. Reading, execution, and independent optimization differ; synthetic CPU work is not large-scale training or robot acceleration.

Use the [glossary](/Infra/en/appendix/glossary/) for terms and the [four-week route](/Infra/en/guides/01-start/) for a project starting point.
