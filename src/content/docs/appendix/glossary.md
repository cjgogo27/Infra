---
title: "术语速查"
sidebar:
  order: 1
---

| 术语 | 中文/含义 | 对应小节 |
| --- | --- | --- |
| Infra | 模型训练、推理与运行的基础设施 | [1.1](/Infra/01-foundations/01/) |
| Tensor / Activation | 张量 / 中间激活 | [1.3](/Infra/01-foundations/03/) |
| SLO / p95 | 服务目标 / 第 95 百分位 | [1.4](/Infra/01-foundations/04/) |
| CT / SFT / RL | 继续训练 / 监督微调 / 强化学习 | [2.1](/Infra/02-training/01/) |
| AMP / BF16 / FP16 | 混合精度 / 两种 16 位浮点格式 | [2.2](/Infra/02-training/02/) |
| Microbatch / Accumulation | 单次小批次 / 梯度累积 | [2.2](/Infra/02-training/02/) |
| Prefetch / Pinned Memory | 预取 / 页锁定主机内存 | [2.3](/Infra/02-training/03/) |
| Checkpoint | 训练状态检查点；也可能指激活重算策略，依语境区分 | [2.4](/Infra/02-training/04/)、[4.3](/Infra/04-performance/03/) |
| Rank / World Size | 进程编号 / 进程组大小 | [3.1](/Infra/03-distributed/01/) |
| DDP / FSDP | 数据并行 / 完全分片数据并行 | [3.1](/Infra/03-distributed/01/)、[3.2](/Infra/03-distributed/02/) |
| TP / PP / CP / EP | 张量 / 流水线 / 上下文 / 专家并行 | [3.3](/Infra/03-distributed/03/) |
| NCCL | NVIDIA 集合通信库 | [3.4](/Infra/03-distributed/04/) |
| Roofline | 以算力与带宽约束理解性能的模型 | [4.2](/Infra/04-performance/02/) |
| Kernel / Fusion | 设备内核 / 操作融合 | [4.4](/Infra/04-performance/04/) |
| Prefill / Decode | 提示词处理 / 迭代生成 | [5.1](/Infra/05-inference/01/) |
| KV Cache / GQA | 键值缓存 / 分组查询注意力 | [5.1](/Infra/05-inference/01/) |
| ONNX / Engine | 模型交换表示 / 后端编译执行产物 | [5.2](/Infra/05-inference/02/) |
| PTQ / QAT | 训练后量化 / 量化感知训练 | [5.3](/Infra/05-inference/03/) |
| Backpressure | 背压，限制进入系统的待处理工作 | [5.4](/Infra/05-inference/04/) |
| VLM / VLA | 视觉语言模型 / 视觉语言动作模型 | [6.1](/Infra/06-embodied/01/) |
| Action Chunk | 一段未来动作 | [6.2](/Infra/06-embodied/02/) |
| Rollout / Policy Lag | 策略采样 / 策略版本滞后 | [6.3](/Infra/06-embodied/03/) |

首次阅读遇到陌生词先搜中文或英文，再回到对应小节的问题场景。缩写相同不保证含义相同，应以具体框架和团队语境为准。
