---
title: "Lab C: a minimal two-GPU DDP run"
sidebar:
  order: 3
---

## Hardware requirements

Requires Linux, two available NVIDIA GPUs, and NCCL-enabled PyTorch. This is not a CPU simulation. Without the hardware, read the source and Section 3.1 instead; do not fill in unmeasured performance.

~~~bash
torchrun --standalone --nproc_per_node=2 labs/ddp.py
~~~

Each process binds LOCAL_RANK, the sampler partitions data, and DDP synchronizes gradients. set_epoch advances sampling each epoch. A final assertion checks that model parameters agree across ranks. Global mean loss is computed by reducing loss sums and sample counts. Equal-length, equal-weight examples do not cover variable-token weighting.

## Acceptance criteria

Only rank zero prints summaries. Effective batch is 8×2=16. Training finishes without a collective hang. This tiny linear model verifies data and synchronization semantics, not multi-GPU scaling.

For a scaling extension, fix global batch and compare one versus two cards under a substantial workload. Record step time, throughput, and communication. Read Section 3.4 before interpreting speedup.

## Optional extension

Migrate to FSDP2 using the tutorial matching your version, then measure peak memory and step time. Merely switching a wrapper does not establish large-scale training expertise. This extension has not been executed as part of the repository's validation.
