import unittest
from src.errors import ErrorAperturaArchivo, ErrorDesconocido
from src.funciones import obtener_args, leer_archivo, extraer_entrada_salida, exigir_csv, procesar_csv

class Test_obtener_args(unittest.TestCase):
    def test_obtener_args_default(self):
        args = obtener_args([])
        self.assertEqual(args, ('src/config.toml', 'toml')) 
    
    def test_obtener_args_custom(self):
        args = obtener_args(['src/custom_config.json', 'json'])
        self.assertEqual(args, ('src/custom_config.json', 'json'))
    
    def test_obtener_args_invalid(self):
        with self.assertRaises(SystemExit) as cm:
            obtener_args(['only_one_arg'])
        self.assertEqual(cm.exception.code, -1)   

'''
class Test_leer_archivo(unittest.TestCase):


class Test_extraer_entrada_salida(unittest.TestCase):


class Test_exigir_csv(unittest.TestCase):


class Test_procesar_csv(unittest.TestCase):
'''

if __name__ == '__main__':
    unittest.main()