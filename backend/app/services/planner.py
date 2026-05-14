def derive_plan(prompt: str, time_budget_minutes: int) -> dict:
    if time_budget_minutes <= 30:
        depth = "rapid"
        checkpoints = [25, 50, 100]
    elif time_budget_minutes <= 240:
        depth = "standard"
        checkpoints = [25, 50, 75, 100]
    else:
        depth = "deep"
        checkpoints = [10, 25, 50, 75, 90, 100]

    return {
        "strategy": depth,
        "checkpoints": checkpoints,
        "steps": [
            "Clarify constraints and success criteria",
            "Implement highest-impact changes first",
            "Validate output and produce confirm/fix artifact",
        ],
        "prompt_summary": prompt[:500],
    }
