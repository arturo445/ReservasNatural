import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Conexion import obtener_conexion

# =====================================================================
# FUNCIONES GENERALES Y CARGA DE DATOS
# =====================================================================

def cargar_parques(lista_widget):
    """Carga los parques en el Listbox o Combobox provisto."""
    lista_widget.delete(0, tk.END) if isinstance(lista_widget, tk.Listbox) else lista_widget.set('')
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Parque_ID, Nombre
            FROM Parques
            ORDER BY Parque_ID
        """)
        parques = cursor.fetchall()
        conexion.close()
        
        if isinstance(lista_widget, tk.Listbox):
            for p in parques:
                lista_widget.insert(tk.END, f"{p[0]} - {p[1]}")
        elif isinstance(lista_widget, ttk.Combobox):
            lista_widget['values'] = [f"{p[0]} - {p[1]}" for p in parques]
    except Exception as e:
        print("Error al cargar parques:", e)

def cargar_visitantes(lista_widget):
    """Carga los visitantes en el Listbox o Combobox provisto."""
    lista_widget.delete(0, tk.END) if isinstance(lista_widget, tk.Listbox) else lista_widget.set('')
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT DNI, Nombre FROM Visitantes")
        visitantes = cursor.fetchall()
        conexion.close()
        
        if isinstance(lista_widget, tk.Listbox):
            for v in visitantes:
                lista_widget.insert(tk.END, f"{v[0]} - {v[1]}")
        elif isinstance(lista_widget, ttk.Combobox):
            lista_widget['values'] = [f"{v[0]} - {v[1]}" for v in visitantes]
    except Exception as e:
        print("Error al cargar visitantes:", e)

def cargar_empleados_gestion(combo):
    combo.set('')
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = """
            SELECT PP.DNI, PP.Nombre
            FROM PersonalParque PP
            INNER JOIN PersonalGestion PG
                ON PP.DNI = PG.DNI
        """
        cursor.execute(query)
        empleados = cursor.fetchall()
        combo['values'] = [f"{e[0]} - {e[1]}" for e in empleados]
        conexion.close()
    except Exception as e:
        print("Error al cargar empleados:", e)

# =====================================================================
# FUNCIONES: PESTAÑA 1 (GESTIÓN BÁSICA)
# =====================================================================

def registrar_visitante():
    nombre = entrada_nombre.get().strip()
    if nombre == "":
        messagebox.showwarning("Advertencia", "El nombre no puede estar vacío.")
        return
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO Visitantes (Nombre) VALUES (?)", (nombre,))
        conexion.commit()
        conexion.close()
        
        entrada_nombre.delete(0, tk.END)
        cargar_visitantes(lista_visitantes)
        cargar_visitantes(combo_visitante_entrada)
        messagebox.showinfo("Éxito", "Visitante registrado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo registrar: {e}")

# =====================================================================
# FUNCIONES: PESTAÑA 2 (VENTA DE ENTRADAS)
# =====================================================================

def registrar_entrada(): 
    visitante_sel = combo_visitante_entrada.get() 
    parque_sel = combo_parque_entrada.get() 
    gestion_sel = combo_gestion.get()
    
    if not visitante_sel or not parque_sel or not gestion_sel or not entrada_precio.get(): 
        messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos para la entrada.") 
        return 
        
    try: 
        precio = float(entrada_precio.get())
        id_visitante = int(visitante_sel.split(" - ")[0]) 
        id_parque = int(parque_sel.split(" - ")[0]) 
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        id_gestion = int(gestion_sel.split(" - ")[0])
        
        conexion = obtener_conexion() 
        cursor = conexion.cursor() 
        cursor.execute( 
            "INSERT INTO Entradas (Fecha, Parque_ID, Visitante_DNI, Gestion_DNI, Precio) VALUES (?, ?, ?, ?, ?)", 
            (fecha_actual, id_parque, id_visitante, id_gestion, precio) 
        ) 
        conexion.commit() 
        conexion.close() 
        
        mostrar_historial_entradas() 
        combo_visitante_entrada.set("")
        combo_parque_entrada.set("")
        combo_gestion.set("")

        entrada_precio.config(state="normal")
        entrada_precio.delete(0, tk.END)
        entrada_precio.config(state="readonly")
        
        messagebox.showinfo("Éxito", "¡Entrada vendida y registrada con éxito!") 
        
    except ValueError: 
        messagebox.showerror("Error de formato", "El precio debe ser un número válido.") 
    except Exception as e: 
        messagebox.showerror("Error", f"No se pudo registrar la entrada: {e}")

def cargar_precio_parque(event=None):
    parque_sel = combo_parque_entrada.get()
    if not parque_sel:
        return
    try:
        id_parque = int(parque_sel.split(" - ")[0])
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT PrecioEntrada FROM Parques WHERE Parque_ID = ?", (id_parque,))
        resultado = cursor.fetchone()

        if resultado:
            precio = resultado[0]
            # Desbloqueamos temporalmente para escribir el precio, luego volvemos a bloquear
            entrada_precio.config(state="normal")
            entrada_precio.delete(0, tk.END)
            entrada_precio.insert(0, str(precio))
            entrada_precio.config(state="readonly")
        conexion.close()
    except Exception as e:
        print("Error al cargar precio:", e)

def mostrar_historial_entradas():
    for fila in tabla_entradas.get_children():
        tabla_entradas.delete(fila)
        
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Visitante, Parque, EmpleadoGestion, Fecha, Precio
            FROM Vista_AtencionVisitantes
            ORDER BY Fecha DESC
        """)
        
        for i, fila in enumerate(cursor):
            fecha_str = fila[3].strftime('%Y-%m-%d %H:%M') if isinstance(fila[3], datetime) else fila[3]
            # Alternancia de colores en las filas
            tag = 'par' if i % 2 == 0 else 'impar'
            tabla_entradas.insert(
                "",
                tk.END,
                values=(fila[0], fila[1], fila[2], fecha_str, f"${fila[4]}"),
                tags=(tag,)
            )
        conexion.close()
    except Exception as e:
        print("Error al cargar historial de entradas:", e)

# =====================================================================
# FUNCIONES: PESTAÑA 3 (BIODIVERSIDAD - ESPECIES)
# =====================================================================

def mostrar_especies_parque(event=None):
    for fila in tabla_especies.get_children():
        tabla_especies.delete(fila)
        
    parque_sel = combo_parque_especies.get()
    if not parque_sel:
        return
        
    try:
        id_parque = int(parque_sel.split(" - ")[0])
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        query = """
            SELECT E.NombreVulgar, E.NombreCientifico, A.Nombre, AE.CantidadIndividuos
            FROM Especies E
            INNER JOIN Areas_Especies AE ON E.Especies_ID = AE.Especie
            INNER JOIN Areas A ON AE.Area = A.Area_ID
            WHERE A.Parque_ID = ?
        """
        cursor.execute(query, (id_parque,))
        
        for i, fila in enumerate(cursor):
            tag = 'par' if i % 2 == 0 else 'impar'
            tabla_especies.insert("", tk.END, values=(fila[0], fila[1], fila[2], fila[3]), tags=(tag,))
            
        conexion.close()
    except Exception as e:
        print("Error al consultar especies:", e)

# =====================================================================
# FUNCIONES: PESTAÑA 4 (REPORTE GANANCIAS-PARQUES)
# =====================================================================

def generar_reporte_ingresos():
    for fila in tabla_reportes.get_children():
        tabla_reportes.delete(fila)

    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("EXEC GenerarIngresosPorParque")

        for i, fila in enumerate(cursor):
            tag = 'par' if i % 2 == 0 else 'impar'
            tabla_reportes.insert("", tk.END, values=(fila[0], f"${fila[1]:,.2f}"), tags=(tag,))
        conexion.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el reporte:\n{e}")

# =====================================================================
# INTERFAZ GRÁFICA PRINCIPAL (DISEÑO PRESTIGE/ECOLÓGICO)
# =====================================================================

ventana = tk.Tk()
ventana.title("Panel de Control - Reserva Natural")
ventana.geometry("1100x750")
ventana.configure(bg="#f4f6f6")  # Fondo general gris muy claro

# ---- CONFIGURACIÓN DE ESTILOS TTK ----
style = ttk.Style()
style.theme_use("clam")

# Paleta de colores globales
COLOR_PRIMARIO = "#2e7d32"     # Verde Bosque / Ecológico
COLOR_ACCION = "#1b5e20"       # Verde más oscuro para estados activos
COLOR_FONDO_TAB = "#ffffff"    # Blanco para contenedores limpios
COLOR_TEXTO = "#2c3e50"        # Gris oscuro profesional para textos

style.configure(".", font=("Segoe UI", 10), foreground=COLOR_TEXTO)

# Estilo del cuaderno (Notebook / Pestañas)
style.configure("TNotebook", background="#f4f6f6", borderwidth=0)
style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 6], background="#e0e0e0", foreground="#555555")
style.map("TNotebook.Tab", background=[("selected", COLOR_PRIMARIO)], foreground=[("selected", "#ffffff")])

# Estilo de los Combobox
style.configure("TCombobox", padding=5, relief="flat", background="#ffffff")
style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")], background=[("readonly", "#ffffff")])

# Estilo de los Treeview (Tablas)
style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#ffffff", fieldbackground="#ffffff", borderwidth=0)
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#eaeded", foreground=COLOR_TEXTO, relief="flat", padding=5)
style.map("Treeview", background=[("selected", "#a9dfbf")], foreground=[("selected", "#196f3d")])

# Función para crear botones modernos sin relieve clásico
def crear_boton_moderno(parent, text, bg_color, command):
    btn = tk.Button(
        parent, text=text, command=command, font=("Segoe UI", 10, "bold"),
        fg="white", bg=bg_color, activebackground=COLOR_ACCION, activeforeground="white",
        relief="flat", bd=0, cursor="hand2", padx=15, pady=8
    )
    # Pequeño efecto Hover interactivo
    btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_ACCION))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
    return btn

# Encabezado Superior Principal
frame_header = tk.Frame(ventana, bg=COLOR_PRIMARIO, pady=15)
frame_header.pack(fill=tk.X)
lbl_titulo_app = tk.Label(frame_header, text="SISTEMA DE GESTIÓN ECOLÓGICA E INGRESOS", font=("Segoe UI", 16, "bold"), fg="white", bg=COLOR_PRIMARIO)
lbl_titulo_app.pack()

# Contenedor de Pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

tab1 = tk.Frame(notebook, bg=COLOR_FONDO_TAB)
tab2 = tk.Frame(notebook, bg=COLOR_FONDO_TAB)
tab3 = tk.Frame(notebook, bg=COLOR_FONDO_TAB)
tab4 = tk.Frame(notebook, bg=COLOR_FONDO_TAB)

notebook.add(tab1, text="  Registros Básicos  ")
notebook.add(tab2, text="  Taquilla / Entradas  ")
notebook.add(tab3, text="  Especies y Biodiversidad  ")
notebook.add(tab4, text="  Reporte de Ganancias  ")

# ---------------------------------------------------------------------
# DISEÑO PESTAÑA 1: REGISTROS BÁSICOS
# ---------------------------------------------------------------------
frame_columnas = tk.Frame(tab1, bg=COLOR_FONDO_TAB)
frame_columnas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

# Izquierda: Parques
lf_parques = tk.LabelFrame(frame_columnas, text=" Parques Registrados ", font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO_TAB, fg=COLOR_PRIMARIO, padx=10, pady=10)
lf_parques.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

lista_parques = tk.Listbox(lf_parques, font=("Segoe UI", 10), bd=1, relief="solid", highlightthickness=0, bg="#fcfcfc", selectbackground="#a9dfbf", selectforeground="#196f3d")
lista_parques.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

btn_c_parques = crear_boton_moderno(lf_parques, "Cargar Parques", COLOR_PRIMARIO, lambda: cargar_parques(lista_parques))
btn_c_parques.pack(fill=tk.X)

# Derecha: Visitantes
lf_visitantes = tk.LabelFrame(frame_columnas, text=" Gestión de Visitantes ", font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO_TAB, fg=COLOR_PRIMARIO, padx=10, pady=10)
lf_visitantes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

tk.Label(lf_visitantes, text="Nombre del Visitante:", font=("Segoe UI", 10), bg=COLOR_FONDO_TAB).pack(anchor=tk.W, pady=(0, 2))
entrada_nombre = tk.Entry(lf_visitantes, font=("Segoe UI", 11), bd=1, relief="solid")
entrada_nombre.pack(fill=tk.X, pady=(0, 10), ipady=4)

btn_reg_vis = crear_boton_moderno(lf_visitantes, "Registrar Nuevo Visitante", "#2980b9", registrar_visitante)
btn_reg_vis.pack(fill=tk.X, pady=(0, 15))

lista_visitantes = tk.Listbox(lf_visitantes, font=("Segoe UI", 10), bd=1, relief="solid", highlightthickness=0, bg="#fcfcfc", selectbackground="#a9dfbf", selectforeground="#196f3d")
lista_visitantes.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

btn_c_vis = crear_boton_moderno(lf_visitantes, "Actualizar Lista", COLOR_PRIMARIO, lambda: cargar_visitantes(lista_visitantes))
btn_c_vis.pack(fill=tk.X)

# ---------------------------------------------------------------------
# DISEÑO PESTAÑA 2: TAQUILLA / ENTRADAS
# ---------------------------------------------------------------------
lf_formulario_entrada = tk.LabelFrame(tab2, text=" Emitir Nueva Entrada ", font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO_TAB, fg=COLOR_PRIMARIO, padx=15, pady=15)
lf_formulario_entrada.pack(fill=tk.X, padx=15, pady=15)

# Organización limpia usando Grid con espaciados unificados
tk.Label(lf_formulario_entrada, text="Seleccione Visitante:", font=("Segoe UI", 10), bg=COLOR_FONDO_TAB).grid(row=0, column=0, sticky=tk.W, pady=8)
combo_visitante_entrada = ttk.Combobox(lf_formulario_entrada, font=("Segoe UI", 10), state="readonly", width=28)
combo_visitante_entrada.grid(row=0, column=1, padx=(10, 25), pady=8)

tk.Label(lf_formulario_entrada, text="Seleccione Parque:", font=("Segoe UI", 10), bg=COLOR_FONDO_TAB).grid(row=0, column=2, sticky=tk.W, pady=8)
combo_parque_entrada = ttk.Combobox(lf_formulario_entrada, font=("Segoe UI", 10), state="readonly", width=28)
combo_parque_entrada.grid(row=0, column=3, padx=10, pady=8)
combo_parque_entrada.bind("<<ComboboxSelected>>", cargar_precio_parque)

tk.Label(lf_formulario_entrada, text="Precio de Entrada ($):", font=("Segoe UI", 10), bg=COLOR_FONDO_TAB).grid(row=1, column=0, sticky=tk.W, pady=8)
entrada_precio = tk.Entry(lf_formulario_entrada, font=("Segoe UI", 10), width=15, state="readonly", bd=1, relief="solid")
entrada_precio.grid(row=1, column=1, sticky=tk.W, padx=10, pady=8, ipady=3)

tk.Label(lf_formulario_entrada, text="Empleado Gestión DNI:", font=("Segoe UI", 10), bg=COLOR_FONDO_TAB).grid(row=1, column=2, sticky=tk.W, pady=8)
combo_gestion = ttk.Combobox(lf_formulario_entrada, font=("Segoe UI", 10), state="readonly", width=28)
combo_gestion.grid(row=1, column=3, padx=10, pady=8)

btn_vender = crear_boton_moderno(lf_formulario_entrada, "Generar y Cobrar Entrada", "#d35400", registrar_entrada)
btn_vender.grid(row=2, column=0, columnspan=4, sticky=tk.E+tk.W, pady=(15, 5))

# Historial usando Treeview estilizado
lf_historial = tk.LabelFrame(tab2, text=" Últimas Visitas Registradas (Vista_AtencionVisitantes) ", font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO_TAB, fg=COLOR_PRIMARIO, padx=10, pady=10)
lf_historial.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

columnas_ent = ("Visitante", "Parque", "Atendido Por", "Fecha/Hora", "Precio")
tabla_entradas = ttk.Treeview(lf_historial, columns=columnas_ent, show="headings")
for col in columnas_ent:
    tabla_entradas.heading(col, text=col)
    tabla_entradas.column(col, width=150, anchor=tk.CENTER)

# Configuración de filas alternas (cebra) para facilitar la lectura
tabla_entradas.tag_configure('par', background='#ffffff')
tabla_entradas.tag_configure('impar', background='#f9f9f9')
tabla_entradas.pack(fill=tk.BOTH, expand=True)

# ---------------------------------------------------------------------
# DISEÑO PESTAÑA 3: ESPECIES Y BIODIVERSIDAD
# ---------------------------------------------------------------------
lf_filtro_especies = tk.Frame(tab3, bg=COLOR_FONDO_TAB, padx=15, pady=15)
lf_filtro_especies.pack(fill=tk.X)

tk.Label(lf_filtro_especies, text="Seleccione un Parque para ver su Fauna/Flora:", font=("Segoe UI", 11), bg=COLOR_FONDO_TAB).pack(side=tk.LEFT, padx=5)
combo_parque_especies = ttk.Combobox(lf_filtro_especies, font=("Segoe UI", 10), state="readonly", width=35)
combo_parque_especies.pack(side=tk.LEFT, padx=10)
combo_parque_especies.bind("<<ComboboxSelected>>", mostrar_especies_parque)

lf_resultado_esp = tk.LabelFrame(tab3, text=" Especies en el Hábitat ", font=("Segoe UI", 11, "bold"), bg=COLOR_FONDO_TAB, fg=COLOR_PRIMARIO, padx=10, pady=10)
lf_resultado_esp.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

columnas_esp = ("Nombre Común", "Nombre Científico", "Área Específica", "Cantidad de Individuos")
tabla_especies = ttk.Treeview(lf_resultado_esp, columns=columnas_esp, show="headings")
for col in columnas_esp:
    tabla_especies.heading(col, text=col)
    tabla_especies.column(col, anchor=tk.CENTER)

tabla_especies.tag_configure('par', background='#ffffff')
tabla_especies.tag_configure('impar', background='#f9f9f9')
tabla_especies.pack(fill=tk.BOTH, expand=True)

# ---------------------------------------------------------------------
# DISEÑO PESTAÑA 4: REPORTES
# ---------------------------------------------------------------------
frame_reportes = tk.Frame(tab4, bg=COLOR_FONDO_TAB, padx=20, pady=20)
frame_reportes.pack(fill=tk.BOTH, expand=True)

lbl_reportes = tk.Label(frame_reportes, text="Reporte de Ingresos Financieros por Parque", font=("Segoe UI", 14, "bold"), bg=COLOR_FONDO_TAB, fg=COLOR_TEXTO)
lbl_reportes.pack(pady=(0, 10))

btn_generar_reporte = crear_boton_moderno(frame_reportes, "Generar Reporte de Caja", "#8e44ad", generar_reporte_ingresos)
btn_generar_reporte.pack(pady=5)

columnas_rep = ("Parque", "Total Ingresos Acumulados")
tabla_reportes = ttk.Treeview(frame_reportes, columns=columnas_rep, show="headings", height=12)
for col in columnas_rep:
    tabla_reportes.heading(col, text=col)
    tabla_reportes.column(col, anchor=tk.CENTER, width=250)

tabla_reportes.tag_configure('par', background='#ffffff')
tabla_reportes.tag_configure('impar', background='#f9f9f9')
tabla_reportes.pack(fill=tk.BOTH, expand=True, pady=15)

# =====================================================================
# PRE-CARGA INICIAL DE DATOS AL ARRANCAR
# =====================================================================
cargar_parques(lista_parques)
cargar_parques(combo_parque_entrada)
cargar_parques(combo_parque_especies)

cargar_visitantes(lista_visitantes)
cargar_visitantes(combo_visitante_entrada)
cargar_empleados_gestion(combo_gestion)

mostrar_historial_entradas()

# Iniciar bucle de ejecución de la ventana
ventana.mainloop()