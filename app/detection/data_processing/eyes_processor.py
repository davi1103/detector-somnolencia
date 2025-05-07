import numpy as np
from typing import List, Tuple


### ------------- Clase para procesar los puntos faciales de los ojos y calcular el EAR (Eye Aspect Ratio) --------###

class EyesProcessor:
    
    # Calcula la distancia euclidiana entre dos puntos
    
    def calcular_distancia(self, p1: List[int], p2: List[int]) -> float:
        distance = np.linalg.norm(np.array(p1) - np.array(p2))
        return distance
    
    
    # Calcula el EAR de un solo ojo, dado un arreglo con 6 puntos específicos.
    
    def calcular_ear_ojo(self, puntos: List[List[int]]) -> float:
        
        p1,p2,p3,p4,p5,p6 = puntos
        
        vertical_1 = self.calcular_distancia(p2, p6)
        vertical_2 = self.calcular_distancia(p3, p5)
        horizontal = self.calcular_distancia(p1, p4)
        
        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        
        return round(ear, 4)
    
    
    # Calcula el EAR para ambos ojos
    
    def calcular_ear(self, puntos_ojos: List[List[int]]) -> Tuple[float,float]:
        
        if len(puntos_ojos) != 12:
            raise ValueError("Se esperaban 12 puntos (6 por cada ojos)")
    
        puntos_ojo_izquierdo = puntos_ojos[:6]
        puntos_ojo_derecho = puntos_ojos[6:]
        
        ear_izq = self.calcular_ear_ojo(puntos_ojo_izquierdo)
        ear_der = self.calcular_ear_ojo(puntos_ojo_derecho)
        
        return ear_izq, ear_der