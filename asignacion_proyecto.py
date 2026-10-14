from datetime import date
from uuid import UUID

class Asignacion_Proyecto:
    def __init__(
        self,
        id_asignacion: UUID,
        empleado,
        proyecto,
        fecha_asignacion: date,
        fecha_desasignacion: date = None,
        activa: bool = True
    ):
        self.id_asignacion = id_asignacion
        self.fecha_asignacion = fecha_asignacion
        self.fecha_desasignacion = fecha_desasignacion
        self.activa = activa

        self.empleado = empleado
        self.proyecto = proyecto
        self.registros_tiempo = []

        empleado.asignaciones.append(self)
        proyecto.asignaciones.append(self)

    def cerrar(self, fecha: date):
        self.fecha_desasignacion = fecha
        self.activa = False

    def esta_vigente(self, fecha: date) -> bool:
        if fecha < self.fecha_asignacion:
            return False

        if self.fecha_desasignacion is not None:
            return fecha <= self.fecha_desasignacion

        return self.activa