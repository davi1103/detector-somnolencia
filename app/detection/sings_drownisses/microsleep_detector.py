class MicrosleepDetector:
    def __init__(self, umbral_ear: float = 0.21, frames_moderado: int = 40, frames_critico: int = 60):
        self.umbral_ear = umbral_ear
        self.frames_moderado = frames_moderado
        self.frames_critico = frames_critico

        self.frames_bajo_umbral = 0
        self.en_microsueno = False
        self.estado = None

    def detectar(self, ear_promedio: float) -> str:
        self.estado = None

        if ear_promedio < self.umbral_ear:
            self.frames_bajo_umbral += 1
            self.en_microsueno = True
        else:
            if self.en_microsueno:
                if self.frames_bajo_umbral >= self.frames_critico:
                    self.estado = 'critico'
                elif self.frames_bajo_umbral >= self.frames_moderado:
                    self.estado = 'moderado'

            # Reiniciamos después de terminar un posible microsueño
            self.frames_bajo_umbral = 0
            self.en_microsueno = False

        return self.estado

    # Reinicia el estado del detector de microsueños
    def reiniciar(self):
        self.frames_bajo_umbral = 0
        self.estado_microsueno = "ninguno"
