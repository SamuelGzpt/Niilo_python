import tkinter as tk
from tkinter import ttk, messagebox
from modules.database import DatabaseManager
from modules.ui_components import UIComponents
from modules.windows import Windows

class ModernRedSocialApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NIILO")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a2e')
        self.root.resizable(True, True)
        
        # Inicializar módulos
        self.db = DatabaseManager()
        self.windows = Windows(self)
        
        self.current_user_id = None
        self.open_windows = []  # Track open windows
        self.query_history = []  # Historial de consultas SQL (solo BD)
        
        # Configurar estilos
        UIComponents.setup_styles()
        self.setup_main_interface()
        
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
        
        # BOTONES DE AUTENTICACIÓN
        auth_frame = tk.Frame(user_panel, bg='#2d2d44')
        auth_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Crear botones con dimensiones específicas y empaquetado correcto
        self.login_btn = tk.Button(auth_frame, text="🔑 INICIAR SESIÓN", 
                            command=self.windows.login_window,
                            bg='#4ecdc4', fg='white', 
                            font=('Segoe UI', 11, 'bold'),
                            border=0, cursor='hand2', 
                            activebackground='#45b7aa',
                            activeforeground='white',
                            padx=20, pady=10,
                            relief='flat')
        self.login_btn.pack(side=tk.LEFT, padx=5)
        
        self.register_btn = tk.Button(auth_frame, text="📝 REGISTRARSE", 
                               command=self.windows.register_window,
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
        for i in range(3):  # 3 filas para acomodar 7 botones
            main_frame.grid_rowconfigure(i, weight=1, minsize=150)
        
        # Botones principales con iconos y colores modernos (incluyendo perfil)
        buttons_config = [
            ("👥 USUARIOS", self.show_users, '#ff6b6b', '#e55656'),
            ("📝 PUBLICACIONES", self.show_posts, '#4ecdc4', '#45b7aa'),
            ("✍️ CREAR POST", self.create_post_window, '#45b7d1', '#357abd'),
            ("🤝 AMISTADES", self.manage_friendships, '#feca57', '#e5b343'),
            ("💬 MENSAJES", self.show_messages, '#ff9ff3', '#e58ce5'),
            ("🗄️ BASE DATOS", self.show_database_viewer, '#6c5ce7', '#5848c4'),
            ("👤 MI PERFIL", self.windows.profile_window, '#a55eea', '#8b5cf6'),
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
    
    def show_users(self):
        """Mostrar ventana de usuarios"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso denegado", "Debes iniciar sesión para ver usuarios")
            return
        
        users_win = UIComponents.create_modern_window(self.root, "👥 Usuarios", "800x600")
        
        # Frame principal
        main_frame = tk.Frame(users_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Usuarios registrados", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=(0, 20))
        
        # Treeview para usuarios
        users_tree = ttk.Treeview(main_frame, 
                                 columns=('ID', 'Nombre', 'Email'),
                                 show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email']:
            users_tree.heading(col, text=col)
            users_tree.column(col, width=150)
        
        # Cargar usuarios
        users = self.db.get_all_users()
        if users:
            for user in users:
                if user[0] != self.current_user_id:  # No mostrar al usuario actual
                    users_tree.insert('', 'end', values=tuple(user))
        
        users_tree.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Botones de acción
        buttons_frame = tk.Frame(main_frame, bg='#1a1a2e')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        send_msg_btn = tk.Button(buttons_frame, text="💬 ENVIAR MENSAJE", 
                                command=lambda: self.send_message_to_selected_user(users_tree),
                                bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                                border=0, cursor='hand2', padx=20, pady=10)
        send_msg_btn.pack(side='left', padx=10)
        
        friend_btn = tk.Button(buttons_frame, text="🤝 SOLICITUD AMISTAD", 
                              command=lambda: self.send_friend_request_to_selected_user(users_tree),
                              bg='#45b7d1', fg='white', font=('Segoe UI', 12, 'bold'),
                              border=0, cursor='hand2', padx=20, pady=10)
        friend_btn.pack(side='left', padx=10)
    
    def send_message_to_selected_user(self, tree):
        """Enviar mensaje al usuario seleccionado"""
        selected = tree.selection()
        if selected:
            user_id = tree.item(selected[0])['values'][0]
            user_name = tree.item(selected[0])['values'][1]
            self.send_message_window(user_id, user_name)
        else:
            messagebox.showwarning("Selección requerida", "Debes seleccionar un usuario")
    
    def send_friend_request_to_selected_user(self, tree):
        """Enviar solicitud de amistad al usuario seleccionado"""
        selected = tree.selection()
        if selected:
            user_id = tree.item(selected[0])['values'][0]
            user_name = tree.item(selected[0])['values'][1]
            
            # Verificar si ya existe una solicitud
            existing, _ = self.db.execute_query("""
                SELECT estado FROM amistades 
                WHERE (usuario1_id = ? AND usuario2_id = ?) 
                   OR (usuario1_id = ? AND usuario2_id = ?)
            """, (self.current_user_id, user_id, user_id, self.current_user_id))
            
            if existing:
                if existing[0][0] == 'aceptada':
                    messagebox.showinfo("Info", "Ya son amigos")
                elif existing[0][0] == 'pendiente':
                    messagebox.showinfo("Info", "Ya existe una solicitud pendiente")
                else:
                    messagebox.showinfo("Info", "Solicitud rechazada anteriormente")
            else:
                if self.db.send_friend_request(self.current_user_id, user_id):
                    messagebox.showinfo("¡Enviado!", f"Solicitud de amistad enviada a {user_name} 🤝")
                else:
                    messagebox.showerror("Error", "No se pudo enviar la solicitud")
        else:
            messagebox.showwarning("Selección requerida", "Debes seleccionar un usuario")
    
    def send_message_window(self, recipient_id, recipient_name):
        """Ventana para enviar mensaje"""
        msg_win = UIComponents.create_modern_window(self.root, f"💬 Mensaje a {recipient_name}", "600x400")
        
        # Frame principal
        main_frame = tk.Frame(msg_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text=f"Enviar mensaje a {recipient_name}", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=(0, 20))
        
        # Campo de mensaje
        message_entry = tk.Text(main_frame, height=5, bg='#16213e', fg='white', 
                                insertbackground='white', border=0, relief='flat',
                                font=('Segoe UI', 10))
        message_entry.pack(fill='x', pady=10)
        
        def send_message():
            contenido = message_entry.get("1.0", tk.END).strip()
            if contenido:
                if self.db.send_message(self.current_user_id, recipient_id, contenido):
                    messagebox.showinfo("¡Enviado!", "Mensaje enviado correctamente")
                    msg_win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo enviar el mensaje")
            else:
                messagebox.showwarning("Campo vacío", "Debes escribir un mensaje")
        
        # Botón enviar
        send_btn = tk.Button(main_frame, text="📤 ENVIAR", command=send_message,
                           bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                           border=0, cursor='hand2', padx=30, pady=10)
        send_btn.pack(pady=20)
    
    def create_post_window(self):
        """Ventana para crear publicación"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso denegado", "Debes iniciar sesión para crear publicaciones")
            return
        
        post_win = UIComponents.create_modern_window(self.root, "✍️ Crear Publicación", "700x500")
        
        # Frame principal
        main_frame = tk.Frame(post_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Crear nueva publicación", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=(0, 20))
        
        # Campo de contenido
        content_entry = tk.Text(main_frame, height=8, bg='#16213e', fg='white',
                                insertbackground='white', border=0, relief='flat',
                                font=('Segoe UI', 10))
        content_entry.pack(fill='x', pady=10)
        
        def publish_post():
            contenido = content_entry.get("1.0", tk.END).strip()
            if contenido:
                if self.db.create_post(self.current_user_id, contenido):
                    messagebox.showinfo("¡Publicado!", "Publicación creada exitosamente")
                    post_win.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo crear la publicación")
            else:
                messagebox.showwarning("Campo vacío", "Debes escribir algo para publicar")
        
        # Botón publicar
        publish_btn = tk.Button(main_frame, text="📝 PUBLICAR", command=publish_post,
                              bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                              border=0, cursor='hand2', padx=30, pady=10)
        publish_btn.pack(pady=20)
    
    def show_posts(self):
        """Mostrar ventana de publicaciones"""
        print("Iniciando show_posts...")
        
        # Debugging del estado de la base de datos
        self.db.debug_database_state()
        
        posts_win = UIComponents.create_modern_window(self.root, "📝 Publicaciones", "900x700")
        
        # Frame principal con scroll
        canvas = tk.Canvas(posts_win, bg='#1a1a2e')
        scrollbar = ttk.Scrollbar(posts_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1a1a2e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title_label = tk.Label(scrollable_frame, text="Publicaciones recientes", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=20)
        
        # Cargar publicaciones
        print("Llamando a get_all_posts...")
        posts = self.db.get_all_posts()
        print(f"Posts obtenidos: {posts}")
        if posts:
            print(f"Procesando {len(posts)} publicaciones...")
            for i, post in enumerate(posts):
                print(f"Procesando post {i+1}: {post}")
                card = UIComponents.create_post_card(scrollable_frame, post)
                
                # Agregar botones de interacción si el usuario está conectado
                if self.current_user_id:
                    interaction_frame = tk.Frame(card, bg='#2d2d44')
                    interaction_frame.pack(fill='x', padx=15, pady=(0, 10))
                    
                    like_btn = tk.Button(interaction_frame, text=f"❤️ {post[7]}", 
                                       command=lambda p=post[0], w=posts_win: self.like_post_and_refresh(p, w),
                                       bg='#ff6b6b', fg='white', font=('Segoe UI', 10),
                                       border=0, cursor='hand2', padx=15, pady=5)
                    like_btn.pack(side='left', padx=5)
                    
                    comment_btn = tk.Button(interaction_frame, text=f"💬 {post[8]}", 
                                          command=lambda p=post[0], a=post[1], c=post[3]: self.show_post_comments_window(p, a, c),
                                          bg='#45b7d1', fg='white', font=('Segoe UI', 10),
                                          border=0, cursor='hand2', padx=15, pady=5)
                    comment_btn.pack(side='left', padx=5)

                    view_comments_btn = tk.Button(interaction_frame, text="VER COMENTARIOS",
                                                command=lambda p=post[0], a=post[1], c=post[3]: self.show_post_comments_window(p, a, c),
                                                bg='#feca57', fg='white', font=('Segoe UI', 10),
                                                border=0, cursor='hand2', padx=15, pady=5)
                    view_comments_btn.pack(side='left', padx=5)
        else:
            print("No se encontraron publicaciones")
            no_posts_label = tk.Label(scrollable_frame, text="No hay publicaciones disponibles", 
                                     font=('Segoe UI', 14), 
                                     bg='#1a1a2e', fg='#a0a0a0')
            no_posts_label.pack(pady=50)
        
        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def like_post_and_refresh(self, post_id, window):
        """Da like a un post y refresca la ventana de posts"""
        if self.db.like_post(self.current_user_id, post_id):
            messagebox.showinfo("¡Me gusta!", "Te gustó esta publicación ❤️")
            window.destroy()
            self.show_posts()
        else:
            messagebox.showerror("Error", "No se pudo dar like a la publicación o ya le diste like.")
    
    def show_post_comments_window(self, post_id, autor, contenido):
        """Muestra los comentarios de una publicación y permite añadir uno nuevo"""
        comments_win = UIComponents.create_modern_window(self.root, f"💬 Comentarios en la publicación de {autor}", "700x600")

        main_frame = tk.Frame(comments_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Post original
        post_frame = tk.Frame(main_frame, bg='#2d2d44', bd=1, relief='solid')
        post_frame.pack(fill='x', pady=(0, 20))
        tk.Label(post_frame, text=f"Publicación de {autor}:", font=('Segoe UI', 12, 'bold'), bg='#2d2d44', fg='#4ecdc4').pack(anchor='w', padx=10, pady=(5,0))
        tk.Label(post_frame, text=contenido, font=('Segoe UI', 10), bg='#2d2d44', fg='white', wraplength=600, justify='left').pack(anchor='w', padx=10, pady=(0,10))

        # Treeview para comentarios
        comments_tree = ttk.Treeview(main_frame, columns=('Autor', 'Comentario', 'Fecha'), show='headings', style="Modern.Treeview")
        comments_tree.heading('Autor', text='Autor')
        comments_tree.heading('Comentario', text='Comentario')
        comments_tree.heading('Fecha', text='Fecha')
        comments_tree.column('Autor', width=150)
        comments_tree.column('Comentario', width=350)
        comments_tree.column('Fecha', width=150)
        
        def load_comments():
            for item in comments_tree.get_children():
                comments_tree.delete(item)
            
            comments_data = self.db.get_post_comments(post_id)
            if comments_data:
                for comment in comments_data:
                    fecha = comment[2].strftime('%d/%m/%Y %H:%M') if hasattr(comment[2], 'strftime') else str(comment[2])
                    comments_tree.insert('', 'end', values=(comment[3], comment[1], fecha))

        comments_tree.pack(fill='both', expand=True)
        load_comments()

        # Frame para añadir comentario
        add_comment_frame = tk.Frame(main_frame, bg='#1a1a2e')
        add_comment_frame.pack(fill='x', pady=(20, 0))

        comment_entry = tk.Text(add_comment_frame, height=3, bg='#16213e', fg='white', font=('Segoe UI', 10), insertbackground='white', border=0)
        comment_entry.pack(fill='x', side='left', expand=True, padx=(0, 10))

        def submit_comment():
            comentario = comment_entry.get("1.0", tk.END).strip()
            if comentario:
                if self.db.comment_post(self.current_user_id, post_id, comentario):
                    messagebox.showinfo("¡Comentado!", "Comentario publicado exitosamente")
                    comment_entry.delete("1.0", tk.END)
                    load_comments() # Recargar comentarios
                else:
                    messagebox.showerror("Error", "No se pudo publicar el comentario")
            else:
                messagebox.showwarning("Campo vacío", "Debes escribir un comentario")
        
        submit_btn = tk.Button(add_comment_frame, text="COMENTAR", command=submit_comment, bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'), border=0, padx=15, pady=5)
        submit_btn.pack(side='right')

    def show_messages(self):
        """Mostrar ventana de mensajes"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso denegado", "Debes iniciar sesión para ver mensajes")
            return
        
        messages_win = UIComponents.create_modern_window(self.root, "💬 Mensajes", "800x600")
        
        # Frame principal
        main_frame = tk.Frame(messages_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Bandeja de entrada", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=(0, 20))
        
        # Treeview para mensajes
        messages_tree = ttk.Treeview(main_frame, 
                                    columns=('Tipo', 'De/Para', 'Mensaje', 'Fecha'),
                                    show='headings', style="Modern.Treeview")
        
        for col in ['Tipo', 'De/Para', 'Mensaje', 'Fecha']:
            messages_tree.heading(col, text=col)
            messages_tree.column(col, width=150)
        
        messages_tree.column('Mensaje', width=300)
        
        # Cargar mensajes
        messages = self.db.get_user_messages(self.current_user_id)
        if messages:
            for msg in messages:
                fecha = msg[2].strftime("%d/%m/%Y %H:%M") if hasattr(msg[2], 'strftime') else str(msg[2])
                contenido = msg[1][:50] + "..." if len(msg[1]) > 50 else msg[1]
                messages_tree.insert('', 'end', values=(msg[4], msg[3], contenido, fecha))
        
        messages_tree.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Botones de acción
        buttons_frame = tk.Frame(main_frame, bg='#1a1a2e')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        new_msg_btn = tk.Button(buttons_frame, text="✉️ NUEVO MENSAJE", 
                               command=self.show_new_message_dialog,
                               bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                               border=0, cursor='hand2', padx=20, pady=10)
        new_msg_btn.pack(side='left', padx=10)
        
        refresh_btn = tk.Button(buttons_frame, text="🔄 ACTUALIZAR", 
                               command=lambda: self.refresh_messages(messages_tree),
                               bg='#45b7d1', fg='white', font=('Segoe UI', 12, 'bold'),
                               border=0, cursor='hand2', padx=20, pady=10)
        refresh_btn.pack(side='left', padx=10)
    
    def show_new_message_dialog(self):
        """Mostrar diálogo para nuevo mensaje"""
        # Obtener lista de usuarios para seleccionar destinatario
        users = self.db.get_all_users()
        if not users:
            messagebox.showinfo("Info", "No hay usuarios disponibles")
            return
        
        # Crear ventana de selección
        select_win = UIComponents.create_modern_window(self.root, "✉️ Nuevo Mensaje", "600x500")
        
        # Frame principal
        main_frame = tk.Frame(select_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Seleccionar destinatario", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=(0, 20))
        
        # Treeview para usuarios
        users_tree = ttk.Treeview(main_frame, 
                                 columns=('ID', 'Nombre', 'Email'),
                                 show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email']:
            users_tree.heading(col, text=col)
            users_tree.column(col, width=150)
        
        # Cargar usuarios (excluyendo al usuario actual)
        for user in users:
            if user[0] != self.current_user_id:
                users_tree.insert('', 'end', values=tuple(user))
        
        users_tree.pack(fill='both', expand=True, padx=20, pady=20)
        
        def send_to_selected():
            selected = users_tree.selection()
            if selected:
                user_id = users_tree.item(selected[0])['values'][0]
                user_name = users_tree.item(selected[0])['values'][1]
                select_win.destroy()
                self.send_message_window(user_id, user_name)
            else:
                messagebox.showwarning("Selección requerida", "Debes seleccionar un destinatario")
        
        # Botón enviar
        send_btn = tk.Button(main_frame, text="📤 ENVIAR MENSAJE", command=send_to_selected,
                           bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                           border=0, cursor='hand2', padx=20, pady=10)
        send_btn.pack(pady=20)
    
    def refresh_messages(self, tree):
        """Actualizar lista de mensajes"""
        # Limpiar árbol
        for item in tree.get_children():
            tree.delete(item)
        
        # Recargar mensajes
        messages = self.db.get_user_messages(self.current_user_id)
        if messages:
            for msg in messages:
                fecha = msg[2].strftime("%d/%m/%Y %H:%M") if hasattr(msg[2], 'strftime') else str(msg[2])
                contenido = msg[1][:50] + "..." if len(msg[1]) > 50 else msg[1]
                tree.insert('', 'end', values=(msg[4], msg[3], contenido, fecha))
        
        messagebox.showinfo("Actualizado", "Lista de mensajes actualizada")
    
    def manage_friendships(self):
        """Gestionar amistades"""
        if not self.current_user_id:
            messagebox.showwarning("Acceso denegado", "Debes iniciar sesión para gestionar amistades")
            return
        
        friends_win = UIComponents.create_modern_window(self.root, "🤝 Gestión de Amistades", "1000x700")
        
        # Notebook para diferentes secciones
        notebook = ttk.Notebook(friends_win, style="Modern.TNotebook")
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Pestaña de amigos
        friends_frame = tk.Frame(notebook, bg='#2d2d44')
        notebook.add(friends_frame, text="👥 Mis Amigos")
        
        friends_tree = ttk.Treeview(friends_frame, 
                                   columns=('ID', 'Nombre', 'Email'),
                                   show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email']:
            friends_tree.heading(col, text=col)
            friends_tree.column(col, width=200)
        
        def load_friends():
            for item in friends_tree.get_children():
                friends_tree.delete(item)
            
            friends = self.db.get_user_friends(self.current_user_id)
            if friends:
                for friend in friends:
                    friends_tree.insert('', 'end', values=tuple(friend))
        
        def send_message_to_friend():
            selected = friends_tree.selection()
            if selected:
                user_id = friends_tree.item(selected[0])['values'][0]
                user_name = friends_tree.item(selected[0])['values'][1]
                self.send_message_window(user_id, user_name)
            else:
                messagebox.showwarning("Selección requerida", "Debes seleccionar un amigo")
        
        # Botones para amigos
        friends_buttons_frame = tk.Frame(friends_frame, bg='#2d2d44')
        friends_buttons_frame.pack(fill='x', padx=20, pady=10)
        
        msg_btn = tk.Button(friends_buttons_frame, text="💬 ENVIAR MENSAJE", command=send_message_to_friend,
                           bg='#4ecdc4', fg='white', font=('Segoe UI', 10, 'bold'),
                           border=0, cursor='hand2', padx=20)
        msg_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(friends_buttons_frame, text="🔄 ACTUALIZAR", command=load_friends,
                               bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                               border=0, cursor='hand2', padx=20)
        refresh_btn.pack(side='left', padx=5)
        
        friends_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Pestaña de solicitudes pendientes
        requests_frame = tk.Frame(notebook, bg='#2d2d44')
        notebook.add(requests_frame, text="📨 Solicitudes Pendientes")
        
        requests_tree = ttk.Treeview(requests_frame, 
                                    columns=('ID', 'Nombre', 'Email', 'Fecha'),
                                    show='headings', style="Modern.Treeview")
        
        for col in ['ID', 'Nombre', 'Email', 'Fecha']:
            requests_tree.heading(col, text=col)
            requests_tree.column(col, width=150)
        
        def load_pending_requests():
            for item in requests_tree.get_children():
                requests_tree.delete(item)
            
            requests = self.db.get_friend_requests(self.current_user_id)
            if requests:
                for req in requests:
                    fecha = req[3].strftime("%d/%m/%Y") if hasattr(req[3], 'strftime') else str(req[3])
                    requests_tree.insert('', 'end', values=(req[0], req[1], req[2], fecha))
        
        def accept_request():
            selected = requests_tree.selection()
            if selected:
                user_id = requests_tree.item(selected[0])['values'][0]
                if self.db.accept_friend_request(user_id, self.current_user_id):
                    messagebox.showinfo("¡Genial!", "Solicitud de amistad aceptada ✅")
                    load_pending_requests()
                else:
                    messagebox.showerror("Error", "No se pudo aceptar la solicitud")
            else:
                messagebox.showwarning("Selección requerida", "Debes seleccionar una solicitud")
        
        def reject_request():
            selected = requests_tree.selection()
            if selected:
                user_id = requests_tree.item(selected[0])['values'][0]
                if self.db.execute_update("UPDATE amistades SET estado = 'rechazada' WHERE usuario1_id = ? AND usuario2_id = ?", (user_id, self.current_user_id)):
                    messagebox.showinfo("Rechazada", "Solicitud rechazada ❌")
                    load_pending_requests()
                else:
                    messagebox.showerror("Error", "No se pudo rechazar la solicitud")
            else:
                messagebox.showwarning("Selección requerida", "Debes seleccionar una solicitud")
        
        # Botones para solicitudes
        req_buttons_frame = tk.Frame(requests_frame, bg='#2d2d44')
        req_buttons_frame.pack(fill='x', padx=20, pady=10)
        
        accept_btn = tk.Button(req_buttons_frame, text="✅ ACEPTAR", command=accept_request,
                              bg='#4ecdc4', fg='white', font=('Segoe UI', 10, 'bold'),
                              border=0, cursor='hand2', padx=20)
        accept_btn.pack(side='left', padx=5)
        
        reject_btn = tk.Button(req_buttons_frame, text="❌ RECHAZAR", command=reject_request,
                              bg='#ff6b6b', fg='white', font=('Segoe UI', 10, 'bold'),
                              border=0, cursor='hand2', padx=20)
        reject_btn.pack(side='left', padx=5)
        
        refresh_req_btn = tk.Button(req_buttons_frame, text="🔄 ACTUALIZAR", command=load_pending_requests,
                                   bg='#45b7d1', fg='white', font=('Segoe UI', 10, 'bold'),
                                   border=0, cursor='hand2', padx=20)
        refresh_req_btn.pack(side='left', padx=5)
        
        requests_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cargar datos iniciales
        load_friends()
        load_pending_requests()
    
    def show_database_viewer(self):
        """Mostrar visor de base de datos con vistas intercambiables de resultados y editor"""
        db_win = UIComponents.create_modern_window(self.root, "🗄️ Explorador de Base de Datos", "1200x700")

        main_frame = tk.Frame(db_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both')

        # Paneles
        left_panel = tk.Frame(main_frame, bg='#16213e', width=200)
        left_panel.pack(side='left', fill='y', padx=(10, 5), pady=10)
        left_panel.pack_propagate(False)

        center_panel = tk.Frame(main_frame, bg='#2d2d44')
        center_panel.pack(side='left', fill='both', expand=True, pady=10)

        # --- Vistas intercambiables en el panel central ---
        results_view = tk.Frame(center_panel, bg='#2d2d44')
        editor_view = tk.Frame(center_panel, bg='#16213e')

        def show_view(view_to_show):
            # Ocultar todas las vistas
            results_view.pack_forget()
            editor_view.pack_forget()
            # Mostrar la vista seleccionada
            view_to_show.pack(fill='both', expand=True)

        # --- Contenido de la Vista de Resultados ---
        self.results_title = tk.Label(results_view, text="Tabla:", font=('Segoe UI', 14, 'bold'), bg='#2d2d44', fg='white')
        self.results_title.pack(pady=10)
        tree_frame = tk.Frame(results_view)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.results_tree = ttk.Treeview(tree_frame, show='headings', style="Modern.Treeview")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.results_tree.pack(fill='both', expand=True)

        # --- Contenido de la Vista de Editor SQL ---
        tk.Label(editor_view, text="Editor de Consultas SQL", font=('Segoe UI', 14, 'bold'), bg='#16213e', fg='white').pack(pady=10)
        query_text = tk.Text(editor_view, height=10, bg='#1a1a2e', fg='white', insertbackground='white', font=('Consolas', 11), relief='flat', bd=2)
        query_text.pack(fill='both', expand=True, padx=10, pady=5)
        execute_custom_btn = tk.Button(editor_view, text="▶️ EJECUTAR CONSULTA", command=lambda: execute_custom_query(), bg='#4ecdc4', fg='white', font=('Segoe UI', 11, 'bold'), border=0)
        execute_custom_btn.pack(pady=10, ipady=8, fill='x', padx=10)
        ttk.Separator(editor_view, orient='horizontal').pack(fill='x', padx=10, pady=10)
        tk.Label(editor_view, text="Consultas de ejemplo (clic para cargar)", font=('Segoe UI', 11, 'bold'), bg='#16213e', fg='white').pack(pady=5)
        queries_list = tk.Listbox(editor_view, bg='#2d2d44', fg='white', font=('Segoe UI', 10), relief='flat', selectbackground='#4ecdc4', height=10)
        queries_list.pack(fill='x', padx=10, pady=(0, 10))

        predefined_queries = [
            "SELECT * FROM usuarios WHERE id = 1;",
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
        for q in predefined_queries:
            queries_list.insert(tk.END, q)

        def load_query_from_list(event):
            selection_indices = queries_list.curselection()
            if not selection_indices: return
            query = queries_list.get(selection_indices[0])
            query_text.delete("1.0", tk.END)
            query_text.insert("1.0", query)
        queries_list.bind('<<ListboxSelect>>', load_query_from_list)

        def execute_custom_query():
            query = query_text.get("1.0", tk.END).strip()
            if not query:
                messagebox.showwarning("Consulta vacía", "El editor de consultas está vacío.", parent=db_win)
                return
            results, columns = self.db.execute_query(query)
            self.update_results_tree(results, columns, "Resultado de consulta personalizada")
            show_view(results_view) # Mostrar resultados tras ejecutar

        # --- Panel Izquierdo (Tablas y control de vistas) ---
        tk.Label(left_panel, text="☰ VISTAS", font=('Segoe UI', 14, 'bold'), bg='#16213e', fg='white').pack(pady=15)
        
        def show_table_data(table_name):
            show_view(results_view)
            query = f"SELECT * FROM {table_name}"
            results, columns = self.db.execute_query(query)
            self.update_results_tree(results, columns, f"Tabla: {table_name.upper()} - {len(results) if results else 0} registros")

        tables = ['usuarios', 'publicaciones', 'me_gusta', 'comentarios', 'amistades', 'mensajes']
        for table in tables:
            icon = {'usuarios': '👥', 'publicaciones': '📝', 'me_gusta': '❤️', 'comentarios': '💬', 'amistades': '🤝', 'mensajes': '✉️'}.get(table, '🗂️')
            btn = tk.Button(left_panel, text=f" {icon} {table.upper()}", font=('Segoe UI', 11), bg='#2d2d44', fg='white', relief='flat', anchor='w', command=lambda t=table: show_table_data(t))
            btn.pack(fill='x', padx=10, pady=4, ipady=5)
            
        ttk.Separator(left_panel, orient='horizontal').pack(fill='x', padx=10, pady=15)

        editor_btn = tk.Button(left_panel, text=" ✏️ EDITOR SQL", font=('Segoe UI', 11, 'bold'), bg='#4ecdc4', fg='white', relief='flat', anchor='w', command=lambda: show_view(editor_view))
        editor_btn.pack(fill='x', padx=10, pady=4, ipady=5)

        # Mostrar vista inicial
        show_table_data('usuarios')
    
    def update_results_tree(self, results, columns, title):
        """Limpia y actualiza el Treeview con nuevos resultados y columnas"""
        self.results_title.config(text=title)
        
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.results_tree['columns'] = ()

        if results and columns:
            self.results_tree['columns'] = columns
            for col in columns:
                self.results_tree.heading(col, text=col)
                self.results_tree.column(col, width=100, anchor='w')
            
            for row in results:
                self.results_tree.insert('', 'end', values=tuple(row))
        elif columns is not None:
             pass # No mostrar nada si no hay resultados, solo limpiar la tabla
        else:
            messagebox.showerror("Error", "No se pudo ejecutar la consulta", parent=self.results_tree.winfo_toplevel())

    def execute_selected_query(self, queries_list):
        """DEPRECATED"""
        pass
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# Punto de entrada
if __name__ == "__main__":
    """
    🚀 NIILO - Red Social Moderna (Versión Modular)
    
    📋 REQUISITOS:
    1. pip install pyodbc tkcalendar
    2. ODBC Driver 17 for SQL Server
    3. SQL Server con base de datos 'red_social'
    
    🎨 CARACTERÍSTICAS:
    - Diseño modular y organizado
    - Módulos separados para mejor mantenimiento
    - Interfaz moderna y responsiva
    - Gestión completa de usuarios, posts, mensajes y amistades
    
    📁 ESTRUCTURA:
    - main.py: Archivo principal
    - modules/database.py: Gestión de base de datos
    - modules/ui_components.py: Componentes de interfaz
    - modules/windows.py: Ventanas específicas
    
    ⚙️ CONFIGURACIÓN:
    Modifica la connection_string en database.py si es necesario
    """
    
    app = ModernRedSocialApp()
    app.run() 