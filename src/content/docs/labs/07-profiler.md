---
title: "实验 G：从CPU时间线提出可验证假设"
sidebar:
  order: 7
---

## 采集一条带语义标记的时间线

先完成 [实验 A](/Infra/labs/01-lab/)，读 [4.1节](/Infra/04-performance/01/)。本实验实际采集CPU工作，不声称观察到CUDA计算或通信。

~~~bash
python labs/profile_pipeline.py --output-dir lab-results/profile
~~~

得到 pipeline.json.trace 与 summary.json。三个范围标记是 prepare_inputs、policy_forward、postprocess：准备输入、执行小模型、后处理。仓库 validation/profile-summary.json 保存一次实际采集摘要，其耗时不是你本机必须复现的标准。

## 一次实际CPU采集：不要当作稳态基准

环境为Windows、PyTorch 2.11.0+cpu、1线程，每个范围采集10次。累计inclusive时间包含子操作；self时间排除这些子操作。单位都是微秒（μs）。

| 范围 | 次数 | inclusive累计μs | inclusive每次均值μs | self累计μs |
| --- | --- | --- | --- | --- |
| prepare_inputs | 10 | 1445.7 | 144.57 | 700.5 |
| policy_forward | 10 | 1888.6 | 188.86 | 506.4 |
| postprocess | 10 | 330.8 | 33.08 | 293.9 |

这里每次均值只是累计值除以10，**不是不带profiler的模型延迟**，也不是p50或p95。本次输入生成也占明显时间，但它不是实际图像解码。建议先提出“复用输入是否减少整体用时”的假设，再独立计时验证。

可下载 [实际CPU trace](https://raw.githubusercontent.com/cjgogo27/Infra/main/validation/profile-pipeline.json.trace) 和 [采集摘要](https://github.com/cjgogo27/Infra/blob/main/validation/profile-summary.json) 对照阅读。

## 用Perfetto打开本地trace

打开 [Perfetto官方UI](https://ui.perfetto.dev/)，选择 **Open trace file**，选取本地 pipeline.json.trace。搜索 prepare_inputs、policy_forward 或 postprocess，展开对应进程/线程轨道，选中一个区间查看持续时间；缩放到同一次调用附近，看三个范围怎样衔接。

如果页面不能加载，先保留trace文件，直接阅读summary.json中的阶段摘要。不需要通过截图证明“看过图”；报告清楚图形检查未完成即可。不要把本机trace上传到不明查看器。

## 怎样从观察走向假设

| 观察 | 暂时可以说 | 下一项验证 |
| --- | --- | --- |
| prepare_inputs累计时间较大 | 此次采样中输入准备值得调查 | 复用固定输入，比较不带profiler的整体耗时 |
| policy_forward较大 | 本例模型执行占比较大 | 固定线程与输入，换batch对照 |
| 某次调用明显更慢 | 存在尾部事件 | 比较相邻调用，复跑并检查系统负载 |

查看摘要时分清范围包含的子操作与自身开销。父范围和子算子持续时间可能重叠，不能把所有行相加当作墙钟时间。Profiler增加开销，最终收益要回到不带profiler的基准验证。

## GPU双轨图：仅教学示意，非实测

~~~text
时间向右 →
CPU: [准备][提交A][提交B]........[同步等待]
GPU:       [拷贝] [计算A][计算B]...........
~~~

这张示意图说明“CPU提交返回”不等于“GPU任务完成”；它不表示本CPU实验真的产生CUDA事件，也不证明存在通信重叠。

自测：如果CPU提交很快，能否宣称GPU只用了这段时间？不能。若GPU出现空白，仅凭空白能否断言是IO？不能，还需对应CPU活动、依赖和数据供给证据。下一步应做可隔离的对照，而不是直接重写kernel。

验收：选一个实际CPU范围、记录其证据、提出一个假设与一个对照实验，并写出至少一个当前trace不能支持的结论。
