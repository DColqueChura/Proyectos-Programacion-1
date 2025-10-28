import unittest
import os
import csv

from src.funciones import procesar_archivo
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

    def test_extension_incorrecta(self):
        path = self._write_file("ventas.txt", VENTAS_OK)
        with self.assertRaises(ErrorNombre):
            procesar_archivo(path)
    
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
        self.assertEqual(rows[0]['Valor Total'], '7.20')
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

if __name__ == '__main__':
    unittest.main()
