import sys
#import csv
from .funciones import procesar_archivo 
from .errors import ErrorAperturaArchivo, ErrorDesconocido

# Recordar Ejecución: python3 -m src.main src/input_num.txt

# Códigos de error:
# -1: Cantidad de argumentos incorrecta
# -2: Los argumentos 2 y 3 deben ser enteros >= 0
# -3: Error desconocido
# -4: Error de apertura de archivo

def main():
    # 1) Parseo de argumentos
    try:
        file = sys.argv[1]
    
    except IndexError:
        sys.stderr.write("Error de Invocación: se esperaba 1 argumento.\n")
        print("Se espera: un archivo de entrada en formato .csv")
        sys.exit(-1)
    except Exception:
        sys.stderr.write("Error desconocido.\n")
        sys.exit(-3)
    else:        
        # 2) Lectura del archivo y obtención de lista de productos (con mis excepciones creadas en errors.py)
        try:
            procesar_archivo(file)

        except (ErrorAperturaArchivo, ErrorDesconocido):
            # Los mensajes los escribe procesar_archivo por stderr
            sys.exit(-4)    
        except Exception:
            sys.stderr.write("Error desconocido.\n")
            sys.exit(-3)
        else:
            exit(0)
        
    finally:
        print("Bye Bye!")

if __name__ == '__main__':
    main()

