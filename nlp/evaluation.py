from sklearn.metrics import precision_score, recall_score, f1_score

def context_retention_score(previous_tokens, current_tokens):
    if not previous_tokens or not current_tokens:
        return 0.0
    prev_set = set(previous_tokens)
    curr_set = set(current_tokens)
    overlap = prev_set.intersection(curr_set)
    return round(len(overlap) / len(curr_set), 3)

def predict_from_score(score, threshold):
    if score == float("-inf"):
        return 0
    return 1 if score >= threshold else 0

def compute_metrics(y_true, y_pred):
    if not y_true or not y_pred:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    return {
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }

def generate_recommendation(context_score, token_count):
    if context_score >= 0.7:
        return "Strong contextual continuity observed. The patient response aligns well with recent conversation."
    if context_score >= 0.4:
        return "Moderate context retention. Consider using simpler or more structured prompts."
    if token_count <= 3:
        return "Very short response detected. Encourage the patient with follow-up questions."
    return "Low contextual alignment detected. The patient may be experiencing difficulty maintaining conversational flow."
