---
title: "Lab B: verify checkpoint recovery"
sidebar:
  order: 2
---

## Run

~~~bash
python labs/checkpoint.py
~~~

The script trains a small CPU network and saves model, AdamW, scheduler, update count, and Python/PyTorch RNG state. It continues three steps as a baseline, creates new model/optimizer objects, reloads the local file, restores randomness, and repeats those steps. Losses and parameters must match exactly.

This simulates recovery with fresh objects, not a new process. Real projects should additionally test process restart and data-loader state. Synthetic data is generated from RNG state without worker prefetch, so this does not cover exact recovery of real input pipelines.

losses_match and parameters_exactly_match should be true. Restore RNG after creating the new model; initialization otherwise consumes the restored random sequence.

## Break one condition, then repair it

In a separate copy, omit scheduler recovery and inspect learning rates and parameters. Omit RNG recovery and observe changed inputs. Load only weights and observe the effect of lost momentum. Change one condition at a time.

Only load the checkpoint generated locally by this script. Arbitrary model files should not be treated as trusted input. The example replaces a temporary file on one filesystem; it does not simulate object storage or distributed saves.
