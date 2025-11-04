


def merge_sort(lista, clave):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio], clave)
    derecha = merge_sort(lista[medio:], clave)

    return combinar(izquierda, derecha, clave)

