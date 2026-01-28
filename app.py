from flask import Flask, render_template, request, redirect, session, jsonify
import time
from collections import deque
import json
from nlp.preprocessing import tokenize
from nlp.ngram_models import NGramModel
from nlp.evaluation import context_retention_score, generate_recommendation
from utils.auth import authenticate_user, register_user
from utils.logger import log_conversation

app = Flask(__name__)
app.secret_key = "secure_session_key"

WINDOW_SIZE = 3
context_window = deque(maxlen=WINDOW_SIZE)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        action = request.form.get("action")

        if action == "register":
            if not register_user(username, password, role):
                return render_template("login.html", error="User already exists")

        if authenticate_user(username, password):
            session["user"] = username
            session["role"] = role
            return redirect("/home")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


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
    data = request.json

    caregiver_query = data.get("caregiver", "")
    patient_response = data.get("patient", "")

    patient_tokens = tokenize(patient_response)

    previous_tokens = []
    for sentence_tokens in context_window:
        previous_tokens.extend(sentence_tokens)

    # Improved context retention
    context_score = context_retention_score(previous_tokens, patient_tokens)

    # N gram models
    unsmoothed_model = NGramModel(n=2)
    smoothed_model = NGramModel(n=2, smoothing="laplace")

    unsmoothed_model.train(patient_tokens)
    smoothed_model.train(patient_tokens)

    unsmoothed_score = unsmoothed_model.sentence_log_probability(patient_tokens)
    smoothed_score = smoothed_model.sentence_log_probability(patient_tokens)

    context_window.append(patient_tokens)

    response_time = round(time.time() - start_time, 4)

    # Therapist style recommendation
    recommendation = generate_recommendation(
        context_score=context_score,
        token_count=len(patient_tokens)
    )

    metrics = {
        "unsmoothed_log_probability": round(unsmoothed_score, 4),
        "smoothed_log_probability": round(smoothed_score, 4),
        "context_retention": context_score,
        "response_time": response_time
    }

    log_conversation(caregiver_query, patient_response, metrics)

    return jsonify({
        "metrics": metrics,
        "explanation": recommendation
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/labeled_data")
def labeled_data():
    with open("data/labeled_data.json", "r") as f:
        return jsonify(json.load(f))


if __name__ == "__main__":
    app.run(debug=True)
