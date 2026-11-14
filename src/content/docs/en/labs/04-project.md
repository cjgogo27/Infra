---
title: "Lab D: a fixed-model ONNX deployment loop"
sidebar:
  order: 4
---

## Default path: CPU, fixed input, no downloaded weights

Use Lab A's 256→512→64 MLP rather than choosing a model. Fix batch=8, input=[8,256], output=[8,64]. Execute PyTorch, export ONNX, and execute with ONNX Runtime CPU. This untrained network demonstrates export mechanics, not task capability.

Use a Python environment with CPU PyTorch, preferably an isolated virtual environment. requirements-deploy.txt pins ONNX 1.23.2 and ONNX Runtime 1.32.0; consult README for the actual validated environment.

~~~bash
python -m pip install -r requirements-deploy.txt
python labs/export_onnx.py --output-dir lab-results/export
~~~

## Actual validation and export-version boundary

validation/export-report.json records one CPU run with PyTorch 2.11.0+cpu, ONNX 1.23.2, and ORT 1.32.0. Maximum absolute error was about 3.28×10⁻⁷, passing rtol=1e-4/atol=1e-5. Each backend used 20 warm-ups and 50 measured calls with one thread. Export took about 278.37 ms, ORT session loading 6.24 ms, and the first ORT call 0.332 ms. These are historical observations, not targets for your machine.

The script deliberately uses legacy torch.onnx.export(dynamo=False), opset17, and fixed shapes for a minimal exercise. Deprecation warnings reflect that boundary. Do not describe this as the currently recommended production export API; validate newer export paths separately against version-specific documentation.

## Inspect artifacts in order

1. Confirm policy.onnx (model), io.npz (common input and both outputs), and report.json (validation/timing) exist; record shapes and versions.
2. Inspect errors and numerical assertions for identical PyTorch/ORT inputs. Stop performance conclusions if correctness fails.
3. Inspect report.json entries pytorch and onnxruntime_cpu, each containing p50_ms, p95_ms, samples_per_second, and raw_ms from 50 warmed calls. Compare latency and throughput while retaining raw data.
4. Distinguish export, first execution, and steady state. Steady-state results do not imply zero export/loading cost.

Fixed random inputs check numerical alignment, not real deployment distributions. The code's tolerance applies to this small FP32 network, not acceptable robot action error. Backend performance depends on device and shape; ONNX is not assumed faster.

## Produce a report

| Configuration | Numerical agreement | p50 | p95 | Throughput | Scope |
| --- | --- | --- | --- | --- | --- |
| PyTorch CPU | Reference | Fill from your run | Same | Same | Fixed batch8, warmed |
| ONNX Runtime CPU | Error/assertion | Fill from your run | Same | Same | Same input and timing convention |

Use your measurements, not historical tutorial values. Explain the changed backend, correctness verification, and scope of improvement or regression. Only then add real image decoding or networking and remeasure end to end.

## Branches and stopping conditions

No GPU is needed. If installation fails, retain environment/error records and finish the PyTorch baseline in [Lab A](/Infra/en/labs/01-lab/). Without a valid export and passed numerical check, record incomplete status rather than a speedup.

Only migrate to TensorRT after obtaining compatible NVIDIA hardware and its software environment. Version/engine portability and dynamic shapes require separate tests. Open vision models and quantization are later extensions, not entry requirements for this lab.

## Primary references

- [PyTorch ONNX](https://docs.pytorch.org/docs/stable/onnx.html)
- [ONNX Runtime Python](https://onnxruntime.ai/docs/get-started/with-python.html)
- [TensorRT](https://docs.nvidia.com/deeplearning/tensorrt/latest/)
