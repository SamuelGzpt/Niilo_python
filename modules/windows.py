import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkcalendar import DateEntry
from datetime import datetime
import os
import shutil
from PIL import Image, ImageTk
from .ui_components import UIComponents

class Windows:
    def __init__(self, app):
        self.app = app
        self.db = app.db
    
    def login_window(self):
        """Ventana de inicio de sesión moderna"""
        login_win = UIComponents.create_modern_window(self.app.root, "🔑 Iniciar Sesión", "700x500")
        
        main_frame = tk.Frame(login_win, bg='#2d2d44')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        tk.Label(main_frame, text="Bienvenido de vuelta", 
                font=('Segoe UI', 16, 'bold'), bg='#2d2d44', fg='white').pack(pady=20)
        
        # Campos de entrada explícitos
        tk.Label(main_frame, text="Email", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        email_entry = tk.Entry(main_frame, font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        email_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 10))

        tk.Label(main_frame, text="Contraseña", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        password_entry = tk.Entry(main_frame, show='*', font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        password_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 20))
        
        def do_login():
            email = email_entry.get()
            password = self.db.hash_password(password_entry.get().strip())
            
            user = self.db.get_user_by_credentials(email, password)
            if user:
                self.app.current_user_id = user[0]
                self.app.user_label.config(text=f"👤 {user[1]} {user[2]}", fg='#4ecdc4')
                
                # Ocultar botones de login/register y mostrar logout
                self.app.login_btn.pack_forget()
                self.app.register_btn.pack_forget()
                self.app.logout_btn.pack(side=tk.LEFT, padx=5)
                
                login_win.destroy()
                messagebox.showinfo("¡Bienvenido!", f"Sesión iniciada como {user[1]} {user[2]}")
            else:
                messagebox.showerror("Error", "Credenciales incorrectas")
        
        # Botón de login
        login_button = tk.Button(main_frame, text="INICIAR SESIÓN", command=do_login,
                               bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                               border=0, cursor='hand2', pady=12)
        login_button.pack(fill='x', pady=20)
        
        # Forzar actualización del layout
        login_win.update_idletasks()
    
    def register_window(self):
        """Ventana de registro moderna"""
        reg_win = UIComponents.create_modern_window(self.app.root, "📝 Crear Cuenta", "900x900")
        
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
        
        # Frame principal
        main_frame = tk.Frame(scrollable_frame, bg='#2d2d44')
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Título
        tk.Label(main_frame, text="Crear nueva cuenta", 
                font=('Segoe UI', 16, 'bold'), bg='#2d2d44', fg='white').pack(pady=20)
        
        # Campos de entrada explícitos
        tk.Label(main_frame, text="Nombre", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        nombre_entry = tk.Entry(main_frame, font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        nombre_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 10))

        tk.Label(main_frame, text="Apellido", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        apellido_entry = tk.Entry(main_frame, font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        apellido_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 10))

        tk.Label(main_frame, text="Email", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        email_entry = tk.Entry(main_frame, font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        email_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 10))

        tk.Label(main_frame, text="Contraseña", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        password_entry = tk.Entry(main_frame, show='*', font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        password_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 10))
        
        # Frame para fecha de nacimiento
        fecha_frame = tk.Frame(main_frame, bg='#2d2d44')
        fecha_frame.pack(fill='x', pady=10)
        
        tk.Label(fecha_frame, text="Fecha de nacimiento", font=('Segoe UI', 10),
               bg='#2d2d44', fg='#a0a0a0').pack(anchor='w')
        
        fecha_entry = DateEntry(fecha_frame, width=20, background='#16213e',
                              foreground='white', borderwidth=0, date_pattern='yyyy-mm-dd')
        fecha_entry.pack(fill='x', ipady=8)
        
        tk.Label(main_frame, text="Ubicación", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10, pady=(10,0))
        ubicacion_entry = tk.Entry(main_frame, font=('Segoe UI', 12), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        ubicacion_entry.pack(fill='x', ipady=8, padx=10, pady=(0, 10))

        tk.Label(main_frame, text="Biografía", font=('Segoe UI', 10), bg='#2d2d44', fg='#a0a0a0').pack(anchor='w', padx=10)
        biografia_entry = tk.Text(main_frame, height=4, font=('Segoe UI', 11), bg='#16213e', fg='white', insertbackground='white', border=0, relief='flat')
        biografia_entry.pack(fill='x', padx=10, pady=(0, 10))
        
        def do_register():
            nombre = nombre_entry.get()
            apellido = apellido_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            fecha_nac = fecha_entry.get_date()
            ubicacion = ubicacion_entry.get()
            biografia = biografia_entry.get("1.0", tk.END).strip()
            
            if not all([nombre, apellido, email, password]):
                messagebox.showerror("Error", "Todos los campos obligatorios deben estar completos")
                return
            
            password_hash = self.db.hash_password(password)
            
            if self.db.create_user(nombre, apellido, email, password_hash, fecha_nac, ubicacion, biografia):
                messagebox.showinfo("¡Éxito!", "Cuenta creada exitosamente. Ya puedes iniciar sesión.")
                reg_win.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear la cuenta. Verifica que el email no esté en uso.")
        
        # Botón de registro
        register_button = tk.Button(main_frame, text="CREAR CUENTA", command=do_register,
                                  bg='#45b7d1', fg='white', font=('Segoe UI', 12, 'bold'),
                                  border=0, cursor='hand2', pady=12)
        register_button.pack(fill='x', pady=20)
        
        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Forzar actualización del layout
        reg_win.update_idletasks()
    
    def profile_window(self):
        """Ventana del perfil del usuario"""
        if not self.app.current_user_id:
            messagebox.showwarning("Acceso denegado", "Debes iniciar sesión para ver tu perfil")
            return
        
        profile_win = UIComponents.create_modern_window(self.app.root, "👤 Mi Perfil", "900x1050")
        
        # Frame principal con scroll
        main_frame = tk.Frame(profile_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)
        
        # Obtener datos del perfil
        profile_data = self.db.get_user_profile(self.app.current_user_id)
        
        if not profile_data:
            # Fallback a datos básicos si la vista de perfil falla
            user_basic_data, _ = self.db.execute_query("SELECT id, nombre, apellido, email, ubicacion, biografia, fecha_registro FROM usuarios WHERE id = ?", (self.app.current_user_id,))
            if user_basic_data:
                user = user_basic_data[0]
                # Crear un tuple de profile_data con valores por defecto para las estadísticas
                profile_data = (
                    user[0],                                    # id
                    f"{user[1]} {user[2]}",                      # nombre_completo
                    user[3],                                    # email
                    user[4],                                    # ubicacion
                    user[5],                                    # biografia
                    user[6],                                    # fecha_registro
                    0,                                          # total_publicaciones
                    0,                                          # total_amigos
                    0,                                          # total_likes_recibidos
                    0,                                          # total_likes_dados
                    0,                                          # total_comentarios_recibidos
                    0,                                          # total_comentarios_dados
                    0,                                          # total_mensajes_enviados
                    0                                           # total_mensajes_recibidos
                )
            else:
                # Si incluso los datos básicos fallan, mostrar el error
                error_frame = tk.Frame(main_frame, bg='#2d2d44')
                error_frame.pack(expand=True, fill='both', padx=20, pady=20)
                
                error_label = tk.Label(error_frame, text="❌ No se pudo cargar el perfil", 
                                      font=('Segoe UI', 16, 'bold'), 
                                      bg='#2d2d44', fg='#ff6b6b')
                error_label.pack(pady=20)
                
                info_label = tk.Label(error_frame, text="El usuario no existe o hay un problema de conexión.", 
                                     font=('Segoe UI', 12), 
                                     bg='#2d2d44', fg='#a0a0a0', justify='left')
                info_label.pack(pady=10)
                return
        
        # Header del perfil con foto simulada
        header_frame = tk.Frame(main_frame, bg='#2d2d44', height=200)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Obtener foto de perfil actual
        current_photo_path = self.db.get_user_photo(self.app.current_user_id)
        
        # Frame para la foto de perfil
        photo_frame = tk.Frame(header_frame, bg='#a55eea', width=120, height=120)
        photo_frame.pack(side='left', padx=30, pady=40)
        photo_frame.pack_propagate(False)
        
        # Variable para almacenar la imagen
        self.profile_photo = None
        
        # Función para cargar y mostrar imagen
        def load_profile_image(image_path=None):
            try:
                if image_path and os.path.exists(image_path):
                    # Cargar y redimensionar imagen
                    image = Image.open(image_path)
                    image = image.resize((120, 120), Image.Resampling.LANCZOS)
                    self.profile_photo = ImageTk.PhotoImage(image)
                    photo_label.config(image=self.profile_photo, text="")
                else:
                    # Mostrar emoji por defecto
                    photo_label.config(image="", text="👤", font=('Segoe UI', 48))
            except Exception as e:
                print(f"Error cargando imagen: {e}")
                photo_label.config(image="", text="👤", font=('Segoe UI', 48))
        
        # Label para mostrar la foto
        photo_label = tk.Label(photo_frame, text="👤", font=('Segoe UI', 48), 
                              bg='#a55eea', fg='white')
        photo_label.pack(expand=True)
        
        # Cargar imagen actual si existe
        load_profile_image(current_photo_path)
        
        # Función para seleccionar y cargar nueva imagen
        def select_profile_image():
            file_types = [
                ('Imágenes', '*.png *.jpg *.jpeg *.gif *.bmp'),
                ('PNG', '*.png'),
                ('JPEG', '*.jpg *.jpeg'),
                ('GIF', '*.gif'),
                ('BMP', '*.bmp'),
                ('Todos los archivos', '*.*')
            ]
            
            file_path = filedialog.askopenfilename(
                title="Seleccionar foto de perfil",
                filetypes=file_types
            )
            
            if file_path:
                try:
                    # Crear directorio para fotos si no existe
                    photos_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profile_photos')
                    os.makedirs(photos_dir, exist_ok=True)
                    
                    # Generar nombre único para la imagen
                    file_ext = os.path.splitext(file_path)[1]
                    new_filename = f"profile_{self.app.current_user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
                    new_path = os.path.join(photos_dir, new_filename)
                    
                    # Copiar imagen al directorio de la aplicación
                    shutil.copy2(file_path, new_path)
                    
                    # Actualizar en la base de datos
                    if self.db.update_user_photo(self.app.current_user_id, new_path):
                        # Cargar y mostrar la nueva imagen
                        load_profile_image(new_path)
                        messagebox.showinfo("Éxito", "Foto de perfil actualizada correctamente")
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la foto en la base de datos")
                        
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{str(e)}")
        
        # Función para editar email
        def edit_email():
            current_email = profile_data[2]
            new_email = simpledialog.askstring("Editar Email", 
                                             f"Email actual: {current_email}\nNuevo email:",
                                             initialvalue=current_email)
            
            if new_email and new_email != current_email:
                if self.db.update_user_email(self.app.current_user_id, new_email):
                    messagebox.showinfo("Éxito", "Email actualizado correctamente")
                    # Actualizar la etiqueta del email
                    email_label.config(text=f"📧 {new_email}")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el email")
        
        # Información básica
        info_frame = tk.Frame(header_frame, bg='#2d2d44')
        info_frame.pack(side='left', padx=30, pady=40, fill='y')
        
        name_label = tk.Label(info_frame, text=profile_data[1], 
                             font=('Segoe UI', 24, 'bold'), 
                             bg='#2d2d44', fg='white')
        name_label.pack(anchor='w')
        
        email_label = tk.Label(info_frame, text=f"📧 {profile_data[2]}", 
                              font=('Segoe UI', 12), 
                              bg='#2d2d44', fg='#a0a0a0')
        email_label.pack(anchor='w', pady=(5, 0))
        
        if profile_data[3]:  # ubicación
            location_label = tk.Label(info_frame, text=f"📍 {profile_data[3]}", 
                                     font=('Segoe UI', 12), 
                                     bg='#2d2d44', fg='#a0a0a0')
            location_label.pack(anchor='w', pady=(5, 0))
        
        # Estadísticas del perfil
        stats_frame = tk.Frame(main_frame, bg='#2d2d44')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats_title = tk.Label(stats_frame, text="📊 Estadísticas", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#2d2d44', fg='white')
        stats_title.pack(anchor='w', padx=20, pady=15)
        
        # Grid de estadísticas
        stats_grid = tk.Frame(stats_frame, bg='#2d2d44')
        stats_grid.pack(fill='x', padx=20, pady=(0, 20))
        
        # Configurar grid
        for i in range(4):
            stats_grid.grid_columnconfigure(i, weight=1)
        
        # Crear tarjetas de estadísticas
        stats_cards = [
            ("📝 Publicaciones", profile_data[6], '#4ecdc4'),
            ("🤝 Amigos", profile_data[7], '#45b7d1'),
            ("❤️ Likes Recibidos", profile_data[8], '#ff6b6b'),
            ("👍 Likes Dados", profile_data[9], '#feca57'),
            ("💬 Comentarios Recibidos", profile_data[10], '#ff9ff3'),
            ("💭 Comentarios Dados", profile_data[11], '#6c5ce7'),
            ("📤 Mensajes Enviados", profile_data[12], '#00b894'),
            ("📥 Mensajes Recibidos", profile_data[13], '#74b9ff')
        ]
        
        # Crear dos filas de estadísticas
        for i, (title, value, color) in enumerate(stats_cards):
            row = i // 4  # 4 columnas por fila
            col = i % 4
            UIComponents.create_stats_card(stats_grid, title, value, color).grid(row=row, column=col, padx=5, pady=5, sticky='ew')
        
        # Información detallada
        details_frame = tk.Frame(main_frame, bg='#2d2d44')
        details_frame.pack(fill='both', expand=True)
        
        details_title = tk.Label(details_frame, text="ℹ️ Información Personal", 
                                font=('Segoe UI', 16, 'bold'), 
                                bg='#2d2d44', fg='white')
        details_title.pack(anchor='w', padx=20, pady=15)
        
        # Frame para información detallada
        info_details_frame = tk.Frame(details_frame, bg='#2d2d44')
        info_details_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Fecha de registro
        if profile_data[5]:  # fecha_registro
            reg_date = profile_data[5].strftime("%d/%m/%Y") if hasattr(profile_data[5], 'strftime') else str(profile_data[5])
            reg_label = tk.Label(info_details_frame, text=f"📅 Miembro desde: {reg_date}", 
                                font=('Segoe UI', 12), 
                                bg='#2d2d44', fg='#a0a0a0')
            reg_label.pack(anchor='w', pady=5)
        
        # Biografía
        if profile_data[4]:  # biografia
            bio_title = tk.Label(info_details_frame, text="📖 Biografía:", 
                                font=('Segoe UI', 12, 'bold'), 
                                bg='#2d2d44', fg='white')
            bio_title.pack(anchor='w', pady=(20, 5))
            
            bio_text = tk.Text(info_details_frame, height=4, wrap='word',
                              font=('Segoe UI', 11), 
                              bg='#16213e', fg='white',
                              insertbackground='white', border=0, relief='flat')
            bio_text.pack(fill='x', pady=(0, 20))
            bio_text.insert('1.0', profile_data[4])
            bio_text.config(state='disabled')  # Solo lectura
        
        # Botones de acción
        actions_frame = tk.Frame(main_frame, bg='#1a1a2e')
        actions_frame.pack(fill='x', pady=(20, 0))
        
        # Botón para editar email
        edit_email_btn = tk.Button(actions_frame, text="✏️ EDITAR EMAIL", 
                                  command=edit_email,
                                  bg='#a55eea', fg='white', font=('Segoe UI', 12, 'bold'),
                                  border=0, cursor='hand2', padx=30, pady=10)
        edit_email_btn.pack(side='left', padx=10)
        
        # Botón para cambiar foto
        photo_btn = tk.Button(actions_frame, text="📷 CAMBIAR FOTO", 
                             command=select_profile_image,
                             bg='#45b7d1', fg='white', font=('Segoe UI', 12, 'bold'),
                             border=0, cursor='hand2', padx=30, pady=10)
        photo_btn.pack(side='left', padx=10)
        
        # Botón para ver actividad reciente
        activity_btn = tk.Button(actions_frame, text="📈 VER ACTIVIDAD", 
                                command=self.activity_window,
                                bg='#4ecdc4', fg='white', font=('Segoe UI', 12, 'bold'),
                                border=0, cursor='hand2', padx=30, pady=10)
        activity_btn.pack(side='left', padx=10)
    
    def check_user_data(self):
        """Verificar datos del usuario en la base de datos"""
        if not self.app.current_user_id:
            return
        
        user = self.db.execute_query("SELECT id, nombre, apellido, email FROM usuarios WHERE id = ?", (self.app.current_user_id,))
        
        if user:
            user_data = user[0]
            messagebox.showinfo("Usuario encontrado", f"ID: {user_data[0]}\nNombre: {user_data[1]} {user_data[2]}\nEmail: {user_data[3]}")
        else:
            messagebox.showerror("Error", "Usuario no encontrado en la base de datos")
    
    def activity_window(self):
        """Ventana de actividad reciente del usuario"""
        if not self.app.current_user_id:
            return
        
        activity_win = UIComponents.create_modern_window(self.app.root, "📈 Actividad Reciente", "800x600")
        
        # Frame principal
        main_frame = tk.Frame(activity_win, bg='#1a1a2e')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, text="Tu actividad en los últimos 30 días", 
                              font=('Segoe UI', 16, 'bold'), 
                              bg='#1a1a2e', fg='white')
        title_label.pack(pady=(0, 20))
        
        # Notebook para diferentes tipos de actividad
        notebook = ttk.Notebook(main_frame, style="Modern.TNotebook")
        notebook.pack(fill='both', expand=True)
        
        def setup_activity_tab(parent):
            """Pestaña para ver publicaciones del usuario"""
            activity_tree = ttk.Treeview(parent, columns=('Contenido', 'Fecha', 'Estado'), show='headings', style="Modern.Treeview")
            activity_tree.heading('Contenido', text='Contenido')
            activity_tree.heading('Fecha', text='Fecha')
            activity_tree.heading('Estado', text='Estado')
            activity_tree.column('Contenido', width=300, anchor='w')
            activity_tree.column('Fecha', width=150, anchor='center')
            
            # Cargar datos
            user_posts = self.app.db.execute_query("SELECT contenido, fecha_publicacion, activa FROM publicaciones WHERE usuario_id = ? ORDER BY fecha_publicacion DESC", (self.app.current_user_id,))[0]
            if user_posts:
                for post in user_posts:
                    fecha = post[1].strftime('%d/%m/%Y %H:%M') if hasattr(post[1], 'strftime') else str(post[1])
                    estado = "Sí" if post[2] else "No"
                    activity_tree.insert('', 'end', values=(post[0], fecha, estado))
            
            activity_tree.pack(fill='both', expand=True, padx=10, pady=10)

        def setup_interactions_tab(parent):
            """Pestaña para ver likes y comentarios del usuario"""
            interaction_tree = ttk.Treeview(parent, columns=('Tipo', 'Detalle', 'Fecha'), show='headings', style="Modern.Treeview")
            interaction_tree.heading('Tipo', text='Tipo')
            interaction_tree.heading('Detalle', text='Detalle')
            interaction_tree.heading('Fecha', text='Fecha')
            interaction_tree.column('Tipo', width=100, anchor='w')
            interaction_tree.column('Detalle', width=400, anchor='w')
            interaction_tree.column('Fecha', width=150, anchor='center')

            # Cargar datos usando la nueva función
            user_interactions = self.app.db.get_user_interactions(self.app.current_user_id)
            if user_interactions:
                for interaction in user_interactions:
                    # El orden es: tipo, fecha, detalle
                    tipo, fecha, detalle = interaction
                    fecha_str = fecha.strftime('%d/%m/%Y %H:%M') if hasattr(fecha, 'strftime') else str(fecha)
                    # Insertar en el orden de las columnas: Tipo, Detalle, Fecha
                    interaction_tree.insert('', 'end', values=(tipo, detalle, fecha_str))
            
            interaction_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Crear frames para las pestañas
        activity_frame = tk.Frame(notebook, bg='#2d2d44')
        interactions_frame = tk.Frame(notebook, bg='#2d2d44')
        
        notebook.add(activity_frame, text="📝 Mis Publicaciones")
        notebook.add(interactions_frame, text="❤️ Mis Interacciones")

        # Configurar el contenido de cada pestaña
        setup_activity_tab(activity_frame)
        setup_interactions_tab(interactions_frame)
        
        notebook.pack(fill='both', expand=True)

    def send_message_to_selected_user(self, tree):
        """Enviar mensaje al usuario seleccionado"""
        selected = tree.selection()
        # ... existing code ... 