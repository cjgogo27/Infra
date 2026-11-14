---
title: "Lab 0: observe one parameter update"
sidebar:
  order: 0
---

## Prerequisites and goal

You need basic Python functions/lists and the ability to run a script. Read the [system overview](/Infra/en/01-foundations/01/) first. This CPU/PyTorch experiment uses Linear(3,1), downloads no data or weights, and demonstrates updates, not a robot policy. Later deployment labs use a larger MLP for a different teaching purpose.

~~~bash
python labs/train_basics.py
~~~

Run from the repository root. If the file is missing, check that the current directory contains labs. If torch is missing, follow the [official installation instructions](https://pytorch.org/get-started/locally/). Begin with CPU; CUDA is not a prerequisite.

## Follow one parameter

Copy a displayed parameter, gradient, and loss into an observation table:

| Stage | Observe | Interpretation |
| --- | --- | --- |
| After forward and loss | Prediction error and parameter value | Forward predicts; loss summarizes error |
| After backward | Gradient and whether the parameter changed | Backpropagation computes sensitivity of loss to the parameter |
| After optimizer.step | Parameter change | The optimizer uses gradients and its own state to update values |

A **parameter** is a learned value. An **activation** is an intermediate result for a particular input. A **gradient** is a loss derivative. An **optimizer** decides how to apply gradients. A **batch** groups samples for a pass; an **epoch** usually traverses the training dataset once. Transformer knowledge is not required here.

The minimal training skeleton is below; the script contains the runnable version:

~~~python
optimizer.zero_grad(set_to_none=True)
prediction = model(x)
loss = loss_fn(prediction, target)
loss.backward()
optimizer.step()
~~~

zero_grad clears old gradients, not model weights. Forward computes predictions; backward computes gradients; step updates parameters.

## Acceptance checks

1. Identify what changes during backward and why parameters normally change at step.
2. Locate input/output shapes and explain the batch dimension.
3. In a separate script copy, omit step, predict whether parameters change, then inspect the output.
4. Omit zero_grad and step, run forward again for each of two new losses, and backpropagate once through each fresh graph. Explain accumulation. Do not directly backpropagate the same loss twice: its graph is normally freed after backward. This deliberate break is not a normal training recommendation.

Continue to [tensors and memory](/Infra/en/01-foundations/03/) and [gradient accumulation](/Infra/en/02-training/02/). Explain the update before studying mixed precision; memorizing every optimizer equation is unnecessary.
