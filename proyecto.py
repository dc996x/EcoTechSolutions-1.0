from datetime import date
from uuid import UUID

class Proyecto:
    def __init__(
        self,
        id_proyecto: UUID,
        nombre: str,
        descripcion: str,
        fecha_inicio: date,
        estado
    ):
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.estado = estado

        self.asignaciones = []

    def actualizar_datos(self, datos: dict):
        for atributo, valor in datos.items():
            if hasattr(self, atributo):
                setattr(self, atributo, valor)

    def activar(self):
        self.estado = "activo"

    def cerrar(self):
        self.estado = "cerrado"