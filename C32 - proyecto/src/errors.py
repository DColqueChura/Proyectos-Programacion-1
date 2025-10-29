# Excepciones propias. Declaradas como clases. Heredan de Exception.

class ErrorAperturaArchivo(Exception):
    """No se pudo abrir/leer el archivo (no existe, sin permisos, etc.)."""
    pass

class ErrorDesconocido(Exception):
    """Error no contemplado."""
    pass
