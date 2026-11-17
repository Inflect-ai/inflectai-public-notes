"""Teaching example derived from Sabriel's delivery design; not production code.

Python 3.9+. No network calls, command execution, or permission decisions.
The operator controls rules.json. Serialize hook invocations per session.
"""

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
HEADER = (
    "CURRENT OPERATOR RULES: these replace conflicting historical summaries.\n"
    "Delivery records context emitted, not understanding or authorization.\n"
)


def fingerprint(record):
    raw = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def applies(record, actor):
    if not actor:
        return True  # Unknown identity widens advisory context; grants no rights.
    scopes = record.get("applies_to", ["*"])
    return "*" in scopes or "actor:" + actor in scopes


def plan_context(records, actor, acts, seen, cap=3000, offset=0, interval=400000):
    """Return (context, next delivery state). Never mark omitted records shown.

    offset measures transcript bytes, not tokens. None means show every live
    applicable rule, as at startup. An empty set means no recognized action.
    """
    selected = []
    for record in records:
        if record["status"] != "LIVE" or not applies(record, actor):
            continue
        if acts is not None and not set(record["acts"]) & acts:
            continue
        digest = fingerprint(record)
        previous = seen.get(record["id"])
        if previous and previous["digest"] == digest:
            distance = offset - previous["offset"]
            if 0 <= distance < interval:
                continue
        selected.append((record, digest))
    if not selected:
        return "", dict(seen)

    remaining = [record["id"] for record, _ in selected]
    blocks, next_seen = [], dict(seen)
    for record, digest in selected:
        block = (
            f'[{record["id"]} v{record["version"]}] {record["text"]}\n'
            f'Source: {record["source"]}\n'
        )
        rest = [name for name in remaining if name != record["id"]]
        tail = "\nNOT SHOWN: " + ", ".join(rest) if rest else ""
        candidate = HEADER + "\n".join(blocks + [block]) + tail
        if len(candidate) > cap:
            continue
        blocks.append(block)
        remaining = rest
        next_seen[record["id"]] = {"digest": digest, "offset": offset}
    tail = "\nNOT SHOWN: " + ", ".join(remaining) if remaining else ""
    context = HEADER + "\n".join(blocks) + tail
    if len(context) > cap:
        raise ValueError("Budget cannot hold even the omitted-rule notice")
    return context, next_seen


def atomic_state(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
        json.dump(value, handle)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    payload = json.load(sys.stdin)
    event = payload.get("hook_event_name")
    if event not in {"SessionStart", "PreToolUse"}:
        return
    # Identity is deliberately unresolved here: show all matching advisory rules.
    # A real adapter must resolve identity from an operator-controlled registry.
    actor = None
    key = json.dumps([payload["session_id"], payload.get("agent_id", "")])
    state_path = ROOT / ".example-state" / (hashlib.sha256(key.encode()).hexdigest() + ".json")
    try:
        seen = json.loads(state_path.read_text())
    except (OSError, ValueError):
        seen = {}
    records = json.loads((ROOT / "rules.json").read_text())
    if event == "SessionStart":
        seen, acts = {}, None  # Startup/resume/compaction get fresh delivery state.
    else:
        # Deliberately no shell parsing. A literal example MCP tool is the action.
        acts = {"deployment"} if payload.get("tool_name") == "mcp__example__deploy" else set()
    try:
        transcript = payload.get("transcript_path")
        offset = Path(transcript).stat().st_size if transcript else 0
    except OSError:
        offset = 0
    context, next_seen = plan_context(records, actor, acts, seen, offset=offset)
    if context:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": event, "additionalContext": context
        }}), flush=True)
    atomic_state(state_path, next_seen)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # Advisory failure only. Enforce production authorization in the tool.
        print("CONTEXT DELIVERY FAILED: " + type(error).__name__, file=sys.stderr)
        sys.exit(1)
