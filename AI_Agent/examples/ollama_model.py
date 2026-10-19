"""可选：通过本地 Ollama /api/chat 接入真实模型，不安装额外 Python 包。"""
from __future__ import annotations

import json
from urllib.request import Request, urlopen


class OllamaModel:
    def __init__(self, model: str, base_url: str = "http://127.0.0.1:11434",
                 timeout: float = 120) -> None:
        if not model.strip():
            raise ValueError("必须选择已在本地安装的模型")
        self.model, self.base_url, self.timeout = model, base_url.rstrip("/"), timeout

    def complete(self, messages: list[dict[str, str]], schema: dict) -> str:
        payload = json.dumps({"model": self.model, "messages": messages,
                              "stream": False, "format": schema,
                              "options": {"temperature": 0}},
                             ensure_ascii=False).encode("utf-8")
        request = Request(self.base_url + "/api/chat", data=payload,
                          headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(request, timeout=self.timeout) as response:
            body = response.read(1_000_001)
        if len(body) > 1_000_000:
            raise ValueError("模型响应超过示例的 1 MB 上限")
        content = json.loads(body)["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("模型响应缺少文本 content")
        return content
