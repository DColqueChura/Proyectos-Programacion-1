import unittest
from src.errors import ErrorAperturaArchivo, ErrorDesconocido
from src.funciones import obtener_args, leer_archivo, extraer_entrada_salida, exigir_csv, procesar_csv

#Comando para ejecutar: python -m unittest discover test

# Códigos de error:
# 2: Error de parseo
# -1: Cantidad de argumentos incorrecta (no lo usaremos si aplicamos defaults)
# -2: El segundo argumento debe ser 'toml' o 'json'
# -3: Error desconocido
# -4: Error de apertura/lectura de archivo (incluye decode)


class Test_obtener_args(unittest.TestCase):

    def test_obtener_args_default(self):
        args = obtener_args([])
        self.assertEqual(args, ('./config.toml', 'toml'))
    
    def test_obtener_args_valido(self):
        args = obtener_args(['--config_file', './mi.json', '--formato', 'json'])
        self.assertEqual(args, ('./mi.json', 'json'))

    def test_obtener_args_invalido(self):
        with self.assertRaises(SystemExit) as cm:
            obtener_args(['--config_file'])
        self.assertEqual(cm.exception.code, 2)   


class Test_leer_archivo(unittest.TestCase):
    def test_leer_archivo_toml_valido(self):
        config = leer_archivo('src/config.toml', 'toml')
        self.assertIsInstance(config, dict)
        self.assertIn('configuracion', config)

    def test_leer_archivo_json_valido(self):
        config = leer_archivo('src/config.json', 'json')
        self.assertIsInstance(config, dict)
        self.assertIn('configuracion', config)

    def test_leer_archivo_no_existente(self):
        with self.assertRaises(ErrorAperturaArchivo):
            leer_archivo('src/no_existe.toml', 'toml')

'''
class Test_extraer_entrada_salida(unittest.TestCase):
    def 



class Test_exigir_csv(unittest.TestCase):

class Test_procesar_csv(unittest.TestCase):
'''

if __name__ == '__main__':
    unittest.main()