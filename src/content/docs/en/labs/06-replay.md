---
title: "Lab F: replay a LabBot interface contract"
sidebar:
  order: 6
---

## Interface validation, not a robot experiment

Read [Section 6.1](/Infra/en/06-embodied/01/) and [Section 6.2](/Infra/en/06-embodied/02/). Samples are synthetic. No weights are downloaded and no robot is connected. Images are metadata only, without image files, visual encoding, or policy inference.

~~~bash
python labs/labbot_replay.py --output lab-results/replay.json
~~~

## Follow one sample

| Field | Teaching convention |
| --- | --- |
| image | RGB, uint8, shape=[1,3,32,32], metadata only |
| joint state | Six joints, fixed j1–j6 order, in radians |
| action | shape=[4,6], four steps of six absolute joint targets in radians |
| observation_ms | Observation time; age=now_ms−observation_ms |
| chunk_start_ms | Chunk start; this exercise rejects a start earlier than now_ms |
| now_ms | Validation time |
| Clock and deadline | Same monotonic clock; maximum allowed age 100 ms |

The 100 ms threshold is an exercise convention, not a robot safety guarantee. Millisecond timestamps from different devices cannot automatically be subtracted; production systems need defined synchronization and mappings. One clock here isolates the interface exercise.

The valid sample uses observation_ms=1000 and now_ms=1040, giving age 40 ms. The stale case uses now_ms=1200, giving 200 ms. Actions have a 20 ms step. Chunk validation is simplified and does not trim already-executed prefixes for asynchronous control.

The script checks valid, wrong_unit, wrong_shape, and stale cases. The valid case should pass and the three faults should be rejected, with outcomes written to JSON. Rejection prevents subsequent action dispatch rather than silently repairing incompatible values.

## Interpret the faults

- wrong_unit: shape may be correct while semantics differ; element count is insufficient.
- wrong_shape: joint dimensions or horizon violate the contract; silent truncation is inappropriate.
- stale: numerically correct data may be too old for execution; obsolete actions should not remain queued.

## Acceptance and transfer

Classify each fault as semantic, structural, or temporal. Calculate an example's age and explain acceptance/rejection. Explain why passing every contract check still does not prove grasping success.

When adapting this schema to a camera or policy, revisit coordinate frames, joint ordering, normalization, and control periods. This exercise does not replace policy evaluation, collision detection, or controller protection.
