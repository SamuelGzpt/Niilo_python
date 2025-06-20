import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
import pyodbc
from datetime import datetime
import hashlib

class ModernRedSocialApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NIILO")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        
        # Configuración de conexión a SQL Server
        self.connection_string = """
        DRIVER={ODBC Driver 17 for SQL Server};
        SERVER=localhost;
        DATABASE=red_social;
        Trusted_Connection=yes;
        """
        
        self.current_user_id = None
        self.open_windows = []  # Track open windows
        self.query_history = []  # Historial de consultas SQL (solo BD)
        self.setup_styles()
        self.setup_main_interface()
        
    def setup_styles(self):
        """Configurar estilos modernos"""
        style = ttk.Style()
        style.theme_use('clam')  # Base theme
        
        # Configurar estilos para Treeview
        style.configure("Modern.Treeview", 
                       background="#2d2d44",
                       foreground="white",
                       fieldbackground="#2d2d44",
                       borderwidth=0)
        style.configure("Modern.Treeview.Heading",
                       background="#16213e",
                       foreground="white",
                       relief="flat")
        
        # Configurar estilos para Notebook
        style.configure("Modern.TNotebook", 
                       background="#1a1a2e",
                       borderwidth=0)
        style.configure("Modern.TNotebook.Tab",
                       background="#2d2d44",
                       foreground="white",
                       padding=[20, 10])
        
    def connect_db(self):
        """Conectar a la base de datos"""
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos:\n{str(e)}")
            return None
    
    def hash_password(self, password):
        """Hash simple para la contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def close_all_windows(self):
        """Cerrar todas las ventanas secundarias abiertas"""
        for window in self.open_windows[:]:  # crea una copia para iteraciones
            try:
                if window.winfo_exists():
                    window.destroy()
                self.open_windows.remove(window)
            except:
                pass
        self.open_windows.clear()
    
    def create_modern_button(self, parent, text, command, bg_color, hover_color, width=200, height=50):
        """Crear botón moderno con efectos hover - VERSIÓN CORREGIDA"""
        # Frame contenedor con dimensiones fijas
        btn_frame = tk.Frame(parent, bg=parent['bg'] if isinstance(parent, dict) else '#2d2d44', 
                            width=width, height=height)
        btn_frame.pack_propagate(False)  # Evita que el frame se redimensione
        
        # Botón que llena todo el frame
        button = tk.Button(btn_frame, text=text, command=command,
                          bg=bg_color, fg='white', font=('Segoe UI', 12, 'bold'),
                          border=0, cursor='hand2', activebackground=hover_color,
                          activeforeground='white', relief='flat')
        button.pack(fill='both', expand=True)
        
        # Hover effects
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=bg_color)
            
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        return btn_frame
    
    def setup_main_interface(self):
        """Configurar la interfaz principal moderna"""
        # Header con gradiente simulado
        header_frame = tk.Frame(self.root, bg='#16213e', height=100)
        header_frame.pack(fill='x', pady=0)
        header_frame.pack_propagate(False)
        
        # Título principal
        title_label = tk.Label(header_frame, text="🌐NIILO", 
                              font=('Segoe UI', 28, 'bold'), 
                              bg='#16213e', fg="#f911f9")
        title_label.pack(pady=20)
        
        # # Subtítulo
        # subtitle_label = tk.Label(header_frame, text="Red social", 
        #                          font=('Segoe UI', 12), 
        #                          bg='#16213e', fg='#a0a0a0')
        # subtitle_label.pack()
        
        # Frame para información de usuario
        user_frame = tk.Frame(self.root, bg='#1a1a2e', height=80)
        user_frame.pack(fill='x', pady=10)
        user_frame.pack_propagate(False)
        
        # Panel de usuario
        user_panel = tk.Frame(user_frame, bg='#2d2d44', relief='flat', bd=2)
        user_panel.pack(fill='x', padx=20, pady=10)
        
        self.user_label = tk.Label(user_panel, text="👤 Usuario no conectado", 
                                  font=('Segoe UI', 14, 'bold'), 
                                  bg='#2d2d44', fg='#ff6b6b')
        self.user_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # BOTONES DE AUTENTICACIÓN - VERSIÓN CORREGIDA
        auth_frame = tk.Frame(user_panel, bg='#2d2d44')
        auth_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Crear botones con dimensiones específicas y empaquetado correcto
        self.login_btn = tk.Button(auth_frame, text="🔑 INICIAR SESIÓN", 
                            command=self.login_window,
                            bg='#4ecdc4', fg='white', 
                            font=('Segoe UI', 11, 'bold'),
                            border=0, cursor='hand2', 
                            activebackground='#45b7aa',
                            activeforeground='white',
                            padx=20, pady=10,
                            relief='flat')
        self.login_btn.pack(side=tk.LEFT, padx=5)
        
        self.register_btn = tk.Button(auth_frame, text="📝 REGISTRARSE", 
                               command=self.register_window,
                               bg='#45b7d1', fg='white', 
                               font=('Segoe UI', 11, 'bold'),
                               border=0, cursor='hand2',
                               activebackground='#357abd',
                               activeforeground='white',
                               padx=20, pady=10,
                               relief='flat')
        self.register_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón de logout (inicialmente oculto)
        self.logout_btn = tk.Button(auth_frame, text="🚪 CERRAR SESIÓN", 
                                   command=self.logout,
                                   bg='#ff6b6b', fg='white', 
                                   font=('Segoe UI', 11, 'bold'),
                                   border=0, cursor='hand2',
                                   activebackground='#e55656',
                                   activeforeground='white',
                                   padx=20, pady=10,
                                   relief='flat')
        
        # Efectos hover para botones de autenticación
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        create_hover_effect(self.login_btn, '#4ecdc4', '#45b7aa')
        create_hover_effect(self.register_btn, '#45b7d1', '#357abd')
        create_hover_effect(self.logout_btn, '#ff6b6b', '#e55656')
        
        # Separador
        separator = tk.Frame(self.root, bg='#16213e', height=2)
        separator.pack(fill='x', pady=20)
        
        # Grid de botones principales
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Configurar grid con tamaños mínimos
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1, minsize=200)
        for i in range(2):  # Cambiado de 3 a 2 filas (eliminamos feed)
            main_frame.grid_rowconfigure(i, weight=1, minsize=150)
        
        # Botones principales con iconos y colores modernos (sin feed)
        buttons_config = [
            ("👥 USUARIOS", self.show_users, '#ff6b6b', '#e55656'),
            ("📝 PUBLICACIONES", self.show_posts, '#4ecdc4', '#45b7aa'),
            ("✍️ CREAR POST", self.create_post_window, '#45b7d1', '#357abd'),
            ("🤝 AMISTADES", self.manage_friendships, '#feca57', '#e5b343'),
            ("💬 MENSAJES", self.show_messages, '#ff9ff3', '#e58ce5'),
            ("🗄️ BASE DATOS", self.show_database_viewer, '#6c5ce7', '#5848c4'),
        ]
        
        # Colocar botones en grid
        for i, (text, command, bg_color, hover_color) in enumerate(buttons_config):
            row = i // 3
            col = i % 3
            
            btn_container = tk.Frame(main_frame, bg='#1a1a2e')
            btn_container.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            btn_container.grid_propagate(False)  # Evitar que se redimensione
            btn_container.configure(width=200, height=150)  # Tamaño fijo
            
            button = tk.Button(btn_container, text=text, command=command,
                             bg=bg_color, fg='white', font=('Segoe UI', 14, 'bold'),
                             border=0, cursor='hand2', activebackground=hover_color,
                             activeforeground='white', relief='flat',
                             pady=20)
            button.pack(fill='both', expand=True)
            
            # Hover effects
            def make_hover(btn, normal_color, hover_color):
                def on_enter(e):
                    btn.config(bg=hover_color)
                def on_leave(e):
                    btn.config(bg=normal_color)
                return on_enter, on_leave
            
            enter_func, leave_func = make_hover(button, bg_color, hover_color)
            button.bind("<Enter>", enter_func)
            button.bind("<Leave>", leave_func)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#16213e', height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(footer_frame, text="© 2025 NIILO - Powered by Python & SQL Server", 
                               font=('Segoe UI', 10), bg='#16213e', fg='#a0a0a0')
        footer_label.pack(pady=10)
    
    def logout(self):
        """Cerrar sesión del usuario"""
        self.current_user_id = None
        self.user_label.config(text="👤 Usuario no conectado", fg='#ff6b6b')
        
        # Ocultar botón logout y mostrar botones de login/register
        self.logout_btn.pack_forget()
        self.login_btn.pack(side=tk.LEFT, padx=5)
        self.register_btn.pack(side=tk.LEFT, padx=5)
        
        messagebox.showinfo("Sesión cerrada", "Has cerrado sesión correctamente")
    
    def create_modern_window(self, title, size="800x600", bg_color="#1a1a2e"):
        """Crear ventana moderna estándar"""
        self.close_all_windows()  # Cerrar ventanas anteriores
        
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(size)
        window.configure(bg=bg_color)
        window.transient(self.root)
        window.grab_set()  # Hacer modal
        window.focus_set()  # Dar foco
        
        # Centrar la ventana
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (int(size.split('x')[0]) // 2)
        y = (window.winfo_screenheight() // 2) - (int(size.split('x')[1]) // 2)
        window.geometry(f"{size}+{x}+{y}")
        
        self.open_windows.append(window)
        
        # Header de la ventana
        header = tk.Frame(window, bg='#16213e', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Título
        title_label = tk.Label(header, text=title, font=('Segoe UI', 18, 'bold'),
                              bg='#16213e', fg='white')
        title_label.pack(side='left', padx=20, pady=15)
        
        # Botón volver
        back_btn = tk.Button(header, text="← VOLVER", command=window.destroy,
                           bg='#ff6b6b', fg='white', font=('Segoe UI', 10, 'bold'),
                           border=0, cursor='hand2', padx=20)
        back_btn.pack(side='right', padx=20, pady=15)
        
        return window
    
    def login_window(self):
        """Ventana de inicio de sesión moderna"""
        login_win = self.create_modern_window("🔑 Iniciar Sesión", "700x500")
        
        # Frame principal
        main_frame = tk.Frame(login_win, bg='#2d2d44')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Título
        tk.Label(main_frame, text="Bienvenido de vuelta", 
                font=('Segoe UI', 16, 'bold'), bg='#2d2d44', fg='white').pack(pady=20)
        
        # Campos de entrada modernos
        def create_modern_entry(parent, placeholder, show=None):
            frame = tk.Frame(parent, bg='#2d2d44')
            frame.pack(fill='x', pady=10)
            
            label = tk.Label(frame, text=placeholder, font=('Segoe UI', 10),
                           bg='#2d2d44', fg='#a0a0a0')
            label.pack(anchor='w')
            
            entry_kwargs = {
                'font': ('Segoe UI', 12),
                'bg': '#16213e',
                'fg': 'white',
                'insertbackground': 'white',
                'border': 0,
                'relief': 'flat'
            }
            if show is not None:
                entry_kwargs['show'] = show
            entry = tk.Entry(frame, **entry_kwargs)
            entry.pack(fill='x', ipady=8)
            
            return entry
        
        email_entry = create_modern_entry(main_frame, "Email")
        password_entry = create_modern_entry(main_frame, "Contraseña", show='*')
        
        def do_login():
            email = email_entry.get()
            password = self.hash_password(password_entry.get())
            
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, apellido FROM usuarios WHERE email = ? AND password_hash = ? AND activo = 1", 
                              (email, password))
                user = cursor.fetchone()
                
                if user:
                    self.current_user_id = user[0]
                    self.user_label.config(text=f"👤 {user[1]} {user[2]}", fg='#4ecdc4')
                    
                    # Ocultar botones de login/register y mostrar logout
                    self.login_btn.pack_forget()
                    self.register_btn.pack_forget()
                    self.logout_btn.pack(side=tk.LEFT, padx=5)
                    
                    login_win.destroy()
                    messagebox.showinfo("¡Bienvenido!", f"Sesión iniciada como {user[1]} {user[2]}")
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas")
                conn.close()
        
        # Botón de login
        login_button = tk.Button(main_frame, text="INICIAR SESIÓN", command=do_login,
                               bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                               border=0, cursor='hand2', pady=12)
        login_button.pack(fill='x', pady=20)
        
        # Forzar actualización del layout
        login_win.update_idletasks()
    
    def register_window(self):
        """Ventana de registro moderna"""
        reg_win = self.create_modern_window("📝 Crear Cuenta", "900x900")
        
        # Crear canvas con scrollbar
        canvas = tk.Canvas(reg_win, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(reg_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Frame principal dentro del scroll
        main_frame = tk.Frame(scrollable_frame, bg='#2d2d44')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        tk.Label(main_frame, text="Únete a NIILO", 
                font=('Segoe UI', 16, 'bold'), bg='#2d2d44', fg='white').pack(pady=20)
        
        # Función para crear entradas modernas
        def create_modern_entry(parent, placeholder, is_text_area=False, show=None):
            frame = tk.Frame(parent, bg='#2d2d44')
            frame.pack(fill='x', pady=8)
            
            label = tk.Label(frame, text=placeholder, font=('Segoe UI', 10),
                           bg='#2d2d44', fg='#a0a0a0')
            label.pack(anchor='w')
            
            if is_text_area:
                entry = tk.Text(frame, font=('Segoe UI', 10), bg='#16213e', fg='white',
                              insertbackground='white', border=0, relief='flat', height=3)
            else:
                entry_kwargs = {
                    'font': ('Segoe UI', 12),
                    'bg': '#16213e',
                    'fg': 'white',
                    'insertbackground': 'white',
                    'border': 0,
                    'relief': 'flat'
                }
                if show is not None:
                    entry_kwargs['show'] = show
                entry = tk.Entry(frame, **entry_kwargs)
            entry.pack(fill='x', ipady=8 if not is_text_area else 0)
            
            return entry
        
        # Campos del formulario
        entries = {}
        fields = [
            ("Nombre *", "nombre"),
            ("Apellido *", "apellido"),
            ("Email *", "email"),
            ("Contraseña *", "password"),
            ("Ubicación", "ubicacion"),
            ("Biografía", "biografia")
        ]
        
        for label, key in fields:
            if key == "password":
                entries[key] = create_modern_entry(main_frame, label, show='*')
            elif key == "biografia":
                entries[key] = create_modern_entry(main_frame, label, is_text_area=True)
            else:
                entries[key] = create_modern_entry(main_frame, label)
        
        # Campo de fecha de nacimiento con calendario
        fecha_frame = tk.Frame(main_frame, bg='#2d2d44')
        fecha_frame.pack(fill='x', pady=8)
        
        tk.Label(fecha_frame, text="Fecha de Nacimiento", font=('Segoe UI', 10),
               bg='#2d2d44', fg='#a0a0a0').pack(anchor='w')
        
        # Calendario moderno
        fecha_calendar = DateEntry(fecha_frame, 
                                 width=20, 
                                 background='#16213e',
                                 foreground='white',
                                 borderwidth=0,
                                 date_pattern='yyyy-mm-dd',
                                 font=('Segoe UI', 12),
                                 selectbackground='#4ecdc4',
                                 selectforeground='white',
                                 normalbackground='#16213e',
                                 normalforeground='white',
                                 weekendbackground='#16213e',
                                 weekendforeground='white',
                                 othermonthbackground='#1a1a2e',
                                 othermonthforeground='#666666',
                                 headersbackground='#2d2d44',
                                 headersforeground='white',
                                 arrowcolor='white',
                                 bordercolor='#4ecdc4',
                                 showweeknumbers=False)
        fecha_calendar.pack(fill='x', ipady=8)
        
        def do_register():
            try:
                values = {}
                for key, entry in entries.items():
                    if key == "biografia":
                        values[key] = entry.get(1.0, tk.END).strip()
                    else:
                        values[key] = entry.get().strip()
                
                # Obtener fecha del calendario
                fecha_nacimiento = fecha_calendar.get_date()
                
                if not all([values['nombre'], values['apellido'], values['email'], values['password']]):
                    messagebox.showerror("Error", "Los campos marcados con * son obligatorios")
                    return
                
                values['password'] = self.hash_password(values['password'])
                
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        EXEC sp_insertar_usuario ?, ?, ?, ?, ?, ?, ?
                    """, (
                        values['nombre'], values['apellido'], values['email'],
                        values['password'], fecha_nacimiento,
                        values.get('ubicacion'), values.get('biografia')
                    ))
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("¡Bienvenido!", "¡Cuenta creada exitosamente!")
                    reg_win.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear cuenta:\n{str(e)}")
        
        register_btn = tk.Button(main_frame, text="CREAR CUENTA", command=do_register,
                               bg='#45b7d1', fg='white', font=('Segoe UI', 12, 'bold'),
                               border=0, cursor='hand2', pady=12, width=20, height=2)
        register_btn.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Forzar actualización del layout
        reg_win.update_idletasks()
    
    def show_users(self):
        """Mostrar usuarios con diseño moderno"""
        users_win = self.create_modern_window("👥 Usuarios Registrados", "1200x800")
        
        # Frame para la tabla
        table_frame = tk.Frame(users_win, bg='#1a1a2e')
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview moderno
        tree = ttk.Treeview(table_frame, columns=('ID', 'Nombre', 'Email', 'Ubicación', 'Registro'), 
                           show='headings', style="Modern.Treeview")
        
        # Configurar columnas
        columns_config = [
            ('ID', 50),
            ('Nombre', 200),
            ('Email', 250),
            ('Ubicación', 150),
            ('Registro', 150)
        ]
        
        for col, width in columns_config:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Cargar datos
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, CONCAT(nombre, ' ', apellido), email, ubicacion, fecha_registro FROM usuarios WHERE activo = 1")
            for row in cursor.fetchall():
                tree.insert('', 'end', values=tuple(row))
            conn.close()
        
        tree.pack(side="left", fill='both', expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame para botones de acción
        action_frame = tk.Frame(users_win, bg='#1a1a2e')
        action_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Botón para enviar mensaje
        send_msg_btn = tk.Button(action_frame, text="💬 ENVIAR MENSAJE", 
                                command=lambda: self.send_message_to_selected_user(tree),
                                bg='#ff9ff3', fg='white', font=('Segoe UI', 10, 'bold'),
                                border=0, cursor='hand2', padx=20, pady=5)
        send_msg_btn.pack(side='left', padx=5)
        
        # Botón para enviar solicitud de amistad
        send_friend_btn = tk.Button(action_frame, text="🤝 SOLICITUD AMISTAD", 
                                   command=lambda: self.send_friend_request_to_selected_user(tree),
                                   bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                                   border=0, cursor='hand2', padx=20, pady=5, width=18, height=2)
        send_friend_btn.pack(side='left', padx=5)
    
    def send_message_to_selected_user(self, tree):
        """Enviar mensaje al usuario seleccionado en el tree"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para enviar mensajes")
            return
        
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Debes seleccionar un usuario para enviarle un mensaje")
            return
        
        user_id = tree.item(selected[0])['values'][0]
        user_name = tree.item(selected[0])['values'][1]
        
        # Verificar si son amigos
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT estado FROM amistades 
                WHERE (usuario1_id = ? AND usuario2_id = ?) 
                   OR (usuario1_id = ? AND usuario2_id = ?)
            """, (self.current_user_id, user_id, user_id, self.current_user_id))
            
            friendship = cursor.fetchone()
            conn.close()
            
            if not friendship or friendship[0] != 'aceptada':
                messagebox.showwarning("Amistad requerida", 
                                     f"Debes ser amigo de {user_name} para enviarle mensajes.\n"
                                     "Primero envía una solicitud de amistad.")
                return
        
        # Abrir ventana de envío de mensaje
        self.send_message_window(user_id, user_name)
    
    def send_friend_request_to_selected_user(self, tree):
        """Enviar solicitud de amistad al usuario seleccionado en el tree"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para enviar solicitudes de amistad")
            return
        
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Debes seleccionar un usuario para enviarle una solicitud de amistad")
            return
        
        user_id = tree.item(selected[0])['values'][0]
        user_name = tree.item(selected[0])['values'][1]
        
        # Verificar que no se envíe solicitud a sí mismo
        if user_id == self.current_user_id:
            messagebox.showwarning("Error", "No puedes enviarte una solicitud de amistad a ti mismo")
            return
        
        # Verificar si ya existe una solicitud o amistad
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT estado FROM amistades 
                WHERE (usuario1_id = ? AND usuario2_id = ?) 
                   OR (usuario1_id = ? AND usuario2_id = ?)
            """, (self.current_user_id, user_id, user_id, self.current_user_id))
            
            existing_friendship = cursor.fetchone()
            
            if existing_friendship:
                if existing_friendship[0] == 'aceptada':
                    messagebox.showinfo("Ya son amigos", f"Ya eres amigo de {user_name}")
                elif existing_friendship[0] == 'pendiente':
                    messagebox.showinfo("Solicitud pendiente", f"Ya tienes una solicitud de amistad pendiente con {user_name}")
                else:
                    messagebox.showinfo("Solicitud rechazada", f"Ya enviaste una solicitud de amistad a {user_name} que fue rechazada")
                conn.close()
                return
            
            # Enviar solicitud de amistad
            try:
                cursor.execute("""
                    INSERT INTO amistades (usuario1_id, usuario2_id, estado, fecha_solicitud)
                    VALUES (?, ?, 'pendiente', GETDATE())
                """, (self.current_user_id, user_id))
                conn.commit()
                
                messagebox.showinfo("¡Solicitud enviada!", f"Solicitud de amistad enviada a {user_name} 🤝")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al enviar solicitud de amistad:\n{str(e)}")
            finally:
                conn.close()
    
    def create_post_window(self):
        """Ventana moderna para crear publicaciones"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para crear publicaciones")
            return
        
        post_win = self.create_modern_window("✍️ Nueva Publicación", "1200x800")
        
        main_frame = tk.Frame(post_win, bg='#2d2d44')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Tipo de publicación con botones modernos
        tk.Label(main_frame, text="Tipo de contenido:", font=('Segoe UI', 12, 'bold'),
                bg='#2d2d44', fg='white').pack(anchor='w', pady=(0, 10))
        
        tipo_frame = tk.Frame(main_frame, bg='#2d2d44')
        tipo_frame.pack(fill='x', pady=10)
        
        tipo_var = tk.StringVar(value="texto")
        
        tipos = [("📝 Texto", "texto"), ("🖼️ Imagen", "imagen"), ("🎥 Video", "video")]
        for i, (text, value) in enumerate(tipos):
            btn = tk.Radiobutton(tipo_frame, text=text, variable=tipo_var, value=value,
                               bg='#16213e', fg='white', selectcolor='#4ecdc4',
                               font=('Segoe UI', 10), activebackground='#2d2d44')
            btn.pack(side='left', padx=10)
        
        # Área de contenido
        tk.Label(main_frame, text="Contenido:", font=('Segoe UI', 12, 'bold'),
                bg='#2d2d44', fg='white').pack(anchor='w', pady=(20, 5))
        
        content_text = tk.Text(main_frame, height=8, font=('Segoe UI', 11),
                              bg='#16213e', fg='white', insertbackground='white',
                              border=0, relief='flat')
        content_text.pack(fill='x', pady=5)
        
        # URL opcional
        tk.Label(main_frame, text="URL multimedia (opcional):", font=('Segoe UI', 10),
                bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', pady=(15, 5))
        
        url_entry = tk.Entry(main_frame, font=('Segoe UI', 10), bg='#16213e', fg='white',
                           insertbackground='white', border=0, relief='flat')
        url_entry.pack(fill='x', ipady=5)
        
        def publish_post():
            contenido = content_text.get(1.0, tk.END).strip()
            tipo = tipo_var.get()
            url_media = url_entry.get().strip() or None
            
            if not contenido:
                messagebox.showerror("Error", "El contenido no puede estar vacío")
                return
            
            try:
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO publicaciones (usuario_id, contenido, tipo, url_media)
                        VALUES (?, ?, ?, ?)
                    """, (self.current_user_id, contenido, tipo, url_media))
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("¡Éxito!", "Publicación creada correctamente")
                    post_win.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al crear publicación:\n{str(e)}")
        
        # Botón publicar
        publish_btn = tk.Button(main_frame, text="🚀 PUBLICAR", command=publish_post,
                              bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                              border=0, cursor='hand2', pady=15)
        publish_btn.pack(fill='x', pady=20)
    
    def show_posts(self):
        """Mostrar publicaciones con diseño moderno"""
        posts_win = self.create_modern_window("📝 Publicaciones", "1000x700")
        
        # Canvas con scroll
        canvas = tk.Canvas(posts_win, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(posts_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cargar publicaciones
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.id, p.contenido, p.tipo, p.fecha_publicacion,
                       CONCAT(u.nombre, ' ', u.apellido) as autor,
                       (SELECT COUNT(*) FROM me_gusta WHERE publicacion_id = p.id) as likes,
                       (SELECT COUNT(*) FROM comentarios WHERE publicacion_id = p.id AND activo = 1) as comentarios
                FROM publicaciones p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.activa = 1 AND u.activo = 1
                ORDER BY p.fecha_publicacion DESC
            """)
            
            posts = cursor.fetchall()
            
            for post in posts:
                self.create_post_card(scrollable_frame, tuple(post))
            
            conn.close()
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_post_card(self, parent, post_data):
        """Crear tarjeta moderna para publicación"""
        post_id, contenido, tipo, fecha, autor, likes, comentarios = post_data
        
        # Card frame
        card = tk.Frame(parent, bg='#2d2d44', relief='flat', bd=1)
        card.pack(fill='x', padx=20, pady=10)
        
        # Header del post
        header = tk.Frame(card, bg='#2d2d44')
        header.pack(fill='x', padx=20, pady=15)
        
        # Avatar simulado y autor
        avatar_label = tk.Label(header, text="👤", font=('Segoe UI', 16),
                              bg='#2d2d44', fg='#4ecdc4')
        avatar_label.pack(side='left')
        
        author_info = tk.Frame(header, bg='#2d2d44')
        author_info.pack(side='left', padx=10)
        
        tk.Label(author_info, text=autor, font=('Segoe UI', 12, 'bold'),
                bg='#2d2d44', fg='white').pack(anchor='w')
        tk.Label(author_info, text=f"{fecha.strftime('%d/%m/%Y %H:%M')} • {tipo.upper()}",
                bg='#2d2d44', fg='#a0a0a0', font=('Segoe UI', 9)).pack(anchor='w')
        
        # Contenido del post
        content_label = tk.Label(card, text=contenido, wraplength=800, justify='left',
                               font=('Segoe UI', 11), bg='#2d2d44', fg='white')
        content_label.pack(anchor='w', padx=20, pady=10)
        
        # Botones de interacción
        actions_frame = tk.Frame(card, bg='#2d2d44')
        actions_frame.pack(fill='x', padx=20, pady=15)
        
        # Botón Like
        like_btn = tk.Button(actions_frame, text=f"❤️ {likes}", 
                           command=lambda: self.like_post(post_id),
                           bg='#ff6b6b', fg='white', font=('Segoe UI', 10),
                           border=0, cursor='hand2', padx=15, pady=5)
        like_btn.pack(side='left', padx=(0, 10))
        
        # Botón Comentar
        comment_btn = tk.Button(actions_frame, text=f"💬 {comentarios}", 
                              command=lambda: self.comment_post(post_id),
                              bg='#45b7d1', fg='white', font=('Segoe UI', 10),
                              border=0, cursor='hand2', padx=15, pady=5, width=12, height=1)
        comment_btn.pack(side='left', padx=(0, 10))
        
        # Botón Ver Comentarios
        view_comments_btn = tk.Button(actions_frame, text="👁️ VER COMENTARIOS", 
                                    command=lambda: self.show_comments(post_id, autor, contenido),
                                    bg='#feca57', fg='white', font=('Segoe UI', 10),
                                    border=0, cursor='hand2', padx=15, pady=5, width=15, height=1)
        view_comments_btn.pack(side='left')
    
    def like_post(self, post_id):
        """Dar like a una publicación"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para dar like")
            return
        
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM me_gusta WHERE usuario_id = ? AND publicacion_id = ?", 
                              (self.current_user_id, post_id))
                
                if cursor.fetchone():
                    messagebox.showinfo("Info", "Ya diste like a esta publicación")
                else:
                    cursor.execute("INSERT INTO me_gusta (usuario_id, publicacion_id) VALUES (?, ?)", 
                                  (self.current_user_id, post_id))
                    conn.commit()
                    messagebox.showinfo("¡Genial!", "Like agregado ❤️")
                
                conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error al dar like:\n{str(e)}")
    
    def comment_post(self, post_id):
        """Comentar una publicación"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para comentar")
            return
        
        comment = simpledialog.askstring("💬 Nuevo Comentario", "Escribe tu comentario:")
        if comment:
            try:
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO comentarios (publicacion_id, usuario_id, contenido)
                        VALUES (?, ?, ?)
                    """, (post_id, self.current_user_id, comment))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("¡Éxito!", "Comentario agregado 💬")
            except Exception as e:
                messagebox.showerror("Error", f"Error al comentar:\n{str(e)}")
    
    def show_comments(self, post_id, autor, contenido):
        """Mostrar comentarios de una publicación"""
        comments_win = self.create_modern_window(f"💬 Comentarios - {autor}", "1000x700")
        
        # Frame principal
        main_frame = tk.Frame(comments_win, bg='#2d2d44')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header con información del post
        header_frame = tk.Frame(main_frame, bg='#2d2d44')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text=f"📝 Publicación de {autor}", 
                font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='#4ecdc4').pack(anchor='w')
        
        # Contenido del post
        content_frame = tk.Frame(header_frame, bg='#16213e', relief='flat', bd=1)
        content_frame.pack(fill='x', pady=10)
        
        content_label = tk.Label(content_frame, text=contenido, wraplength=800, justify='left',
                               font=('Segoe UI', 11), bg='#16213e', fg='white', padx=15, pady=10)
        content_label.pack(anchor='w')
        
        # Separador
        separator = tk.Frame(main_frame, height=2, bg='#4ecdc4')
        separator.pack(fill='x', pady=20)
        
        # Frame para comentarios
        comments_frame = tk.Frame(main_frame, bg='#2d2d44')
        comments_frame.pack(fill='both', expand=True)
        
        # Título de comentarios
        tk.Label(comments_frame, text="💬 Comentarios", 
                font=('Segoe UI', 12, 'bold'), bg='#2d2d44', fg='white').pack(anchor='w', pady=(0, 10))
        
        # Canvas con scroll para comentarios
        canvas = tk.Canvas(comments_frame, bg='#2d2d44', highlightthickness=0)
        scrollbar = ttk.Scrollbar(comments_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2d2d44')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cargar comentarios
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.contenido, c.fecha_comentario, CONCAT(u.nombre, ' ', u.apellido) as autor
                FROM comentarios c
                JOIN usuarios u ON c.usuario_id = u.id
                WHERE c.publicacion_id = ? AND c.activo = 1
                ORDER BY c.fecha_comentario ASC
            """, (post_id,))
            
            comments = cursor.fetchall()
            
            if comments:
                for comment in comments:
                    self.create_comment_card(scrollable_frame, comment)
            else:
                # Mensaje cuando no hay comentarios
                no_comments_frame = tk.Frame(scrollable_frame, bg='#16213e', relief='flat', bd=1)
                no_comments_frame.pack(fill='x', padx=10, pady=10)
                
                tk.Label(no_comments_frame, text="📝 No hay comentarios aún. ¡Sé el primero en comentar!", 
                        font=('Segoe UI', 11), bg='#16213e', fg='#a0a0a0', padx=15, pady=20).pack()
            
            conn.close()
        
        canvas.pack(side="left", fill='both', expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón para cerrar
        close_btn = tk.Button(main_frame, text="❌ CERRAR", command=comments_win.destroy,
                             bg='#ff6b6b', fg='white', font=('Segoe UI', 12, 'bold'),
                             border=0, cursor='hand2', pady=10, width=15, height=2)
        close_btn.pack(pady=20)
    
    def create_comment_card(self, parent, comment_data):
        """Crear tarjeta para un comentario"""
        contenido, fecha, autor = comment_data
        
        # Card frame
        card = tk.Frame(parent, bg='#16213e', relief='flat', bd=1)
        card.pack(fill='x', padx=10, pady=5)
        
        # Header del comentario
        header = tk.Frame(card, bg='#16213e')
        header.pack(fill='x', padx=15, pady=(10, 5))
        
        # Avatar y autor
        avatar_label = tk.Label(header, text="👤", font=('Segoe UI', 12),
                              bg='#16213e', fg='#4ecdc4')
        avatar_label.pack(side='left')
        
        author_info = tk.Frame(header, bg='#16213e')
        author_info.pack(side='left', padx=8)
        
        tk.Label(author_info, text=autor, font=('Segoe UI', 10, 'bold'),
                bg='#16213e', fg='white').pack(anchor='w')
        tk.Label(author_info, text=fecha.strftime('%d/%m/%Y %H:%M'),
                bg='#16213e', fg='#a0a0a0', font=('Segoe UI', 8)).pack(anchor='w')
        
        # Contenido del comentario
        content_label = tk.Label(card, text=contenido, wraplength=700, justify='left',
                               font=('Segoe UI', 10), bg='#16213e', fg='white')
        content_label.pack(anchor='w', padx=15, pady=(0, 10))
    
    def show_messages(self):
        """Mostrar mensajes con diseño moderno"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión")
            return
        
        msg_win = self.create_modern_window("💬 Mis Mensajes", "1000x700")
        
        # Panel principal con notebook
        notebook = ttk.Notebook(msg_win, style="Modern.TNotebook")
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tab 1: Bandeja de entrada
        inbox_frame = tk.Frame(notebook, bg='#1a1a2e')
        notebook.add(inbox_frame, text="📥 Bandeja de Entrada")
        
        # Header
        header_frame = tk.Frame(inbox_frame, bg='#2d2d44')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="💬 Bandeja de Mensajes", 
                font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='#4ecdc4').pack(pady=15)
        
        # Frame para botones de acción
        action_frame = tk.Frame(inbox_frame, bg='#1a1a2e')
        action_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        # Botón para enviar nuevo mensaje
        new_msg_btn = tk.Button(action_frame, text="✉️ NUEVO MENSAJE", 
                               command=self.show_new_message_dialog,
                               bg='#4ecdc4', fg='white', font=('Segoe UI', 10, 'bold'),
                               border=0, cursor='hand2', padx=20, pady=5)
        new_msg_btn.pack(side='left', padx=5)
        
        # Botón para insertar mensajes de prueba
        test_msg_btn = tk.Button(action_frame, text="🧪 MENSAJES PRUEBA", 
                                command=self.insert_test_messages,
                                bg='#feca57', fg='white', font=('Segoe UI', 10, 'bold'),
                                border=0, cursor='hand2', padx=20, pady=5)
        test_msg_btn.pack(side='left', padx=5)
        
        # Botón para actualizar mensajes
        refresh_btn = tk.Button(action_frame, text="🔄 ACTUALIZAR", 
                               command=lambda: self.refresh_messages(tree),
                               bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                               border=0, cursor='hand2', padx=20, pady=5, width=15, height=2)
        refresh_btn.pack(side='left', padx=5)
        
        # Tabla de mensajes
        tree = ttk.Treeview(inbox_frame, columns=('De', 'Para', 'Mensaje', 'Fecha', 'Estado'), 
                           show='headings', style="Modern.Treeview")
        
        columns_config = [
            ('De', 120),
            ('Para', 120),
            ('Mensaje', 300),
            ('Fecha', 120),
            ('Estado', 80)
        ]
        
        for col, width in columns_config:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Scrollbar
        scrollbar_msg = ttk.Scrollbar(inbox_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_msg.set)
        
        # Cargar mensajes
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                # Primero verificar si hay mensajes en la tabla
                cursor.execute("SELECT COUNT(*) FROM mensajes")
                total_result = cursor.fetchone()
                total_messages = total_result[0] if total_result else 0
                print(f"Total de mensajes en la BD: {total_messages}")
                
                # Verificar si hay mensajes para este usuario
                cursor.execute("""
                    SELECT COUNT(*) FROM mensajes 
                    WHERE emisor_id = ? OR receptor_id = ?
                """, (self.current_user_id, self.current_user_id))
                user_result = cursor.fetchone()
                user_messages = user_result[0] if user_result else 0
                print(f"Mensajes para usuario {self.current_user_id}: {user_messages}")
                
                # Consulta principal simplificada
                cursor.execute("""
                    SELECT 
                        u1.nombre + ' ' + u1.apellido as emisor,
                        u2.nombre + ' ' + u2.apellido as receptor,
                        m.contenido as mensaje,
                        m.fecha_envio,
                        '○ No leído' as estado
                    FROM mensajes m
                    JOIN usuarios u1 ON m.emisor_id = u1.id
                    JOIN usuarios u2 ON m.receptor_id = u2.id
                    WHERE m.emisor_id = ? OR m.receptor_id = ?
                    ORDER BY m.fecha_envio DESC
                """, (self.current_user_id, self.current_user_id))
                
                rows = cursor.fetchall()
                print(f"Encontrados {len(rows)} mensajes para usuario {self.current_user_id}")
                
                for i, row in enumerate(rows):
                    print(f"Mensaje {i+1}: {row}")
                    # Truncar mensaje si es muy largo
                    mensaje = row[2]
                    if len(mensaje) > 50:
                        mensaje = mensaje[:50] + "..."
                    
                    tree.insert('', 'end', values=(row[0], row[1], mensaje, row[3], row[4]))
                    
                if len(rows) == 0:
                    # Insertar mensaje informativo
                    tree.insert('', 'end', values=('Sistema', 'Tú', 'No hay mensajes aún. Usa el botón "🧪 MENSAJES PRUEBA"', 'N/A', 'N/A'))
                    
            except Exception as e:
                print(f"Error al cargar mensajes: {e}")
                import traceback
                traceback.print_exc()
                tree.insert('', 'end', values=('Error', 'Error', f'Error: {str(e)}', 'N/A', 'N/A'))
            finally:
                conn.close()
        
        tree.pack(side="left", fill='both', expand=True, padx=20, pady=10)
        scrollbar_msg.pack(side="right", fill="y", pady=10)
        
        # Tab 2: Conversaciones
        conversations_frame = tk.Frame(notebook, bg='#1a1a2e')
        notebook.add(conversations_frame, text="💬 Conversaciones")
        
        tk.Label(conversations_frame, text="Conversaciones con amigos", 
                font=('Segoe UI', 14, 'bold'), bg='#1a1a2e', fg='white').pack(pady=20)
        
        # Lista de conversaciones
        conv_tree = ttk.Treeview(conversations_frame, columns=('Amigo', 'Último Mensaje', 'Fecha'), 
                                show='headings', style="Modern.Treeview")
        
        for col in ['Amigo', 'Último Mensaje', 'Fecha']:
            conv_tree.heading(col, text=col)
            conv_tree.column(col, width=200)
        
        # Cargar conversaciones
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT
                    CASE 
                        WHEN m.emisor_id = ? THEN u2.nombre + ' ' + u2.apellido
                        ELSE u1.nombre + ' ' + u1.apellido
                    END as amigo,
                    LEFT(m.contenido, 40) + '...' as ultimo_mensaje,
                    m.fecha_envio
                FROM mensajes m
                JOIN usuarios u1 ON m.emisor_id = u1.id
                JOIN usuarios u2 ON m.receptor_id = u2.id
                WHERE m.emisor_id = ? OR m.receptor_id = ?
                AND m.fecha_envio = (
                    SELECT MAX(fecha_envio) 
                    FROM mensajes 
                    WHERE (emisor_id = ? AND receptor_id = m.receptor_id)
                       OR (emisor_id = m.emisor_id AND receptor_id = ?)
                )
                ORDER BY m.fecha_envio DESC
            """, (self.current_user_id, self.current_user_id, self.current_user_id, 
                  self.current_user_id, self.current_user_id))
            
            for row in cursor.fetchall():
                conv_tree.insert('', 'end', values=tuple(row))
            conn.close()
        
        conv_tree.pack(fill='both', expand=True, padx=20, pady=10)
    
    def show_new_message_dialog(self):
        """Mostrar diálogo para seleccionar destinatario y enviar mensaje"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión")
            return
        
        # Ventana para seleccionar destinatario
        select_win = self.create_modern_window("✉️ Nuevo Mensaje", "1200x800")
        
        main_frame = tk.Frame(select_win, bg='#2d2d44')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        tk.Label(main_frame, text="Selecciona un amigo para enviar mensaje:", 
                font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='white').pack(pady=20)
        
        # Lista de amigos
        friends_tree = ttk.Treeview(main_frame, columns=('ID', 'Nombre', 'Email'), 
                                   show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email']:
            friends_tree.heading(col, text=col)
            friends_tree.column(col, width=150)
        
        # Cargar amigos
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, CONCAT(u.nombre, ' ', u.apellido), u.email
                FROM amistades a
                JOIN usuarios u ON (
                    CASE 
                        WHEN a.usuario1_id = ? THEN a.usuario2_id 
                        ELSE a.usuario1_id 
                    END = u.id
                )
                WHERE (a.usuario1_id = ? OR a.usuario2_id = ?) 
                AND a.estado = 'aceptada'
            """, (self.current_user_id, self.current_user_id, self.current_user_id))
            
            for row in cursor.fetchall():
                friends_tree.insert('', 'end', values=tuple(row))
            conn.close()
        
        friends_tree.pack(fill='both', expand=True, pady=20)
        
        def send_to_selected():
            selected = friends_tree.selection()
            if not selected:
                messagebox.showwarning("Selección requerida", "Debes seleccionar un amigo")
                return
            
            user_id = friends_tree.item(selected[0])['values'][0]
            user_name = friends_tree.item(selected[0])['values'][1]
            
            select_win.destroy()
            self.send_message_window(user_id, user_name)
        
        # Botones
        buttons_frame = tk.Frame(main_frame, bg='#2d2d44')
        buttons_frame.pack(fill='x', pady=20)
        
        send_btn = tk.Button(buttons_frame, text="📤 ENVIAR MENSAJE", command=send_to_selected,
                            bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                            border=0, cursor='hand2', pady=12)
        send_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(buttons_frame, text="❌ CANCELAR", command=select_win.destroy,
                              bg='#ff6b6b', fg='white', font=('Segoe UI', 12, 'bold'),
                              border=0, cursor='hand2', pady=12)
        cancel_btn.pack(side='right', padx=5)
    
    def send_message_window(self, recipient_id, recipient_name):
        """Ventana para enviar mensaje a un amigo"""
        msg_win = self.create_modern_window(f"💬 Mensaje para {recipient_name}", "1200x800")
        
        main_frame = tk.Frame(msg_win, bg='#2d2d44')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Header
        tk.Label(main_frame, text=f"Enviando mensaje a:", 
                font=('Segoe UI', 12), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w')
        
        tk.Label(main_frame, text=f"👤 {recipient_name}", 
                font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='#4ecdc4').pack(anchor='w', pady=(0, 20))
        
        # Área de mensaje
        tk.Label(main_frame, text="Tu mensaje:", font=('Segoe UI', 12, 'bold'),
                bg='#2d2d44', fg='white').pack(anchor='w', pady=(0, 5))
        
        message_text = tk.Text(main_frame, height=10, font=('Segoe UI', 11),
                              bg='#16213e', fg='white', insertbackground='white',
                              border=0, relief='flat', wrap='word')
        message_text.pack(fill='both', expand=True, pady=5)
        
        # Contador de caracteres
        char_count_label = tk.Label(main_frame, text="0/500 caracteres", 
                                   font=('Segoe UI', 9), bg='#2d2d44', fg='#a0a0a0')
        char_count_label.pack(anchor='e', pady=5)
        
        def update_char_count(event=None):
            content = message_text.get(1.0, tk.END).strip()
            count = len(content)
            char_count_label.config(text=f"{count}/500 caracteres")
            if count > 500:
                char_count_label.config(fg='#ff6b6b')
            else:
                char_count_label.config(fg='#a0a0a0')
        
        message_text.bind('<KeyRelease>', update_char_count)
        
        def send_message():
            mensaje = message_text.get(1.0, tk.END).strip()
            
            if not mensaje:
                messagebox.showerror("Error", "El mensaje no puede estar vacío")
                return
            
            if len(mensaje) > 500:
                messagebox.showerror("Error", "El mensaje no puede exceder 500 caracteres")
                return
            
            try:
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO mensajes (emisor_id, receptor_id, contenido)
                        VALUES (?, ?, ?)
                    """, (self.current_user_id, recipient_id, mensaje))
                    conn.commit()
                    conn.close()
                    
                    messagebox.showinfo("¡Enviado!", f"Mensaje enviado a {recipient_name} 💬")
                    msg_win.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al enviar mensaje:\n{str(e)}")
        
        # Botones
        buttons_frame = tk.Frame(main_frame, bg='#2d2d44')
        buttons_frame.pack(fill='x', pady=20)
        
        send_btn = tk.Button(buttons_frame, text="📤 ENVIAR MENSAJE", command=send_message,
                            bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                            border=0, cursor='hand2', pady=12)
        send_btn.pack(side='right', padx=5)
        
        cancel_btn = tk.Button(buttons_frame, text="❌ CANCELAR", command=msg_win.destroy,
                              bg='#ff6b6b', fg='white', font=('Segoe UI', 12, 'bold'),
                              border=0, cursor='hand2', pady=12)
        cancel_btn.pack(side='right', padx=5)
        
        # Forzar actualización del layout
        msg_win.update_idletasks()
    
    def insert_test_messages(self):
        """Insertar mensajes de prueba para testing"""
        if not self.current_user_id:
            messagebox.showwarning("Error", "Debes estar logueado")
            return
            
        try:
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                
                print(f"Insertando mensajes de prueba para usuario {self.current_user_id}")
                
                # Obtener otros usuarios
                cursor.execute("SELECT id FROM usuarios WHERE id != ? AND activo = 1", (self.current_user_id,))
                other_users = cursor.fetchall()
                
                print(f"Encontrados {len(other_users)} otros usuarios")
                
                if other_users:
                    # Insertar mensajes de prueba
                    test_messages = [
                        "¡Hola! ¿Cómo estás?",
                        "Me gustó tu publicación",
                        "¿Quieres ser mi amigo?",
                        "Gracias por aceptar mi solicitud",
                        "¿Qué tal tu día?"
                    ]
                    
                    inserted_count = 0
                    for i, message in enumerate(test_messages):
                        recipient_id = other_users[i % len(other_users)][0]
                        print(f"Insertando mensaje '{message}' de {self.current_user_id} a {recipient_id}")
                        
                        cursor.execute("""
                            INSERT INTO mensajes (emisor_id, receptor_id, contenido)
                            VALUES (?, ?, ?)
                        """, (self.current_user_id, recipient_id, message))
                        inserted_count += 1
                    
                    conn.commit()
                    print(f"Se insertaron {inserted_count} mensajes exitosamente")
                    messagebox.showinfo("Éxito", f"Se insertaron {inserted_count} mensajes de prueba")
                else:
                    print("No hay otros usuarios para enviar mensajes de prueba")
                    messagebox.showinfo("Info", "No hay otros usuarios para enviar mensajes de prueba")
                
                conn.close()
        except Exception as e:
            print(f"Error al insertar mensajes de prueba: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al insertar mensajes de prueba:\n{str(e)}")
    
    def refresh_messages(self, tree):
        """Actualizar la lista de mensajes en el tree"""
        # Limpiar el tree
        for item in tree.get_children():
            tree.delete(item)
        
        # Recargar mensajes
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                print(f"Actualizando mensajes para usuario ID: {self.current_user_id}")
                
                # Verificar si hay mensajes para este usuario
                cursor.execute("""
                    SELECT COUNT(*) FROM mensajes 
                    WHERE emisor_id = ? OR receptor_id = ?
                """, (self.current_user_id, self.current_user_id))
                user_result = cursor.fetchone()
                user_messages = user_result[0] if user_result else 0
                print(f"Mensajes para usuario {self.current_user_id}: {user_messages}")
                
                # Consulta principal
                cursor.execute("""
                    SELECT 
                        u1.nombre + ' ' + u1.apellido as emisor,
                        u2.nombre + ' ' + u2.apellido as receptor,
                        m.contenido as mensaje,
                        m.fecha_envio,
                        '○ No leído' as estado
                    FROM mensajes m
                    JOIN usuarios u1 ON m.emisor_id = u1.id
                    JOIN usuarios u2 ON m.receptor_id = u2.id
                    WHERE m.emisor_id = ? OR m.receptor_id = ?
                    ORDER BY m.fecha_envio DESC
                """, (self.current_user_id, self.current_user_id))
                
                rows = cursor.fetchall()
                print(f"Encontrados {len(rows)} mensajes para usuario {self.current_user_id}")
                
                for i, row in enumerate(rows):
                    print(f"Mensaje {i+1}: {row}")
                    # Truncar mensaje si es muy largo
                    mensaje = row[2]
                    if len(mensaje) > 50:
                        mensaje = mensaje[:50] + "..."
                    
                    tree.insert('', 'end', values=(row[0], row[1], mensaje, row[3], row[4]))
                    
                if len(rows) == 0:
                    # Insertar mensaje informativo
                    tree.insert('', 'end', values=('Sistema', 'Tú', 'No hay mensajes aún. Usa el botón "🧪 MENSAJES PRUEBA"', 'N/A', 'N/A'))
                    
            except Exception as e:
                print(f"Error al actualizar mensajes: {e}")
                import traceback
                traceback.print_exc()
                tree.insert('', 'end', values=('Error', 'Error', f'Error: {str(e)}', 'N/A', 'N/A'))
            finally:
                conn.close()
    
    def show_database_viewer(self):
        """Visualizador moderno de base de datos"""
        db_win = self.create_modern_window("🗄️ Explorador de Base de Datos", "1000x700")
        
        # Panel principal
        main_panel = tk.Frame(db_win, bg='#1a1a2e')
        main_panel.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Panel de selección de tablas
        table_panel = tk.Frame(main_panel, bg='#2d2d44', width=200)
        table_panel.pack(side='left', fill='y', padx=(0, 10))
        table_panel.pack_propagate(False)
        
        tk.Label(table_panel, text="📊 TABLAS", font=('Segoe UI', 12, 'bold'),
                bg='#2d2d44', fg='#4ecdc4').pack(pady=15)
        
        # Lista de tablas
        tables = ['usuarios', 'publicaciones', 'me_gusta', 'comentarios', 'amistades', 'mensajes']
        
        # --- PANEL DE CONSULTAS PREDEFINIDAS ---
        queries_panel = tk.Frame(main_panel, bg='#2d2d44', width=500)
        queries_panel.pack(side='right', fill='y', padx=(10, 0))
        queries_panel.pack_propagate(False)
        
        tk.Label(queries_panel, text="📝 Consultas de ejemplo (haz clic y ejecuta)", font=('Segoe UI', 12, 'bold'),
                 bg='#2d2d44', fg='#feca57').pack(pady=(15, 5))
        
        # Consultas predefinidas
        predefined_queries = [
            "SELECT * FROM usuarios WHERE id = 19;",
            "SELECT u.* FROM usuarios u JOIN amistades a ON (u.id = a.usuario1_id OR u.id = a.usuario2_id) WHERE (a.usuario1_id = 1 OR a.usuario2_id = 1) AND a.estado = 'aceptada' AND u.id != 1;",
            "SELECT * FROM usuarios WHERE nombre LIKE '%Ma%' OR apellido LIKE '%Ma%';",
            "SELECT TOP 5 * FROM publicaciones WHERE activa = 1 ORDER BY fecha_publicacion DESC;",
            "SELECT publicacion_id, COUNT(*) AS total_likes FROM me_gusta WHERE publicacion_id = 1 GROUP BY publicacion_id;",
            "SELECT * FROM comentarios WHERE publicacion_id = 1 AND activo = 1;",
            "SELECT * FROM usuarios WHERE DATEDIFF(YEAR, fecha_nacimiento, GETDATE()) > 30;",
            "SELECT * FROM usuarios WHERE ubicacion = 'Barcelona';",
            "SELECT CAST(fecha_publicacion AS DATE) AS dia, COUNT(*) AS total FROM publicaciones GROUP BY CAST(fecha_publicacion AS DATE);",
            "SELECT COUNT(*) AS total_activos FROM usuarios WHERE activo = 1;"
        ]
        
        queries_listbox = tk.Listbox(queries_panel, bg='#16213e', fg='white', font=('Consolas', 9),
                                     width=70, height=18, border=0, highlightthickness=0, selectbackground='#4ecdc4')
        for i, q in enumerate(predefined_queries, 1):
            queries_listbox.insert(tk.END, f"{i}. {q}")
        queries_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Área para mostrar y editar la consulta seleccionada
        selected_query_text = tk.Text(queries_panel, height=4, font=('Consolas', 10), bg='#1a1a2e', fg='white',
                                      wrap='word', border=0)
        selected_query_text.pack(fill='x', padx=10, pady=(0, 10))
        selected_query_text.config(state='normal')  # Ahora editable
        
        def on_query_select(event=None):
            sel = queries_listbox.curselection()
            if sel:
                idx = sel[0]
                query = predefined_queries[idx]
                selected_query_text.delete(1.0, tk.END)
                selected_query_text.insert(tk.END, query)
        queries_listbox.bind('<<ListboxSelect>>', on_query_select)
        
        # Botón para ejecutar la consulta (toma el texto actual del widget)
        def execute_selected_query():
            query = selected_query_text.get(1.0, tk.END).strip()
            if not query:
                messagebox.showwarning("Consulta vacía", "Debes escribir o seleccionar una consulta para ejecutarla.")
                return
            # Ejecutar y mostrar resultado en el panel de datos
            for item in data_tree.get_children():
                data_tree.delete(item)
            conn = self.connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(query)
                    if cursor.description:
                        columns = [desc[0] for desc in cursor.description]
                        data_tree.configure(columns=columns)
                        data_tree.configure(show='headings')
                        for col in columns:
                            data_tree.heading(col, text=col)
                            data_tree.column(col, width=120)
                        rows = cursor.fetchall()
                        for row in rows:
                            data_tree.insert('', 'end', values=tuple(row))
                        info_label.config(text=f"Consulta ejecutada: {query[:60]}{'...' if len(query)>60 else ''} - {len(rows)} filas")
                    else:
                        info_label.config(text="Consulta ejecutada (sin resultados de tabla)")
                    conn.close()
                except Exception as e:
                    messagebox.showerror("Error SQL", f"Error al ejecutar la consulta:\n{str(e)}")
                    conn.close()
        execute_btn = tk.Button(queries_panel, text="▶️ EJECUTAR CONSULTA", command=execute_selected_query,
                               bg='#4ecdc4', fg='white', font=('Segoe UI', 11, 'bold'),
                               border=0, cursor='hand2', pady=10)
        execute_btn.pack(pady=(0, 15))
        
        # --- FIN PANEL CONSULTAS PREDEFINIDAS ---
        
        def show_table_data(table_name):
            # Limpiar datos anteriores
            for item in data_tree.get_children():
                data_tree.delete(item)
            # Configurar tabla
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                query1 = f"SELECT TOP 1 * FROM {table_name}"
                cursor.execute(query1)
                columns = [description[0] for description in cursor.description]
                self.add_query_history(query1)
                data_tree.configure(columns=columns)
                data_tree.configure(show='headings')
                for col in columns:
                    data_tree.heading(col, text=col)
                    data_tree.column(col, width=100)
                query2 = f"SELECT TOP 100 * FROM {table_name}"
                cursor.execute(query2)
                rows = cursor.fetchall()
                self.add_query_history(query2)
                for row in rows:
                    data_tree.insert('', 'end', values=tuple(row))
                conn.close()
                info_label.config(text=f"Tabla: {table_name.upper()} - {len(rows)} registros")
        # Botones para cada tabla
        for table in tables:
            btn = tk.Button(table_panel, text=f"📋 {table.upper()}", 
                          command=lambda t=table: show_table_data(t),
                          bg='#16213e', fg='white', font=('Segoe UI', 9),
                          border=0, cursor='hand2', pady=8)
            btn.pack(fill='x', padx=10, pady=2)
        # Panel de datos
        data_panel = tk.Frame(main_panel, bg='#1a1a2e')
        data_panel.pack(side='left', fill='both', expand=True)
        # Información
        info_frame = tk.Frame(data_panel, bg='#2d2d44')
        info_frame.pack(fill='x', pady=(0, 10))
        info_label = tk.Label(info_frame, text="Selecciona una tabla para ver los datos", 
                             font=('Segoe UI', 11), bg='#2d2d44', fg='white')
        info_label.pack(pady=10)
        # Treeview para datos
        data_tree = ttk.Treeview(data_panel, style="Modern.Treeview")
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_panel, orient="vertical", command=data_tree.yview)
        h_scrollbar = ttk.Scrollbar(data_panel, orient="horizontal", command=data_tree.xview)
        data_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        # Pack scrollbars y treeview
        data_tree.pack(side="left", fill='both', expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        # Mostrar primera tabla por defecto
        show_table_data('usuarios')
    
    def manage_friendships(self):
        """Gestión moderna de amistades"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión")
            return
        
        friends_win = self.create_modern_window("🤝 Gestión de Amistades", "800x600")
        
        # Notebook moderno
        notebook = ttk.Notebook(friends_win, style="Modern.TNotebook")
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tab 1: Mis amigos
        friends_frame = tk.Frame(notebook, bg='#1a1a2e')
        notebook.add(friends_frame, text="👥 Mis Amigos")
        
        tk.Label(friends_frame, text="Tus conexiones", font=('Segoe UI', 12, 'bold'),
                bg='#1a1a2e', fg='white').pack(pady=10)
        
        friends_tree = ttk.Treeview(friends_frame, columns=('ID', 'Nombre', 'Email', 'Estado'), 
                                   show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email', 'Estado']:
            friends_tree.heading(col, text=col)
            friends_tree.column(col, width=150)
        
        def load_friends():
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.id, CONCAT(u.nombre, ' ', u.apellido), u.email, a.estado
                    FROM amistades a
                    JOIN usuarios u ON (
                        CASE 
                            WHEN a.usuario1_id = ? THEN a.usuario2_id 
                            ELSE a.usuario1_id 
                        END = u.id
                    )
                    WHERE (a.usuario1_id = ? OR a.usuario2_id = ?) 
                    AND a.estado = 'aceptada'
                """, (self.current_user_id, self.current_user_id, self.current_user_id))
                
                for item in friends_tree.get_children():
                    friends_tree.delete(item)
                
                for row in cursor.fetchall():
                    friends_tree.insert('', 'end', values=tuple(row))
                conn.close()
        
        def send_message_to_friend():
            selected = friends_tree.selection()
            if selected:
                friend_id = friends_tree.item(selected[0])['values'][0]
                friend_name = friends_tree.item(selected[0])['values'][1]
                self.send_message_window(friend_id, friend_name)
        
        # Botones para amigos
        friends_buttons_frame = tk.Frame(friends_frame, bg='#1a1a2e')
        friends_buttons_frame.pack(fill='x', padx=20, pady=10)
        
        message_btn = tk.Button(friends_buttons_frame, text="💬 ENVIAR MENSAJE", command=send_message_to_friend,
                               bg='#ff9ff3', fg='white', font=('Segoe UI', 10, 'bold'),
                               border=0, cursor='hand2', padx=20)
        message_btn.pack(side='left', padx=5)
        
        refresh_friends_btn = tk.Button(friends_buttons_frame, text="🔄 ACTUALIZAR", command=load_friends,
                                       bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                                       border=0, cursor='hand2', padx=20, pady=5, width=15, height=2)
        refresh_friends_btn.pack(side='left', padx=5)
        
        friends_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cargar amigos al abrir
        load_friends()
        
        # Tab 2: Buscar usuarios
        search_frame = tk.Frame(notebook, bg='#1a1a2e')
        notebook.add(search_frame, text="🔍 Buscar")
        
        # Tab 3: Solicitudes pendientes
        requests_frame = tk.Frame(notebook, bg='#1a1a2e')
        notebook.add(requests_frame, text="📩 Solicitudes")
        
        tk.Label(requests_frame, text="Solicitudes de amistad pendientes", 
                 font=('Segoe UI', 12, 'bold'), bg='#1a1a2e', fg='white').pack(pady=10)
        
        requests_tree = ttk.Treeview(requests_frame, columns=('ID', 'Nombre', 'Email', 'Fecha'), 
                                    show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email', 'Fecha']:
            requests_tree.heading(col, text=col)
            requests_tree.column(col, width=150)
        
        def load_pending_requests():
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.id, CONCAT(u.nombre, ' ', u.apellido), u.email, a.fecha_solicitud
                    FROM amistades a
                    JOIN usuarios u ON a.usuario1_id = u.id
                    WHERE a.usuario2_id = ? AND a.estado = 'pendiente'
                """, (self.current_user_id,))
                
                for item in requests_tree.get_children():
                    requests_tree.delete(item)
                
                for row in cursor.fetchall():
                    requests_tree.insert('', 'end', values=tuple(row))
                conn.close()
        
        def accept_request():
            selected = requests_tree.selection()
            if selected:
                user_id = requests_tree.item(selected[0])['values'][0]
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE amistades SET estado = 'aceptada' 
                        WHERE usuario1_id = ? AND usuario2_id = ?
                    """, (user_id, self.current_user_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("¡Genial!", "Solicitud de amistad aceptada ✅")
                    load_pending_requests()
        
        def reject_request():
            selected = requests_tree.selection()
            if selected:
                user_id = requests_tree.item(selected[0])['values'][0]
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE amistades SET estado = 'rechazada' 
                        WHERE usuario1_id = ? AND usuario2_id = ?
                    """, (user_id, self.current_user_id))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Rechazada", "Solicitud rechazada ❌")
                    load_pending_requests()
        
        # Botones para manejar solicitudes
        req_buttons_frame = tk.Frame(requests_frame, bg='#1a1a2e')
        req_buttons_frame.pack(fill='x', padx=20, pady=10)
        
        accept_btn = tk.Button(req_buttons_frame, text="✅ ACEPTAR", command=accept_request,
                  bg='#4ecdc4', fg='white', font=('Segoe UI', 10, 'bold'),
                  border=0, cursor='hand2', padx=20)
        accept_btn.pack(side='left', padx=5)
        
        reject_btn = tk.Button(req_buttons_frame, text="❌ RECHAZAR", command=reject_request,
                  bg='#ff6b6b', fg='white', font=('Segoe UI', 10, 'bold'),
                  border=0, cursor='hand2', padx=20)
        reject_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(req_buttons_frame, text="🔄 ACTUALIZAR", command=load_pending_requests,
                   bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                   border=0, cursor='hand2', padx=20, pady=5, width=15, height=2)
        refresh_btn.pack(side='left', padx=5)
        
        requests_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cargar solicitudes al abrir
        load_pending_requests()
        
        # Barra de búsqueda moderna
        search_header = tk.Frame(search_frame, bg='#2d2d44')
        search_header.pack(fill='x', padx=20, pady=20)
        
        tk.Label(search_header, text="🔍 Buscar nuevos amigos", 
                font=('Segoe UI', 12, 'bold'), bg='#2d2d44', fg='white').pack(pady=10)
        
        search_entry = tk.Entry(search_header, font=('Segoe UI', 11), bg='#16213e', fg='white',
                              insertbackground='white', border=0, relief='flat')
        search_entry.pack(fill='x', ipady=8, pady=5)
        
        # Resultados de búsqueda
        search_tree = ttk.Treeview(search_frame, columns=('ID', 'Nombre', 'Email'), 
                                  show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email']:
            search_tree.heading(col, text=col)
            search_tree.column(col, width=150)
        
        def search_users():
            search_term = search_entry.get()
            if search_term:
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT id, CONCAT(nombre, ' ', apellido), email 
                        FROM usuarios 
                        WHERE (nombre LIKE ? OR apellido LIKE ?) AND id != ? AND activo = 1
                    """, (f'%{search_term}%', f'%{search_term}%', self.current_user_id))
                    
                    for item in search_tree.get_children():
                        search_tree.delete(item)
                    
                    for row in cursor.fetchall():
                        search_tree.insert('', 'end', values=tuple(row))
                    conn.close()
        
        def send_friend_request():
            selected = search_tree.selection()
            if selected:
                user_id = search_tree.item(selected[0])['values'][0]
                user_name = search_tree.item(selected[0])['values'][1]
                
                # Verificar si ya existe una solicitud
                conn = self.connect_db()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT estado FROM amistades 
                        WHERE (usuario1_id = ? AND usuario2_id = ?) 
                           OR (usuario1_id = ? AND usuario2_id = ?)
                    """, (self.current_user_id, user_id, user_id, self.current_user_id))
                    
                    existing = cursor.fetchone()
                    
                    if existing:
                        if existing[0] == 'aceptada':
                            messagebox.showinfo("Info", "Ya son amigos")
                        elif existing[0] == 'pendiente':
                            messagebox.showinfo("Info", "Ya existe una solicitud pendiente")
                        else:
                            messagebox.showinfo("Info", "Solicitud rechazada anteriormente")
                    else:
                        try:
                            cursor.execute("""
                                INSERT INTO amistades (usuario1_id, usuario2_id, estado)
                                VALUES (?, ?, 'pendiente')
                            """, (self.current_user_id, user_id))
                            conn.commit()
                            messagebox.showinfo("¡Enviado!", f"Solicitud de amistad enviada a {user_name} 🤝")
                        except Exception as e:
                            messagebox.showerror("Error", f"Error al enviar solicitud:\n{str(e)}")
                    conn.close()
        
        # Botones
        buttons_frame = tk.Frame(search_frame, bg='#1a1a2e')
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        search_btn = tk.Button(buttons_frame, text="🔍 BUSCAR", command=search_users,
                             bg='#4ecdc4', fg='white', font=('Segoe UI', 10, 'bold'),
                             border=0, cursor='hand2', padx=20)
        search_btn.pack(side='left', padx=5)
        
        request_btn = tk.Button(buttons_frame, text="➕ ENVIAR SOLICITUD", command=send_friend_request,
                              bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                              border=0, cursor='hand2', padx=20, pady=5, width=18, height=2)
        request_btn.pack(side='left', padx=5)
        
        search_tree.pack(fill='both', expand=True, padx=20, pady=10)
    
    def add_query_history(self, query):
        """Agrega una consulta al historial, máximo 10"""
        self.query_history.append(query)
        if len(self.query_history) > 10:
            self.query_history = self.query_history[-10:]
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# Punto de entrada
if __name__ == "__main__":
    """
    🚀 SOCIAL HUB - Red Social Moderna
    
    📋 REQUISITOS:
    1. pip install pyodbc
    2. ODBC Driver 17 for SQL Server
    3. SQL Server con base de datos 'red_social'
    
    🎨 CARACTERÍSTICAS:
    - Diseño moderno con gradientes
    - Ventanas que se auto-cierran
    - Botón volver en cada ventana
    - Visualizador de BD integrado
    - Interfaz responsiva y elegante
    
    ⚙️ CONFIGURACIÓN:
    Modifica la connection_string si es necesario
    """
    
    app = ModernRedSocialApp()
    app.run()