import json
import pandas as pd

def load_conversations(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []

    for convo in data["transcripts"]:
        transcript_id = convo["transcript_id"]
        intent = convo["intent"]
        domain = convo["domain"]

        for idx, turn in enumerate(convo["conversation"]):
            rows.append({
                "transcript_id": transcript_id,
                "turn_id": idx,
                "speaker": turn["speaker"],
                "text": turn["text"],
                "intent": intent,
                "domain": domain,
                "is_escalation": intent.lower().startswith("escalation")
            })

    return pd.DataFrame(rows)
