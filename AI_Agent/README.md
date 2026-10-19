# AI Agent：沿 Hello Agents 主线学习

[← 仓库首页](../README.md)

本主题以 Datawhale [Hello Agents](https://github.com/datawhalechina/hello-agents) 为学习主线，按“基础 → 范式与框架 → 记忆、上下文与协作 → 训练与评估 → 综合项目”归纳知识。把相互关联的知识放在同一章，并以“仓库学习助手”贯穿代码与练习。

## 章节目录与上游映射

| 本仓库章节 | Hello Agents 对应章号 |
| --- | --- |
| [Agent 概念与语言模型基础](01-Agent概念与语言模型基础.md) | 1、2、3 |
| [经典智能体范式](02-经典智能体范式.md) | 4 |
| [平台与框架的选择](03-平台与框架的选择.md) | 5、6 |
| [工具调用与最小框架](04-工具调用与最小框架.md) | 7 |
| [记忆与检索增强](05-记忆与检索增强.md) | 8 |
| [上下文工程](06-上下文工程.md) | 9 |
| [多智能体协作与通信协议](07-多智能体协作与通信协议.md) | 6、10 |
| [Agentic RL 与训练](08-AgenticRL与训练.md) | 11 |
| [评估、调试与可靠性](09-评估调试与可靠性.md) | 12 |
| [综合实践与毕业设计](10-综合实践与毕业设计.md) | 13、14、15、16 |

## 推荐学习路线

1. **理解闭环**：第 1、2 章，分清观察、行动、计划与反馈。
2. **运行内核**：第 3、4 章，理解平台/框架后，亲手追踪一次工具调用。
3. **让信息可用**：第 5、6 章，处理知识、历史与输入预算。
4. **扩展系统**：第 7 章，学习角色交接、任务状态和通信边界。
5. **判断是否变好**：先运行第 9 章评估；需要参数优化时再读第 8 章训练。
6. **完成交付**：第 10 章，把知识点变成可运行、可复现的项目。

只做第一版应用时，可先读 1、2、4、5、6、9、10 章。SFT/RL 是进阶路线，理解并运行 Agent 不要求先训练模型。

先修：[Python 基础](../1.PYTHON基础/Python基础.md)、[语言模型与 Transformer](../5.自然语言处理/04-注意力与Transformer.md)。需要理解梯度和损失时可读[深度学习](../3.深度学习/README.md)。

## 关键知识点直达

| 想解决的问题 | 阅读位置 |
| --- | --- |
| 对话、工作流和 Agent 如何区分？ | [控制方式与适用情形](01-Agent概念与语言模型基础.md#对话工作流与-agent-的选择) |
| ReAct、规划和反思怎样组合？ | [三种范式对比](02-经典智能体范式.md#三种范式如何组合) |
| 模型输出怎样变成真实工具调用？ | [动作协议](04-工具调用与最小框架.md#动作协议与原生-tool-calling) |
| Memory 与 RAG 的关系是什么？ | [信息分工](05-记忆与检索增强.md#记忆与-rag-的分工) |
| 上下文太长怎么办？ | [GSSC](06-上下文工程.md#gssc从候选信息到模型输入)、[预算](06-上下文工程.md#预算如何计算) |
| MCP 和 A2A 各做什么？ | [通信协议与协作](07-多智能体协作与通信协议.md) |
| 反思与训练有什么区别？ | [运行时反思](02-经典智能体范式.md#reflection-与-reflexion)、[参数优化](08-AgenticRL与训练.md) |
| 怎么知道修改有效？ | [分层评估](09-评估调试与可靠性.md)、[综合项目](10-综合实践与毕业设计.md) |

## 配套代码

[运行说明](examples/README.md)提供 Python 3.10+ 标准库实现：

- `core.py`：模型接口、动作解析、工具注册与校验、有界执行循环和轨迹。
- `patterns.py`：带依赖的 Plan-and-Solve、有验收与修改上限的 Reflection。
- `retrieval.py`：TF-IDF 检索、隔离与过期记忆、完整证据包的上下文选择。
- `demo.py`：工具调用、规划反思、记忆、仓库笔记助手四种演示。
- `ollama_model.py`：可选本地真实模型接口；`evaluate.py` 与测试覆盖运行边界。

从仓库根目录即可运行：

```bash
python AI_Agent/examples/demo.py react
python AI_Agent/examples/demo.py study --question "RAG 与记忆有什么区别？"
python AI_Agent/examples/evaluate.py
python -m unittest discover -s AI_Agent/examples -p "test_*.py" -v
```

离线演示使用固定脚本或摘录策略，验证组件和控制逻辑；真实模型可选接入本地 Ollama。协议客户端、GPU 训练、生产级持久化与并发调度不在示例实现范围内，相关章节提供概念和扩展路径。

原有 [RAG 简明笔记](RAG%28Retrieval%20Augmented%20Generation%29检索增强生成.md)保留，用作速查。

## 参考来源与整理方式

整理日期：2026-10-19。Hello Agents 参考快照：[`36f583c`](https://github.com/datawhalechina/hello-agents/tree/36f583c233ea5cee4537ef93455702b55053af18)。各章末尾链接到该快照的对应中文教程，方便对照学习；[上游主页](https://github.com/datawhalechina/hello-agents)和[在线阅读](https://hello-agents.datawhale.cc/)可查看后续更新。

本仓库正文为重新组织的学习归纳，配套代码为针对本仓库设计的教学实现，不是官方 HelloAgents 框架，也不是逐章完整复刻。教程中的旅行、研究、小镇与毕业设计归入综合实践；框架名称在同一章对照，范式在同一章比较。

感谢 Datawhale 与 Hello Agents 贡献者。上游作品采用 [CC BY-NC-SA 4.0](https://github.com/datawhalechina/hello-agents/blob/36f583c233ea5cee4537ef93455702b55053af18/LICENSE.txt)；使用或再分发上游原文、图片和代码时请查阅对应许可。本次没有复制其图片、整章正文或框架代码。
