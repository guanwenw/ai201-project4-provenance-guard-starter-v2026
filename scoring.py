import config

def combine_signals(model_score: float, style_score: float) -> float:
    """Weighted average with a disagreement pull toward 0.5."""
    combined = config.WEIGHT_MODEL_SIGNAL * model_score + config.WEIGHT_STYLE_SIGNAL * style_score
    if abs(model_score - style_score) > 0.4:
        combined = combined * 0.8 + 0.5 * 0.2
    return round(max(0.0, min(1.0, combined)), 4)

def score_to_label(score: float) -> tuple[str, str]:
    """Turn a score into a guess and the reader-facing label text."""
    if score >= config.AI_THRESHOLD:
        return "ai", "This writing looks machine-generated to us."
    if score <= config.HUMAN_THRESHOLD:
        return "human", "This writing looks like a person wrote it."
    return "unsure", (
        "We can't tell whether a person or a machine wrote this, so we're "
        "not labelling it either way."
    )

def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
