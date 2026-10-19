"""Plan-and-Solve 与有次数上限的 Reflection：由调用方注入规划、执行和审查函数。"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Step:
    id: str
    instruction: str
    depends_on: tuple[str, ...] = ()


def plan_and_solve(task: str, planner: Callable[[str], list[Step]],
                   executor: Callable[[Step, dict[str, str]], str],
                   max_steps: int = 8) -> dict[str, str]:
    steps = planner(task)
    if not steps or not 1 <= len(steps) <= max_steps:
        raise ValueError("计划为空或超出步骤预算")
    # 先完整校验，再开始执行；本例要求依赖均在前面的步骤中。
    known: set[str] = set()
    for step in steps:
        if not step.id or step.id in known or not set(step.depends_on) <= known:
            raise ValueError("步骤 ID 重复或依赖尚未定义")
        known.add(step.id)
    results: dict[str, str] = {}
    for step in steps:
        inputs = {key: results[key] for key in step.depends_on}
        results[step.id] = executor(step, inputs)
    return results


@dataclass(frozen=True)
class Review:
    accepted: bool
    feedback: str


@dataclass(frozen=True)
class ReflectionResult:
    text: str
    accepted: bool
    revisions: int


def reflect(draft: str, reviewer: Callable[[str], Review],
            reviser: Callable[[str, str], str], max_revisions: int = 2) -> ReflectionResult:
    if type(max_revisions) is not int or max_revisions < 0:
        raise ValueError("修改次数必须为非负整数")
    for count in range(max_revisions + 1):
        review = reviewer(draft)
        if review.accepted:
            return ReflectionResult(draft, True, count)
        if count == max_revisions:
            return ReflectionResult(draft, False, count)
        draft = reviser(draft, review.feedback)
    raise AssertionError("不可达")
