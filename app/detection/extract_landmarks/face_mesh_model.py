
import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Any


# ------- Configuración y ejecución el modelo MediaPipe FaceMesh para obtener landmarks faciales ------- #


class FaceMeshLandmarks:

    def __init__(self, max_faces=1, detection_conf=0.6, tracking_conf=0.6):
        self.modelo = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )

    def procesar(self, frame: np.ndarray) -> Tuple[bool, Any]:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = self.modelo.process(frame_rgb)
        return bool(resultados.multi_face_landmarks), resultados