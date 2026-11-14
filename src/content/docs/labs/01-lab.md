---
title: "实验 A：测量、复跑，再解释结果"
sidebar:
  order: 1
---

## 准备与第一次运行

先完成 [实验 0](/Infra/labs/00-training/)，读 [延迟与吞吐](/Infra/01-foundations/04/)。在仓库根目录、已安装 PyTorch 的 Python 环境中运行。CPU 即可，不下载模型或数据。

~~~bash
python labs/benchmark.py --device cpu --batch 1 --threads 1 --output lab-results/b1.json
python labs/benchmark.py --device cpu --batch 32 --threads 1 --output lab-results/b32.json
python labs/compare_benchmarks.py lab-results/b1.json lab-results/b32.json
~~~

固定线程数，是为了避免两次运行默认线程池不同。记录 Python、PyTorch、设备、线程、输入尺寸和后台负载。示例网络是 256→512→64 的合成 MLP，输入常驻内存；不是已训练的 VLA。

## 字段怎样读

| 字段 | 含义与单位 |
| --- | --- |
| p50_ms、p95_ms | 每次整批调用的延迟分位数，单位ms |
| samples_per_second | 总样本数 / 全部测量调用的总耗时 |
| raw_ms | 每次原始耗时，保存在JSON中，便于检查离群点 |
| peak_allocated_bytes | CUDA活跃tensor分配峰值；CPU为null，不是0 |
| correctness | 输出对照检查；不等于模型任务准确率 |

吞吐应按 batch×测量次数÷总秒数计算。**不能用 batch÷p50 推算测量吞吐**：分位数不是所有调用的平均值。每样本摊销时间可用总耗时÷总样本数，但它不等于在线单请求延迟。

## 已有记录的判读示范

下表引用仓库 validation/b1.json 与 validation/b32.json：Windows、PyTorch 2.11.0+cpu、14线程、20次预热与100次测量。它们是历史单次运行，**不是上面固定1线程命令的预期性能**。

| batch | p50（ms/批） | p95（ms/批） | 样本/s |
| --- | --- | --- | --- |
| 1 | 0.09155 | 0.10931 | 7984.92 |
| 32 | 0.14520 | 0.19217 | 231469.76 |

可说：这两份记录中，大batch的每批分位延迟更高，但样本吞吐也更高。不能说：每个在线用户响应更快、VLA提速同样多、或者这一次差异已经稳定可复现。微小CPU调用容易受线程池和调度影响。

## 独立进程复跑

~~~bash
python labs/repeat_benchmark.py --batch 1 --runs 3 --threads 1 --output-dir lab-results/repeat-b1
python labs/repeat_benchmark.py --batch 32 --runs 3 --threads 1 --output-dir lab-results/repeat-b32
~~~

每次运行在独立进程中进行。查看各次原始结果及 summary.json，比较运行间波动。三次是入门练习，不是统计显著性的保证；若波动接近改动收益，应继续调查负载、预热和样本数，而非挑最好一次。

## 可选分支与失败处理

有兼容CUDA环境时，可将单次命令改为 --device cuda；边界同步测的是串行调用墙钟时间，包含主机提交等开销，不代表异步服务最大吞吐。添加 --compile 需本机支持相应后端；首次编译不计入稳态测量，要另报冷启动。

| 现象 | 下一步 |
| --- | --- |
| 找不到脚本 | 回仓库根目录，确认存在labs目录 |
| No module named torch | 在当前Python环境按官方说明安装PyTorch |
| CUDA unavailable | 先完成CPU路线；核对设备与PyTorch构建，不把CPU结果称作GPU结果 |
| 编译后端不可用 | 保留eager基线，记录原因；不要为了完成本实验强行配置整个CUDA栈 |
| 数值断言失败 | 先核对dtype、输入和后端，不能忽略错误继续报告性能 |

--trace 可额外采集少量调用，采集在计时后执行。要学习分阶段判读，继续 [实验 G](/Infra/labs/07-profiler/)。

验收：解释一份JSON、比较两个配置、保留全部复跑记录，并明确至少两条不能得出的结论。
