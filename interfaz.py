import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from decimal import Decimal, InvalidOperation
from uuid import uuid4

from departamento import Departamento
from empleado import Empleado
from usuario import Usuario
from proyecto import Proyecto
from asignacion_proyecto import Asignacion_Proyecto
from registro_tiempo import Registro_Tiempo

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión EcoTechSolutions")
        self.geometry("820x580")
        self.minsize(820, 580)
        self.color_fondo = "#DCDAD5"
        self.configure(background=self.color_fondo)

        self.departamentos = []
        self.empleados = []
        self.usuarios = []
        self.proyectos = []
        self.asignaciones = []
        self.registros = []

        self._crear_estilos()
        self._crear_interfaz()
        self._actualizar_listas()
        self._mostrar_resumen()

    def _crear_estilos(self):
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TFrame", background=self.color_fondo)
        estilo.configure("TLabel", background=self.color_fondo)
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 17, "bold"),
                         background=self.color_fondo)
        estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 10),
                         background=self.color_fondo)
        estilo.configure("Accion.TButton", padding=6)
        estilo.configure("TNotebook", background=self.color_fondo, borderwidth=0)
        estilo.configure("TNotebook.Tab", padding=(10, 5))
        estilo.map(
            "TNotebook.Tab",
            padding=[("selected", (10, 5)), ("!selected", (10, 5))]
        )
        estilo.configure("Treeview", rowheight=25)

    def _crear_interfaz(self):
        cabecera = ttk.Frame(self, padding=(16, 10))
        cabecera.pack(fill="x")

        ttk.Label(
            cabecera, text="Sistema de Gestión", style="Titulo.TLabel"
        ).pack(side="left", anchor="w")

        try:
            from pathlib import Path
            self.logo = tk.PhotoImage(file=str(Path(__file__).resolve().parent / "logo.png"))
            factor = max(1, (self.logo.width() + 179) // 180)
            if factor > 1:
                self.logo = self.logo.subsample(factor, factor)
            ttk.Label(cabecera, image=self.logo).pack(
                side="right", anchor="e", padx=(12, 0)
            )
        except tk.TclError:
            pass

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        self.tab_inicio = ttk.Frame(self.tabs, padding=12)
        self.tab_departamentos = ttk.Frame(self.tabs, padding=12)
        self.tab_empleados = ttk.Frame(self.tabs, padding=12)
        self.tab_usuarios = ttk.Frame(self.tabs, padding=12)
        self.tab_proyectos = ttk.Frame(self.tabs, padding=12)
        self.tab_asignaciones = ttk.Frame(self.tabs, padding=12)
        self.tab_registros = ttk.Frame(self.tabs, padding=12)

        for tab, nombre in [
            (self.tab_inicio, "Resumen"),
            (self.tab_departamentos, "Departamentos"),
            (self.tab_empleados, "Empleados"),
            (self.tab_usuarios, "Usuarios"),
            (self.tab_proyectos, "Proyectos"),
            (self.tab_asignaciones, "Asignaciones"),
            (self.tab_registros, "Registro de tiempo"),
        ]:
            self.tabs.add(tab, text=nombre)

        self._crear_tab_inicio()
        self._crear_tab_departamentos()
        self._crear_tab_empleados()
        self._crear_tab_usuarios()
        self._crear_tab_proyectos()
        self._crear_tab_asignaciones()
        self._crear_tab_registros()

        pie = ttk.Frame(self, padding=(12, 4))
        pie.pack(fill="x")
        ttk.Label(pie, text="Modo sin base de datos: los datos se mantienen solo mientras la aplicación está abierta.").pack(anchor="w")

    def _crear_tab_inicio(self):
        ttk.Label(self.tab_inicio, text="Resumen del sistema", style="Titulo.TLabel").pack(anchor="w", pady=(0, 12))
        self.resumen_var = tk.StringVar()
        ttk.Label(self.tab_inicio, textvariable=self.resumen_var, justify="left", font=("Segoe UI", 11)).pack(anchor="w")
        ttk.Button(self.tab_inicio, text="Actualizar resumen", command=self._mostrar_resumen).pack(anchor="w", pady=12)
        ttk.Label(
            self.tab_inicio,
            text="Puedes crear y modificar datos desde las pestañas. Las fechas deben usar AAAA-MM-DD.",
            wraplength=780
        ).pack(anchor="w", pady=(8, 0))

    def _crear_tab_departamentos(self):
        form = ttk.LabelFrame(self.tab_departamentos, text="Crear departamento", padding=10)
        form.pack(fill="x")
        self.dep_nombre = tk.StringVar(value="")
        self.dep_activo = tk.BooleanVar(value=False)
        self._campo(form, "Nombre", self.dep_nombre, 0, 0)
        ttk.Checkbutton(form, text="Activo", variable=self.dep_activo).grid(row=0, column=2, padx=10, sticky="w")
        ttk.Button(form, text="Crear departamento", command=self._crear_departamento).grid(row=0, column=3, padx=8)
        self.dep_tree = self._crear_tabla(
            self.tab_departamentos,
            ("nombre", "activo", "empleados", "gerente"),
            ("Nombre", "Activo", "N.º empleados", "Gerente")
        )
        acciones = ttk.Frame(self.tab_departamentos)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Asignar gerente al empleado seleccionado", command=self._asignar_gerente).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Agregar empleado seleccionado", command=self._agregar_empleado_dep).pack(side="left", padx=6)
        ttk.Button(acciones, text="Quitar empleado seleccionado", command=self._quitar_empleado_dep).pack(side="left", padx=6)

    def _crear_tab_empleados(self):
        form = ttk.LabelFrame(self.tab_empleados, text="Crear empleado", padding=10)
        form.pack(fill="x")
        self.emp_nombre = tk.StringVar(value="")
        self.emp_direccion = tk.StringVar(value="")
        self.emp_telefono = tk.StringVar(value="")
        self.emp_correo = tk.StringVar(value="")
        self.emp_fecha = tk.StringVar(value="")
        self.emp_salario = tk.StringVar(value="")
        self.emp_activo = tk.BooleanVar(value=False)
        self._campo(form, "Nombre completo", self.emp_nombre, 0, 0)
        self._campo(form, "Dirección", self.emp_direccion, 0, 2)
        self._campo(form, "Teléfono", self.emp_telefono, 1, 0)
        self._campo(form, "Correo", self.emp_correo, 1, 2)
        self._campo(form, "Fecha inicio (AAAA-MM-DD)", self.emp_fecha, 2, 0)
        self._campo(form, "Salario", self.emp_salario, 2, 2)
        ttk.Checkbutton(form, text="Activo", variable=self.emp_activo).grid(row=3, column=0, sticky="w", pady=5)
        ttk.Button(form, text="Crear empleado", command=self._crear_empleado).grid(row=3, column=2, sticky="w", pady=5)
        self.emp_tree = self._crear_tabla(
            self.tab_empleados,
            ("nombre", "telefono", "correo", "fecha", "salario", "activo", "departamento"),
            ("Nombre", "Teléfono", "Correo", "Inicio contrato", "Salario", "Activo", "Departamento")
        )
        acciones = ttk.Frame(self.tab_empleados)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Actualizar teléfono y salario", command=self._actualizar_empleado).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Activar / desactivar", command=self._alternar_empleado).pack(side="left", padx=6)
        ttk.Button(acciones, text="Asignar departamento", command=self._asignar_departamento_empleado).pack(side="left", padx=6)
        ttk.Button(acciones, text="Crear usuario para empleado", command=self._crear_usuario_empleado).pack(side="left", padx=6)

    def _crear_tab_usuarios(self):
        form = ttk.LabelFrame(self.tab_usuarios, text="Crear usuario", padding=10)
        form.pack(fill="x")
        self.usu_nombre = tk.StringVar(value="")
        self.usu_clave = tk.StringVar(value="")
        self.usu_activo = tk.BooleanVar(value=False)
        self._campo(form, "Nombre de usuario", self.usu_nombre, 0, 0)
        self._campo(form, "Contraseña (demo)", self.usu_clave, 0, 2)
        ttk.Checkbutton(form, text="Activo", variable=self.usu_activo).grid(row=1, column=0, sticky="w", pady=5)
        ttk.Button(form, text="Crear usuario independiente", command=self._crear_usuario).grid(row=1, column=2, sticky="w", pady=5)
        self.usu_tree = self._crear_tabla(self.tab_usuarios, ("nombre", "activo", "empleado"), ("Usuario", "Activo", "Empleado asociado"))
        acciones = ttk.Frame(self.tab_usuarios)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Verificar contraseña", command=self._verificar_usuario).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Cambiar contraseña", command=self._cambiar_clave).pack(side="left", padx=6)
        ttk.Button(acciones, text="Probar permiso ADMIN", command=self._probar_permiso).pack(side="left", padx=6)

    def _crear_tab_proyectos(self):
        form = ttk.LabelFrame(self.tab_proyectos, text="Crear proyecto", padding=10)
        form.pack(fill="x")
        self.proy_nombre = tk.StringVar(value="")
        self.proy_desc = tk.StringVar(value="")
        self.proy_fecha = tk.StringVar(value="")
        self.proy_estado = tk.StringVar(value="")
        self._campo(form, "Nombre", self.proy_nombre, 0, 0)
        self._campo(form, "Descripción", self.proy_desc, 0, 2)
        self._campo(form, "Fecha inicio (AAAA-MM-DD)", self.proy_fecha, 1, 0)
        ttk.Label(form, text="Estado").grid(row=1, column=2, sticky="w", padx=(8, 4), pady=4)
        ttk.Combobox(form, textvariable=self.proy_estado, values=("activo", "cerrado"), state="readonly", width=22).grid(row=1, column=3, sticky="w", padx=4, pady=4)
        ttk.Button(form, text="Crear proyecto", command=self._crear_proyecto).grid(row=2, column=0, sticky="w", pady=6)
        self.proy_tree = self._crear_tabla(self.tab_proyectos, ("nombre", "descripcion", "fecha", "estado", "asignaciones"), ("Nombre", "Descripción", "Fecha inicio", "Estado", "Asignaciones"))
        acciones = ttk.Frame(self.tab_proyectos)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Actualizar descripción", command=self._actualizar_proyecto).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Activar / cerrar", command=self._alternar_proyecto).pack(side="left", padx=6)

    def _crear_tab_asignaciones(self):
        form = ttk.LabelFrame(self.tab_asignaciones, text="Crear asignación", padding=10)
        form.pack(fill="x")
        self.asig_emp = ttk.Combobox(form, state="readonly", width=28)
        self.asig_proy = ttk.Combobox(form, state="readonly", width=28)
        self.asig_fecha = tk.StringVar(value="")
        ttk.Label(form, text="Empleado").grid(row=0, column=0, sticky="w", padx=4)
        self.asig_emp.grid(row=1, column=0, padx=4, pady=4, sticky="w")
        ttk.Label(form, text="Proyecto").grid(row=0, column=1, sticky="w", padx=4)
        self.asig_proy.grid(row=1, column=1, padx=4, pady=4, sticky="w")
        ttk.Label(form, text="Fecha asignación (AAAA-MM-DD)").grid(row=0, column=2, sticky="w", padx=4)
        ttk.Entry(form, textvariable=self.asig_fecha, width=22).grid(row=1, column=2, padx=4, pady=4, sticky="w")
        ttk.Button(form, text="Crear asignación", command=self._crear_asignacion).grid(row=1, column=3, padx=8)
        self.asig_tree = self._crear_tabla(self.tab_asignaciones, ("empleado", "proyecto", "fecha", "desasignacion", "activa", "registros"), ("Empleado", "Proyecto", "Asignación", "Desasignación", "Activa", "Registros"))
        acciones = ttk.Frame(self.tab_asignaciones)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Comprobar vigencia por fecha", command=self._comprobar_vigencia).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Cerrar asignación", command=self._cerrar_asignacion).pack(side="left", padx=6)

    def _crear_tab_registros(self):
        form = ttk.LabelFrame(self.tab_registros, text="Crear registro de tiempo", padding=10)
        form.pack(fill="x")
        self.reg_asig = ttk.Combobox(form, state="readonly", width=28)
        self.reg_fecha = tk.StringVar(value="")
        self.reg_horas = tk.StringVar(value="")
        self.reg_desc = tk.StringVar(value="")
        ttk.Label(form, text="Asignación").grid(row=0, column=0, sticky="w", padx=4)
        self.reg_asig.grid(row=1, column=0, padx=4, pady=4, sticky="w")
        self._campo(form, "Fecha (AAAA-MM-DD)", self.reg_fecha, 0, 1)
        self._campo(form, "Horas", self.reg_horas, 0, 3)
        self._campo(form, "Descripción", self.reg_desc, 2, 0)
        ttk.Button(form, text="Crear registro", command=self._crear_registro).grid(row=3, column=0, sticky="w", pady=6)
        self.reg_tree = self._crear_tabla(self.tab_registros, ("fecha", "horas", "descripcion", "asignacion", "valido", "creacion"), ("Fecha", "Horas", "Descripción", "Asignación", "Horas válidas", "Creación"))
        acciones = ttk.Frame(self.tab_registros)
        acciones.pack(fill="x", pady=8)
        ttk.Button(acciones, text="Actualizar descripción", command=self._actualizar_registro).pack(side="left", padx=(0, 6))
        ttk.Button(acciones, text="Validar horas", command=self._validar_registro).pack(side="left", padx=6)

    def _campo(self, padre, texto, variable, fila, columna):
        ttk.Label(padre, text=texto).grid(row=fila, column=columna, sticky="w", padx=4, pady=4)
        ttk.Entry(padre, textvariable=variable, width=25).grid(row=fila, column=columna + 1, sticky="w", padx=4, pady=4)

    def _crear_tabla(self, padre, columnas, titulos):
        contenedor = ttk.Frame(padre)
        contenedor.pack(fill="both", expand=True, pady=(12, 0))
        tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", selectmode="browse")
        scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=tabla.yview)
        scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        contenedor.rowconfigure(0, weight=1)
        contenedor.columnconfigure(0, weight=1)
        for col, titulo in zip(columnas, titulos):
            tabla.heading(col, text=titulo)
            tabla.column(col, width=145, minwidth=90, anchor="w")
        return tabla

    @staticmethod
    def _fecha(texto):
        return date.fromisoformat(texto.strip())

    def _seleccion(self, tabla, lista, mensaje):
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selección requerida", mensaje)
            return None
        try:
            return lista[int(seleccionado[0])]
        except (ValueError, IndexError):
            messagebox.showerror("Error", "No se pudo identificar el elemento seleccionado.")
            return None

    def _crear_departamento(self):
        nombre = self.dep_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Dato requerido", "Escribe el nombre del departamento.")
            return
        obj = Departamento(id_departamento=uuid4(), nombre=nombre, activo=self.dep_activo.get())
        self.departamentos.append(obj)
        self._actualizar_listas()
        messagebox.showinfo("Correcto", f"Departamento '{nombre}' creado.")

    def _crear_empleado(self):
        try:
            nombre = self.emp_nombre.get().strip()
            if not nombre:
                raise ValueError("El nombre es obligatorio.")
            salario = Decimal(self.emp_salario.get().strip())
            if salario < 0:
                raise ValueError("El salario no puede ser negativo.")
            obj = Empleado(
                id_empleado=uuid4(),
                nombre_completo=nombre,
                direccion=self.emp_direccion.get().strip(),
                telefono=self.emp_telefono.get().strip(),
                correo=self.emp_correo.get().strip(),
                fecha_inicio_contrato=self._fecha(self.emp_fecha.get()),
                salario=salario,
                activo=self.emp_activo.get()
            )
            self.empleados.append(obj)
            self._actualizar_listas()
            messagebox.showinfo("Correcto", f"Empleado '{nombre}' creado.")
        except (ValueError, InvalidOperation) as exc:
            messagebox.showerror("Datos inválidos", f"Revisa los datos del empleado.\n{exc}")

    def _actualizar_empleado(self):
        emp = self._seleccion(self.emp_tree, self.empleados, "Selecciona un empleado.")
        if emp is None:
            return
        dialogo = tk.Toplevel(self)
        dialogo.title("Actualizar empleado")
        dialogo.transient(self)
        dialogo.grab_set()
        telefono = tk.StringVar(value=emp.telefono)
        salario = tk.StringVar(value=str(emp.salario))
        self._campo(dialogo, "Teléfono", telefono, 0, 0)
        self._campo(dialogo, "Salario", salario, 1, 0)
        def guardar():
            try:
                valor_salario = Decimal(salario.get())
                if valor_salario < 0:
                    raise ValueError("El salario no puede ser negativo.")
                emp.actualizar_datos({"telefono": telefono.get().strip(), "salario": valor_salario})
                self._actualizar_listas()
                dialogo.destroy()
            except (ValueError, InvalidOperation) as exc:
                messagebox.showerror("Datos inválidos", str(exc), parent=dialogo)
        ttk.Button(dialogo, text="Guardar cambios", command=guardar).grid(row=2, column=1, padx=8, pady=8, sticky="w")

    def _alternar_empleado(self):
        emp = self._seleccion(self.emp_tree, self.empleados, "Selecciona un empleado.")
        if emp is None:
            return
        (emp.desactivar if emp.activo else emp.activar)()
        self._actualizar_listas()

    def _asignar_departamento_empleado(self):
        emp = self._seleccion(self.emp_tree, self.empleados, "Selecciona un empleado.")
        if emp is None:
            return
        if not self.departamentos:
            messagebox.showwarning("Sin departamentos", "Crea un departamento primero.")
            return
        nombres = [d.nombre for d in self.departamentos]
        elegido = self._elegir("Asignar departamento", "Selecciona el departamento:", nombres)
        if elegido is None:
            return
        departamento = self.departamentos[nombres.index(elegido)]
        emp.asignar_departamento(departamento)
        self._actualizar_listas()

    def _crear_usuario_empleado(self):
        emp = self._seleccion(self.emp_tree, self.empleados, "Selecciona un empleado.")
        if emp is None:
            return
        if emp.usuario is not None:
            messagebox.showwarning("Usuario existente", "Este empleado ya tiene un usuario asociado.")
            return
        nombre = tk.simpledialog.askstring("Crear usuario", "Nombre de usuario:", parent=self)
        if not nombre:
            return
        clave = tk.simpledialog.askstring("Crear usuario", "Contraseña de prueba:", show="*", parent=self)
        if not clave:
            return
        usuario = Usuario(id_usuario=uuid4(), nombre_usuario=nombre.strip(), password_hash=clave, activo=True)
        emp.usuario = usuario
        self.usuarios.append(usuario)
        self._actualizar_listas()

    def _crear_usuario(self):
        nombre, clave = self.usu_nombre.get().strip(), self.usu_clave.get()
        if not nombre or not clave:
            messagebox.showwarning("Datos requeridos", "Indica usuario y contraseña.")
            return
        usuario = Usuario(id_usuario=uuid4(), nombre_usuario=nombre, password_hash=clave, activo=self.usu_activo.get())
        self.usuarios.append(usuario)
        self._actualizar_listas()
        messagebox.showinfo("Correcto", f"Usuario '{nombre}' creado.")

    def _usuario_seleccionado(self):
        return self._seleccion(self.usu_tree, self.usuarios, "Selecciona un usuario.")

    def _verificar_usuario(self):
        usuario = self._usuario_seleccionado()
        if usuario is None:
            return
        clave = tk.simpledialog.askstring("Verificar contraseña", f"Contraseña para {usuario.nombre_usuario}:", show="*", parent=self)
        if clave is None:
            return
        correcto = usuario.verificar_contrasena(clave)
        messagebox.showinfo("Resultado", "Contraseña correcta." if correcto else "Contraseña incorrecta.")

    def _cambiar_clave(self):
        usuario = self._usuario_seleccionado()
        if usuario is None:
            return
        clave = tk.simpledialog.askstring("Cambiar contraseña", "Nueva contraseña:", show="*", parent=self)
        if not clave:
            return
        usuario.cambiar_contrasena(clave)
        messagebox.showinfo("Correcto", "Contraseña actualizada.")

    def _probar_permiso(self):
        usuario = self._usuario_seleccionado()
        if usuario is not None:
            messagebox.showinfo("Permisos", "Sí tiene permiso." if usuario.tiene_permiso("ADMIN") else "No tiene permiso.")

    def _crear_proyecto(self):
        nombre = self.proy_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Dato requerido", "El nombre del proyecto es obligatorio.")
            return
        try:
            obj = Proyecto(
                id_proyecto=uuid4(),
                nombre=nombre,
                descripcion=self.proy_desc.get().strip(),
                fecha_inicio=self._fecha(self.proy_fecha.get()),
                estado=self.proy_estado.get()
            )
            self.proyectos.append(obj)
            self._actualizar_listas()
            messagebox.showinfo("Correcto", f"Proyecto '{nombre}' creado.")
        except ValueError as exc:
            messagebox.showerror("Fecha inválida", str(exc))

    def _actualizar_proyecto(self):
        proyecto = self._seleccion(self.proy_tree, self.proyectos, "Selecciona un proyecto.")
        if proyecto is None:
            return
        descripcion = tk.simpledialog.askstring("Actualizar descripción", "Nueva descripción:", initialvalue=proyecto.descripcion, parent=self)
        if descripcion is not None:
            proyecto.actualizar_datos({"descripcion": descripcion.strip()})
            self._actualizar_listas()

    def _alternar_proyecto(self):
        proyecto = self._seleccion(self.proy_tree, self.proyectos, "Selecciona un proyecto.")
        if proyecto is None:
            return
        if proyecto.estado == "activo":
            proyecto.cerrar()
        else:
            proyecto.activar()
        self._actualizar_listas()

    def _crear_asignacion(self):
        if not self.empleados or not self.proyectos:
            messagebox.showwarning("Faltan datos", "Crea al menos un empleado y un proyecto.")
            return
        try:
            idx_emp = self.asig_emp.current()
            idx_proy = self.asig_proy.current()
            if idx_emp < 0 or idx_proy < 0:
                raise ValueError("Selecciona un empleado y un proyecto.")
            obj = Asignacion_Proyecto(
                id_asignacion=uuid4(),
                empleado=self.empleados[idx_emp],
                proyecto=self.proyectos[idx_proy],
                fecha_asignacion=self._fecha(self.asig_fecha.get())
            )
            self.asignaciones.append(obj)
            self._actualizar_listas()
            messagebox.showinfo("Correcto", "Asignación creada.")
        except ValueError as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def _comprobar_vigencia(self):
        asig = self._seleccion(self.asig_tree, self.asignaciones, "Selecciona una asignación.")
        if asig is None:
            return
        texto = tk.simpledialog.askstring("Comprobar vigencia", "Fecha a comprobar (AAAA-MM-DD):", initialvalue=date.today().isoformat(), parent=self)
        if not texto:
            return
        try:
            fecha = self._fecha(texto)
            vigente = asig.esta_vigente(fecha)
            messagebox.showinfo("Resultado", f"La asignación {'está' if vigente else 'no está'} vigente el {fecha}.")
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato AAAA-MM-DD.")

    def _cerrar_asignacion(self):
        asig = self._seleccion(self.asig_tree, self.asignaciones, "Selecciona una asignación.")
        if asig is None:
            return
        texto = tk.simpledialog.askstring("Cerrar asignación", "Fecha de desasignación (AAAA-MM-DD):", initialvalue=date.today().isoformat(), parent=self)
        if not texto:
            return
        try:
            asig.cerrar(self._fecha(texto))
            self._actualizar_listas()
        except ValueError:
            messagebox.showerror("Fecha inválida", "Usa el formato AAAA-MM-DD.")

    def _crear_registro(self):
        if not self.asignaciones:
            messagebox.showwarning("Sin asignaciones", "Crea una asignación primero.")
            return
        try:
            idx = self.reg_asig.current()
            if idx < 0:
                raise ValueError("Selecciona una asignación.")
            horas = Decimal(self.reg_horas.get().strip())
            if horas <= 0:
                raise ValueError("Las horas deben ser mayores que cero.")
            registro = Registro_Tiempo(
                id_registro=uuid4(),
                fecha=self._fecha(self.reg_fecha.get()),
                horas=horas,
                descripcion=self.reg_desc.get().strip(),
                asignacion=self.asignaciones[idx]
            )
            self.registros.append(registro)
            self._actualizar_listas()
            messagebox.showinfo("Correcto", "Registro de tiempo creado.")
        except (ValueError, InvalidOperation) as exc:
            messagebox.showerror("Datos inválidos", str(exc))

    def _actualizar_registro(self):
        registro = self._seleccion(self.reg_tree, self.registros, "Selecciona un registro.")
        if registro is None:
            return
        descripcion = tk.simpledialog.askstring("Actualizar descripción", "Nueva descripción:", initialvalue=registro.descripcion, parent=self)
        if descripcion is not None:
            registro.actualizar_descripcion(descripcion.strip())
            self._actualizar_listas()

    def _validar_registro(self):
        registro = self._seleccion(self.reg_tree, self.registros, "Selecciona un registro.")
        if registro is not None:
            messagebox.showinfo("Validación", "Las horas son válidas." if registro.validar_horas() else "Las horas no son válidas.")

    def _asignar_gerente(self):
        departamento = self._seleccion(self.dep_tree, self.departamentos, "Selecciona un departamento.")
        if departamento is None:
            return
        if not self.empleados:
            messagebox.showwarning("Sin empleados", "Crea un empleado primero.")
            return
        elegido = self._elegir("Asignar gerente", "Selecciona al gerente:", [e.nombre_completo for e in self.empleados])
        if elegido is not None:
            departamento.cambiar_gerente(self.empleados[[e.nombre_completo for e in self.empleados].index(elegido)])
            self._actualizar_listas()

    def _agregar_empleado_dep(self):
        departamento = self._seleccion(self.dep_tree, self.departamentos, "Selecciona un departamento.")
        if departamento is None:
            return
        if not self.empleados:
            messagebox.showwarning("Sin empleados", "Crea un empleado primero.")
            return
        elegido = self._elegir("Agregar empleado", "Selecciona al empleado:", [e.nombre_completo for e in self.empleados])
        if elegido is not None:
            departamento.agregar_empleado(self.empleados[[e.nombre_completo for e in self.empleados].index(elegido)])
            self._actualizar_listas()

    def _quitar_empleado_dep(self):
        departamento = self._seleccion(self.dep_tree, self.departamentos, "Selecciona un departamento.")
        if departamento is None:
            return
        if not departamento.empleados:
            messagebox.showinfo("Sin empleados", "Este departamento no tiene empleados.")
            return
        elegido = self._elegir("Quitar empleado", "Selecciona al empleado:", [e.nombre_completo for e in departamento.empleados])
        if elegido is not None:
            departamento.quitar_empleado(departamento.empleados[[e.nombre_completo for e in departamento.empleados].index(elegido)])
            self._actualizar_listas()

    def _elegir(self, titulo, texto, opciones):
        dialogo = tk.Toplevel(self)
        dialogo.title(titulo)
        dialogo.transient(self)
        dialogo.grab_set()
        ttk.Label(dialogo, text=texto).pack(padx=12, pady=(12, 5), anchor="w")
        variable = tk.StringVar()
        combo = ttk.Combobox(dialogo, textvariable=variable, values=opciones, state="readonly", width=38)
        combo.pack(padx=12, pady=5)
        if opciones:
            combo.current(0)
        resultado = {"valor": None}
        def aceptar():
            resultado["valor"] = variable.get() or None
            dialogo.destroy()
        ttk.Button(dialogo, text="Aceptar", command=aceptar).pack(pady=(5, 12))
        self.wait_window(dialogo)
        return resultado["valor"]

    def _actualizar_listas(self):
        self._llenar(self.dep_tree, self.departamentos, lambda d: (
            d.nombre, "Sí" if d.activo else "No", len(d.empleados),
            d.gerente.nombre_completo if d.gerente else "Sin gerente"
        ))
        self._llenar(self.emp_tree, self.empleados, lambda e: (
            e.nombre_completo, e.telefono, e.correo, e.fecha_inicio_contrato,
            e.salario, "Sí" if e.activo else "No",
            e.departamento.nombre if e.departamento else "Sin departamento"
        ))
        def nombre_empleado(usuario):
            return next((e.nombre_completo for e in self.empleados if e.usuario is usuario), "Sin empleado")
        self._llenar(self.usu_tree, self.usuarios, lambda u: (
            u.nombre_usuario, "Sí" if u.activo else "No", nombre_empleado(u)
        ))
        self._llenar(self.proy_tree, self.proyectos, lambda p: (
            p.nombre, p.descripcion, p.fecha_inicio, p.estado, len(p.asignaciones)
        ))
        self._llenar(self.asig_tree, self.asignaciones, lambda a: (
            a.empleado.nombre_completo, a.proyecto.nombre, a.fecha_asignacion,
            a.fecha_desasignacion or "—", "Sí" if a.activa else "No", len(a.registros_tiempo)
        ))
        self._llenar(self.reg_tree, self.registros, lambda r: (
            r.fecha, r.horas, r.descripcion,
            f"{r.asignacion.empleado.nombre_completo} - {r.asignacion.proyecto.nombre}",
            "Sí" if r.validar_horas() else "No", r.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        ))
        self.asig_emp["values"] = [e.nombre_completo for e in self.empleados]
        self.asig_proy["values"] = [p.nombre for p in self.proyectos]
        self.reg_asig["values"] = [
            f"{a.empleado.nombre_completo} - {a.proyecto.nombre} ({a.fecha_asignacion})"
            for a in self.asignaciones
        ]
        if self.empleados and self.asig_emp.current() < 0:
            self.asig_emp.current(0)
        if self.proyectos and self.asig_proy.current() < 0:
            self.asig_proy.current(0)
        if self.asignaciones and self.reg_asig.current() < 0:
            self.reg_asig.current(0)
        self._mostrar_resumen()

    @staticmethod
    def _llenar(tabla, objetos, convertir):
        tabla.delete(*tabla.get_children())
        for i, objeto in enumerate(objetos):
            tabla.insert("", "end", iid=str(i), values=convertir(objeto))

    def _mostrar_resumen(self):
        if not hasattr(self, "resumen_var"):
            return
        self.resumen_var.set(
            f"Departamentos: {len(self.departamentos)}\n"
            f"Empleados: {len(self.empleados)}\n"
            f"Usuarios: {len(self.usuarios)}\n"
            f"Proyectos: {len(self.proyectos)}\n"
            f"Asignaciones: {len(self.asignaciones)}\n"
            f"Registros de tiempo: {len(self.registros)}"
        )

    def _cargar_datos_demo(self):
        pass

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
