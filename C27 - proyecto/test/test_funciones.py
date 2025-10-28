import unittest
from src.errors import ErrorAperturaArchivo, ErrorValor
from src.funciones import leer_archivo, sublista, suma, promedio

class Test_leer_archivo(unittest.TestCase):
    def test_file_not_found(self):
        # Archivo que no existe
        filename = "test/test_FileNotFoundError_exception_file.txt"
        self.assertRaises(ErrorAperturaArchivo, leer_archivo, filename)
    
    def test_permission_error_exception(self):
        filename = "test/test_FileNotFoundError_exception_file.txt"
        self.assertRaises(ErrorAperturaArchivo, leer_archivo, filename)
    
    def test_value_error_exception(self):
        # Archivo con un valor inválido
        filename = "test/test_ValorInvalido_file.txt"
        self.assertRaises(ErrorValor, leer_archivo, filename)

    def test_una_linea(self):
        filename = "test/test_UnaLinea_file.txt"
        esperado = [23, 43, 56]
        self.assertEqual(leer_archivo(filename), esperado)
    
    def test_muchas_Lineas(self):
        filename = "test/test_MuchasLineas_file.txt"
        esperado = [23, 43, 56, 4, 56, 99, 67, 6, 0, 1]
        self.assertEqual(leer_archivo(filename), esperado)

class Test_sublista(unittest.TestCase):
    # Se ejecuta antes de cada test de esta clase.
    # Sirve para preparar datos comunes.
    def setUp(self):
        self.lista = [23,43,56,4,56,99,67,6,0,1]

    def test_indices_cambiados(self):
        inf = 5
        sup = 2
        self.assertEqual(sublista(self.lista, inf, sup), [])
    
    def test_inferior_fuera_de_rango_devuelve_vacio(self):
        self.assertEqual(sublista(self.lista, 100, 120), [])
    
    def test_superior_recortado(self):
        self.assertEqual(sublista(self.lista, 7, 50), [6,0,1])

    def test_rango_normal(self):
        self.assertEqual(sublista(self.lista, 2, 6), [56,4,56,99]) 

    def test_indices_negativos_error(self):
        self.assertRaises(ValueError, sublista, self.lista, -1, 3)

    def test_sublista_ultimo_elemento(self):
        elemento_final = sublista(self.lista, len(self.lista)-1, len(self.lista))
        self.assertEqual(elemento_final, [1])

class Test_suma(unittest.TestCase):
    def setUp(self):
        self.lista = [1,2,3,4,5,6]
    
    def test_suma_rango(self):
        self.assertEqual(suma(self.lista, 1, 4), 2+3+4)

    def test_suma_indice_superior_excede(self):
        l = [1,2,3,4,5,6]
        self.assertEqual(suma(self.lista, 1, 22), 20)
    
    def test_suma_indice_inferior_zero(self):
        l = [1,2,3,4,5,6]
        self.assertEqual(suma(self.lista, 0, 3), 6)

class Test_promedio(unittest.TestCase):
    def setUp(self):
        self.lista = [1,2,3,4,5,6]

    def test_promedio_ok(self):
        inf = 0
        sup = 3
        self.assertAlmostEqual(promedio(self.lista, inf, sup), (1+2+3)/3)

    def test_promedio_rango_vacio(self):
        inf = 5
        sup = 5
        self.assertRaises(ValueError, promedio, self.lista, inf, sup)

if __name__ == '__main__':
    unittest.main()