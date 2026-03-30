import re

ACTION_STARTERS = (
    "todo:",
    "todo",
    "action:",
    "action",
    "fix",
    "review",
    "update",
    "create",
    "add",
    "remove",
    "implement",
    "investigate",
    "schedule",
    "assign",
    "send",
    "email",
    "call",
    "meet",
    "plan",
    "prepare",
    "document",
    "refactor",
    "test",
    "follow up",
    "follow-up",
    "complete",
    "finalize",
    "prioritize",
    "approve",
    "submit",
    "deploy",
    "merge",
)
ACTION_KEYWORDS = (
    "asap",
    "deadline",
    "due by",
    "due",
    "need to",
    "must",
    "should",
    "please",
    "action required",
    "action item",
    "follow-up",
    "follow up",
)


def _normalize_line(line: str) -> str:
    clean = line.strip()
    clean = re.sub(r"^[\s>*-]+", "", clean)
    return clean.strip()


def _is_action_item(line: str) -> bool:
    normalized = line.lower().strip()
    if not normalized:
        return False

    if any(normalized.startswith(prefix) for prefix in ACTION_STARTERS):
        return True

    if re.search(r"\b(?:" + r"|".join(re.escape(keyword) for keyword in ACTION_KEYWORDS) + r")\b", normalized):
        return True

    if normalized.endswith("!"):
        return bool(re.match(r"^(please\s+)?[a-z]+", normalized))

    return False


def extract_action_items(text: str) -> list[str]:
    lines = [_normalize_line(line) for line in text.splitlines() if line.strip()]
    results: list[str] = []
    for line in lines:
        if _is_action_item(line):
            results.append(line)
    return results


