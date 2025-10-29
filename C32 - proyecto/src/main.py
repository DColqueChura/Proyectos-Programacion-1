'''
1. Tome dos parámetros de entrada; un archivo de configuración y un 
string “json” o “toml” de forma que el primer parámetro sea leído de 
acuerdo al formato estipulado por el segundo parámetro. Si estos 
parámetro no son hallados, el formato por defecto debe ser toml y el 
nombre del archivo config.toml, y 
2. el archivo debe determinar el nombre del archivo de entrada y el de 
salida, ambos serán leídos/escritos en formato csv, tal como se hizo 
con anterioridad. Ejemplo de archivo de configuración en formato toml: 
  
[configuracion] 
entrada = “nombre_del_archivo_de_entrada” 
salida = “nombre_del_archivo_de_salida”

Aceptá dos esquemas de config: plano (entrada/salida) o anidado (configuracion.entrada/salida).
'''

import sys
from .funciones import obtener_args, leer_archivo, extraer_entrada_salida
from .errors import ErrorAperturaArchivo, ErrorDesconocido 

# Recordar Ejecución: python3 -m src.main <configuracion> <formato>

# Códigos de error:
# -1: Cantidad de argumentos incorrecta (no lo usaremos si aplicamos defaults)
# -2: El segundo argumento debe ser 'toml' o 'json'
# -3: Error desconocido
# -4: Error de apertura/lectura de archivo (incluye decode)

def main():
    # Pedir Archivos de entrada
    configuracion, formato = obtener_args()
    
    # Validación explícita del formato
    if formato not in ("toml", "json"):
        sys.stderr.write("Error: el segundo argumento debe ser 'toml' o 'json'.\n")
        sys.exit(-2)

    try:
        archivo_formateado = leer_archivo(configuracion, formato)       
        entrada, salida = extraer_entrada_salida(archivo_formateado)
    except ErrorAperturaArchivo:
        # Mensaje detallado ya se imprimió en funciones.py o lo imprime Python (decode/permiso)
        sys.exit(-4)
    except ErrorDesconocido:
        sys.stderr.write("Error desconocido.\n")
        sys.exit(-3)
    
    print(f"Archivo de entrada: {entrada}")
    print(f"Archivo de salida: {salida}")

if __name__ == '__main__':
    main()
      
