import unittest
from src.funciones_orden import ordenar as merge_sort
from src.funciones_csv import clave_valor_total

class TestMergeSort(unittest.TestCase):
    def test_lista_vacia(self):
        lista = []
        ordenada = merge_sort(lista, 'Producto')
        self.assertEqual(ordenada, [])

    def test_lista_un_elemento(self):
        lista = [{'Producto': 'Manzanas', 'Valor Total': '5.00'}]
        ordenada = merge_sort(lista, 'Producto')
        self.assertEqual(ordenada, lista)

    def test_lista_varios_elementos(self):
        lista = [
            {'Producto': 'Peras', 'Valor Total': '8.00'},
            {'Producto': 'Manzanas', 'Valor Total': '5.00'},
            {'Producto': 'Naranjas', 'Valor Total': '7.20'}
        ]
        ordenada_esperada = [
            {'Producto': 'Peras', 'Valor Total': '8.00'},
            {'Producto': 'Naranjas', 'Valor Total': '7.20'},
            {'Producto': 'Manzanas', 'Valor Total': '5.00'}
        ]
        ordenada = merge_sort(lista, clave = clave_valor_total)
        self.assertEqual(ordenada, ordenada_esperada)