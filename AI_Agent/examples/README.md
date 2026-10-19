# Agent 配套代码

[← Agent 主题目录](../README.md) · [综合实践](../10-综合实践与毕业设计.md)

使用 Python 3.10+ 标准库即可运行离线示例，无需 API Key、GPU 或 pip 安装。所有命令从仓库根目录执行。Windows 终端若出现中文编码问题，可设置 `$env:PYTHONIOENCODING="utf-8"` 后重试。

## 代码地图

| 文件 | 学习内容 |
| --- | --- |
| [core.py](core.py) | 动作 JSON、工具契约、执行循环、错误与终止状态 |
| [patterns.py](patterns.py) | 计划依赖、顺序执行、反馈与反思预算 |
| [retrieval.py](retrieval.py) | TF-IDF、记忆 owner/TTL、原子证据上下文 |
| [demo.py](demo.py) | 四种可运行演示与仓库笔记检索 |
| [ollama_model.py](ollama_model.py) | 可选真实模型适配器 |
| [evaluate.py](evaluate.py) | 独立评分、来源召回与资料不足拒答 |
| [eval_cases.json](eval_cases.json) | 三条独立于策略的期望结果 |
| [test_examples.py](test_examples.py) | 执行与检索边界回归测试 |

## 离线演示

```bash
python AI_Agent/examples/demo.py react
python AI_Agent/examples/demo.py patterns
python AI_Agent/examples/demo.py memory
python AI_Agent/examples/demo.py study --question "Agent 的工具与环境有什么关系？"
```

| 模式 | 实际执行内容 | 应观察的结果 |
| --- | --- | --- |
| `react` | 固定动作脚本调用真实 add 函数 | `finished`、答案 42、工具观察中 value=42 |
| `patterns` | 固定计划与规则审查，传递分钟/小时依赖 | 150 分钟、2.5 小时、一次修改后通过 |
| `memory` | 写入两用户记录，查询一用户并构造上下文 | 只返回 student-a 的 Python 偏好 |
| `study` | 按二级标题读取两份仓库笔记、词面检索、摘录 | 真实片段及来源；无词面重叠时说明不足 |

离线脚本用于教学重放，不能据此声称模型学会了工具调用、规划或反思。`study` 的离线策略只摘录首条结果，不做语义充分性判断。

## 可选：本地真实模型

1. 先在本机安装并启动 Ollama，安装你希望实验的模型。
2. 用 `ollama list` 查看实际模型名，将下方占位符替换为该名称。
3. 模型与服务需支持本例使用的 JSON Schema 结构化输出。默认连接本机 `http://127.0.0.1:11434`。

```bash
python AI_Agent/examples/demo.py react --live --model YOUR_LOCAL_MODEL
python AI_Agent/examples/demo.py study --live --model YOUR_LOCAL_MODEL --question "RAG 与记忆有什么区别？"
```

可用 `--base-url` 显式选择自己的服务地址。真实模式会发送问题、工具描述和取得的公开笔记片段；没有配置密钥的云端接口不属于本例支持范围。

实现基于 [Ollama Chat API](https://docs.ollama.com/api/chat)及[结构化输出](https://docs.ollama.com/capabilities/structured-outputs)。模型返回 JSON 后仍由执行器校验；不同模型可能发生格式错误、错误选工具或提前结束。默认最多六轮模型调用，适配器单请求超时 120 秒。两项预算含义不同。

`model_error` 表示接口/模型调用失败，可检查服务是否运行、模型名称是否正确和结构化输出是否支持。`step_limit` 表示轮数耗尽，应查看 trace；不会自动放大预算。

## 评估与验证

```bash
python AI_Agent/examples/evaluate.py
python -m unittest discover -s AI_Agent/examples -p "test_*.py" -v
```

评估集只有三个案例，使用独立的小知识库检查来源召回与无证据拒答。它是可改写的回归起点，不是完整问答评测集，也不评估回答与证据的语义支持关系。

测试通过本地替身校验 Ollama 的 HTTP 请求/响应契约，不会连接真实服务。真实模型推理质量、联网表现、GPU 训练、MCP/A2A/ANP 互通均需在相应环境另做验证。

## 实现边界与扩展顺序

- 核心工具 Schema 只支持必填的平面基本类型，复杂输入需更完整的校验器。
- 工具动作是教学文本 JSON 协议；对接原生 Tool Calling 时需适配消息角色与调用 ID。
- 记忆只在进程内；字符上下文预算不是 token 计数，且未自动裁剪执行循环中的历史。
- TF-IDF 使用英文词和中文单字。分块按标题，未处理任意文档的超长章节、所有代码块边界或文档访问权限。
- 内置工具只做有限数加法和固定公开笔记检索。轮数预算不能中断阻塞工具；增加外部工具时另设超时、结果大小与业务约束。

推荐先扩充真实问题集，再改进分块与检索，之后接入模型、持久化记忆和协议适配。每次扩展保留旧基线，比较质量与成本。
