import sys
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .errors import ErrorAperturaArchivo, ErrorNombre, ErrorDesconocido

def procesar_archivo(file: str):
    ''' Esta comprobación se hace en la función main().
    
    if not file.endswith('.csv'):
        raise ErrorNombre(f"Formato incorrecto: {file}\n")
    '''
    
    try:
        filename_out = file.rsplit('.', 1)[0] + '_por_producto.csv'
        colum_out = ['Producto', 'Fecha de Inicio', 'Fecha Final', 'Cantidad', 'Valor Total']

        with open(file, 'r', encoding = 'utf-8', newline= '') as input_csv, \
            open(filename_out, 'w', encoding ='utf-8', newline='') as output_csv:
    
            lector = csv.DictReader(input_csv)

            esperados = {'Fecha', 'Producto', 'Cantidad', 'ValorUnitario'}
            encontrados = { (header or '').strip() for header in (lector.fieldnames or []) }

            if not esperados.issubset(encontrados):
                raise ErrorAperturaArchivo(f"Encabezados inválidos. Esperados: {sorted(esperados)}. Encontrados: {sorted(encontrados)}")

            escritor = csv.DictWriter(output_csv, fieldnames=colum_out)
            escritor.writeheader()    # Escribe los nombres de las columnas
            
            # Acumulador por producto
            productos_dict = {} # producto -> {'fecha_inicio': date, 'fecha_fin': date, 'cantidad': int, 'valor_total': float}

            for fila in lector:
                #Obtención y preparación de datos por fila
                producto = fila.get('Producto','').strip() #Trae valores de forma segura
                if not producto:
                    continue
                
                fecha = fila.get('Fecha','').strip()
                try:
                    fecha = datetime.strptime(fecha, '%Y-%m-%d').date() #solo la fecha No la hora, porque no la especifico
                except ValueError:
                    #sys.stderr.write("Error de input: fecha inválida en " + file + '\n')
                    raise ErrorAperturaArchivo()
                
                try:
                    cantidad = int(fila.get('Cantidad', '0').strip() or 0)
                except (ValueError, TypeError):
                    cantidad = 0

                vu = (fila.get('ValorUnitario','0').strip().replace(',', '.') or 0.0)
                try:
                    vu = Decimal(vu)    
                except (InvalidOperation, ValueError):
                    vu = Decimal('0.0')

                #Acumular
                if producto not in productos_dict:   
                    # Si el producto no existe. Acumular por producto
                    productos_dict[producto] = {
                        'fecha_inicio': fecha,
                        'fecha_fin'   : fecha,
                        'cantidad'    : cantidad,
                        'valor_total' : cantidad * vu
                    }
                else:
                    p = productos_dict[producto]
                    p['fecha_inicio'] = min(p['fecha_inicio'], fecha)
                    p['fecha_fin']    = max(p['fecha_fin'], fecha)
                    p['cantidad']    += cantidad
                    p['valor_total'] += (Decimal(cantidad) * vu)
                    
            # Escritura final
            for producto, data in sorted(productos_dict.items()):
                # Formateo seguro de dinero a 2 decimales
                total_2d = data['valor_total'].quantize(Decimal('0.01'))

                escritor.writerow({
                    'Producto': producto,
                    'Fecha de Inicio': data['fecha_inicio'].strftime('%Y-%m-%d'),
                    'Fecha Final': data['fecha_fin'].strftime('%Y-%m-%d'),
                    'Cantidad': data['cantidad'],
                    'Valor Total': f"{total_2d}",
                })
        return
    
    except (ErrorAperturaArchivo, ErrorNombre):
        # Dejo pasar las excepciones propias sin convertirlas a ErrorDesconocido
        raise
    except FileNotFoundError:
        sys.stderr.write("Error de input: no existe el archivo " + file + '\n')
        raise ErrorAperturaArchivo(f"No existe: {file}\n")
    
    except PermissionError:
        sys.stderr.write(f"Error de valor leído del input {file}.\n")
        raise ErrorAperturaArchivo(f"Sin permisos: {file}.\n")
    
    except LookupError as e:
        sys.stderr.write(f"Error de codificación al leer {file}: {e}\n")
        raise ErrorAperturaArchivo(f"Codificación inválida en: {file}\n")
    
    except Exception as e:
        sys.stderr.write("Error desconocido\n")
        raise ErrorDesconocido(str(e))
    
