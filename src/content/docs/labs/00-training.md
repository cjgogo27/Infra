---
title: "实验 0：看见一次参数更新"
sidebar:
  order: 0
---

## 先修与目标

会运行 Python，知道列表和函数即可开始。先读 [系统总览](/Infra/01-foundations/01/)。本实验只需 CPU 和 PyTorch，用Linear(3,1)解释训练更新，不下载数据或权重，也不训练机器人策略。后续部署实验另用较大的MLP演示导出；两者承担不同教学任务。

~~~bash
python labs/train_basics.py
~~~

在仓库根目录运行。若提示找不到文件，先检查当前目录是否包含 labs 文件夹；若缺少 torch，按 [PyTorch 官方安装页](https://pytorch.org/get-started/locally/) 安装适合设备的构建。首次练习选 CPU 路线，无需先安装 CUDA。

## 跟着一个参数走

把脚本输出的一个参数值、梯度值和 loss 抄成三行观察记录：

| 阶段 | 你要观察什么 | 为什么 |
| --- | --- | --- |
| 前向与 loss 之后 | 预测与目标的差异，参数值 | 前向计算预测，loss 把误差汇成标量 |
| backward 之后 | 参数的梯度，参数是否已变 | 反向传播计算改变参数会怎样影响 loss |
| optimizer.step 之后 | 参数变化 | 优化器根据梯度及自身状态执行更新 |

这里的**参数**是被学习的数；**激活**是某次输入计算产生的中间结果；**梯度**是 loss 对参数的导数；**优化器**决定怎样用梯度更新参数。一个 **batch** 是一次共同处理的样本集合；一个 **epoch** 通常表示遍历一轮训练数据。本实验不需要先理解 Transformer。

训练循环最小骨架如下，实际可运行版本在脚本中：

~~~python
optimizer.zero_grad(set_to_none=True)
prediction = model(x)
loss = loss_fn(prediction, target)
loss.backward()
optimizer.step()
~~~

zero_grad 清理旧梯度；forward 得到 prediction；backward 产生梯度；step 才更新参数。不要把清梯度误解为把模型权重清零。

## 验收与小练习

1. 指出 backward 前后哪些量改变，解释为什么参数通常等到 step 才改变。
2. 找到输入和输出 shape，说明首维与 batch 的关系。
3. 在脚本副本中暂停 step，预测参数是否变化，再检查输出。
4. 暂停 zero_grad 和 step，分别重新forward计算两个loss，各对自己的新计算图做一次backward，解释梯度累积。不要直接对同一个loss重复backward；默认计算图会在反向后释放。不要把这个破坏练习写成正常训练方案。

完成后读 [Tensor 与显存账本](/Infra/01-foundations/03/) 和 [梯度累积](/Infra/02-training/02/)。能解释上述过程，再进入混合精度；无需背下优化器的所有公式。
