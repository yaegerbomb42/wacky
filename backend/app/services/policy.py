FORBIDDEN_PATTERNS = [
    "create hidden ip",
    "evade detection",
    "steal",
    "unauthorized purchase",
]

def validate_task(prompt: str) -> tuple[bool, str]:
    low = prompt.lower()
    for pat in FORBIDDEN_PATTERNS:
        if pat in low:
            return False, f"Prompt violates policy: {pat}"
    return True, "ok"
