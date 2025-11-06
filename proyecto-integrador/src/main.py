import sys

from .funciones_toml_json import obtener_args, leer_archivo, extraer_entrada_salida, exigir_csv, procesar_csv
from .funciones_csv import clave_valor_total, procesar_archivo, leer_csv, escribir_csv_desde_diccionarios
from .funciones_orden import ordenar as merge_sort
from .errors import ErrorAperturaArchivo, ErrorNombre, ErrorDesconocido

# Recordar Ejecución: python3 -m src.main --config_file src/<configuracion> --formato <formato>

# Códigos de error:
# -1: Cantidad de argumentos incorrecta (no lo usaremos si aplicamos defaults)
# -2: El segundo argumento debe ser 'toml' o 'json'
# -3: Error desconocido
# -4: Error de apertura/lectura de archivo (incluye decode)

def main():

    ###########################
    ## Procesamiento TOML/JSON
    ###########################

    configuracion_file, formato = obtener_args()
    #print(f"Archivo de configuración : {configuracion_file}")
    #print(f"Formato de configuración : {formato}")  

    if formato not in ("toml", "json"):
        sys.stderr.write(f"Error: formato inválido \n")
        sys.exit(-2)

    try:
        archivo_formateado = leer_archivo(configuracion_file, formato)
        entrada, salida = extraer_entrada_salida(archivo_formateado)

    except ErrorAperturaArchivo as e:
        sys.stderr.write(f"ErrorAperturaArchivo: {e}\n")
        sys.exit(-4)

    except ErrorDesconocido as e:
        sys.stderr.write(f"ErrorDesconocido: {e}\n")
        sys.exit(-3)

    # Extracción de paths
    print(f"Archivo de entrada: {entrada}")
    print(f"Archivo de salida: {salida}")

    ###########################################
    # Procesamiento CSV (agrupado por producto)
    ###########################################

    # Validar que los archivos sean CSV
    exigir_csv(entrada, salida)

    try:
        resultado_csv = procesar_archivo(entrada)

    except (ErrorAperturaArchivo, ErrorDesconocido):
        # Los mensajes los escribe procesar_archivo por stderr
        sys.exit(-4)    
    except Exception:
        sys.stderr.write("Error desconocido.\n")
        sys.exit(-3)

    #############################################
    # Ordenamiento MergeSort (en orden decreciente)
    #############################################

    # Leer el CSV generado (devuelve lista de diccionarios)
    filas = leer_csv(resultado_csv)

    try:
        # Ordenar por Valor Total usando la función clave_valor_total
        filas_ordenadas = merge_sort(filas, clave = clave_valor_total)
        print(f"Ordenamiento completado. Se ordenaron {len(filas_ordenadas)} filas.")
        print(filas_ordenadas)
        
        # Escribir el archivo de salida final usando `salida` del config
        escribir_csv_desde_diccionarios(filas_ordenadas, salida)
        print(f"Escritura del archivo de salida: {salida}")

    except Exception:
        sys.stderr.write("Error desconocido durante el ordenamiento.\n")
        sys.exit(-3)

    
if __name__ == '__main__':
    main()