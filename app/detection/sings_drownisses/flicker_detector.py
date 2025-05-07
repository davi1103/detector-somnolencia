###### ------- Detecta parpadeos válidos basándose en el EAR (Eye Aspect Ratio) y su duración --------- #######

class FlickerDetector:
    
    # Inicializa el detector de parpadeos
    
    def __init__(self, umbral_ear: float = 0.21, min_duracion: int = 3, max_duracion: int = 7):
        
        self.umbral_ear = umbral_ear              # Umbral para considerar ojos cerrados
        self.min_duracion = min_duracion          # Frames mínimos para un parpadeo válido
        self.max_duracion = max_duracion          # Máximo de frames para NO considerar microsueño

        self.frames_bajo_umbral = 0               # Contador de frames consecutivos con ojos cerrados
        self.parpadeando = False                  # Estado actual: si está ocurriendo un parpadeo
        self.contador_parpadeos = 0               # Total de parpadeos detectados
        self.ear_actual = 0.0                     # Último valor promedio del EAR

        self.cooldown_frames = 0                  # Tiempo de espera tras detectar un parpadeo
        self.cooldown_duracion = 4                # Evita detecciones múltiples muy cercanas


    # Evalúa si ha ocurrido un parpadeo válido según los valores de EAR izquierdo y derecho.

    def detectar(self, ear_izq: float, ear_der: float) -> bool:
        self.ear_actual = (ear_izq + ear_der) / 2.0
        parpadeo_detectado = False

    

        # Control de cooldown: esperar cierto número de frames después de un parpadeo
        if self.cooldown_frames > 0:
            self.cooldown_frames -= 1
            return False

        if self.ear_actual < self.umbral_ear:
            self.frames_bajo_umbral += 1
        else:
            if self.parpadeando:
                # Validamos si la duración fue adecuada para considerarlo parpadeo
                if self.min_duracion <= self.frames_bajo_umbral <= self.max_duracion:
                    self.contador_parpadeos += 1
                    parpadeo_detectado = True
                    
                    self.cooldown_frames = self.cooldown_duracion

                # Reiniciamos el conteo
                self.frames_bajo_umbral = 0
                self.parpadeando = False
            else:
                self.frames_bajo_umbral = 0

        # Si estamos acumulando frames bajos, marcamos que está parpadeando
        if self.frames_bajo_umbral >= self.min_duracion:
            self.parpadeando = True

        return parpadeo_detectado


    # Devuelve el número total de parpadeos detectados.

    def obtener_contador(self) -> int:
        return self.contador_parpadeos


    # Devuelve el último valor promedio calculado del EAR.
    
    def obtener_ear(self) -> float:
        return self.ear_actual
    
    
    # Reinicia todos los contadores y estados del detector

    def reiniciar(self):
        self.contador_parpadeos = 0
        self.parpadeando = False
        self.frames_bajo_umbral = 0
        self.cooldown_frames = 0
