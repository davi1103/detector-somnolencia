class DrowsinessProbability:

    def __init__(self):
        self.probabilidad = 0.0
        self.contador_parpadeos = 0
        self.frames_sin_eventos = 0
        self.frames_por_minuto = 30 * 60  # Asumiendo 30 fps
        self.frames_para_descuento = self.frames_por_minuto

        # Cooldowns para evitar aumentos repetidos
        self.cooldown_bostezo = 0
        self.cooldown_microsueno = 0

    def actualizar_por_parpadeo(self):
        self.contador_parpadeos += 1

    def actualizar_por_bostezo(self):
        if self.cooldown_bostezo == 0:
            self._aumentar_probabilidad(6)
            self.cooldown_bostezo = 90  # 3 segundos de espera

    def actualizar_por_microsueno(self, tipo: str):
        if self.cooldown_microsueno == 0:
            if tipo == 'moderado':
                self._aumentar_probabilidad(12)
            elif tipo == 'critico':
                self._aumentar_probabilidad(20)
            self.cooldown_microsueno = 120  # 4 segundos

    def tick(self):
        self.frames_sin_eventos += 1

        # Reducir cooldowns progresivamente
        if self.cooldown_bostezo > 0:
            self.cooldown_bostezo -= 1
        if self.cooldown_microsueno > 0:
            self.cooldown_microsueno -= 1

        # Cada minuto evalúa si debe disminuir o aumentar ligeramente
        if self.frames_sin_eventos >= self.frames_para_descuento:
            if self.contador_parpadeos >= 25:
                self._aumentar_probabilidad(2)
            else:
                self._disminuir_probabilidad(4)

            self.frames_sin_eventos = 0
            self.contador_parpadeos = 0

    def obtener_probabilidad(self) -> float:
        return round(self.probabilidad, 2)

    def _aumentar_probabilidad(self, cantidad: float):
        self.probabilidad = min(100.0, self.probabilidad + cantidad)
        self.frames_sin_eventos = 0

    def _disminuir_probabilidad(self, cantidad: float):
        self.probabilidad = max(0.0, self.probabilidad - cantidad)
        self.frames_sin_eventos = 0
