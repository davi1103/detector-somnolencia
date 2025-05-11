import numpy as np
from typing import Tuple, Dict
from .face_mesh_model import FaceMeshLandmarks
from .face_mesh_drawer import FaceMeshDraw
from .face_mesh_extractor import FaceMeshExtractor
from app.detection.utils.rotation_utils import calcular_inclinacion_pitch


###### ----------- Procesador central que coordina detección, extracción y visualización de la malla facial ------ ##########

class FaceMeshProcessor:
 
    def __init__(self):
        self.landmarks = FaceMeshLandmarks()
        self.dibujador = FaceMeshDraw()
        self.extractor = FaceMeshExtractor()


    #Procesa una imagen, detecta la malla facial, extrae los puntos clave y los dibuja.
    #Devuelve (puntos extraídos, si hay rostro, frame con dibujo).

    def process(self, imagen_cara: np.ndarray) -> Tuple[Dict[str, Dict[str, list]], bool, np.ndarray]:

        initial_frame = imagen_cara.copy()
        face_exist, face_mesh_info = self.landmarks.procesar(imagen_cara)

        if not face_exist:
            return {}, face_exist, initial_frame

        face_points = self.extractor.extract_points(imagen_cara.shape, face_mesh_info)
        angulo_pitch = calcular_inclinacion_pitch(face_points)

        if abs(angulo_pitch) > 35:  # umbral ajustable
            print(f"🔄 Cabeza muy inclinada (pitch = {angulo_pitch:.2f}°). Detección descartada.")
            return {}, False, initial_frame

        points = {
            'eyes': self.extractor.get_eyes_points(face_points),
            'mouth': self.extractor.get_mouth_points(face_points),
        }

        self.dibujador.dibujar(initial_frame, face_mesh_info)
        
        return points, face_exist, initial_frame