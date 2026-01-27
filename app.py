from flask import Flask, render_template, request, redirect, session, jsonify
import time
from collections import deque

from nlp.preprocessing import tokenize
from nlp.ngram_models import NGramModel
from nlp.evaluation import context_retention_score
from utils.auth import authenticate_user, register_user
from utils.logger import log_conversation

app = Flask(__name__)
app.secret_key = "secure_session_key"

WINDOW_SIZE = 3
context_window = deque(maxlen=WINDOW_SIZE)


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
    return render_template("home.html", role=session["role"])


@app.route("/process", methods=["POST"])
def process():
    start_time = time.time()
    data = request.json

    caregiver_query = data.get("caregiver")
    patient_response = data.get("patient")

    patient_tokens = tokenize(patient_response)

    previous_tokens = []
    for sentence_tokens in context_window:
        previous_tokens.extend(sentence_tokens)

    context_score = context_retention_score(previous_tokens, patient_tokens)

    unsmoothed_model = NGramModel(n=2)
    smoothed_model = NGramModel(n=2, smoothing="laplace")

    unsmoothed_model.train(patient_tokens)
    smoothed_model.train(patient_tokens)

    unsmoothed_score = unsmoothed_model.sentence_log_probability(patient_tokens)
    smoothed_score = smoothed_model.sentence_log_probability(patient_tokens)

    context_window.append(patient_tokens)

    response_time = round(time.time() - start_time, 4)

    metrics = {
        "unsmoothed_log_probability": round(unsmoothed_score, 4),
        "smoothed_log_probability": round(smoothed_score, 4),
        "context_retention": context_score,
        "response_time": response_time
    }

    log_conversation(caregiver_query, patient_response, metrics)

    explanation = (
        "The patient response maintains conversational context across recent turns."
        if context_score >= 0.6
        else "The patient response shows reduced context continuity. Consider simplifying or rephrasing."
    )

    return jsonify({
        "metrics": metrics,
        "explanation": explanation
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
