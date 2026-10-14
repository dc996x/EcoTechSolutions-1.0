from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

class Registro_Tiempo:
    def __init__(
        self,
        id_registro: UUID,
        fecha: date,
        horas: Decimal,
        descripcion: str,
        asignacion
    ):
        self.id_registro = id_registro
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion
        self.fecha_creacion = datetime.now()

        self.asignacion = asignacion
        asignacion.registros_tiempo.append(self)

    def validar_horas(self) -> bool:
        return self.horas > 0

    def actualizar_descripcion(self, texto: str):
        self.descripcion = texto