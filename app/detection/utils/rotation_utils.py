import numpy as np
from typing import List

def calcular_inclinacion_pitch(face_points: List[List[int]]) -> float:
    """
    Calcula el ángulo de pitch (inclinación vertical) entre la nariz y el mentón.
    Devuelve un valor en grados. Positivo si mira hacia arriba, negativo si hacia abajo.
    """
    try:
        p_nariz = np.array(face_points[1][1:])     # Landmark de la nariz
        p_menton = np.array(face_points[199][1:])  # Landmark del mentón

        dx = p_menton[0] - p_nariz[0]
        dy = p_menton[1] - p_nariz[1]

        # Calculamos el ángulo respecto a la vertical (eje Y)
        angulo_rad = np.arctan2(dx, dy)
        angulo_deg = np.degrees(angulo_rad)

        return angulo_deg  # positivo o negativo
    except:
        return 0.0