async function submitConversation() {
    const caregiverText = document.getElementById("caregiverText").value.trim();
    const patientText = document.getElementById("patientText").value.trim();

    if (!caregiverText || !patientText) {
        alert("Please enter both caregiver question and patient response.");
        return;
    }

    try {
        const response = await fetch("/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                caregiver: caregiverText,
                patient: patientText
            })
        });

        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        // Update table values
        document.getElementById("uScore").textContent = data.metrics.unsmoothed_log_probability;
        document.getElementById("sScore").textContent = data.metrics.smoothed_log_probability;
        document.getElementById("uContext").textContent = data.metrics.context_retention;
        document.getElementById("sContext").textContent = data.metrics.context_retention; // same score for both
        document.getElementById("uTime").textContent = data.metrics.response_time;
        document.getElementById("sTime").textContent = data.metrics.response_time;

        // Update explanation
        document.getElementById("explanationText").textContent = data.explanation;

        // Chart update
        const ctx = document.getElementById("comparisonChart").getContext("2d");

        // Only destroy if it's a Chart instance
        if (window.comparisonChart instanceof Chart) {
            window.comparisonChart.destroy();
        }

        window.comparisonChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Log Probability", "Context Retention", "Response Time"],
                datasets: [
                    {
                        label: "Unsmoothed",
                        data: [
                            data.metrics.unsmoothed_log_probability,
                            data.metrics.context_retention,
                            data.metrics.response_time
                        ],
                        backgroundColor: "rgba(255, 99, 132, 0.6)"
                    },
                    {
                        label: "Smoothed",
                        data: [
                            data.metrics.smoothed_log_probability,
                            data.metrics.context_retention,
                            data.metrics.response_time
                        ],
                        backgroundColor: "rgba(54, 162, 235, 0.6)"
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (err) {
        console.error("Error submitting conversation:", err);
        alert("An error occurred while processing the conversation.");
    }
}
