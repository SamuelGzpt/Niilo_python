import pyodbc
from tkinter import messagebox
import hashlib

class DatabaseManager:
    def __init__(self):
        self.connection_string = """
        DRIVER={ODBC Driver 17 for SQL Server};
        SERVER=localhost;
        DATABASE=red_social;
        Trusted_Connection=yes;
        """
    
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
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta y retornar resultados con cabeceras"""
        conn = self.connect_db()
        if not conn:
            return None, None
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            results = cursor.fetchall()
            # Obtener nombres de las columnas
            columns = [column[0] for column in cursor.description]
            conn.close()
            return results, columns
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            conn.close()
            return None, None
    
    def execute_update(self, query, params=None):
        """Ejecutar consulta de actualización (INSERT, UPDATE, DELETE)"""
        conn = self.connect_db()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error ejecutando actualización: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def get_user_by_credentials(self, email, password_hash):
        """Obtener usuario por credenciales"""
        query = "SELECT id, nombre, apellido FROM usuarios WHERE email = ? AND password_hash = ? AND activo = 1"
        results, _ = self.execute_query(query, (email, password_hash))
        return results[0] if results else None
    
    def create_user(self, nombre, apellido, email, password_hash, fecha_nacimiento, ubicacion, biografia):
        """Crear nuevo usuario"""
        query = """
        INSERT INTO usuarios (nombre, apellido, email, password_hash, fecha_nacimiento, ubicacion, biografia)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute_update(query, (nombre, apellido, email, password_hash, fecha_nacimiento, ubicacion, biografia))
    
    def get_user_profile(self, user_id):
        """Obtener perfil completo del usuario con estadísticas detalladas"""
        query = """
        SELECT 
            u.id,
            CONCAT(u.nombre, ' ', u.apellido) AS nombre_completo,
            u.email,
            u.ubicacion,
            u.biografia,
            u.fecha_registro,
            -- Estadísticas de publicaciones
            ISNULL(posts_stats.total_publicaciones, 0) AS total_publicaciones,
            -- Estadísticas de amigos
            ISNULL(friends_stats.total_amigos, 0) AS total_amigos,
            -- Estadísticas de likes
            ISNULL(likes_received.total_likes_recibidos, 0) AS total_likes_recibidos,
            ISNULL(likes_given.total_likes_dados, 0) AS total_likes_dados,
            -- Estadísticas de comentarios
            ISNULL(comments_received.total_comentarios_recibidos, 0) AS total_comentarios_recibidos,
            ISNULL(comments_given.total_comentarios_dados, 0) AS total_comentarios_dados,
            -- Estadísticas de mensajes
            ISNULL(messages_sent.total_mensajes_enviados, 0) AS total_mensajes_enviados,
            ISNULL(messages_received.total_mensajes_recibidos, 0) AS total_mensajes_recibidos
        FROM usuarios u
        -- Subconsulta para publicaciones
        LEFT JOIN (
            SELECT usuario_id, COUNT(*) as total_publicaciones
            FROM publicaciones 
            WHERE activa = 1
            GROUP BY usuario_id
        ) posts_stats ON u.id = posts_stats.usuario_id
        -- Subconsulta para amigos
        LEFT JOIN (
            SELECT 
                CASE 
                    WHEN usuario1_id = ? THEN usuario2_id 
                    ELSE usuario1_id 
                END as friend_id
            FROM amistades 
            WHERE (usuario1_id = ? OR usuario2_id = ?) AND estado = 'aceptada'
        ) friends_temp ON u.id = friends_temp.friend_id
        LEFT JOIN (
            SELECT COUNT(*) as total_amigos
            FROM (
                SELECT 
                    CASE 
                        WHEN usuario1_id = ? THEN usuario2_id 
                        ELSE usuario1_id 
                    END as friend_id
                FROM amistades 
                WHERE (usuario1_id = ? OR usuario2_id = ?) AND estado = 'aceptada'
            ) friends_list
        ) friends_stats ON 1=1
        -- Subconsulta para likes recibidos
        LEFT JOIN (
            SELECT p.usuario_id, COUNT(*) as total_likes_recibidos
            FROM me_gusta mg
            JOIN publicaciones p ON mg.publicacion_id = p.id
            WHERE p.activa = 1
            GROUP BY p.usuario_id
        ) likes_received ON u.id = likes_received.usuario_id
        -- Subconsulta para likes dados
        LEFT JOIN (
            SELECT usuario_id, COUNT(*) as total_likes_dados
            FROM me_gusta
            GROUP BY usuario_id
        ) likes_given ON u.id = likes_given.usuario_id
        -- Subconsulta para comentarios recibidos
        LEFT JOIN (
            SELECT p.usuario_id, COUNT(*) as total_comentarios_recibidos
            FROM comentarios c
            JOIN publicaciones p ON c.publicacion_id = p.id
            WHERE c.activo = 1 AND p.activa = 1
            GROUP BY p.usuario_id
        ) comments_received ON u.id = comments_received.usuario_id
        -- Subconsulta para comentarios dados
        LEFT JOIN (
            SELECT usuario_id, COUNT(*) as total_comentarios_dados
            FROM comentarios
            WHERE activo = 1
            GROUP BY usuario_id
        ) comments_given ON u.id = comments_given.usuario_id
        -- Subconsulta para mensajes enviados
        LEFT JOIN (
            SELECT emisor_id, COUNT(*) as total_mensajes_enviados
            FROM mensajes
            GROUP BY emisor_id
        ) messages_sent ON u.id = messages_sent.emisor_id
        -- Subconsulta para mensajes recibidos
        LEFT JOIN (
            SELECT receptor_id, COUNT(*) as total_mensajes_recibidos
            FROM mensajes
            GROUP BY receptor_id
        ) messages_received ON u.id = messages_received.receptor_id
        WHERE u.id = ? AND u.activo = 1
        """
        
        results, _ = self.execute_query(query, (user_id, user_id, user_id, user_id, user_id, user_id, user_id))
        return results[0] if results else None
    
    def get_all_users(self):
        """Obtener todos los usuarios activos"""
        query = "SELECT id, CONCAT(nombre, ' ', apellido), email FROM usuarios WHERE activo = 1"
        results, _ = self.execute_query(query)
        return results
    
    def get_user_posts(self, user_id, limit=30):
        """Obtener publicaciones de un usuario"""
        query = """
        SELECT p.id, p.contenido, p.fecha_publicacion, p.tipo,
               COUNT(DISTINCT mg.id) as likes,
               COUNT(DISTINCT c.id) as comentarios
        FROM publicaciones p
        LEFT JOIN me_gusta mg ON p.id = mg.publicacion_id
        LEFT JOIN comentarios c ON p.id = c.publicacion_id AND c.activo = 1
        WHERE p.usuario_id = ? AND p.activa = 1
        GROUP BY p.id, p.contenido, p.fecha_publicacion, p.tipo
        ORDER BY p.fecha_publicacion DESC
        """
        results, _ = self.execute_query(query, (user_id,))
        return results
    
    def create_post(self, user_id, contenido, tipo='texto', url_media=None):
        """Crear nueva publicación"""
        query = "INSERT INTO publicaciones (usuario_id, contenido, tipo, url_media) VALUES (?, ?, ?, ?)"
        return self.execute_update(query, (user_id, contenido, tipo, url_media))
    
    def get_all_posts(self):
        """Obtener todas las publicaciones activas con información completa"""
        # Primero hacer una consulta simple para verificar que hay datos
        simple_query = "SELECT COUNT(*) FROM publicaciones WHERE activa = 1"
        count_result, _ = self.execute_query(simple_query)
        print(f"Total de publicaciones activas: {count_result[0][0] if count_result else 0}")
        
        # Consulta simplificada para obtener las publicaciones
        query = """
        SELECT 
            p.id,
            CONCAT(u.nombre, ' ', u.apellido) as autor,
            u.id as usuario_id,
            p.contenido,
            p.fecha_publicacion,
            p.tipo,
            p.url_media,
            ISNULL(likes_count.total_likes, 0) as total_likes,
            ISNULL(comments_count.total_comentarios, 0) as total_comentarios
        FROM publicaciones p
        JOIN usuarios u ON p.usuario_id = u.id
        LEFT JOIN (
            SELECT publicacion_id, COUNT(*) as total_likes 
            FROM me_gusta 
            GROUP BY publicacion_id
        ) likes_count ON p.id = likes_count.publicacion_id
        LEFT JOIN (
            SELECT publicacion_id, COUNT(*) as total_comentarios 
            FROM comentarios 
            WHERE activo = 1
            GROUP BY publicacion_id
        ) comments_count ON p.id = comments_count.publicacion_id
        WHERE p.activa = 1 AND u.activo = 1
        ORDER BY p.fecha_publicacion DESC
        """
        results, _ = self.execute_query(query)
        print(f"Publicaciones obtenidas: {len(results) if results else 0}")
        return results
    
    def like_post(self, user_id, post_id):
        """Dar like a una publicación"""
        query = "INSERT INTO me_gusta (usuario_id, publicacion_id) VALUES (?, ?)"
        return self.execute_update(query, (user_id, post_id))
    
    def comment_post(self, user_id, post_id, contenido):
        """Comentar una publicación"""
        query = "INSERT INTO comentarios (usuario_id, publicacion_id, contenido) VALUES (?, ?, ?)"
        return self.execute_update(query, (user_id, post_id, contenido))
    
    def get_post_comments(self, post_id):
        """Obtener comentarios de una publicación"""
        query = """
        SELECT c.id, c.contenido, c.fecha_comentario, CONCAT(u.nombre, ' ', u.apellido)
        FROM comentarios c
        JOIN usuarios u ON c.usuario_id = u.id
        WHERE c.publicacion_id = ? AND c.activo = 1
        ORDER BY c.fecha_comentario ASC
        """
        results, _ = self.execute_query(query, (post_id,))
        return results
    
    def send_message(self, sender_id, receiver_id, contenido):
        """Enviar mensaje"""
        query = "INSERT INTO mensajes (emisor_id, receptor_id, contenido) VALUES (?, ?, ?)"
        return self.execute_update(query, (sender_id, receiver_id, contenido))
    
    def get_user_messages(self, user_id):
        """Obtener mensajes de un usuario"""
        query = """
        SELECT m.id, m.contenido, m.fecha_envio, m.leido,
               CONCAT(u.nombre, ' ', u.apellido) as sender_name,
               CASE WHEN m.emisor_id = ? THEN 'Enviado' ELSE 'Recibido' END as tipo
        FROM mensajes m
        JOIN usuarios u ON (m.emisor_id = u.id OR m.receptor_id = u.id)
        WHERE (m.emisor_id = ? OR m.receptor_id = ?) AND u.id != ?
        ORDER BY m.fecha_envio DESC
        """
        results, _ = self.execute_query(query, (user_id, user_id, user_id, user_id))
        return results
    
    def get_user_interactions(self, user_id, days=30):
        """Obtener interacciones de un usuario (likes y comentarios)"""
        query = f"""
            SELECT 'Like' as tipo, mg.fecha_like as fecha, 
                   CONCAT('Te gustó una publicación de ', u.nombre, ' ', u.apellido) as detalle
            FROM me_gusta mg
            JOIN publicaciones p ON mg.publicacion_id = p.id
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE mg.usuario_id = ? AND mg.fecha_like >= DATEADD(DAY, -{days}, GETDATE())
            UNION ALL
            SELECT 'Comentario' as tipo, c.fecha_comentario as fecha,
                   CONCAT('Comentaste en una publicación de ', u.nombre, ' ', u.apellido) as detalle
            FROM comentarios c
            JOIN publicaciones p ON c.publicacion_id = p.id
            JOIN usuarios u ON p.usuario_id = u.id
            WHERE c.usuario_id = ? AND c.fecha_comentario >= DATEADD(DAY, -{days}, GETDATE())
            ORDER BY fecha DESC
        """
        results, _ = self.execute_query(query, (user_id, user_id))
        return results if results else []
    
    def send_friend_request(self, sender_id, receiver_id):
        """Enviar solicitud de amistad"""
        query = "INSERT INTO amistades (usuario1_id, usuario2_id, estado) VALUES (?, ?, 'pendiente')"
        return self.execute_update(query, (sender_id, receiver_id))
    
    def get_friend_requests(self, user_id):
        """Obtener solicitudes de amistad pendientes"""
        query = """
        SELECT u.id, CONCAT(u.nombre, ' ', u.apellido), u.email, a.fecha_solicitud
        FROM amistades a
        JOIN usuarios u ON a.usuario1_id = u.id
        WHERE a.usuario2_id = ? AND a.estado = 'pendiente'
        """
        results, _ = self.execute_query(query, (user_id,))
        return results if results is not None else []
    
    def accept_friend_request(self, sender_id, receiver_id):
        """Aceptar solicitud de amistad"""
        query = "UPDATE amistades SET estado = 'aceptada' WHERE usuario1_id = ? AND usuario2_id = ?"
        return self.execute_update(query, (sender_id, receiver_id))
    
    def get_user_friends(self, user_id):
        """Obtener amigos de un usuario"""
        query = """
        SELECT u.id, CONCAT(u.nombre, ' ', u.apellido), u.email
        FROM usuarios u
        JOIN amistades a ON (u.id = a.usuario1_id OR u.id = a.usuario2_id)
        WHERE (a.usuario1_id = ? OR a.usuario2_id = ?) 
        AND a.estado = 'aceptada' AND u.id != ? AND u.activo = 1
        """
        results, _ = self.execute_query(query, (user_id, user_id, user_id))
        return results
    
    def update_user_photo(self, user_id, photo_path):
        """Actualizar foto de perfil del usuario"""
        query = "UPDATE usuarios SET imagen_perfil = ? WHERE id = ?"
        return self.execute_update(query, (photo_path, user_id))
    
    def get_user_photo(self, user_id):
        """Obtener ruta de la foto de perfil del usuario"""
        query = "SELECT imagen_perfil FROM usuarios WHERE id = ?"
        results, _ = self.execute_query(query, (user_id,))
        return results[0][0] if results and results[0][0] else None
    
    def update_user_email(self, user_id, new_email):
        """Actualizar email del usuario"""
        query = "UPDATE usuarios SET email = ? WHERE id = ?"
        return self.execute_update(query, (new_email, user_id))
    
    def debug_database_state(self):
        """Función de debugging para verificar el estado de la base de datos"""
        print("=== DEBUGGING DATABASE STATE ===")
        
        # Verificar conexión
        conn = None
        try:
            conn = self.connect_db()
            if conn is None:
                print("✗ No se pudo conectar a la base de datos")
                return
            print("✓ Conexión a la base de datos exitosa")
        except Exception as e:
            print(f"✗ Error de conexión: {e}")
            return
        
        # Verificar tabla usuarios
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios WHERE activo = 1")
            result = cursor.fetchone()
            user_count = result[0] if result else 0
            print(f"✓ Usuarios activos: {user_count}")
        except Exception as e:
            print(f"✗ Error consultando usuarios: {e}")
        
        # Verificar tabla publicaciones
        try:
            cursor.execute("SELECT COUNT(*) FROM publicaciones")
            result = cursor.fetchone()
            total_posts = result[0] if result else 0
            print(f"✓ Total de publicaciones: {total_posts}")
            
            cursor.execute("SELECT COUNT(*) FROM publicaciones WHERE activa = 1")
            result = cursor.fetchone()
            active_posts = result[0] if result else 0
            print(f"✓ Publicaciones activas: {active_posts}")
            
            # Mostrar algunas publicaciones de ejemplo
            cursor.execute("SELECT TOP 3 id, usuario_id, contenido, activa FROM publicaciones")
            sample_posts = cursor.fetchall()
            print(f"✓ Ejemplos de publicaciones: {sample_posts}")
            
        except Exception as e:
            print(f"✗ Error consultando publicaciones: {e}")
        
        # Verificar tabla me_gusta
        try:
            cursor.execute("SELECT COUNT(*) FROM me_gusta")
            result = cursor.fetchone()
            likes_count = result[0] if result else 0
            print(f"✓ Total de likes: {likes_count}")
        except Exception as e:
            print(f"✗ Error consultando likes: {e}")
        
        # Verificar tabla comentarios
        try:
            cursor.execute("SELECT COUNT(*) FROM comentarios")
            result = cursor.fetchone()
            comments_count = result[0] if result else 0
            print(f"✓ Total de comentarios: {comments_count}")
        except Exception as e:
            print(f"✗ Error consultando comentarios: {e}")
        
        if conn:
            conn.close()
        print("=== FIN DEBUGGING ===") 