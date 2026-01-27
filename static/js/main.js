function submitConversation() {
    const caregiver = document.getElementById("caregiverText").value;
    const patient = document.getElementById("patientText").value;

    fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            caregiver: caregiver,
            patient: patient
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("contextScore").innerText =
            data.metrics.context_retention;

        document.getElementById("responseTime").innerText =
            data.metrics.response_time + " s";

        document.getElementById("unsmoothedScore").innerText =
            data.metrics.unsmoothed_log_probability;

        document.getElementById("smoothedScore").innerText =
            data.metrics.smoothed_log_probability;

        document.getElementById("explanationText").innerText =
            data.explanation;
    });
}
