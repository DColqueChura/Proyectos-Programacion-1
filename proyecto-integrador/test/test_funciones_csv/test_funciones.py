import unittest
import tempfile
import os
import csv

from decimal import Decimal, InvalidOperation

from src.funciones_csv import clave_valor_total, procesar_archivo, leer_csv, escribir_csv_desde_diccionarios
from src.errors import ErrorAperturaArchivo, ErrorNombre


VENTAS_OK = """Fecha,Producto,Cantidad,ValorUnitario
2025-01-03,Manzanas,10,0.50
2025-01-05,Peras,5,0.80
2025-01-08,Manzanas,7,0.55
2025-01-10,Naranjas,12,0.60
2025-01-12,Peras,9,0.85
"""

VENTAS_COMA_DECIMAL = """Fecha,Producto,Cantidad,ValorUnitario
2025-01-10,Naranjas,12,0,60
"""

VENTAS_CON_FECHA_INVALIDA = """Fecha,Producto,Cantidad,ValorUnitario
XXXX-01-03,Manzanas,10,0.50
2025-01-05,Peras,5,0.80
"""

HEADER_INVALIDO = """Fec,Prod,Cant,ValorU
2025-01-03,Manzanas,10,0.50
"""

class TestClaveValorTotal(unittest.TestCase):
    
    def test_valor_entero(self):
        fila = {'Valor Total': '1500'}
        self.assertEqual(clave_valor_total(fila), Decimal('1500'))

    def test_valor_decimal_punto(self):
        fila = {'Valor Total': '1234.56'}
        self.assertEqual(clave_valor_total(fila), Decimal('1234.56'))

    def test_valor_decimal_coma(self):
        fila = {'Valor Total': '7890,12'}
        self.assertEqual(clave_valor_total(fila), Decimal('7890.12'))

    def test_valor_con_espacios(self):
        fila = {'Valor Total': '  345.67  '}
        self.assertEqual(clave_valor_total(fila), Decimal('345.67'))

    def test_valor_invalido(self):
        fila = {'Valor Total': 'abc123'}
        self.assertEqual(clave_valor_total(fila), Decimal('0.0'))

    def test_valor_vacio(self):
        fila = {'Valor Total': ''}
        self.assertEqual(clave_valor_total(fila), Decimal('0.0'))

class TestProcesarArchivo(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test/"
        os.makedirs(self.test_dir, exist_ok=True)

    def _write_file(self, name, content):
        path = os.path.join(self.test_dir, name)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        return path

    def _read_csv(self, path):
        with open(path, "r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            return r.fieldnames, list(r)

    # ---- Tests de errores
    def test_file_not_found(self):
        fake_path = os.path.join(self.test_dir, "no_existe.csv")
        with self.assertRaises(ErrorAperturaArchivo):
            procesar_archivo(fake_path)
    
    def test_header_invalido(self):
        path = self._write_file("ventas.csv", HEADER_INVALIDO)
        with self.assertRaises(ErrorAperturaArchivo):
            procesar_archivo(path)
    
    # ---- Tests funcionales
    def test_generacion_archivo_y_cabeceras(self):
        inp = self._write_file("ventas.csv", VENTAS_OK)
        out_path = procesar_archivo(inp) or inp.replace(".csv", "_por_producto.csv")

        self.assertTrue(os.path.exists(out_path))
        headers, rows = self._read_csv(out_path)

        self.assertEqual(
            headers,
            ['Producto', 'Fecha de Inicio', 'Fecha Final', 'Cantidad', 'Valor Total'],
        )
        self.assertGreaterEqual(len(rows), 1)

    def test_acumula_por_producto_correctamente(self):
        inp = self._write_file("ventas.csv", VENTAS_OK)
        out_path = procesar_archivo(inp) or inp.replace(".csv", "_por_producto.csv")
        _, rows = self._read_csv(out_path)

        tabla = {r['Producto'].strip(): r for r in rows}

        # Manzanas
        self.assertIn('Manzanas', tabla)
        self.assertEqual(tabla['Manzanas']['Fecha de Inicio'], '2025-01-03')
        self.assertEqual(tabla['Manzanas']['Fecha Final'], '2025-01-08')
        self.assertEqual(int(tabla['Manzanas']['Cantidad']), 17)
        self.assertEqual(tabla['Manzanas']['Valor Total'], '8.85')

        # Peras
        self.assertIn('Peras', tabla)
        self.assertEqual(tabla['Peras']['Fecha de Inicio'], '2025-01-05')
        self.assertEqual(tabla['Peras']['Fecha Final'], '2025-01-12')
        self.assertEqual(int(tabla['Peras']['Cantidad']), 14)
        self.assertEqual(tabla['Peras']['Valor Total'], '11.65')

        # Naranjas
        self.assertIn('Naranjas', tabla)
        self.assertEqual(tabla['Naranjas']['Fecha de Inicio'], '2025-01-10')
        self.assertEqual(tabla['Naranjas']['Fecha Final'], '2025-01-10')
        self.assertEqual(int(tabla['Naranjas']['Cantidad']), 12)
        self.assertEqual(tabla['Naranjas']['Valor Total'], '7.20')

    def test_valor_unitario_con_coma_decimal(self):
        inp = self._write_file("ventas.csv", VENTAS_COMA_DECIMAL)
        out_path = procesar_archivo(inp) or inp.replace(".csv", "_por_producto.csv")
        _, rows = self._read_csv(out_path)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['Producto'].strip(), 'Naranjas')
        self.assertEqual(rows[0]['Valor Total'], '0.00')
    '''
    def test_salta_fila_con_fecha_invalida(self):
        inp = self._write_file("ventas.csv", VENTAS_CON_FECHA_INVALIDA)
        out_path = procesar_archivo(inp) or inp.replace(".csv", "_por_producto.csv")
        _, rows = self._read_csv(out_path)

        # Solo debe quedar Peras
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r['Producto'], 'Peras')
        self.assertEqual(r['Cantidad'], '5')
        self.assertEqual(r['Valor Total'], '4.00')
        self.assertEqual(r['Fecha de Inicio'], '2025-01-05')
        self.assertEqual(r['Fecha Final'], '2025-01-05')
    '''

class TestLeerCsv(unittest.TestCase):
    def test_leer_csv_valido(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.csv")

            # Crear CSV de prueba
            with open(input_file, "w", encoding="utf-8", newline="") as f:
                f.write("col1,col2,col3\n")
                f.write("1,2,3\n")
                f.write("4,5,6\n")

            # Ejecutar función
            try:
                filas = leer_csv(input_file)
            except Exception as e:
                self.fail(f"leer_csv lanzó una excepción inesperada: {e}")

            # Verificar contenido
            self.assertEqual(len(filas), 2)
            self.assertEqual(filas[0], {'col1': '1', 'col2': '2', 'col3': '3'})
            self.assertEqual(filas[1], {'col1': '4', 'col2': '5', 'col3': '6'})

class TestEscribirCsvDesdeDiccionarios(unittest.TestCase):
    def test_escribir_csv_desde_diccionarios(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "output.csv")
            fieldnames = ['col1', 'col2', 'col3']
            data = [
                {'col1': '1', 'col2': '2', 'col3': '3'},
                {'col1': '4', 'col2': '5', 'col3': '6'},
            ]
            
            # Ejecutar función
            try:
                escribir_csv_desde_diccionarios(data, output_file)
            except Exception as e:
                self.fail(f"escribir_csv_desde_diccionarios lanzó una excepción inesperada: {e}")

            # Verificar contenido
            with open(output_file, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                filas = list(reader)

            self.assertEqual(len(filas), 2)
            self.assertEqual(filas[0], {'col1': '1', 'col2': '2', 'col3': '3'})
            self.assertEqual(filas[1], {'col1': '4', 'col2': '5', 'col3': '6'})

if __name__ == '__main__':
    unittest.main()
