import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
        
        # Subtítulo
        subtitle_label = tk.Label(header_frame, text="Red social", 
                                 font=('Segoe UI', 12), 
                                 bg='#16213e', fg='#a0a0a0')
        subtitle_label.pack()
        
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
        login_btn = tk.Button(auth_frame, text="🔑 INICIAR SESIÓN", 
                            command=self.login_window,
                            bg='#4ecdc4', fg='white', 
                            font=('Segoe UI', 11, 'bold'),
                            border=0, cursor='hand2', 
                            activebackground='#45b7aa',
                            activeforeground='white',
                            padx=20, pady=10,
                            relief='flat')
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = tk.Button(auth_frame, text="📝 REGISTRARSE", 
                               command=self.register_window,
                               bg='#45b7d1', fg='white', 
                               font=('Segoe UI', 11, 'bold'),
                               border=0, cursor='hand2',
                               activebackground='#357abd',
                               activeforeground='white',
                               padx=20, pady=10,
                               relief='flat')
        register_btn.pack(side=tk.LEFT, padx=5)
        
        # Efectos hover para botones de autenticación
        def create_hover_effect(button, normal_color, hover_color):
            def on_enter(e):
                button.config(bg=hover_color)
            def on_leave(e):
                button.config(bg=normal_color)
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
        
        create_hover_effect(login_btn, '#4ecdc4', '#45b7aa')
        create_hover_effect(register_btn, '#45b7d1', '#357abd')
        
        # Separador
        separator = tk.Frame(self.root, bg='#16213e', height=2)
        separator.pack(fill='x', pady=20)
        
        # Grid de botones principales
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        # Configurar grid
        for i in range(3):
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            main_frame.grid_rowconfigure(i, weight=1)
        
        # Botones principales con iconos y colores modernos
        buttons_config = [
            ("👥 USUARIOS", self.show_users, '#ff6b6b', '#e55656'),
            ("📝 PUBLICACIONES", self.show_posts, '#4ecdc4', '#45b7aa'),
            ("✍️ CREAR POST", self.create_post_window, '#45b7d1', '#357abd'),
            ("📱 MI FEED", self.show_feed, '#96ceb4', '#7eb89b'),
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
    
    def create_modern_window(self, title, size="800x600", bg_color="#1a1a2e"):
        """Crear ventana moderna estándar"""
        self.close_all_windows()  # Cerrar ventanas anteriores
        
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(size)
        window.configure(bg=bg_color)
        window.transient(self.root)
        window.grab_set()
        
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
        login_win = self.create_modern_window("🔑 Iniciar Sesión", "500x400")
        
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
            
            entry = tk.Entry(frame, font=('Segoe UI', 12), bg='#16213e', fg='white',
                           insertbackground='white', border=0, relief='flat', show=show)
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
    
    def register_window(self):
        """Ventana de registro moderna"""
        reg_win = self.create_modern_window("📝 Crear Cuenta", "600x700")
        
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
        
        tk.Label(main_frame, text="Únete a Social Hub", 
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
                entry = tk.Entry(frame, font=('Segoe UI', 12), bg='#16213e', fg='white',
                               insertbackground='white', border=0, relief='flat', show=show)
            entry.pack(fill='x', ipady=8 if not is_text_area else 0)
            
            return entry
        
        # Campos del formulario
        entries = {}
        fields = [
            ("Nombre *", "nombre"),
            ("Apellido *", "apellido"),
            ("Email *", "email"),
            ("Contraseña *", "password"),
            ("Fecha Nacimiento (YYYY-MM-DD)", "fecha_nacimiento"),
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
        
        def do_register():
            try:
                values = {}
                for key, entry in entries.items():
                    if key == "biografia":
                        values[key] = entry.get(1.0, tk.END).strip()
                    else:
                        values[key] = entry.get().strip()
                
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
                        values['password'], values.get('fecha_nacimiento') or None,
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
                               border=0, cursor='hand2', pady=12)
        register_btn.pack(fill='x', pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_users(self):
        """Mostrar usuarios con diseño moderno"""
        users_win = self.create_modern_window("👥 Usuarios Registrados", "900x600")
        
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
                tree.insert('', 'end', values=row)
            conn.close()
        
        tree.pack(side="left", fill='both', expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_post_window(self):
        """Ventana moderna para crear publicaciones"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión para crear publicaciones")
            return
        
        post_win = self.create_modern_window("✍️ Nueva Publicación", "600x500")
        
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
                self.create_post_card(scrollable_frame, post)
            
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
                              border=0, cursor='hand2', padx=15, pady=5)
        comment_btn.pack(side='left')
    
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
    
    def show_feed(self):
        """Mostrar feed personal"""
        feed_win = self.create_modern_window("📱 Mi Feed Personal", "900x600")
        
        main_frame = tk.Frame(feed_win, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Información del feed
        info_frame = tk.Frame(main_frame, bg='#2d2d44')
        info_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(info_frame, text="📱 Tu Feed Personalizado", 
                font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='#4ecdc4').pack(pady=15)
        
        # Tabla moderna
        tree = ttk.Treeview(main_frame, columns=('Autor', 'Contenido', 'Tipo', 'Fecha', 'Likes', 'Comentarios'), 
                           show='headings', style="Modern.Treeview")
        
        columns_config = [
            ('Autor', 150),
            ('Contenido', 300),
            ('Tipo', 80),
            ('Fecha', 120),
            ('Likes', 60),
            ('Comentarios', 80)
        ]
        
        for col, width in columns_config:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Scrollbar
        scrollbar_feed = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_feed.set)
        
        # Cargar datos del feed
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT autor, LEFT(contenido, 50) + '...', tipo, 
                       fecha_publicacion, total_likes, total_comentarios 
                FROM vista_feed_noticias 
                ORDER BY fecha_publicacion DESC
            """)
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=row)
            conn.close()
        
        tree.pack(side="left", fill='both', expand=True)
        scrollbar_feed.pack(side="right", fill="y")
    
    def manage_friendships(self):
        """Gestión moderna de amistades"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión")
            return
        
        friends_win = self.create_modern_window("🤝 Gestión de Amistades", "800x600")
        
        # Notebook moderno
        notebook = ttk.Notebook(friends_win, style="Modern.TNotebook")
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tab 1: Mis amigos (versión actualizada)
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
            friends_tree.insert('', 'end', values=row)
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
                               border=0, cursor='hand2', padx=20)
refresh_friends_btn.pack(side='left', padx=5)

friends_tree.pack(fill='both', expand=True, padx=20, pady=10)

# Cargar amigos al abrir
load_friends()
        # # Tab 1: Mis amigos
        # friends_frame = tk.Frame(notebook, bg='#1a1a2e')
        # notebook.add(friends_frame, text="👥 Mis Amigos")
        
        # tk.Label(friends_frame, text="Tus conexiones", font=('Segoe UI', 12, 'bold'),
        #         bg='#1a1a2e', fg='white').pack(pady=10)
        
        # friends_tree = ttk.Treeview(friends_frame, columns=('Nombre', 'Email', 'Estado'), 
        #                            show='headings', style="Modern.Treeview")
        
        # for col in ['Nombre', 'Email', 'Estado']:
        #     friends_tree.heading(col, text=col)
        #     friends_tree.column(col, width=200)
        
        # friends_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
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
            requests_tree.insert('', 'end', values=row)
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
                       border=0, cursor='hand2', padx=20)
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
                        search_tree.insert('', 'end', values=row)
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
                              border=0, cursor='hand2', padx=20)
        request_btn.pack(side='left', padx=5)
        
        search_tree.pack(fill='both', expand=True, padx=20, pady=10)
    
    def show_messages(self):
        """Mostrar mensajes con diseño moderno"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso Denegado", "Debes iniciar sesión")
            return
        
        msg_win = self.create_modern_window("💬 Mis Mensajes", "800x600")
        
        main_frame = tk.Frame(msg_win, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2d2d44')
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text="💬 Bandeja de Mensajes", 
                font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='#4ecdc4').pack(pady=15)
        
        # Tabla de mensajes
        tree = ttk.Treeview(main_frame, columns=('De', 'Para', 'Mensaje', 'Fecha', 'Estado'), 
                           show='headings', style="Modern.Treeview")
        
        columns_config = [
            ('De', 120),
            ('Para', 120),
            ('Mensaje', 250),
            ('Fecha', 120),
            ('Estado', 80)
        ]
        
        for col, width in columns_config:
            tree.heading(col, text=col)
            tree.column(col, width=width)
        
        # Scrollbar
        scrollbar_msg = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar_msg.set)
        
        # Cargar mensajes
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    u1.nombre + ' ' + u1.apellido as emisor,
                    u2.nombre + ' ' + u2.apellido as receptor,
                    LEFT(m.contenido, 40) + '...' as mensaje,
                    m.fecha_envio,
                    CASE WHEN m.leido = 1 THEN '✓ Leído' ELSE '○ No leído' END as estado
                FROM mensajes m
                JOIN usuarios u1 ON m.emisor_id = u1.id
                JOIN usuarios u2 ON m.receptor_id = u2.id
                WHERE m.emisor_id = ? OR m.receptor_id = ?
                ORDER BY m.fecha_envio DESC
            """, (self.current_user_id, self.current_user_id))
            
            for row in cursor.fetchall():
                tree.insert('', 'end', values=row)
            conn.close()
        
        tree.pack(side="left", fill='both', expand=True)
        scrollbar_msg.pack(side="right", fill="y")
    def send_message_window(self, recipient_id, recipient_name):
    """Ventana para enviar mensaje a un amigo"""
    msg_win = self.create_modern_window(f"💬 Mensaje para {recipient_name}", "600x500")
    
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
        
        def show_table_data(table_name):
            # Limpiar datos anteriores
            for item in data_tree.get_children():
                data_tree.delete(item)
            
            # Configurar tabla
            conn = self.connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Obtener estructura de la tabla
                cursor.execute(f"SELECT TOP 1 * FROM {table_name}")
                columns = [description[0] for description in cursor.description]
                
                # Configurar columnas del treeview
                data_tree.configure(columns=columns)
                data_tree.configure(show='headings')
                
                for col in columns:
                    data_tree.heading(col, text=col)
                    data_tree.column(col, width=100)
                
                # Obtener datos
                cursor.execute(f"SELECT TOP 100 * FROM {table_name}")
                rows = cursor.fetchall()
                
                for row in rows:
                    data_tree.insert('', 'end', values=row)
                
                conn.close()
                
                # Actualizar etiqueta de información
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
        data_panel.pack(side='right', fill='both', expand=True)
        
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