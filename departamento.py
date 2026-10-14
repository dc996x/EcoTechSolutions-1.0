from uuid import UUID

class Departamento:
    def __init__(
        self,
        id_departamento: UUID,
        nombre: str,
        activo: bool = True
    ):
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.activo = activo

        self.empleados = []
        self.gerente = None

    def cambiar_gerente(self, empleado):
        self.gerente = empleado

    def agregar_empleado(self, empleado):
        if empleado not in self.empleados:
            self.empleados.append(empleado)
            empleado.departamento = self

    def quitar_empleado(self, empleado):
        if empleado in self.empleados:
            self.empleados.remove(empleado)
            empleado.departamento = None