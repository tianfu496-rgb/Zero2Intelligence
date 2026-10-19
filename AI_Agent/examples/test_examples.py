"""运行：python -m unittest discover -s AI_Agent/examples -p 'test_*.py' -v。"""
import json
import unittest
from unittest.mock import patch, MagicMock

from core import Action, ScriptedModel, Tool, ToolRegistry, final_action, run_agent, tool_action
from demo import patterns_demo, study
from evaluate import evaluate
from ollama_model import OllamaModel
from patterns import Review, Step, plan_and_solve, reflect
from retrieval import Document, MemoryStore, Packet, Retriever, build_context


class ExamplesTest(unittest.TestCase):
    def setUp(self):
        self.tools = ToolRegistry()
        self.tools.register(Tool("add", "sum", {"a": "number", "b": "number"}, lambda a, b: a + b))

    def test_tool_result_drives_next_turn(self):
        class ObservingModel:
            def complete(inner, messages, schema):
                if len(messages) == 2:
                    return tool_action("add", a=2, b=3)
                self.assertIn('"value": 5', messages[-1]["content"])
                return final_action("5")
        result = run_agent(ObservingModel(), self.tools, "sum")
        self.assertEqual((result.status, result.answer), ("finished", "5"))

    def test_format_error_can_recover(self):
        model = ScriptedModel(["not json", final_action("recovered")])
        self.assertEqual(run_agent(model, self.tools, "x").answer, "recovered")

    def test_unknown_tool_never_executes(self):
        model = ScriptedModel([tool_action("shell", command="anything"), final_action("blocked")])
        result = run_agent(model, self.tools, "x")
        self.assertFalse(result.trace[0]["observation"]["ok"])

    def test_reject_bool_and_extra_arguments(self):
        for args in [{"a": True, "b": 2}, {"a": 1, "b": 2, "path": "x"}, {"a": float("inf"), "b": 2}]:
            self.assertFalse(self.tools.call("add", args)["ok"])

    def test_tool_exception_becomes_observation(self):
        self.tools.register(Tool("divide", "divide", {"a": "number"}, lambda a: a / 0))
        self.assertEqual(self.tools.call("divide", {"a": 1})["error"], "ZeroDivisionError")

    def test_step_budget_stops_repeated_tools(self):
        model = ScriptedModel([tool_action("add", a=1, b=1)] * 3)
        self.assertEqual(run_agent(model, self.tools, "x", max_turns=3).status, "step_limit")

    def test_model_failure_is_not_success(self):
        self.assertEqual(run_agent(ScriptedModel([]), self.tools, "x").status, "model_error")

    def test_action_rejects_inconsistent_final_and_nan(self):
        for raw in ['{"kind":"final","tool":"add","arguments":{},"answer":"x"}',
                    '{"kind":"tool","tool":"add","arguments":{"a":NaN},"answer":""}']:
            with self.assertRaises(ValueError):
                Action.parse(raw)

    def test_plan_dependency_validation_precedes_execution(self):
        called = []
        with self.assertRaises(ValueError):
            plan_and_solve("x", lambda _: [Step("b", "x", ("missing",))],
                           lambda step, inputs: called.append(step.id))
        self.assertEqual(called, [])
        self.assertEqual(patterns_demo()["plan_results"]["hours"], "2.5")

    def test_reflection_reports_unresolved_after_budget(self):
        result = reflect("wrong", lambda _: Review(False, "fix"), lambda text, feedback: text, 2)
        self.assertFalse(result.accepted)
        self.assertEqual(result.revisions, 2)

    def test_memory_isolation_expiry_and_delete(self):
        store = MemoryStore()
        store.put("a", "one", "Python", ttl=2, now=10)
        store.put("b", "one", "Python")
        self.assertEqual(len(store.recall("a", "Python", now=11)), 1)
        self.assertEqual(store.recall("a", "Python", now=12), [])
        store.delete("b", "one")
        self.assertEqual(store.recall("b", "Python"), [])

    def test_no_overlap_returns_no_evidence(self):
        docs = [Document("a", "Python", "a.md")]
        self.assertEqual(Retriever(docs).search("unrelated"), [])
        self.assertTrue(study("unrelated", documents=docs).answer.startswith("资料不足"))

    def test_repository_study_question_retrieves_comparison_section(self):
        result = study("RAG 与记忆有什么区别？")
        self.assertEqual(result.status, "finished")
        self.assertIn("笔记摘录：\n记忆与 RAG 的分工", result.answer)
        self.assertIn("#记忆与-rag-的分工", result.answer)

    def test_context_preserves_whole_packet_and_budget(self):
        packet = Packet("evidence" * 100, "a", 1)
        context = build_context("rule", "question", [packet], budget_chars=100)
        self.assertNotIn("[a]", context)
        self.assertLessEqual(len(context), 100)
        with self.assertRaises(ValueError):
            build_context("rule" * 100, "q", [], budget_chars=100)

    def test_ollama_transport_contract_without_live_service(self):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps(
            {"message": {"content": final_action("ok")}}).encode()
        with patch("ollama_model.urlopen", return_value=response) as send:
            text = OllamaModel("local-test-model").complete([{"role": "user", "content": "q"}], {"type": "object"})
            self.assertEqual(Action.parse(text).answer, "ok")
            request = send.call_args.args[0]
            body = json.loads(request.data)
            self.assertFalse(body["stream"])
            self.assertEqual(body["format"], {"type": "object"})

    def test_small_regression_suite(self):
        self.assertEqual(evaluate()["passed"], 3)


if __name__ == "__main__":
    unittest.main()
