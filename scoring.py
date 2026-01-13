# scoring.py

def compute_human_score(action_log, reward_log, total_steps, done):
    """
    Returns: score (0–100), level string, feedback list
    """

    score = 50

    # Speed
    if total_steps <= 5:
        score += 20
    elif total_steps <= 8:
        score += 10
    else:
        score -= 5

    # Decision quality
    good = sum(1 for r in reward_log if r > 0)
    bad = sum(1 for r in reward_log if r < 0)

    score += good * 3
    score -= bad * 4

    # Outcome
    if done:
        score += 20
    else:
        score -= 20

    score = max(0, min(100, score))

    if score >= 95:
        level = "Tier-3 Ready"
    elif score >= 85:
        level = "Tier-2 Ready"
    elif score >= 70:
        level = "Tier-1 Ready"
    elif score >= 50:
        level = "Junior SOC"
    else:
        level = "Needs Training"

    feedback = []
    if bad > good:
        feedback.append("Too many risky actions taken.")
    if total_steps > 8:
        feedback.append("Slow containment.")
    if not done:
        feedback.append("Incident not fully resolved.")

    return score, level, feedback
