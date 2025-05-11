// static/js/script.js

let events = [];
let chart;
let detectionInterval = null;

function getIconForEvent(type) {
    switch (type) {
        case "Parpadeo": return "👁️ Parpadeo";
        case "Microsueño": return "😴 Microsueño";
        case "Bostezo": return "😮 Bostezo";
        default: return type;
    }
}

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById("avgProbability").textContent = data.avgProbability;
            document.getElementById("recordedTime").textContent = data.recordedTime;
            document.getElementById("blinkCount").textContent = data.blinkCount;
            document.getElementById("microsleepCount").textContent = data.microsleepCount;
            document.getElementById("yawnCount").textContent = data.yawnCount;

            const table = document.getElementById("eventTable");
            table.innerHTML = "";
            data.events.forEach(event => {
                const row = table.insertRow();
                row.innerHTML = `
                    <td>${event.id}</td>
                    <td>${event.time}</td>
                    <td>${event.duration}</td>
                    <td>${event.risk}</td>
                    <td>${event.probability}</td>
                    <td>${getIconForEvent(event.eventType)}</td>
                `;
            });

            events = data.events;

            const labels = data.events.map(e => e.time);
            const values = data.events.map(e => parseFloat(e.probability.replace('%', '')));

            if (chart) {
                chart.data.labels = labels;
                chart.data.datasets[0].data = values;
                chart.update();
            } else {
                const ctx = document.getElementById('probabilityChart')?.getContext('2d');
                if (ctx) {
                    chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Probabilidad de Somnolencia',
                                data: values,
                                borderWidth: 2,
                                borderColor: 'rgba(0, 123, 255, 1)',
                                fill: false
                            }]
                        },
                        options: {
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    max: 100
                                }
                            }
                        }
                    });
                }
            }
        });
}

detectionInterval = setInterval(fetchData, 1000);

const exportBtn = document.getElementById("exportBtn");
if (exportBtn) {
    exportBtn.addEventListener("click", () => {
        const csv = events.map(e => `${e.id},${e.time},${e.duration},${e.risk},${e.probability},${e.eventType}`).join("\n");
        const blob = new Blob(["ID,Hora,Duración,Riesgo,Probabilidad,Tipo de evento\n" + csv], { type: 'text/csv' });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "registro_somnolencia.csv";
        link.click();
    });
}

const startBtn = document.getElementById("startBtn");
if (startBtn) {
    startBtn.addEventListener("click", () => {
        const welcomeCard = document.querySelector('.welcome .card');
        if (welcomeCard) {
            welcomeCard.classList.add("fade-out");
            setTimeout(() => {
                window.location.assign("/dashboard");
            }, 500);
        } else {
            window.location.assign("/dashboard");
        }
    });
}

const stopBtn = document.getElementById("stopBtn");
if (stopBtn) {
    stopBtn.addEventListener("click", () => {
        clearInterval(detectionInterval);
        alert("🛑 Detección detenida correctamente.");

        const video = document.getElementById("videoStream");
        if (video) video.style.display = "none";

        stopBtn.style.display = "none";

        const actionsDiv = stopBtn.parentNode;

        const continueBtn = document.createElement("button");
        continueBtn.textContent = "Continuar Detección";
        continueBtn.classList.add("btn-continue");
        continueBtn.style.margin = "10px";
        continueBtn.onclick = () => {
            video.style.display = "block";
            detectionInterval = setInterval(fetchData, 1000);
            continueBtn.remove();
            restartBtn.remove();
            stopBtn.style.display = "inline-block";
        };

        const restartBtn = document.createElement("button");
        restartBtn.textContent = "Empezar de nuevo";
        restartBtn.classList.add("btn-restart");
        restartBtn.style.margin = "10px";
        restartBtn.onclick = () => {
            fetch("/reiniciar", { method: "POST" })
                .then(() => location.reload());
        };

        actionsDiv.appendChild(continueBtn);
        actionsDiv.appendChild(restartBtn);
    });
}
