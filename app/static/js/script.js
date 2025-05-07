/* script.js */
let avgProbability = 0;
let midRisk = 0;
let highRisk = 0;
let totalSeconds = 0;
let events = [];

function updateDashboard() {
    document.getElementById("avgProbability").textContent = avgProbability + "%";
    document.getElementById("midRisk").textContent = midRisk;
    document.getElementById("highRisk").textContent = highRisk;
    document.getElementById("recordedTime").textContent = new Date(totalSeconds * 1000).toISOString().substr(11, 8);
}

function addEventToTable(event) {
    const table = document.getElementById("eventTable");
    const row = table.insertRow();
    row.innerHTML = `
        <td>${event.id}</td>
        <td>${event.time}</td>
        <td>${event.duration}</td>
        <td>${event.risk}</td>
        <td>${event.probability}</td>
        <td>${event.alertType}</td>
    `;
}

document.getElementById("startBtn")?.addEventListener("click", () => {
    window.location.href = "/dashboard";
});

document.getElementById("stopBtn")?.addEventListener("click", () => {
    alert("Detección detenida.");
});

document.getElementById("exportBtn")?.addEventListener("click", () => {
    const csv = events.map(e => `${e.id},${e.time},${e.duration},${e.risk},${e.probability},${e.alertType}`).join("\n");
    const blob = new Blob(["ID,Hora,Duración,Riesgo,Probabilidad,Tipo de alerta\n" + csv], { type: 'text/csv' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "registro_somnolencia.csv";
    link.click();
});
