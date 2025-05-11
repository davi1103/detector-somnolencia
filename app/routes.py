from flask import Flask, render_template, Response, jsonify, request
import cv2
from app.detection.detection_main import DrowsinessDetection
import time

app = Flask(__name__)

detector = DrowsinessDetection()
camera = cv2.VideoCapture(0)
eventos = []
ultima_probabilidad = 0.0
inicio_tiempo = time.time()

# Contadores globales
blink_count = 0
microsleep_count = 0
yawn_count = 0

def gen_frames():
    global ultima_probabilidad, eventos, blink_count, microsleep_count, yawn_count

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame, parpadeo, microsueno_nivel, bostezo, ear, prob = detector.proceso_imagen(frame)

            tipo_evento = "-"
            if parpadeo:
                blink_count += 1
                tipo_evento = "Parpadeo"
            elif microsueno_nivel:
                microsleep_count += 1
                tipo_evento = "Microsueño"
            elif bostezo:
                yawn_count += 1
                tipo_evento = "Bostezo"

            if tipo_evento != "-":
                evento = {
                    "id": len(eventos) + 1,
                    "time": time.strftime("%H:%M:%S"),
                    "duration": "1 seg",
                    "risk": microsueno_nivel if microsueno_nivel else "-",
                    "probability": f"{prob:.0f}%",
                    "eventType": tipo_evento
                }
                eventos.append(evento)

            ultima_probabilidad = prob

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data')
def data():
    global eventos, inicio_tiempo
    elapsed_time = int(time.time() - inicio_tiempo)
    avg_prob = sum([float(e['probability'].strip('%')) for e in eventos]) / len(eventos) if eventos else 0

    return jsonify({
        "avgProbability": f"{avg_prob:.0f}%",
        "recordedTime": time.strftime("%H:%M:%S", time.gmtime(elapsed_time)),
        "events": eventos[-30:],  # últimos 30
        "blinkCount": blink_count,
        "microsleepCount": microsleep_count,
        "yawnCount": yawn_count
    })

@app.route('/reiniciar', methods=['POST'])
def reiniciar():
    global eventos, inicio_tiempo, blink_count, microsleep_count, yawn_count, detector

    eventos = []
    blink_count = 0
    microsleep_count = 0
    yawn_count = 0
    inicio_tiempo = time.time()

    # Reinicia el estado interno del detector (EAR, MAR, probabilidad)
    detector.reiniciar()

    return jsonify({"status": "ok"})
