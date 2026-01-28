from sklearn.metrics import precision_score, recall_score, f1_score
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words("english"))


def meaningful_tokens(tokens):
    """
    Remove stopwords and short tokens
    """
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def context_retention_score(previous_tokens, current_tokens):
    """
    Measures how much of the previous context
    is retained in the current response.
    Returns a value between 0 and 1.
    """
    if not previous_tokens or not current_tokens:
        return 0.0

    prev_meaningful = set(meaningful_tokens(previous_tokens))
    curr_meaningful = set(meaningful_tokens(current_tokens))

    if not curr_meaningful:
        return 0.0

    shared = prev_meaningful.intersection(curr_meaningful)

    score = len(shared) / len(curr_meaningful)
    return round(score, 3)


def generate_recommendation(context_score, token_count):
    """
    Therapist style rule based recommendations
    """
    if token_count < 3:
        return "Patient response is very brief. Encourage simple follow-up questions."

    if context_score < 0.3:
        return (
            "Low contextual continuity detected. "
            "Consider simplifying the question or rephrasing with concrete prompts."
        )

    if context_score < 0.6:
        return (
            "Moderate context retention observed. "
            "Provide gentle clarification to reinforce understanding."
        )

    return (
        "Good contextual understanding observed. "
        "Continue the conversation at the same level."
    )
