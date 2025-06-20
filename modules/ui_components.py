import tkinter as tk
from tkinter import ttk

class UIComponents:
    @staticmethod
    def setup_styles():
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
    
    @staticmethod
    def create_modern_button(parent, text, command, bg_color, hover_color, width=200, height=50):
        """Crear botón moderno con efectos hover"""
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
    
    @staticmethod
    def create_modern_entry(parent, placeholder, is_text_area=False, show=None):
        """Crear campo de entrada moderno"""
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
        
        if is_text_area:
            entry = tk.Text(frame, height=4, wrap='word', **entry_kwargs)
        else:
            entry = tk.Entry(frame, **entry_kwargs)
        
        entry.pack(fill='x', ipady=8)
        return entry
    
    @staticmethod
    def create_modern_window(parent, title, size="800x600", bg_color="#1a1a2e"):
        """Crear ventana moderna estándar"""
        window = tk.Toplevel(parent)
        window.title(title)
        window.geometry(size)
        window.configure(bg=bg_color)
        window.transient(parent)
        window.grab_set()  # Hacer modal
        window.focus_set()  # Dar foco
        
        # Centrar la ventana
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (int(size.split('x')[0]) // 2)
        y = (window.winfo_screenheight() // 2) - (int(size.split('x')[1]) // 2)
        window.geometry(f"{size}+{x}+{y}")
        
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
    
    @staticmethod
    def create_post_card(parent, post_data):
        """Crear tarjeta de publicación moderna"""
        card_frame = tk.Frame(parent, bg='#2d2d44', relief='flat', bd=2)
        card_frame.pack(fill='x', padx=20, pady=10)
        
        # Header de la tarjeta
        header_frame = tk.Frame(card_frame, bg='#2d2d44')
        header_frame.pack(fill='x', padx=15, pady=10)
        
        # Información del autor
        author_label = tk.Label(header_frame, text=f"👤 {post_data[1]}", 
                               font=('Segoe UI', 12, 'bold'), 
                               bg='#2d2d44', fg='#4ecdc4')
        author_label.pack(side='left')
        
        # Fecha
        fecha = post_data[4].strftime("%d/%m/%Y %H:%M") if hasattr(post_data[4], 'strftime') else str(post_data[4])
        date_label = tk.Label(header_frame, text=f"📅 {fecha}", 
                             font=('Segoe UI', 10), 
                             bg='#2d2d44', fg='#a0a0a0')
        date_label.pack(side='right')
        
        # Contenido
        content_frame = tk.Frame(card_frame, bg='#2d2d44')
        content_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        content_label = tk.Label(content_frame, text=post_data[3], 
                                font=('Segoe UI', 11), 
                                bg='#2d2d44', fg='white', 
                                wraplength=600, justify='left')
        content_label.pack(anchor='w')
        
        # Footer con estadísticas y botones
        footer_frame = tk.Frame(card_frame, bg='#2d2d44')
        footer_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        # Estadísticas
        stats_frame = tk.Frame(footer_frame, bg='#2d2d44')
        stats_frame.pack(side='left')
        
        likes_label = tk.Label(stats_frame, text=f"❤️ {post_data[7]}", 
                              font=('Segoe UI', 10), 
                              bg='#2d2d44', fg='#ff6b6b')
        likes_label.pack(side='left', padx=(0, 15))
        
        comments_label = tk.Label(stats_frame, text=f"💬 {post_data[8]}", 
                                 font=('Segoe UI', 10), 
                                 bg='#2d2d44', fg='#45b7d1')
        comments_label.pack(side='left')
        
        return card_frame
    
    @staticmethod
    def create_comment_card(parent, comment_data):
        """Crear tarjeta de comentario"""
        comment_frame = tk.Frame(parent, bg='#16213e', relief='flat', bd=1)
        comment_frame.pack(fill='x', padx=10, pady=5)
        
        # Header del comentario
        header_frame = tk.Frame(comment_frame, bg='#16213e')
        header_frame.pack(fill='x', padx=10, pady=5)
        
        author_label = tk.Label(header_frame, text=f"👤 {comment_data[3]}", 
                               font=('Segoe UI', 10, 'bold'), 
                               bg='#16213e', fg='#4ecdc4')
        author_label.pack(side='left')
        
        fecha = comment_data[2].strftime("%d/%m/%Y %H:%M") if hasattr(comment_data[2], 'strftime') else str(comment_data[2])
        date_label = tk.Label(header_frame, text=f"📅 {fecha}", 
                             font=('Segoe UI', 9), 
                             bg='#16213e', fg='#a0a0a0')
        date_label.pack(side='right')
        
        # Contenido del comentario
        content_label = tk.Label(comment_frame, text=comment_data[1], 
                                font=('Segoe UI', 10), 
                                bg='#16213e', fg='white', 
                                wraplength=500, justify='left')
        content_label.pack(anchor='w', padx=10, pady=(0, 5))
        
        return comment_frame
    
    @staticmethod
    def create_stats_card(parent, title, value, color):
        """Crear tarjeta de estadísticas"""
        card_frame = tk.Frame(parent, bg=color, relief='flat', bd=2)
        
        value_label = tk.Label(card_frame, text=str(value), 
                              font=('Segoe UI', 24, 'bold'), 
                              bg=color, fg='white')
        value_label.pack(pady=(15, 5))
        
        title_label = tk.Label(card_frame, text=title, 
                              font=('Segoe UI', 10), 
                              bg=color, fg='white')
        title_label.pack(pady=(0, 15))
        
        return card_frame 