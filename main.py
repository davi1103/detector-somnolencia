import cv2
from app.detection.detection_main import DrowsinessDetection

def setup_camera(index=1):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        raise RuntimeError("No se puede abrir la cámara.")
    print("Cámara detectada correctamente...")
    return cap

def main():
    try:
        cap = setup_camera()
        detector = DrowsinessDetection()

        ultima_probabilidad = 0.0  # <- Probabilidad registrada en el frame anterior

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("⚠️ No se logró detectar ningún frame.")
                break

            frame, parpadeo, microsueno_nivel, bostezo, ear, prob = detector.proceso_imagen(frame)

            if parpadeo:
                print("👁️ ¡Parpadeo detectado!")
            if microsueno_nivel == 'moderado':
                print("😴 Microsueño leve: ojos cerrados por 2 segundos.")
            elif microsueno_nivel == 'critico':
                print("🚨 Microsueño crítico: ojos cerrados más de 3 segundos. ¡ALERTA!")
            if bostezo:
                print("😮 ¡Bostezo detectado!")

            # Solo mostrar si la probabilidad ha aumentado
            if prob > ultima_probabilidad:
                print(f"📊 Probabilidad de somnolencia aumentó a: {prob:.2f}%")
                ultima_probabilidad = prob  # Actualiza el último valor registrado

            cv2.imshow("Malla Facial - Detección de Somnolencia", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("🛑 Saliendo del sistema...")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
