---
title: "Lab E: weight accumulation by valid elements"
sidebar:
  order: 5
---

## Run and question

Complete [Lab 0](/Infra/en/labs/00-training/) and read [Section 2.2](/Infra/en/02-training/02/). This experiment uses synthetic CPU data.

~~~bash
python labs/accumulation.py
~~~

The question is how unequal microbatches reproduce the full-batch objective, not merely whether gradients can be added.

## Calculate before running

Suppose a first microbatch has one valid element and mean loss 10; a second has three valid elements and mean loss 2:

~~~text
Global mean = (1×10 + 3×2) / (1+3) = 4
Incorrect mean of means = (10+2)/2 = 6
~~~

These objectives weight elements differently, so gradients may differ. Equal microbatch weighting matches a global mean only when valid counts are equal. Define whether an element means a sample, non-padding token, or action component.

## Interpret the fields

| Field | Meaning |
| --- | --- |
| full_vs_weighted_max_error | Difference between correctly weighted accumulation and full batch; must meet the script's assertion tolerance |
| wrong_mean_max_error | Difference caused by deliberately averaging microbatch means |
| tail_window_max_error | Difference after correctly normalizing the final partial window; must meet the assertion |

Floating-point ordering can change final digits; exact zero is not required. Use the declared tolerances and assertions. Incorrect weighting may accidentally agree on special data, so explain the objective as well as inspecting numbers.

## Acceptance criteria

Explain why effective batch=b×D×A is a count, not a loss-weight definition. Change valid counts, predict the weights, then run. Explain why a final window with two microbatches should not blindly be divided by a planned four accumulation steps.

This does not validate DDP/FSDP communication or distributed loss scaling; rank-reduction semantics must also be included in a multi-GPU derivation.
