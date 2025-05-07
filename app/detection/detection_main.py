import numpy as np
from detection.extract_landmarks.face_mesh_processor import FaceMeshProcessor
from detection.data_processing.eyes_processor import EyesProcessor
from detection.data_processing.mouth_processor import MouthProcessor
from detection.sings_drownisses.flicker_detector import FlickerDetector
from detection.sings_drownisses.microsleep_detector import MicrosleepDetector
from detection.sings_drownisses.yawn_detector import YawnDetector
from detection.probability.drowsiness_probability import DrowsinessProbability




######## ------------- Clase principal que integra todos los módulos de procesamiento facial y detección de signos de somnolencia: parpadeos, microsueños y bostezos  ----- ######3

class DrowsinessDetection:

    def __init__(self):
        self.malla_facial = FaceMeshProcessor()
        self.eyes_processor = EyesProcessor()
        self.mouth_processor = MouthProcessor()
        self.flicker_detector = FlickerDetector()
        self.microsleep_detector = MicrosleepDetector()
        self.yawn_detector = YawnDetector()
        self.probabilidad_somnolencia = DrowsinessProbability()


    # Procesa un frame de imagen, detecta el rostro, calcula EAR y MAR, y detecta eventos de somnolencia.

    def proceso_imagen(self, imagen_cara: np.ndarray):

        puntos_faciales, existe_cara, imagen_original = self.malla_facial.process(imagen_cara)

        if not existe_cara:
            return imagen_original, None, None, None, None, None

        # Obtenemos los puntos faciales necesarios (Ojos y Boca)
        puntos_ojos = puntos_faciales.get('eyes', {}).get('distances', [])
        puntos_boca = puntos_faciales.get('mouth', {}).get('distances', [])

        # Obtenemos el EAR de ambos ojos y el MAR de la boca
        ear_izq, ear_der = self._procesar_ear(puntos_ojos)
        mar = self._procesar_mar(puntos_boca)

        # Detectar signos
        parpadeo_detectado = self._detectar_parpadeo(ear_izq, ear_der)
        ear_promedio = self.flicker_detector.obtener_ear()
        microsueno_nivel = self.microsleep_detector.detectar(ear_promedio)
        bostezo = self.yawn_detector.detectar(mar)
        
        if parpadeo_detectado:
            self.probabilidad_somnolencia.actualizar_por_parpadeo()
        if bostezo:
            self.probabilidad_somnolencia.actualizar_por_bostezo()
        if microsueno_nivel:
            self.probabilidad_somnolencia.actualizar_por_microsueno(microsueno_nivel)

        self.probabilidad_somnolencia.tick()
        probabilidad = self.probabilidad_somnolencia.obtener_probabilidad()

        return imagen_original, parpadeo_detectado, microsueno_nivel, bostezo, ear_promedio, probabilidad


    # Calcula el EAR para ambos ojos si se tienen los 12 puntos necesarios.

    def _procesar_ear(self, puntos_ojos: list) -> tuple:

        if len(puntos_ojos) == 12:
            return self.eyes_processor.calcular_ear(puntos_ojos)
        return None, None
    
    
    # Calcula el MAR si se tienen los 4 puntos necesarios.

    def _procesar_mar(self, puntos_boca: list) -> float:
  
        if len(puntos_boca) == 4:
            return self.mouth_processor.calcular_mar(puntos_boca)
        return None
    
    
    # Determina si hubo un parpadeo a partir del EAR de ambos ojos.

    def _detectar_parpadeo(self, ear_izq: float, ear_der: float) -> bool:

        if ear_izq is not None and ear_der is not None:
            return self.flicker_detector.detectar(ear_izq, ear_der)
        return False