import numpy as np
from typing import List

##### ------------- Clase para procesar puntos faciales de la boca y calcular el MAR (Mouth Aspect Ratio). ---------- ########


class MouthProcessor:
    
    # Calcula la distancia euclidiana entre dos puntos

    def calcular_distancia(self, p1: List[int], p2: List[int]) -> float:
        return np.linalg.norm(np.array(p1) - np.array(p2))
    
    
    # Calcula el MAR (Mouth Aspect Ratio) usando 4 puntos específicos

    def calcular_mar(self, puntos_boca: List[List[int]]) -> float:
        
        if len(puntos_boca) != 4:
            raise ValueError("Se esperaban 4 puntos para calcular MAR.")

        p1, p2, p3, p4 = puntos_boca

        horizontal = self.calcular_distancia(p1, p2)
        vertical = self.calcular_distancia(p3, p4)

        if horizontal == 0:
            return 0.0

        mar = vertical / horizontal
        
        return round(mar, 4)