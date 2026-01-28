from flask import Flask, render_template, request, redirect, session, jsonify
import time
from collections import deque

# NLP modules
from nlp.preprocessing import tokenize
from nlp.ngram_models import NGramModel
from nlp.evaluation import context_retention_score, generate_recommendation

# Utilities
from utils.auth import authenticate_user, register_user
from utils.logger import log_conversation

app = Flask(__name__)
app.secret_key = "secure_session_key"

WINDOW_SIZE = 3
context_window = deque(maxlen=WINDOW_SIZE)
def safe_number(val): 
    if val == float("-inf") or val == float("inf"): return "Infinity" 
    return round(val, 4)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        action = request.form.get("action")

        if action == "register":
            success = register_user(username, password, role)
            if not success:
                return render_template("login.html", error="User already exists")

        user = authenticate_user(username, password)
        if user:
            session["user"] = username
            session["role"] = user["role"]
            return redirect("/home")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("home.html")

@app.route("/process", methods=["POST"])
def process():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    start_time = time.time()
    data = request.get_json()

    caregiver_query = data.get("caregiver", "").strip()
    patient_response = data.get("patient", "").strip()

    if not caregiver_query or not patient_response:
        return jsonify({"error": "Invalid input"}), 400

    patient_tokens = tokenize(patient_response)

    training_corpus = list(context_window) if context_window else [patient_tokens]
# Ensure it's always a list of lists
    training_corpus = [list(toks) for toks in training_corpus]


    unsmoothed_model = NGramModel(n=2)
    smoothed_model = NGramModel(n=2, smoothing="laplace")

    unsmoothed_model.train(training_corpus)
    smoothed_model.train(training_corpus)

    unsmoothed_score = unsmoothed_model.sentence_log_probability(patient_tokens)
    smoothed_score = smoothed_model.sentence_log_probability(patient_tokens)

    context_score = context_retention_score(
        previous_tokens=[tok for sent in training_corpus for tok in sent],
        current_tokens=patient_tokens
    )

    context_window.append(patient_tokens)

    response_time = round(time.time() - start_time, 4)

    recommendation = generate_recommendation(
        context_score=context_score,
        token_count=len(patient_tokens)
    )

    metrics = {
    "unsmoothed_log_probability": safe_number(unsmoothed_score),
    "smoothed_log_probability": safe_number(smoothed_score),
    "context_retention": context_score,
    "response_time": response_time
}


    log_conversation(caregiver_query, patient_response, metrics)

    return jsonify({
        "metrics": metrics,
        "explanation": recommendation
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
