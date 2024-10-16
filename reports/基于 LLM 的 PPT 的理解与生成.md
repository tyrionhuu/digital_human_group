# 基于 LLM 的 PPT 的理解与生成

[toc]

## 课题简介

## 主要研究学科和方向

主要研究方向为语言与视觉模型的应用。

## 工作计划与时间安排

1个月完成调研

1个月编写代码

2个月完成修改论文。

## 文献检索总述

### PPTC Benchmark: Evaluating Large Language Models for PowerPoint Task Completion

http://arxiv.org/abs/2311.01767

PowerPoint Task Completion (PPTC) benchmark 是一个用于评估大语言模型 (LLMs) 在多回合、多模态环境中创建和编辑 PowerPoint 文件能力的评测基准。现有的 LLM 评估主要集中在零样本/小样本自然语言任务和将指令翻译为工具 API 的能力上，而 PPTC 则旨在填补复杂工具使用评估的空白。

### LayoutPrompter: Awaken the Design Ability of Large Language Models

https://proceedings.neurips.cc/paper_files/paper/2023/hash/88a129e44f25a571ae8b838057c46855-Abstract-Conference.html

LayoutPrompter 是一种用于条件图形布局生成的新方法，旨在自动将用户约束映射到高质量的布局。尽管现有方法取得了一些进展，但其通用性和数据效率不足，限制了实际应用。LayoutPrompter 通过使用大语言模型 (LLMs) 进行上下文学习来解决这些问题，由三大关键组件组成：输入输出序列化、动态示例选择和布局排序。

- **输入输出序列化**：设计每个布局生成任务的输入和输出格式。
- **动态示例选择**：为给定的输入选择最有用的提示示例。
- **布局排序**：从 LLM 的多个输出中挑选质量最高的布局。

### From Local to Global: A Graph RAG Approach to Query-Focused Summarization

http://arxiv.org/abs/2404.16130

Graph RAG 是一种用于在私有文本语料库上回答问题的创新方法，结合了检索增强生成 (RAG) 和图结构方法的优势，解决了传统 RAG 在处理全局性问题时的局限性，如“数据集中有哪些主要主题？”。这些问题本质上是查询聚焦的摘要 (QFS) 任务，而不是简单的检索任务。现有的 QFS 方法无法扩展到典型 RAG 系统所需的大规模文本。

### ChartReader: A Unified Framework for Chart Derendering and Comprehension without Heuristic Rules

https://openaccess.thecvf.com/content/ICCV2023/html/Cheng_ChartReader_A_Unified_Framework_for_Chart_Derendering_and_Comprehension_without_ICCV_2023_paper.html

ChartReader 是一种统一的框架，旨在解决图表理解中的挑战，通过无缝集成图表的反解析和理解任务，提升性能和准确性。图表具有多种类型和复杂的组成部分，使得传统的图表理解方法依赖启发式规则或 OCR 系统，效果不够理想。

ChartReader 包括基于 Transformer 的图表组件检测模块和扩展的预训练视觉语言模型，用于执行 Chart-to-X 任务。通过从标注数据集中自动学习图表的规则，ChartReader 减少了手动规则制定的需求，提升了效率和精度。此外，还引入数据变量替换技术，并扩展预训练模型的输入和位置嵌入，实现跨任务训练。