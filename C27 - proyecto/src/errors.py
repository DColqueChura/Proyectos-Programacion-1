# Excepciones propias. Declaradas como clases. Heredan de Exception.

class ErrorAperturaArchivo(Exception):
    """No se pudo abrir/leer el archivo (no existe, sin permisos, etc.)."""
    pass

class ErrorValor(Exception):
    """El archivo tiene valores inválidos (no enteros)."""
    pass

class ErrorDesconocido(Exception):
    """Error no contemplado."""
    pass
