
###### ---------- Clase que gestiona la probabilidad de somnolencia con base en eventos detectados. ------ #######

class DrowsinessProbability:
  

    def __init__(self):
        
        self.probabilidad = 0.0  # Porcentaje actual de somnolencia (0% a 100%)
        self.contador_parpadeos = 0
        self.frames_sin_eventos = 0
        self.frames_por_minuto = 30 * 60  # Asumiendo 30 fps
        self.frames_para_descuento = self.frames_por_minuto  # Cada minuto se evalúa inactividad
        
        

    def actualizar_por_parpadeo(self):
        self.contador_parpadeos += 1



    def actualizar_por_bostezo(self):
        self._aumentar_probabilidad(10)



    def actualizar_por_microsueno(self, tipo: str):
        if tipo == 'moderado':
            self._aumentar_probabilidad(30)
        elif tipo == 'critico':
            self._aumentar_probabilidad(60)


# Llamar una vez por frame. Evalúa si hay que ajustar probabilidad.

    def tick(self):

        self.frames_sin_eventos += 1

        # Cada minuto, evaluamos condiciones
        if self.frames_sin_eventos >= self.frames_para_descuento:
            if self.contador_parpadeos >= 25:
                self._aumentar_probabilidad(4)
            else:
                self._disminuir_probabilidad(3)

            # Reiniciar contador
            self.contador_parpadeos = 0
            self.frames_sin_eventos = 0



    def obtener_probabilidad(self) -> float:
        return round(self.probabilidad, 2)



    def _aumentar_probabilidad(self, cantidad: float):
        self.probabilidad = min(100.0, self.probabilidad + cantidad)
        self.frames_sin_eventos = 0



    def _disminuir_probabilidad(self, cantidad: float):
        self.probabilidad = max(0.0, self.probabilidad - cantidad)
        self.frames_sin_eventos = 0