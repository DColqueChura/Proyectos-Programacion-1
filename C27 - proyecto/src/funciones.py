import sys
from .errors import ErrorAperturaArchivo, ErrorValor, ErrorDesconocido

def leer_archivo(file: str) -> list[int]:
    try:
        with (open(file, 'r') as input):
            lista_num = []
            for line in input:
                line_in = (line.strip()).split(' ')
                line_in = [int(i) for i in line_in]
                lista_num.extend(line_in)
        return lista_num
    
    except FileNotFoundError:
        sys.stderr.write("Error de archivo: no existe el archivo " + file)
        raise ErrorAperturaArchivo(f"No existe: {file}")
    except PermissionError:
        sys.stderr.write(f"Error de valor leído del archivo {file}.\n")
        raise ErrorAperturaArchivo(f"Sin permisos: {file}.\n")
    except ValueError:
        sys.stderr.write(f"Error de valor leído del archivo {file}\n")
        raise ErrorValor(f"Valor inválido en {file}.\n")
    except Exception as e:
        sys.stderr.write("Error desconocido")
        raise ErrorDesconocido(str(e))
    

def sublista(l: list[int], inf: int, sup: int) -> list[int]:
    if inf < 0 or sup < 0:
        raise ValueError("Los índices deben ser >= 0")
    if inf >=sup or inf >= len(l):
        return []
    if sup >= len(l):
        inf_local = inf
        sup_local = len(l)
    return l[inf:sup]

def suma(l: list[int], inf: int, sup: int) -> int:
    """Suma de la sublista l[pos1:pos2] con mismas reglas que sublista."""
    return sum(sublista(l, inf, sup))

def promedio(l: list[int], inf: int, sup: int) -> float:
    """Promedio de l[pos1:pos2]. Lanza ValueError si el rango es vacío."""
    sl = sublista(l, inf, sup)
    if not sl:
        raise ValueError("Rango vacío; no se puede calcular promedio")
    return sum(sl) / len(sl)

