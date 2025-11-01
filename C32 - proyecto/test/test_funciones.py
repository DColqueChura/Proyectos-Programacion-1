import unittest
import tempfile
import os

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


class Test_extraer_entrada_salida(unittest.TestCase):
    def test_extraer_entrada_salida_valido(self):
        config_data ={
            "configuracion": {
                "entrada": "src/in.csv",
                "salida": "src/out.csv"
            }
        }
        entrada, salida = extraer_entrada_salida(config_data)
        self.assertEqual(entrada, 'src/in.csv')
        self.assertEqual(salida, 'src/out.csv')
    
    def test_extraer_entrada_salida_no_existente(self):
        config_data ={
            "configuracion": {
                "entrada": "src/in.csv",
                #"salida": "src/out.csv"
            }
        }
        with self.assertRaises(SystemExit) as cm:
            extraer_entrada_salida(config_data)
            self.assertEqual(cm.exception.code, -4)

    def test_extraer_entrada_salida_invalido(self):
        with self.assertRaises(SystemExit) as cm:
            extraer_entrada_salida(config_data={})
            self.assertEqual(cm.exception.code, -3)
    

class Test_exigir_csv(unittest.TestCase):
    def test_exigir_csv_valido(self):
        try:
            exigir_csv('data/input.csv', 'data/output.csv')
        except SystemExit:
            self.fail("exigir_csv levantó un SystemExit inexplicablemente!")
    
    def test_exigir_csv_salida_No_csv(self):
        try:
            exigir_csv('data/input.csv', 'data/output.txt')
        except SystemExit:
            self.fail("exigir_csv levantó un SystemExit inexplicablemente!")


class Test_procesar_csv(unittest.TestCase):
    def test_procesar_csv_valido(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.csv")
            output_file = os.path.join(tmpdir, "output.csv")

            # Crear CSV de prueba
            with open(input_file, "w", encoding="utf-8", newline="") as f:
                f.write("col1,col2,col3\n")
                f.write("1,2,3\n")
                f.write("4,5,6\n")

            # Ejecutar función
            try:
                procesar_csv(input_file, output_file)
            except Exception as e:
                self.fail(f"procesar_csv lanzó una excepción inesperada: {e}")

            # Verificar salida
            self.assertTrue(os.path.exists(output_file), "No se creó el archivo de salida")

            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("col1,col2,col3", content)


if __name__ == '__main__':
    unittest.main()