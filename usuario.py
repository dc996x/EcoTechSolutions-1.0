from uuid import UUID

class Usuario:
    def __init__(
        self,
        id_usuario: UUID,
        nombre_usuario: str,
        password_hash: str,
        activo: bool = True
    ):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.password_hash = password_hash
        self.activo = activo

        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.ultimo_acceso = None

    def verificar_contrasena(self, clave: str) -> bool:
        return self.password_hash == clave

    def cambiar_contrasena(self, clave: str):
        self.password_hash = clave

    def tiene_permiso(self, codigo: str) -> bool:
        return self.activo