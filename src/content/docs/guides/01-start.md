---
title: "从零开始：四周学习与验收"
sidebar:
  order: 1
---

先走一条明确的CPU路线，再决定是否进入GPU、多卡或真机。默认项目统一使用仓库小模型和合成数据，不要求自行选模型、找权重或租GPU。每周8–12小时只是规划建议，验收比读完页数更重要。

## 第一周：理解一次训练和一次测量

按 [1.1系统总览](/Infra/01-foundations/01/) → [实验0](/Infra/labs/00-training/) → [1.2主机与GPU](/Infra/01-foundations/02/) → [1.3显存](/Infra/01-foundations/03/) → [1.4指标](/Infra/01-foundations/04/) → [实验A](/Infra/labs/01-lab/) 阅读与运行。

交付：记录一个参数在forward、backward和step前后的变化；保留两种batch的JSON；正确解释每批延迟、每样本摊销时间和吞吐。不能解释这些时，先不要跳到FSDP或CUDA Kernel。

## 第二周：训练正确性与性能证据

读 [2.2梯度累积](/Infra/02-training/02/)，做 [实验E](/Infra/labs/05-accumulation/)；读 [2.4检查点](/Infra/02-training/04/)，做 [实验B](/Infra/labs/02-resume/)。再读 [2.3数据IO](/Infra/02-training/03/)、[4.1Profiler](/Infra/04-performance/01/)、[4.3显存与图](/Infra/04-performance/03/)，做 [实验G](/Infra/labs/07-profiler/)。

交付：解释一个错误归一化例子；验证恢复；挑一个实际CPU范围提出假设，再用不带profiler的基准验证。没有加速也应保留证据与解释。

## 第三周：固定模型完成一次部署

读 [3.1 DDP](/Infra/03-distributed/01/)、[3.2 FSDP](/Infra/03-distributed/02/) 理解复制与分片；再读 [5.1 KV](/Infra/05-inference/01/)、[5.2导出](/Infra/05-inference/02/)，完成 [实验D](/Infra/labs/04-project/) 的固定batch8小模型ONNX/ORT CPU路线。

交付：一份导出文件、数值对齐结果和两后端性能表；解释为什么导出成功不等于部署更快。没有完成导出时如实记录阻碍，不把阅读官方教程当作实际部署经历。

## 第四周：具身接口与面试表达

读 [6.1接口](/Infra/06-embodied/01/)、[6.2动作块](/Infra/06-embodied/02/)、[6.4项目证据](/Infra/06-embodied/04/)，做 [实验F](/Infra/labs/06-replay/) 的正常/错误单位/错误shape/过期样本回放。

交付：接口契约、拒绝故障的记录、CPU优化报告和 [递进面试题](/Infra/appendix/interview/) 答题记录。用三分钟讲清问题、证据、改动、收益或负结果及局限。合成回放不是训练VLA，更不是机器人控制成功。

## GPU与进阶分支

| 条件 | 可增加的实验 | 条件不满足时 |
| --- | --- | --- |
| 一张兼容CUDA GPU | 实验A的CUDA计时与显存记录 | 保留CPU结果，明确不推断GPU性能 |
| Linux、两张GPU、NCCL可用 | [实验C](/Infra/labs/03-ddp/) | 手算副本/梯度通信，不填实测加速 |
| 已完成CPU导出，兼容TensorRT环境 | 实验D的GPU后端拓展 | 停在ORT CPU，不跳过数值对齐 |
| 有合法可用模型/数据和足够资源 | 开放视觉模型或策略离线回放 | 先完成LabBot合成接口检查 |

第一轮先略读3.3的CP/EP、4.4底层Kernel以及复杂RL。第二轮再读 [3.3](/Infra/03-distributed/03/)、[3.4](/Infra/03-distributed/04/)、[4.2](/Infra/04-performance/02/)、[4.4](/Infra/04-performance/04/)、[2.1](/Infra/02-training/01/)、[5.3](/Infra/05-inference/03/)、[5.4](/Infra/05-inference/04/)、[6.3](/Infra/06-embodied/03/)。全部是岗位相关知识，但无需同时成为实践主线。

## 一天内要面试

读1.1、1.3、1.4、2.2、3.1、3.2、4.1、5.1、6.1的场景与核心解释；至少亲手跑实验0和A，再做三组面试情景题。明确区分“阅读了解”“实际运行”“独立优化”，不要把速读包装成分布式工程经验。
