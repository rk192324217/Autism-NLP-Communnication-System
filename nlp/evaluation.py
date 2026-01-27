from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_predictions(y_true, y_pred):
    return {
        "precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "f1": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }

def context_retention_score(previous_tokens, current_tokens):
    if not previous_tokens or not current_tokens:
        return 0.0

    overlap = set(previous_tokens).intersection(set(current_tokens))
    return round(len(overlap) / len(set(previous_tokens)), 3)
