import sys
from funciones import leer_archivo, sublista, promedio
from errors import ErrorAperturaArchivo, ErrorValor, ErrorDesconocido

# Códigos de error:
# -1: Cantidad de argumentos incorrecta
# -2: Los argumentos 2 y 3 deben ser enteros >= 0
# -3: Error desconocido

def main():
    # 1) Parseo de argumentos
    try:
        file = sys.argv[1]
        pos1 = int(sys.argv[2])
        pos2 = int(sys.argv[3])
    except IndexError:
        sys.stderr.write("Error de Invocación: se deben recibir 3 argumentos.\n")
        print("Se espera: un archivo y 2 enteros positivos")
        sys.exit(-1)
    except ValueError:
        sys.stderr.write("Error de tipo: el segundo y/o tercer argumento no son int.\n")
        sys.exit(-2)
    except Exception:
        sys.stderr.write("Error desconocido.\n")
        sys.exit(-3)
    else:
        # 2) Validación de no-negatividad
        if pos1 < 0 or pos2 < 0:
            sys.stderr.write("Error: los índices deben ser enteros >= 0\n")
            sys.exit(-2)
        
        # 3) Lectura del archivo (con mis excepciones creadas en errors.py)
        try:
            lista_num = leer_archivo(file)

        except (ErrorAperturaArchivo, ErrorDesconocido, ErrorValor):
            # Los mensajes los escribe leer_archivo por stderr
            sys.exit(-3)    
        
        # 4) Reglas del enunciado para el rango
        # - si pos2 < pos1 -> valor 0
        # - si pos1 > len(lista) -> valor 0
        # - si pos2 > len(lista) -> se recorta a len(lista)
        if pos2<pos1 or pos1>len(lista_num):
            resultado = 0
        else:
            if pos2>len(lista_num):
                pos2 = len(lista_num)

            # 5) Cálculo del promedio en el rango (se usa suma y sublista en la función promedio)
            try:
                resultado = promedio(lista_num, pos1, pos2)
            except ValueError:
                # Si el rango quedó vacío
                resultado = 0
        
        # 6) Mostrar el resultado (solo el número, claro y directo)
        print(resultado)

    finally:
        print("Bye Bye!")

if __name__ == '__main__':
    main()

