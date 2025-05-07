# console_test.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
from detection.detection_main import DrowsinessDetection


def setup_camera(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("No se puede abrir la cámara.")
    print("📷 Cámara detectada correctamente...")
    return cap

def main():
    try:
        cap = setup_camera()
        detector = DrowsinessDetection()
        ultima_probabilidad = 0.0  # Valor anterior de probabilidad

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("⚠️ No se logró detectar ningún frame.")
                break

            frame, parpadeo, microsueno_nivel, bostezo, ear, prob = detector.proceso_imagen(frame)

            # Mostrar eventos detectados
            if parpadeo:
                print("👁️ ¡Parpadeo detectado!")
            if microsueno_nivel == 'moderado':
                print("😴 Microsueño leve: ojos cerrados por 2 segundos.")
            elif microsueno_nivel == 'critico':
                print("🚨 Microsueño crítico: ojos cerrados más de 3 segundos. ¡ALERTA!")
            if bostezo:
                print("😮 ¡Bostezo detectado!")

            # Solo imprimir si la probabilidad sube
            if prob > ultima_probabilidad:
                print(f"📊 Probabilidad de somnolencia aumentó a: {prob:.2f}%")
                ultima_probabilidad = prob

            # Mostrar el frame en una ventana
            cv2.imshow("🧠 Malla Facial - Detección de Somnolencia", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Saliendo del sistema...")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
