from datetime import date
from decimal import Decimal
from uuid import UUID

class Empleado:
    def __init__(
        self,
        id_empleado: UUID,
        nombre_completo: str,
        direccion: str,
        telefono: str,
        correo: str,
        fecha_inicio_contrato: date,
        salario: Decimal,
        activo: bool = True
    ):
        self.id_empleado = id_empleado
        self.nombre_completo = nombre_completo
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.fecha_inicio_contrato = fecha_inicio_contrato
        self.salario = salario
        self.activo = activo

        self.departamento = None
        self.usuario = None
        self.asignaciones = []

    def actualizar_datos(self, datos: dict):
        for atributo, valor in datos.items():
            if hasattr(self, atributo):
                setattr(self, atributo, valor)

    def asignar_departamento(self, departamento):
        departamento.agregar_empleado(self)

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False