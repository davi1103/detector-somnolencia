from typing import Any
import mediapipe as mp
import numpy as np


#### --------- Dibuja la malla facial sobre la imagen con configuración personalizada ----------- #######

class FaceMeshDraw:


    def __init__(self):
        
        self.dibujo = mp.solutions.drawing_utils        # inicializamos la variable con el modulo de dibujo de mediapipe
        self.lineas = self.dibujo.DrawingSpec(thickness=1, color=(255, 255, 255))  # Configuracion de lineas
        self.puntos = self.dibujo.DrawingSpec(thickness=1, circle_radius=1, color=(255, 0, 0)) # Configuracion de puntos


    # Dibuja las conexiones y puntos de la malla facial sobre el frame proporcionado

    def dibujar(self, frame: np.ndarray, face_info: Any):
        
        for rostro in face_info.multi_face_landmarks:
            self.dibujo.draw_landmarks(
                image=frame,
                landmark_list=rostro,
                connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=self.puntos,
                connection_drawing_spec=self.lineas
            )