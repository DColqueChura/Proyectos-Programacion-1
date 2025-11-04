import sys

from .funciones_toml_json import obtener_args, leer_archivo, extraer_entrada_salida, exigir_csv, procesar_csv
from .funciones_csv import procesar_archivo
from .errors import ErrorAperturaArchivo, ErrorNombre, ErrorDesconocido

# Recordar Ejecución: python3 -m src.main --config_file src/config --formato json

# Códigos de error:
# -1: Cantidad de argumentos incorrecta (no lo usaremos si aplicamos defaults)
# -2: El segundo argumento debe ser 'toml' o 'json'
# -3: Error desconocido
# -4: Error de apertura/lectura de archivo (incluye decode)

def main():
    configuracion_file, formato = obtener_args()
    print(f"Archivo de configuración: {configuracion_file}")
    print(f"Formato de configuración: {formato}")

if __name__ == '__main__':
    main()