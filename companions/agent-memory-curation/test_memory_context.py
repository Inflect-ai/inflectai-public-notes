import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from memory_context import plan_context
from worked_example import BUDGET, NEW, OLD, simulate


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.records = json.loads(Path(__file__).with_name("rules.json").read_text())

    def deliver(self, seen=None, **kwargs):
        return plan_context(self.records, None, {"deployment"}, seen or {}, **kwargs)

    def test_first_delivery(self):
        context, state = self.deliver()
        self.assertIn("exact artifact", context)
        self.assertIn("deployment-review", state)

    def test_history_is_not_current_context(self):
        context, state = self.deliver()
        self.assertNotIn("earlier deployment procedure", context)
        self.assertNotIn("deployment-review-old", state)

    def test_identical_content_is_suppressed(self):
        _, state = self.deliver()
        self.assertEqual(self.deliver(state)[0], "")

    def test_change_without_version_bump_still_reshows(self):
        _, state = self.deliver()
        self.records[0]["text"] = "Updated operator instruction."
        self.assertIn("Updated operator instruction", self.deliver(state)[0])

    def test_compaction_reset(self):
        self.deliver()
        self.assertIn("exact artifact", self.deliver({})[0])

    def test_distance_refresh(self):
        _, state = self.deliver(offset=10)
        self.assertEqual(self.deliver(state, offset=400009)[0], "")
        self.assertIn("exact artifact", self.deliver(state, offset=400010)[0])

    def test_shortened_transcript_refreshes(self):
        _, state = self.deliver(offset=100)
        self.assertIn("exact artifact", self.deliver(state, offset=0)[0])

    def test_scope_and_unknown_actor(self):
        self.records[0]["applies_to"] = ["actor:reviewer"]
        self.assertTrue(self.deliver()[0])
        context, _ = plan_context(self.records, "builder", {"deployment"}, {})
        self.assertEqual(context, "")

    def test_omission_does_not_mark_shown(self):
        self.records[0]["text"] = "x" * 1000
        context, state = self.deliver(cap=220)
        self.assertIn("NOT SHOWN: deployment-review", context)
        self.assertLessEqual(len(context), 220)
        self.assertEqual(state, {})
        self.assertIn("x" * 1000, self.deliver(state)[0])

    def test_skipped_large_record_does_not_starve_small_record(self):
        small = copy.deepcopy(self.records[0])
        small.update(id="short", text="Read this.", source="s")
        self.records[0]["text"] = "x" * 1000
        self.records.append(small)
        context, state = self.deliver(cap=300)
        self.assertIn("Read this.", context)
        self.assertNotIn("deployment-review", state)
        self.assertIn("short", state)

    def test_action_filter(self):
        context, _ = plan_context(self.records, None, {"read"}, {})
        self.assertEqual(context, "")

    def test_startup_selects_all_applicable_live_records(self):
        context, _ = plan_context(self.records, None, None, {})
        self.assertIn("exact artifact", context)


class WorkedExampleTests(unittest.TestCase):
    def test_legacy_loader_preserves_old_and_drops_new(self):
        result = simulate()
        self.assertIn(NEW, result["combined"])
        self.assertIn(OLD, result["legacy"])
        self.assertNotIn(NEW, result["legacy"])
        self.assertEqual(len(result["legacy"]), BUDGET)

    def test_curated_loader_delivers_current_and_reports_omission(self):
        result = simulate()
        self.assertIn(NEW, result["curated"])
        self.assertNotIn(OLD, result["curated"])
        self.assertIn("NOT SHOWN: notes", result["curated"])
        self.assertNotIn("notes", result["seen"])
        self.assertLessEqual(len(result["curated"]), BUDGET)

    def test_next_revision_refreshes_the_same_session(self):
        result = simulate()
        self.assertIn("Record the rollback plan too.", result["refreshed"])
        self.assertNotEqual(result["seen"]["deploy"]["digest"],
                            result["refreshed_seen"]["deploy"]["digest"])
        self.assertLessEqual(len(result["refreshed"]), BUDGET)


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("memory_context.py", "rules.json"):
            shutil.copyfile(Path(__file__).with_name(name), self.root / name)

    def invoke(self, event, **extra):
        payload = {"hook_event_name": event, "session_id": "test-session"}
        payload.update(extra)
        result = subprocess.run(
            [sys.executable, str(self.root / "memory_context.py")],
            input=json.dumps(payload), text=True, capture_output=True, check=True
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def test_startup_emits_context_without_permission_grant(self):
        output = self.invoke("SessionStart")["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        self.assertIn("exact artifact", output["additionalContext"])
        self.assertNotIn("permissionDecision", output)

    def test_repeated_call_then_compaction_reset(self):
        call = {"tool_name": "mcp__example__deploy"}
        self.assertTrue(self.invoke("PreToolUse", **call))
        self.assertFalse(self.invoke("PreToolUse", **call))
        self.assertTrue(self.invoke("SessionStart", source="compact"))

    def test_child_delivery_is_independent_of_parent(self):
        self.invoke("SessionStart")
        output = self.invoke("PreToolUse", tool_name="mcp__example__deploy", agent_id="child")
        self.assertIn("exact artifact", output["hookSpecificOutput"]["additionalContext"])

    def test_unrelated_event_is_silent(self):
        self.assertEqual(self.invoke("PostToolUse"), {})


if __name__ == "__main__":
    unittest.main()
