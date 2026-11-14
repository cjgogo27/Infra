---
title: "按岗位、故障与兴趣查阅"
sidebar:
  order: 2
---

## 岗位能力对照

| JD 能力 | 阅读位置 | 可展示证据 |
| --- | --- | --- |
| VLA/VLM 训练部署 | [2.1](/Infra/02-training/01/)、[6.1](/Infra/06-embodied/01/), [6.2](/Infra/06-embodied/02/), [6.3](/Infra/06-embodied/03/), [6.4](/Infra/06-embodied/04/) | 输入输出契约和离线回放 |
| CT/SFT/RL | [2.1](/Infra/02-training/01/), [2.2](/Infra/02-training/02/)、[6.3](/Infra/06-embodied/03/) | loss mask 与阶段耗时分析 |
| 分布式训练 | [3.1](/Infra/03-distributed/01/), [3.2](/Infra/03-distributed/02/), [3.3](/Infra/03-distributed/03/), [3.4](/Infra/03-distributed/04/) | DDP 运行日志与 batch 计算 |
| 数据 IO、Checkpoint | [2.3](/Infra/02-training/03/), [2.4](/Infra/02-training/04/) | 数据供给对照、恢复一致性 |
| 计算图、显存、重叠 | [4.1](/Infra/04-performance/01/), [4.2](/Infra/04-performance/02/), [4.3](/Infra/04-performance/03/), [4.4](/Infra/04-performance/04/)、[3.4](/Infra/03-distributed/04/) | trace、内存账本与单因素比较 |
| 导出、量化、TensorRT | [5.2](/Infra/05-inference/02/), [5.3](/Infra/05-inference/03/) | 输出对齐与精度/速度表 |
| 服务化和端到端优化 | [1.4](/Infra/01-foundations/04/)、[5.4](/Infra/05-inference/04/)、[6.4](/Infra/06-embodied/04/) | p50/p95、吞吐、排队时间 |
| Kernel / Plugin 加分项 | [4.4](/Infra/04-performance/04/) | 多尺寸正确性与 benchmark |
| Attention / KV 加分项 | [5.1](/Infra/05-inference/01/) | 容量估算与并发实验 |

## 从故障进入

- **第一步就 OOM**：先读 [显存账本](/Infra/01-foundations/03/)，再看 [显存与计算图](/Infra/04-performance/03/)。
- **GPU 总在等**：看 [数据 IO](/Infra/02-training/03/) 与 [Profiler](/Infra/04-performance/01/)。
- **多卡一直卡住**：看 [DDP](/Infra/03-distributed/01/) 和 [NCCL](/Infra/03-distributed/04/)，找最早异常 rank。
- **首字慢 / 并发上不去**：看 [KV Cache](/Infra/05-inference/01/) 和 [服务化](/Infra/05-inference/04/)。
- **模型快，机器人慢**：看 [端到端预算](/Infra/06-embodied/04/)，检查观测年龄、队列与过期结果。

## 先分清三个相近名称

Triton 语言用于编写 GPU kernel；Triton Inference Server 用于模型服务；TensorRT 用于目标硬件上的推理优化与执行。TRT-LLM 聚焦大语言模型，不能假定覆盖任意具身网络。

FSDP 与 Megatron 是训练系统中的不同组件或路线；verl 组织 LLM RL 数据流，可集成训练与推理后端。选工具应从任务与瓶颈出发。
