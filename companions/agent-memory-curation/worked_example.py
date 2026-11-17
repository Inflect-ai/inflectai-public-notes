"""Reproduce a dropped instruction, then curate the same input. No live hooks."""

from memory_context import plan_context


BUDGET = 500
OLD = "Deploy after the branch is reviewed."
NEW = "Deploy only after the exact artifact is reviewed."
NOTES = "Investigation notes from the previous session. " * 20


def record(name, text, status, priority, version=1):
    return {
        "id": name, "text": text, "status": status, "priority": priority,
        "version": version, "applies_to": ["*"], "acts": ["deployment"],
        "source": "operator-decision:example-" + str(version),
    }


def simulate():
    # Both instructions exist. The legacy loader spends the budget in file order.
    combined = "\n\n".join([OLD, NOTES, NEW])
    legacy = combined[:BUDGET]

    records = [
        record("old-deploy", OLD, "ENDED", 0),
        record("notes", NOTES, "LIVE", 10),
        record("deploy", NEW, "LIVE", 0, version=2),
    ]
    ordered = sorted(records, key=lambda r: r["priority"])
    curated, seen = plan_context(ordered, None, {"deployment"}, {}, cap=BUDGET)

    # Replace the live instruction again; retain version 2 as history.
    current = records[2]
    records.append(dict(current, id="deploy-v2-history", status="ENDED"))
    current.update(version=3, source="operator-decision:example-3",
                   text=NEW + " Record the rollback plan too.")
    ordered = sorted(records, key=lambda r: r["priority"])
    refreshed, refreshed_seen = plan_context(
        ordered, None, {"deployment"}, seen, cap=BUDGET
    )
    return {
        "combined": combined, "legacy": legacy, "curated": curated,
        "refreshed": refreshed, "seen": seen, "refreshed_seen": refreshed_seen,
    }


def main():
    result = simulate()
    print("APPEND-ONLY LOADER")
    print("Old instruction loaded:", OLD in result["legacy"])
    print("New instruction exists in the input:", NEW in result["combined"])
    print("New instruction loaded:", NEW in result["legacy"])
    print("Delivered characters:", len(result["legacy"]))
    print("\nCURATED LOADER")
    print(result["curated"])
    print("\nAFTER THE NEXT OPERATOR CHANGE")
    print(result["refreshed"])


if __name__ == "__main__":
    main()
