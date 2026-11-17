import tkinter as tk
from tkinter import messagebox
from backend.logica import GestorLavaya, HORARIOS_DISPONIBLES

class LavayaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LavaYa - Autolavado Express")
        self.root.geometry("420x720")
        self.root.resizable(False, False)

        # Conexión con el Backend
        self.backend = GestorLavaya()

        # Paleta de colores
        self.BG_MAIN = "#F5F7F5"
        self.COLOR_GREEN = "#9FE827"
        self.COLOR_DARK = "#0F172A"
        self.COLOR_TEXT_MUTED = "#64748B"
        self.COLOR_CARD_BG = "#FFFFFF"

        self.root.config(bg=self.BG_MAIN)

        # Estado temporal de la sesión
        self.usuario_actual = None
        self.placa_actual = ""
        self.vehiculo_sel = "Automóvil / Sedán"
        self.ajuste_vehiculo = 0
        self.lavado_sel = "Lavado Completo"
        self.precio_lavado = 25000
        self.turno_sel = "08:00 AM"
        self.duracion_sel = "1 hora"

        self.container = tk.Frame(self.root, bg=self.BG_MAIN)
        self.container.pack(fill="both", expand=True)

        self.mostrar_inicio()

    def limpiar_pantalla(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def crear_header(self, mostrar_logout=False):
        header = tk.Frame(self.container, bg=self.BG_MAIN, height=60)
        header.pack(fill="x", padx=20, pady=10)

        lbl_logo = tk.Label(header, text="💧", bg=self.COLOR_GREEN, fg="white", font=("Arial", 14, "bold"), width=2, height=1)
        lbl_logo.pack(side="left")

        lbl_titulo = tk.Label(header, text=" LavaYa\n AUTOLAVADO EXPRESS", bg=self.BG_MAIN, fg=self.COLOR_DARK, font=("Arial", 9, "bold"), justify="left")
        lbl_titulo.pack(side="left", padx=5)

        if mostrar_logout:
            btn_out = tk.Button(header, text="🚪", bg="#E2E8F0", fg=self.COLOR_DARK, bd=0, font=("Arial", 10), command=self.mostrar_inicio)
            btn_out.pack(side="right")

    # 1. INICIO
    def mostrar_inicio(self):
        self.limpiar_pantalla()
        self.crear_header()

        frame_body = tk.Frame(self.container, bg=self.BG_MAIN)
        frame_body.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(frame_body, text="AUTOSERVICIO DIGITAL", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w", pady=(5,0))
        tk.Label(frame_body, text="¿Qué deseas hacer?", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 18, "bold")).pack(anchor="w")
        tk.Label(frame_body, text="Comienza tu lavado en menos de un minuto.", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 9)).pack(anchor="w", pady=(0, 15))

        card_reg = tk.Frame(frame_body, bg="#EFFECA", bd=1, relief="solid")
        card_reg.pack(fill="x", pady=5, ipady=8)
        tk.Button(card_reg, text="👤  Registrar nuevo cliente                    >", bg="#EFFECA", fg=self.COLOR_DARK, bd=0, font=("Arial", 10, "bold"), command=self.mostrar_registro).pack(fill="both", padx=10)

        card_login = tk.Frame(frame_body, bg=self.COLOR_CARD_BG, bd=1, relief="solid")
        card_login.pack(fill="x", pady=5, ipady=8)
        tk.Button(card_login, text="🔑  Iniciar sesión                                      >", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, bd=0, font=("Arial", 10, "bold"), command=self.mostrar_login).pack(fill="both", padx=10)

        card_admin = tk.Frame(frame_body, bg="#E2E8F0", bd=1, relief="solid")
        card_admin.pack(fill="x", pady=5, ipady=8)
        tk.Button(card_admin, text="⚙️  Modo Administrador                           >", bg="#E2E8F0", fg=self.COLOR_DARK, bd=0, font=("Arial", 10, "bold"), command=self.mostrar_login_admin).pack(fill="both", padx=10)

        frame_status = tk.Frame(frame_body, bg=self.COLOR_CARD_BG, bd=1, relief="solid")
        frame_status.pack(fill="x", side="bottom", pady=15, ipady=5)
        tk.Label(frame_status, text=" Servicio disponible 24 horas\n    Abierto todos los días", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 8), justify="left").pack(side="left", padx=10)
        tk.Label(frame_status, text="Abierto", bg="#DCFCE7", fg="#15803D", font=("Arial", 8, "bold"), padx=8, pady=2).pack(side="right", padx=10)

    # 2. LOGIN ADMIN
    def mostrar_login_admin(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Volver", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_inicio).pack(anchor="w")

        tk.Label(frame, text="ACCESO RESTRINGIDO", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w", pady=(10,0))
        tk.Label(frame, text="Panel de Admin", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 18, "bold")).pack(anchor="w")

        tk.Label(frame, text="Contraseña de administrador:", bg=self.BG_MAIN, fg=self.COLOR_DARK, font=("Arial", 9, "bold")).pack(anchor="w", pady=(15, 2))
        ent_admin_pass = tk.Entry(frame, show="*", font=("Arial", 10), bd=1, relief="solid")
        ent_admin_pass.pack(fill="x", ipady=4)

        def validar():
            if self.backend.validar_admin(ent_admin_pass.get()):
                self.mostrar_panel_admin()
            else:
                messagebox.showerror("Error", "Contraseña de administrador incorrecta.")

        btn_acceder = tk.Button(frame, text="Ingresar al Panel ➔", bg=self.COLOR_GREEN, fg=self.COLOR_DARK, font=("Arial", 10, "bold"), bd=0, command=validar)
        btn_acceder.pack(fill="x", pady=20, ipady=6)

    # 3. PANEL DE ADMINISTRADOR
    def mostrar_panel_admin(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Label(frame, text="MODO ADMINISTRADOR", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(frame, text="Pedidos y Ventas Registradas", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 15, "bold")).pack(anchor="w", pady=(0, 5))

        frame_lista = tk.Frame(frame, bg=self.BG_MAIN)
        frame_lista.pack(fill="both", expand=True, pady=5)

        scroll_x = tk.Scrollbar(frame_lista, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        lista_pedidos = tk.Listbox(
            frame_lista,
            font=("Arial", 10, "bold"),
            fg=self.COLOR_DARK,
            bg=self.COLOR_CARD_BG,
            selectbackground="#D9F99D",
            selectforeground=self.COLOR_DARK,
            bd=1,
            relief="solid",
            height=12,
            xscrollcommand=scroll_x.set
        )
        lista_pedidos.pack(fill="both", expand=True)
        scroll_x.config(command=lista_pedidos.xview)

        lbl_total_ventas = tk.Label(frame, text="Total recaudado: $0", bg=self.BG_MAIN, fg=self.COLOR_DARK, font=("Arial", 10, "bold"))
        lbl_total_ventas.pack(anchor="e", pady=5)

        def cargar_registros():
            lista_pedidos.delete(0, tk.END)
            pedidos, total_dinero = self.backend.obtener_pedidos_y_total()
            if not pedidos:
                lista_pedidos.insert(tk.END, "  No hay ventas registradas aún.")
            else:
                for i, p in enumerate(pedidos, start=1):
                    lista_pedidos.insert(tk.END, f" #{i}  |  {p}")
            lbl_total_ventas.config(text=f"Total recaudado: ${total_dinero:,}")

        def eliminar_seleccionado():
            sel = lista_pedidos.curselection()
            if not sel:
                messagebox.showwarning("Atención", "Selecciona un pedido de la lista para eliminar.")
                return
            if self.backend.eliminar_pedido(sel[0]):
                cargar_registros()
                messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")

        cargar_registros()

        btn_eliminar = tk.Button(frame, text="🗑️ Eliminar pedido seleccionado", bg="#FCA5A5", fg="#991B1B", font=("Arial", 9, "bold"), bd=0, command=eliminar_seleccionado)
        btn_eliminar.pack(fill="x", pady=4, ipady=5)

        btn_salir = tk.Button(frame, text="Cerrar Sesión Admin", bg="#E2E8F0", fg=self.COLOR_DARK, font=("Arial", 9), bd=0, command=self.mostrar_inicio)
        btn_salir.pack(fill="x", pady=4, ipady=5)

    # 4. REGISTRO USUARIOS
    def mostrar_registro(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Volver", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_inicio).pack(anchor="w")
        tk.Label(frame, text="NUEVO CLIENTE", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w", pady=(5, 0))
        tk.Label(frame, text="Crea tu cuenta", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 18, "bold")).pack(anchor="w")

        fields = [
            ("Nombre completo", "Ej. Juan jaramillo"),
            ("Nombre de usuario", "Elige un usuario"),
            ("Correo (@gmail.com)", "Ej. juan@gmail.com"),
            ("Contraseña", "Mínimo 6 caracteres"),
            ("Placa del vehículo", "Ej. KLM 482")
        ]

        self.entries = {}
        for label, ph in fields:
            tk.Label(frame, text=label, bg=self.BG_MAIN, fg=self.COLOR_DARK, font=("Arial", 8, "bold")).pack(anchor="w", pady=(3, 1))
            if label == "Contraseña":
                ent = tk.Entry(frame, show="*", font=("Arial", 10), bd=1, relief="solid")
            else:
                ent = tk.Entry(frame, font=("Arial", 10), bd=1, relief="solid")
            ent.pack(fill="x", ipady=2)
            self.entries[label] = ent

        btn_crear = tk.Button(frame, text="Crear cuenta ➔", bg=self.COLOR_GREEN, fg=self.COLOR_DARK, font=("Arial", 10, "bold"), bd=0, command=self.guardar_registro)
        btn_crear.pack(fill="x", pady=12, ipady=6)

    def guardar_registro(self):
        nombre = self.entries["Nombre completo"].get().strip()
        user = self.entries["Nombre de usuario"].get().strip()
        correo = self.entries["Correo (@gmail.com)"].get().strip().lower()
        password = self.entries["Contraseña"].get().strip()
        placa = self.entries["Placa del vehículo"].get().strip().upper()

        if not all([nombre, user, correo, password, placa]):
            messagebox.showwarning("Campos incompletos", "Por favor completa todos los campos.")
            return

        if not correo.endswith("@gmail.com") or len(correo) <= 10:
            messagebox.showerror("Correo inválido", "El correo debe ser válido y terminar en @gmail.com")
            return

        exito, mensaje = self.backend.registrar_usuario(nombre, user, correo, password, placa)
        if not exito:
            messagebox.showerror("Registro duplicado", mensaje)
            return

        messagebox.showinfo("¡Cuenta creada!", f"Bienvenido {nombre}. Ahora puedes iniciar sesión.")
        self.mostrar_login()

    # 5. LOGIN USUARIOS
    def mostrar_login(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Volver", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_inicio).pack(anchor="w")
        tk.Label(frame, text="BIENVENIDO DE NUEVO", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w", pady=(10,0))
        tk.Label(frame, text="Inicia sesión", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 18, "bold")).pack(anchor="w")

        tk.Label(frame, text="Nombre de usuario", bg=self.BG_MAIN, fg=self.COLOR_DARK, font=("Arial", 8, "bold")).pack(anchor="w", pady=(10, 2))
        ent_user = tk.Entry(frame, font=("Arial", 10), bd=1, relief="solid")
        ent_user.pack(fill="x", ipady=4)

        tk.Label(frame, text="Contraseña", bg=self.BG_MAIN, fg=self.COLOR_DARK, font=("Arial", 8, "bold")).pack(anchor="w", pady=(10, 2))
        ent_pass = tk.Entry(frame, show="*", font=("Arial", 10), bd=1, relief="solid")
        ent_pass.pack(fill="x", ipady=4)

        def intentar_login():
            u = ent_user.get().strip()
            p = ent_pass.get().strip()

            if not u or not p:
                messagebox.showwarning("Campos vacíos", "Ingresa tu usuario y contraseña.")
                return

            nombre, placa = self.backend.validar_usuario(u, p)
            if nombre is None:
                messagebox.showerror("Error de acceso", "Usuario no registrado o contraseña incorrecta.")
                return

            self.usuario_actual = nombre
            self.placa_actual = placa
            self.mostrar_paso1()

        btn_ingresar = tk.Button(frame, text="Ingresar al autoservicio ➔", bg=self.COLOR_GREEN, fg=self.COLOR_DARK, font=("Arial", 10, "bold"), bd=0, command=intentar_login)
        btn_ingresar.pack(fill="x", pady=20, ipady=6)

    # 6. SELECCIÓN DE VEHÍCULO
    def mostrar_paso1(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Cerrar sesión", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_inicio).pack(anchor="w")
        tk.Label(frame, text="PASO 1 DE 4", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(frame, text="Selecciona tu\nvehículo", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 16, "bold"), justify="left").pack(anchor="w", pady=5)

        vehiculos = [
            ("🚗", "Automóvil / Sedán", "Vehículo estándar de 4 puertas"),
            ("🚙", "Camioneta / SUV", "Mayor tamaño y superficie"),
            ("🏍️", "Motocicleta", "Lavado rápido especializado")
        ]

        def elegir(nom):
            self.vehiculo_sel = nom
            self.ajuste_vehiculo = 0
            self.mostrar_paso2()

        for icono, nombre, desc in vehiculos:
            card = tk.Frame(frame, bg=self.COLOR_CARD_BG, bd=1, relief="solid")
            card.pack(fill="x", pady=5, ipady=8)
            
            lbl_info = tk.Label(card, text=f"{icono} {nombre}\n     {desc}", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 9, "bold"), justify="left")
            lbl_info.pack(side="left", padx=8)

            btn_sel = tk.Button(card, text="Seleccionar ➔", bg="#F1F5F9", fg=self.COLOR_DARK, font=("Arial", 8, "bold"), bd=0, command=lambda n=nombre: elegir(n))
            btn_sel.pack(side="right", padx=10)

    # 7. SELECCIÓN DE LAVADO
    def mostrar_paso2(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Volver", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_paso1).pack(anchor="w")
        tk.Label(frame, text="PASO 2 DE 4", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(frame, text="Elige tu tipo de\nlavado", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 16, "bold"), justify="left").pack(anchor="w", pady=5)

        servicios = [
            ("Lavado Sencillo", "Exterior y secado · 30 min", 15000, "30 minutos"),
            ("Lavado Completo", "Exterior + aspirado interior · 1 hora", 25000, "1 hora"),
            ("Lavado Premium", "Limpieza total + encerado · 2 horas", 45000, "2 horas")
        ]

        def elegir(nom, prec, dur):
            self.lavado_sel = nom
            self.precio_lavado = prec
            self.duracion_sel = dur
            self.mostrar_paso_turno()

        for nombre, desc, precio, duracion in servicios:
            bg_col = "#EFFECA" if nombre == "Lavado Completo" else self.COLOR_CARD_BG
            card = tk.Frame(frame, bg=bg_col, bd=1, relief="solid")
            card.pack(fill="x", pady=5, ipady=8)

            lbl_txt = tk.Label(card, text=f"💧 {nombre}\n   {desc}", bg=bg_col, fg=self.COLOR_DARK, font=("Arial", 9, "bold"), justify="left")
            lbl_txt.pack(side="left", padx=8)

            btn_p = tk.Button(card, text=f"${precio:,}", bg=self.COLOR_DARK, fg="white", font=("Arial", 8, "bold"), bd=0, command=lambda n=nombre, p=precio, d=duracion: elegir(n, p, d))
            btn_p.pack(side="right", padx=10)

    # 8. SELECCIÓN DE TURNO 
    def mostrar_paso_turno(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Volver", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_paso2).pack(anchor="w")
        tk.Label(frame, text="PASO 3 DE 4 · SERVICIO 24H", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(frame, text="Reserva tu turno\nsin hacer fila", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 16, "bold"), justify="left").pack(anchor="w", pady=(2, 10))

        grid_frame = tk.Frame(frame, bg=self.BG_MAIN)
        grid_frame.pack(fill="both", expand=True)

        turnos_ocupados = self.backend.obtener_turnos_ocupados()

        def elegir_turno(hora):
            self.turno_sel = hora
            self.mostrar_paso3()

        fila = 0
        columna = 0
        for hora in HORARIOS_DISPONIBLES:
            if hora in turnos_ocupados:
                btn = tk.Button(
                    grid_frame,
                    text=f"❌ {hora}\nOcupado",
                    bg="#E2E8F0",
                    fg="#94A3B8",
                    font=("Arial", 8, "bold"),
                    bd=1,
                    relief="solid",
                    width=14,
                    pady=4,
                    state="disabled"
                )
            else:
                btn = tk.Button(
                    grid_frame,
                    text=f"🕒 {hora}",
                    bg=self.COLOR_CARD_BG,
                    fg=self.COLOR_DARK,
                    font=("Arial", 9, "bold"),
                    bd=1,
                    relief="solid",
                    width=14,
                    pady=8,
                    command=lambda h=hora: elegir_turno(h)
                )
            btn.grid(row=fila, column=columna, padx=6, pady=6)
            columna += 1
            if columna == 2:
                columna = 0
                fila += 1

    # 9. CONFIRMACIÓN Y GUARDADO EN DATOS.TXT
    def mostrar_paso3(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Button(frame, text="< Volver", bg=self.BG_MAIN, bd=0, fg=self.COLOR_TEXT_MUTED, command=self.mostrar_paso_turno).pack(anchor="w")
        tk.Label(frame, text="ÚLTIMO PASO", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack(anchor="w")
        tk.Label(frame, text="Confirma tu pedido", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 16, "bold")).pack(anchor="w")

        card = tk.Frame(frame, bg=self.COLOR_CARD_BG, bd=1, relief="solid")
        card.pack(fill="x", pady=10, padx=5, ipady=8)

        tk.Label(card, text="✔  Resumen del servicio", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=2)
        tk.Label(card, text=f"Cliente: {self.usuario_actual}   |   Placa: {self.placa_actual}", bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED, font=("Arial", 8)).pack(anchor="w", padx=10)
        tk.Label(card, text=f"Vehículo: {self.vehiculo_sel}", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 8)).pack(anchor="w", padx=10, pady=2)
        tk.Label(card, text=f"Servicio: {self.lavado_sel}", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 8)).pack(anchor="w", padx=10)
        tk.Label(card, text=f"Duración estimada: {self.duracion_sel}", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 8)).pack(anchor="w", padx=10)
        tk.Label(card, text=f"Turno reservado: {self.turno_sel}", bg=self.COLOR_CARD_BG, fg="#15803D", font=("Arial", 8, "bold")).pack(anchor="w", padx=10, pady=2)

        total = self.backend.calcular_total(self.precio_lavado, self.ajuste_vehiculo)

        tk.Label(card, text=f"Precio base: ${self.precio_lavado:,}", bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED, font=("Arial", 8)).pack(anchor="e", padx=10, pady=(5,0))
        
        tk.Label(card, text=f"TOTAL A PAGAR: ${total:,}", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 11, "bold")).pack(anchor="e", padx=10, pady=5)

        def procesar_pedido():
            try:
                self.backend.guardar_pedido(
                    self.usuario_actual,
                    self.placa_actual,
                    self.vehiculo_sel,
                    self.lavado_sel,
                    self.turno_sel,
                    total
                )
                self.mostrar_exito()
            except Exception as e:
                messagebox.showerror("Error al guardar", f"No se pudo guardar el pedido:\n{e}")

        btn_confirmar = tk.Button(frame, text="Confirmar turno y reservar bahía ➔", bg=self.COLOR_GREEN, fg=self.COLOR_DARK, font=("Arial", 9, "bold"), bd=0, command=procesar_pedido)
        btn_confirmar.pack(fill="x", pady=10, ipady=6)

        btn_cancelar = tk.Button(frame, text="Cancelar", bg="#E2E8F0", fg=self.COLOR_DARK, font=("Arial", 9), bd=0, command=self.mostrar_inicio)
        btn_cancelar.pack(fill="x", ipady=4)

    # 10. PANTALLA ÉXITO
    def mostrar_exito(self):
        self.limpiar_pantalla()
        self.crear_header(True)

        frame = tk.Frame(self.container, bg=self.BG_MAIN)
        frame.pack(fill="both", expand=True, padx=20)

        tk.Label(frame, text="🟢", font=("Arial", 36), bg=self.BG_MAIN).pack(pady=(20, 5))
        tk.Label(frame, text="TURNO RESERVADO", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8, "bold")).pack()
        tk.Label(frame, text=f"¡Todo listo, {self.usuario_actual}!", fg=self.COLOR_DARK, bg=self.BG_MAIN, font=("Arial", 16, "bold")).pack(pady=5)
        tk.Label(frame, text="Llega puntual a tu hora reservada.\nTu bahía estará libre sin esperas.", fg=self.COLOR_TEXT_MUTED, bg=self.BG_MAIN, font=("Arial", 8), justify="center").pack()

        card = tk.Frame(frame, bg=self.COLOR_CARD_BG, bd=1, relief="solid")
        card.pack(fill="x", pady=20, ipady=15)
        tk.Label(card, text="BAHÍA ASIGNADA · TURNO", bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED, font=("Arial", 8, "bold")).pack()
        tk.Label(card, text=f"Bahía 03 · {self.turno_sel}", bg=self.COLOR_CARD_BG, fg=self.COLOR_DARK, font=("Arial", 16, "bold")).pack()
        tk.Label(card, text=f"Tiempo estimado: {self.duracion_sel}", bg=self.COLOR_CARD_BG, fg=self.COLOR_TEXT_MUTED, font=("Arial", 8)).pack()

        btn_inicio = tk.Button(frame, text="Volver al inicio ➔", bg=self.COLOR_GREEN, fg=self.COLOR_DARK, font=("Arial", 10, "bold"), bd=0, command=self.mostrar_inicio)
        btn_inicio.pack(fill="x", pady=10, ipady=6)