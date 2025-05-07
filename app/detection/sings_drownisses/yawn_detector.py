
########## --------- Detecta bostezos basándose en el MAR (Mouth Aspect Ratio) y su duración sostenida --------- #########

class YawnDetector:
    
    # Inicializa el detector de bostezos
    
    def __init__(self, umbral_mar: float = 0.5, frames_requeridos: int = 30):
        
        self.umbral_mar = umbral_mar  # Umbral mínimo de MAR para considerar un bostezo
        self.frames_requeridos = frames_requeridos  # Cantidad de frames consecutivos sobre el umbral para confirmar un bostezo

        self.frames_sobre_umbral = 0
        self.bostezo_activo = False
        self.total_bostezos = 0
        self.detectado = False


    # Detecta si ha ocurrido un bostezo a partir del valor actual de MAR

    def detectar(self, mar: float) -> bool:
        self.detectado = False

        if mar > self.umbral_mar:
            self.frames_sobre_umbral += 1

            if not self.bostezo_activo and self.frames_sobre_umbral >= self.frames_requeridos:
                self.total_bostezos += 1
                self.bostezo_activo = True
                self.detectado = True
                print("😮 ¡Bostezo detectado!")

        else:
            self.frames_sobre_umbral = 0
            self.bostezo_activo = False

        return self.detectado
    
    
    # Devuelve el número total de bostezos detectados

    def obtener_total(self) -> int:
        return self.total_bostezos


    # Reinicia todos los contadores y estados del detector de bostezos

    def reiniciar(self):
        self.total_bostezos = 0
        self.frames_sobre_umbral = 0
        self.bostezo_activo = False
        self.detectado = False