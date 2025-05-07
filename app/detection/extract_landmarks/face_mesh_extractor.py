from typing import List, Dict, Any

##### ------------- Extrae puntos de interés de la malla facial: ojos, boca, etc -------- ####


class FaceMeshExtractor:
    
    # Convierte los puntos normalizados de la malla en coordenadas absolutas respecto al tamaño de la imagen
    
    def extract_points(self, face_image_shape, face_mesh_info: Any) -> List[List[int]]:
        h, w, _ = face_image_shape
        mesh_points = [
            [i, int(pt.x * w), int(pt.y * h)]
            for face in face_mesh_info.multi_face_landmarks
            for i, pt in enumerate(face.landmark)
        ]
        return mesh_points
    
    
    # Extrae los puntos específicos de una región facial (ojos, boca, etc.) según los índices dados.

    def extract_feature_points(self, face_points: List[List[int]], feature_indices: dict) -> Dict[str, List[List[int]]]:
        result = {}
        for sub_feature, sub_indices in feature_indices.items():
            result[sub_feature] = [face_points[i][1:] for i in sub_indices]
        return result
    
    
    # Devuelve los puntos de ambos ojos necesarios para el cálculo del EAR.

    def get_eyes_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        feature_indices = {
            'distances': [33, 160, 158, 133, 153, 144, 362, 385, 387, 263, 373, 380]
        }
        return self.extract_feature_points(face_points, feature_indices)


    # Devuelve los puntos de ambos ojos necesarios para el cálculo del MAR.

    def get_mouth_points(self, face_points: List[List[int]]) -> Dict[str, List[List[int]]]:
        feature_indices = {
            'distances': [61, 291, 13, 14]
        }
        return self.extract_feature_points(face_points, feature_indices)

