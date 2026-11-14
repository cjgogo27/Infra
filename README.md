# 听懂大模型与具身智能 Infra

从零理解训练、推理与部署，面向 Infra 实习准备与工程入门。

📖 **[在线阅读](https://cjgogo27.github.io/Infra/)** · [从零开始](src/content/docs/guides/01-start.md) · [实验](src/content/docs/labs/01-lab.md)

## 内容

- 6 章 24 节正文，34 个内容页面，约 17,207 个中文字符。
- 系统与显存基础；CT/SFT/RL；数据 IO 与 Checkpoint。
- DDP/FSDP/ZeRO、Megatron 并行、NCCL 与资源调度。
- Profiler、Roofline、计算图、CUDA/Triton Kernel。
- Attention/KV Cache、导出、TensorRT/TRT-LLM、量化与服务化。
- VLM/VLA、Diffusion 动作头、Action Chunk、机器人 RL 与闭环延迟。
- 四周路线、岗位对照、术语表、自测、交互预算计算器和实验代码。

每节从工程问题出发，包含中英术语、通俗解释、上下游影响、LabBot 教学案例、自测和一手参考。LabBot 是虚构案例，正文数字为明确标注的估算，不冒充机器人实测。

## 本地阅读与构建

推荐 Node.js 22 LTS、Python 3.11+。在仓库根目录：

~~~bash
npm ci
npm run dev
npm run check:content
npm run build
npm run preview
~~~

浏览器打开命令输出地址下的 /Infra/。正式构建使用 Pagefind 全文搜索；开发模式可能不提供完整索引。

## 实验

先按 [PyTorch 官方说明](https://pytorch.org/get-started/locally/) 安装适合设备的版本。

~~~bash
python labs/benchmark.py --device cpu --batch 1
python labs/checkpoint.py
~~~

GPU 基准：python labs/benchmark.py --device cuda --trace。
两卡实验需 Linux/CUDA/NCCL：torchrun --standalone --nproc_per_node=2 labs/ddp.py。

## 实际验证与限制

2026-11-14 在 Windows、Python 3.12.5、PyTorch 2.11.0+cpu 上运行实验 A、B。检查点继续 3 步的 loss 与模型参数严格一致。原始 CPU 基准记录位于 [validation](validation/)；它们仅表示本机小型 MLP 的一次实验，不是大模型或机器人性能。Node 24.14.0 本地构建通过，CI 使用 Node 22。

未执行 CUDA、DDP、FSDP、TensorRT、量化、torch.compile 或真实机器人实验。相应章节讲机制与实验方法，不声明完成这些工程验证。

## 文件组织

- src/content/docs/：全部正文、路线与实验说明。
- src/components/Budget.astro：交互计算器。
- labs/：可运行教学实验。
- scripts/check_content.py：章节结构与内部链接检查。
- .github/workflows/pages.yml：构建并部署 GitHub Pages。

## 来源与致谢

写作组织和呈现体验参考 [cionHuang 的《“听懂”具身智能——以人形机器人为例》](https://cionhuang.github.io/A_Brief_Tutorial_of_Humanoid_Robot/)，使用同类 Astro/Starlight 文档框架。正文、案例、代码、样式调整与计算器独立编写；未复制原书正文或图片，也不代表原作者背书。

技术来源在各节末尾，核对日期 2026-11-14。框架版本变化时请对照所安装版本文档。欢迎带复现步骤或来源的修正。

浏览器视觉检查未执行：当前会话不支持普通网页预览。已检查静态构建、内部页面与资源链接、计算器默认/修改/无效输入逻辑。外部链接检查中的网络超时不等同于失效链接，记录见 validation/source-links.json。
