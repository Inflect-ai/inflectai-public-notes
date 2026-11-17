# Agent Memory Curation - Runnable Teaching Example

Companion for Thomson Nguy's technical note, **Memory Curation - Solving the Problem of Forgetful Agents.**

This package reproduces an old instruction filling the context budget while its replacement is dropped. It then marks the old instruction ended, gives the current instruction priority, and prints the corrected context. A second operator change refreshes the instruction in the same simulated session.

## Run

Python 3.9 or later. Standard library only; no dependencies, model calls, credentials, or network access.

From the repository root:

```sh
cd companions/agent-memory-curation
python3 worked_example.py
python3 -m unittest discover -s . -p 'test*.py' -v
```

The demonstration uses a 500-character budget. The first loader includes the old instruction and drops the replacement even though it is present in the input. The curated loader delivers the replacement within the same budget and names the omitted notes. The next operator change adds a rollback instruction and is delivered again.

The 19 tests cover status and action filtering, scope, content changes, repeat suppression, compaction reset, transcript growth and shrinkage, over-budget omissions, the worked example, and subprocess adapter behavior.

## Files

| File | Purpose |
| --- | --- |
| [memory_context.py](memory_context.py) | Pure context selector plus an illustrative JSON hook adapter. |
| [worked_example.py](worked_example.py) | Prints the append-only failure, curated delivery, and next revision. |
| [rules.json](rules.json) | Two synthetic operator decisions: one current, one ended. |
| [test_memory_context.py](test_memory_context.py) | Nineteen standard-library tests; adapter tests use temporary directories. |

## Hook Adapter

The adapter reads one JSON event from standard input. For `SessionStart`, it resets delivery state. For `PreToolUse`, it recognizes only the literal fixture tool `mcp__example__deploy`. It emits `hookSpecificOutput.additionalContext`, never a permission grant or a deployment action. Running the adapter writes delivery state under `.example-state/` beside the script. It may inspect a supplied transcript path to measure file size; it does not read transcript content. The demonstration and tests do not install any hooks.

The operator supplies current status, wording, scope, and ordering. In the worked example, priority sorting happens before calling `plan_context`; the selector does not infer which instruction has authority. Only complete rendered rule blocks count as delivered. Omitted rules remain eligible. The production system described in the article also has a short-form delivery path; this teaching example intentionally omits that extra policy.

## Limits

All decisions and fixtures here are synthetic. This is a newly written teaching adaptation, not an export of the production memory control plane, private rulings, or authorization logic. It checks emitted context, not whether a model reads, understands, or follows it.

Unknown actor identity widens advisory context and grants no rights. The adapter does not establish a trusted identity, parse arbitrary shell commands, arbitrate conflicting authorities, or enforce authorization. Keep the rule file operator-controlled. Serialize calls per session or replace the local state file with transactional storage; atomic replacement alone does not prevent concurrent lost updates. Persisting delivery after output is not an end-to-end acknowledgement from a runtime or model.

Before attaching a real runtime, validate that runtime's event contract and inspect what the agent actually receives. Enforce consequential-action permissions in the execution tool, independently of this reminder.

## License

The Python, JSON fixture, tests, and associated documentation in this directory are licensed under the [MIT License](LICENSE), copyright 2026 InflectAI, Inc. This directory-local license does not license the article, parent repository, private implementation, or trademarks.
