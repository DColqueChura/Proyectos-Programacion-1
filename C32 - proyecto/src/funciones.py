
import sys
import toml
import json
import csv
import argparse

from toml import TomlDecodeError
from json import JSONDecodeError
from csv import DictReader, DictWriter

from .errors import ErrorAperturaArchivo, ErrorDesconocido

# Códigos de error:
# -1: Cantidad de argumentos incorrecta (no lo usaremos si aplicamos defaults)
# -2: El segundo argumento debe ser 'toml' o 'json'
# -3: Error desconocido
# -4: Error de apertura/lectura de archivo (incluye decode)


def obtener_args(argv=None):    #si argv es None, argparse toma sys.argv[1:]).
    """
    Reglas:
    - Sin args -> defaults: config.toml toml
    - Con 2 args -> archivo y formato}
    - Con otro número -> argparse se encarga del error automáticamente.
    """

    parser = argparse.ArgumentParser(
        prog="Mi programa con argumentos",
        description="Sirve como ejemplo de cómo usar la biblioteca argparse.",
        epilog="Ejemplo: python -m programa.programa --config_file path/al/archivo/de/configuracion.json --formato json"
    )
    parser.add_argument("--config_file", type=str, default='./config.toml',
                        help='Path al archivo de configuración.')
    parser.add_argument("--formato", type=str, choices=["toml", "json"],
                        default="toml", help="Formato del archivo de configuración.")
    
    # Si argv es None, argparse usa sys.argv automáticamente
    args = parser.parse_args(argv)
    try:
        return args.config_file, (args.formato).lower()

    except SystemExit as e:
        # argparse ya imprimió el error
        sys.exit(-1)

"""
    Lee el archivo de configuración según el formato indicado.
    Lanza excepciones propias en caso de error.
    Devuelve un diccionario con la configuración.
"""
def leer_archivo(file, formato: str) -> dict:
    # Si se prefiere validar formato SOLO aquí (y no en main), descomentar:
    # if formato not in ("toml", "json"):
    #     sys.stderr.write("Error: el segundo argumento debe ser 'toml' o 'json'.\n")
    #     sys.exit(-2)

    try:
        with open(file, 'r', encoding="utf-8") as f:
            if formato == "toml":
                return toml.load(f)
            elif formato == "json":
                return json.load(f)
            else:
                # (Si) Ya se valida en main, esto no debería ocurrir
                sys.stderr.write("Error: el segundo argumento debe ser 'toml' o 'json'.\n")
                sys.exit(-2)
    except (FileNotFoundError, IOError, TomlDecodeError, JSONDecodeError) as e:
        # Propago el except para que main decida el código de salida
        raise ErrorAperturaArchivo from e
    except Exception as e:
        raise ErrorDesconocido from e
    
"""
    Soporta:
    - Plano: {'entrada': '...', 'salida': '...'}
    - Anidado: {'configuracion': {'entrada': '...', 'salida': '...'}}
"""
'''
    1. dict.get(clave, valor_por_defecto)
        Metodo que intenta devolver dict[clave],
        pero si esa clave no existe, devuelve el valor por defecto (sin lanzar error).
    2. .get() evita KeyError.
'''
def extraer_entrada_salida(config_data: dict):
    try: 
        base = config_data.get("configuracion", config_data)
        entrada = base["entrada"]
        salida = base["salida"]
        return entrada, salida

    except KeyError as e:
        sys.stderr.write(f"Falta la clave '{e.args[0]}' en el archivo de configuración.\n")
        sys.exit(-4)
    except Exception as e:
        sys.stderr.write(f"Error desconocido al extraer campos: {e}.\n")
        sys.exit(-3)
        

def exigir_csv(archivo_entrada, archivo_salida):
    if not archivo_entrada.lower().endswith('.csv'):
        sys.stderr.write("Error: El archivo de entrada debe ser un archivo CSV.\n")
        sys.exit(-4)
    
    # El archivo de salida puede no ser csv, no se exige nada aquí
    filename_out = archivo_salida.rsplit('.', 1)[0] + '.csv'
    return filename_out

def procesar_csv(file_in, file_out):
    try:
        with open(file_in, 'r', encoding = 'utf-8', newline= '') as input_csv, \
                open(file_out, 'w', encoding ='utf-8', newline='') as output_csv:

            lector = csv.DictReader(input_csv)
            _fieldnames = [ (header or '').strip() for header in (lector.fieldnames or []) ]

           # _fieldnames = list(encontrados)
            escritor = csv.DictWriter(output_csv, fieldnames=_fieldnames)
            escritor.writeheader()    # Escribe los nombres de las columnas
            for fila in lector:
                escritor.writerow(fila)
            
    except Exception as e:
        raise ErrorDesconocido(str(e))