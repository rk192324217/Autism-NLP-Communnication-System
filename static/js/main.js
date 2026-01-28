let chart;

function submitConversation() {
    const caregiver = document.getElementById("caregiverText").value.trim();
    const patient = document.getElementById("patientText").value.trim();

    if (!caregiver || !patient) {
        alert("Please fill both fields");
        return;
    }

    fetch("/process", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    body: JSON.stringify({ caregiver, patient })
})


}

function updateUI(metrics, explanation) {
    document.getElementById("uScore").innerText = metrics.unsmoothed_log_probability;
    document.getElementById("sScore").innerText = metrics.smoothed_log_probability;
    document.getElementById("uContext").innerText = metrics.context_retention;
    document.getElementById("sContext").innerText = metrics.context_retention;
    document.getElementById("uTime").innerText = metrics.response_time;
    document.getElementById("sTime").innerText = metrics.response_time;

    document.getElementById("explanation").innerText = explanation;

    drawChart(metrics);
}

function drawChart(metrics) {
    const ctx = document.getElementById("chart").getContext("2d");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Unsmoothed", "Smoothed"],
            datasets: [{
                label: "Log Probability",
                data: [
                    metrics.unsmoothed_log_probability,
                    metrics.smoothed_log_probability
                ],
                backgroundColor: ["#dc3545", "#3e7cb1"]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: false }
            }
        }
    });
}
