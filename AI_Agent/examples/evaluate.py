"""小型离线回归集；统计摘录策略的检索/拒答行为，不是 LLM 基准成绩。"""
from __future__ import annotations

import json
from pathlib import Path

from demo import study
from retrieval import Document


def evaluate() -> dict:
    cases = json.loads(Path(__file__).with_name("eval_cases.json").read_text(encoding="utf-8"))
    documents = [Document("tool", "工具调用由执行器校验参数并执行。", "tools.md"),
                 Document("rag", "RAG 先检索资料，再根据证据生成回答。", "rag.md")]
    rows = []
    for case in cases:
        # 期望字段只交给评分器，策略只能看到问题和知识库。
        result = study(case["question"], documents=documents)
        found = [hit for event in result.trace if event["event"] == "tool"
                 and event["observation"]["ok"] for hit in event["observation"]["value"]]
        abstained = result.answer.startswith("资料不足")
        source_ok = case["expected_source"] is None or any(
            hit["source"] == case["expected_source"] for hit in found)
        passed = result.status == "finished" and source_ok and abstained == case["expected_abstain"]
        rows.append({"id": case["id"], "passed": passed, "status": result.status,
                     "retrieved_sources": [hit["source"] for hit in found], "abstained": abstained})
    return {"mode": "offline_extractive_regression", "cases": len(rows),
            "passed": sum(row["passed"] for row in rows), "results": rows}


if __name__ == "__main__":
    report = evaluate()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["passed"] == report["cases"] else 1)
