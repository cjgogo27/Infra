---
title: "实验 A：测一次推理，比较批量"
sidebar:
  order: 1
---

## 目的与环境

只依赖 Python 和 PyTorch。CPU 即可完成；CUDA 模式需兼容的 NVIDIA GPU、驱动与 PyTorch。按 [PyTorch 官方安装页](https://pytorch.org/get-started/locally/) 选择自己的构建，不照抄跨硬件安装命令。仓库验证环境与结果见 README。

下面命令在仓库根目录运行，Windows PowerShell 与 Linux shell 都可使用。无需下载模型或数据，也不会连接机器人。

~~~bash
python labs/benchmark.py --device cpu --batch 1 --output lab-results/b1.json
python labs/benchmark.py --device cpu --batch 32 --output lab-results/b32.json
~~~

GPU 可用时：
~~~bash
python labs/benchmark.py --device cuda --batch 8 --trace --output lab-results/gpu.json
~~~

## 观察什么

输出包含每次原始耗时、p50/p95、吞吐、版本与正确性检查。GPU 模式额外记录峰值 allocated 显存；不把它当成 nvidia-smi 的进程总显存。

脚本预热后，对每次调用做边界同步，以墙钟测量同步调用时延。它测的是常驻输入的小型 MLP，不含 IO、网络、排队或完整模型；不能把这里的吞吐称为 VLA 性能。串行同步测量也不代表异步服务的最大吞吐。

比较 batch 增大后，单批延迟与每样本摊销时间是否同时下降。每个配置重复独立运行，记录系统负载；短 CPU 测量会受线程池和系统调度影响。

## 可选：编译与 trace

添加 --compile 比较编译后的稳态性能。需要当前平台支持 torch.compile 后端，首次编译可能耗时较长；本脚本把它排除在稳态计时之外，不代表冷启动成本为零。不能运行时记录环境原因，不伪造结果。

--trace 在测量结束后额外采集 5 次调用，因此 profiler 开销不混入基准。可用兼容 Chrome trace 的查看器打开 .json.trace 文件。原始结果默认在 lab-results，被 Git 忽略，便于保留本地实验而不混入正文。
