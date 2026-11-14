---
title: "实验 D：固定小模型的ONNX部署闭环"
sidebar:
  order: 4
---

## 默认路线：CPU、固定输入、不下载权重

不再自行选模型：沿用实验A的 256→512→64 MLP，固定batch=8，输入shape=[8,256]，输出shape=[8,64]，先执行PyTorch，再导出ONNX并用ONNX Runtime CPU执行。这个无训练任务的网络用于验证导出机制，不代表有任务能力。

先准备有CPU PyTorch的Python环境。建议使用独立虚拟环境，避免改变其它项目依赖。仓库 requirements-deploy.txt 锁定 ONNX 1.23.2 和 ONNX Runtime 1.32.0；具体实测环境见README。

~~~bash
python -m pip install -r requirements-deploy.txt
python labs/export_onnx.py --output-dir lab-results/export
~~~

## 实测记录与导出版本边界

仓库 validation/export-report.json 记录PyTorch 2.11.0+cpu、ONNX 1.23.2、ORT 1.32.0的一次CPU验证。最大绝对误差约3.28×10⁻⁷，通过rtol=1e-4、atol=1e-5检查；20次预热后各测量50次、线程数1。导出约278.37ms，ORT session加载约6.24ms，首次ORT调用约0.332ms；这些是单次历史记录，不是本机目标值。

脚本明确使用legacy torch.onnx.export(dynamo=False)、opset17和固定shape，便于演示最小闭环。出现弃用提醒是预期的版本边界；不要把这个入门例称作当前推荐的生产导出API。新版导出路线应另按对应版本官方文档验证。

## 按顺序检查产物

1. 确认输出目录包含policy.onnx（模型）、io.npz（同一输入及两后端输出）、report.json（验证与计时记录），记录模型/输入shape和环境版本。
2. 检查PyTorch与ONNX Runtime对同一输入的误差和数值断言；失败就停止性能结论。
3. 查看report.json的pytorch和onnxruntime_cpu两项，其中各有p50_ms、p95_ms、samples_per_second及raw_ms；它们来自两个后端预热后的50次测量。分别比较延迟与吞吐，保留原始数据。
4. 把导出耗时、首次执行与稳态执行区分开；本实验的稳态结果不代表导出或加载开销为零。

随机固定输入用于数值对齐，不覆盖真实部署分布。容差以代码声明为准；它只是这个FP32小网络的数值门槛，不能照搬为机器人动作允许误差。不同后端快慢取决于机器与形状，不预设ONNX一定更快。

## 从空表到一份报告

| 配置 | 数值对齐 | p50 | p95 | 吞吐 | 测量边界 |
| --- | --- | --- | --- | --- | --- |
| PyTorch CPU | 参考输出 | 从本机记录填写 | 同左 | 同左 | 固定batch8，预热后 |
| ONNX Runtime CPU | 误差/断言结果 | 从本机记录填写 | 同左 | 同左 | 同一输入与计时口径 |

填写本次记录而非教程里的历史数值。最后写三句话：“改了什么执行后端；输出如何验证；在哪个测量范围内更快/更慢”。先形成这个闭环，再添加真实图像解码或网络服务，重新测端到端开销。

## 硬件分支与停止点

没有GPU也可完成本实验。安装失败时保留环境和错误信息，先回到 [实验 A](/Infra/labs/01-lab/) 完成PyTorch基线；未生成ONNX或未通过数值对齐，就明确记录未完成，不填速度收益。

有兼容NVIDIA GPU及对应TensorRT环境后，才把已验证的固定形状模型迁移到TensorRT。版本、引擎兼容性和动态shape需要另测；这不是本CPU实验已经覆盖的能力。开放视觉模型与量化属于下一轮项目，而非本实验的起步门槛。

## 一手资料

- [PyTorch ONNX](https://docs.pytorch.org/docs/stable/onnx.html)
- [ONNX Runtime Python](https://onnxruntime.ai/docs/get-started/with-python.html)
- [TensorRT](https://docs.nvidia.com/deeplearning/tensorrt/latest/)
