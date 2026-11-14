---
title: "Lab D: from an offline model to a deployment report"
sidebar:
  order: 4
---

## Choose a manageable model

Start with a vision encoder or small action head using legally available weights/data suitable for your machine. Record source, revision, license, and preprocessing. A giant VLA download is not required.

## Validate each boundary

1. Establish a PyTorch baseline at FP32 or an appropriate precision, fixing inputs, randomness, and eval mode.
2. Save representative inputs/outputs and check dimensions, layout, color channels, and ranges.
3. Export using documentation for your installed PyTorch/backend; record unsupported operations.
4. Compare absolute/relative errors and task quality. Derive thresholds from the task.
5. Separate export/compilation, cold start, and warmed execution.
6. Add real decoding/preprocessing and remeasure end to end. Preserve the result if gains disappear.
7. If supported, compare quantization and evaluate calibration coverage.

## Deliverable table

| Configuration | Quality | p50 | p95 | Throughput | Peak memory | Conditions |
| --- | --- | --- | --- | --- | --- | --- |
| Baseline | Not measured | Not measured | Not measured | Not measured | Not measured | Hardware and inputs |
| One change | Not measured | Not measured | Not measured | Not measured | Not measured | One changed mechanism |

These are blank experiment records, not results. Without a backend/GPU, complete the interface contract, estimate, and reproduction plan. An estimate is not a measurement.

## Primary references

- [PyTorch ONNX](https://docs.pytorch.org/docs/stable/onnx.html)
- [TensorRT](https://docs.nvidia.com/deeplearning/tensorrt/latest/)
- [LeRobot](https://huggingface.co/docs/lerobot/index)
