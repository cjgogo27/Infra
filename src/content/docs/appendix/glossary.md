---
title: "术语速查"
sidebar:
  order: 1
---

| 术语 | 中文/含义 | 对应小节 |
| --- | --- | --- |
| Infra | 模型训练、推理与运行的基础设施 | 1.1 |
| Tensor / Activation | 张量 / 中间激活 | 1.3 |
| SLO / p95 | 服务目标 / 第 95 百分位 | 1.4 |
| CT / SFT / RL | 继续训练 / 监督微调 / 强化学习 | 2.1 |
| AMP / BF16 / FP16 | 混合精度 / 两种 16 位浮点格式 | 2.2 |
| Microbatch / Accumulation | 单次小批次 / 梯度累积 | 2.2 |
| Prefetch / Pinned Memory | 预取 / 页锁定主机内存 | 2.3 |
| Checkpoint | 训练状态检查点；也可能指激活重算策略，依语境区分 | 2.4、4.3 |
| Rank / World Size | 进程编号 / 进程组大小 | 3.1 |
| DDP / FSDP | 数据并行 / 完全分片数据并行 | 3.1、3.2 |
| TP / PP / CP / EP | 张量 / 流水线 / 上下文 / 专家并行 | 3.3 |
| NCCL | NVIDIA 集合通信库 | 3.4 |
| Roofline | 以算力与带宽约束理解性能的模型 | 4.2 |
| Kernel / Fusion | 设备内核 / 操作融合 | 4.4 |
| Prefill / Decode | 提示词处理 / 迭代生成 | 5.1 |
| KV Cache / GQA | 键值缓存 / 分组查询注意力 | 5.1 |
| ONNX / Engine | 模型交换表示 / 后端编译执行产物 | 5.2 |
| PTQ / QAT | 训练后量化 / 量化感知训练 | 5.3 |
| Backpressure | 背压，限制进入系统的待处理工作 | 5.4 |
| VLM / VLA | 视觉语言模型 / 视觉语言动作模型 | 6.1 |
| Action Chunk | 一段未来动作 | 6.2 |
| Rollout / Policy Lag | 策略采样 / 策略版本滞后 | 6.3 |

首次阅读遇到陌生词先搜中文或英文，再回到对应小节的问题场景。缩写相同不保证含义相同，应以具体框架和团队语境为准。
