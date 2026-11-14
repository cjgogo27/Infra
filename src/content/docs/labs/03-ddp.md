---
title: "实验 C：两卡 DDP 的最小训练"
sidebar:
  order: 3
---

## 硬件条件

需要 Linux、两张可用 NVIDIA GPU 与支持 NCCL 的 PyTorch。本实验不是 CPU 模拟，不满足条件时先读源码与 3.1 节；没有实测就不填写速度结果。

~~~bash
torchrun --standalone --nproc_per_node=2 labs/ddp.py
~~~

每个进程绑定 LOCAL_RANK 对应 GPU，采样器分配数据，DDP 同步梯度。每 epoch 推进 set_epoch，最终断言各卡模型参数一致。全局平均 loss 通过累计损失总和与样本数归约计算；示例数据等长等权，不涵盖变长 token 加权。

## 验收

确认只有 rank 0 输出汇总；有效 batch 为 8×2=16；训练结束无集合通信等待。不要把这个小型线性模型拿来证明多卡性能，它主要验证数据和同步语义。

扩展实验应固定全局 batch，比较单卡与两卡，在足够大的真实计算负载下记录 step time、吞吐与通信；先读 3.4 节，再讨论加速比。

## 可选进阶

按对应版本官方教程迁移到 FSDP2，记录峰值显存与 step time；在有完整证据前不把“改用了 FSDP”写成“解决了大规模训练问题”。本仓库不声称已执行这个进阶实验。
