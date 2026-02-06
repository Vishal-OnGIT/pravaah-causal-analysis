import re

ESCALATION_KEYWORDS = [
    "supervisor", "manager", "complaint", "legal",
    "frustrating", "unacceptable", "wasted enough time",
    "lawyer", "escalate", "formal complaint"
]
CAUSAL_LENSES = {
    "delay": ["wait", "long", "time", "delay", "hours", "days"],
    "repetition": ["again", "multiple", "times", "repeated", "called"],
    "escalation_request": ["supervisor", "manager", "escalate"],
    "legal_threat": ["legal", "lawyer", "complaint", "sue"],
    "resolution_failure": ["not fixed", "didn't work", "unresolved"]
}

def score_turn(text):
    score = 0
    text_lower = text.lower()

    for kw in ESCALATION_KEYWORDS:
        if kw in text_lower:
            score += 2

    if "not" in text_lower or "never" in text_lower:
        score += 1

    if "again" in text_lower or "multiple" in text_lower:
        score += 1

    return score


def detect_query_focus(query):
    query = query.lower()
    active_lenses = []

    for lens, keywords in CAUSAL_LENSES.items():
        for kw in keywords:
            if kw in query:
                active_lenses.append(lens)
                break

    return active_lenses

def extract_causal_evidence(df, query):
    lenses = detect_query_focus(query)

    escalation_df = df[df["is_escalation"]]
    evidence = []

    for tid, group in escalation_df.groupby("transcript_id"):
        group = group.copy()

        def lens_score(text):
            score = 0
            text = text.lower()
            for lens in lenses:
                for kw in CAUSAL_LENSES[lens]:
                    if kw in text:
                        score += 2
            return score

        group["causal_score"] = group["text"].apply(lens_score)

        top = group[group["causal_score"] > 0].sort_values(
            "causal_score", ascending=False
        ).head(3)

        if not top.empty:
            evidence.append({
                "transcript_id": tid,
                "factors": top["text"].tolist()
            })

    return evidence, lenses

def generate_explanation(lenses):
    if not lenses:
        return (
            "Escalations are primarily caused by unresolved repeated issues, "
            "explicit requests for supervisors, and a perceived lack of resolution."
        )

    explanations = []

    if "delay" in lenses:
        explanations.append(
            "Prolonged delays in resolving customer issues increase frustration, "
            "making escalation more likely."
        )

    if "repetition" in lenses:
        explanations.append(
            "Repeated unresolved interactions signal service failure, which strongly "
            "contributes to escalation."
        )

    if "escalation_request" in lenses:
        explanations.append(
            "Explicit requests for supervisors indicate loss of trust in frontline support, "
            "often preceding escalation."
        )

    if "legal_threat" in lenses:
        explanations.append(
            "Mentions of legal action or formal complaints reflect severe dissatisfaction "
            "and directly trigger escalation outcomes."
        )

    if "resolution_failure" in lenses:
        explanations.append(
            "Perceived lack of resolution reinforces customer dissatisfaction, "
            "leading to escalation."
        )

    return " ".join(explanations)
