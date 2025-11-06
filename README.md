
# Repositorio de Proyectos en Python

Este repositorio reúne tres proyectos desarrollados como parte de las prácticas universitarias de programación en Python. Cada uno implementa manejo de errores mediante estructuras `try` y `except`, y sigue una arquitectura clara compuesta por dos carpetas principales:

* **`src/`** → Código fuente, funciones principales y módulo de errores.
* **`test/`** → Pruebas unitarias con `unittest` que validan el correcto funcionamiento del programa.

---

## 🧩 Proyectos

### **C27 – Procesamiento de números y archivo TXT**

Lee dos números y un archivo `.txt`, procesa los datos en listas y calcula el promedio de los valores dentro del intervalo definido por los números de entrada.

### **C29 – Procesamiento de archivos CSV**

Procesa un archivo `.csv` de entrada y genera un nuevo archivo de salida, agregando columnas y datos adicionales. Incluye manejo de lectura/escritura y validación de datos.

### **C32 – Procesamiento y validación de configuración**

Proyecto más reciente. Implementa lectura y validación de archivos de configuración (`.json`, `.toml`), manejo de excepciones personalizadas y pruebas unitarias robustas.

### **C33 – Proyecto Integrador: Procesamiento y Ordenamiento de CSV**
Proyecto integrador que combina conceptos de los anteriores.  
Implementa un flujo completo que:

* Lee un archivo `.csv` con ventas o registros.
* Agrupa la información por producto y genera un nuevo archivo con totales.
* Ordena los resultados mediante el algoritmo **Merge Sort**, usando funciones de clave (`clave_valor_total`) para comparar valores numéricos.
* Escribe un archivo final de salida validado.
* Aplica manejo exhaustivo de excepciones personalizadas (`ErrorNombre`, `ErrorAperturaArchivo`, `ErrorDesconocido`).
* Incluye pruebas unitarias para todas las funciones y casos de error.

---

## ⚙️ Ejecución

### 🔹 Ejecutar el programa principal

Desde la carpeta del proyecto (por ejemplo `C32 - proyecto`):

```bash
python src/main.py
```

Se debe asegurar de de que los archivos de entrada o configuración existan en las rutas esperadas por el programa.

---

### 🔹 Ejecutar los tests

Para correr todas las pruebas unitarias del proyecto:

```bash
python -m unittest discover test
```

O para ejecutar un test específico:

```bash
python -m unittest test.test_funciones
```

Para C32 - proyecto integrador

TODOS los test:
```bash
python -m unittest discover -s test -p "test_*.py"
```

UNA subcarpeta de test en específico:
```bash
python -m unittest discover -s test/<subcarpeta de test "test_"> -p "test_*.py"
```
---

## 🧠 Tecnologías y conceptos aplicados

* **Python 3.11+**
* Estructuras `try / except`
* Manejo de archivos (`.txt`, `.csv`, `.json`, `.toml`)
* Testing con `unittest`
* Algoritmos de ordenamiento (Merge Sort)
* Modularización y control de errores
* Validación y buenas prácticas de desarrollo

---

## 📂 Estructura general

```
C27 - proyecto/
C29 - proyecto/
C32 - proyecto/
│
├── src/
│   ├── funciones.py
│   ├── errores.py
│   └── main.py
└── test/
    ├── test_funciones.py
    └── test_main.py

C33 - proyecto_integrador/
│
├── src/
│   ├── funciones_csv.py
│   ├── funciones_orden.py
│   ├── funciones_toml_json.py
│   ├── errors.py
│   └── main.py
└── test/
    ├── test_funciones_csv.py
    ├── test_funciones_orden.py
    └── test_main.py

```
📊 Resultados Esperados (Proyecto Integrador)

🧾 Archivo de entrada (ventas.csv)

```csv
Fecha,Producto,Cantidad,ValorUnitario
2024-06-01,Peras,5,1.60
2024-06-03,Manzanas,3,2.00
2024-06-05,Peras,2,1.70
2024-06-10,Naranjas,4,1.80
```

⚙️ Archivo agrupado por producto (ventas_por_producto.csv)
| Producto | Fecha de Inicio | Fecha Final | Cantidad | Valor Total |
| -------- | --------------- | ----------- | -------- | ----------- |
| Manzanas | 2024-06-03      | 2024-06-03  | 3        | 6.00        |
| Naranjas | 2024-06-10      | 2024-06-10  | 4        | 7.20        |
| Peras    | 2024-06-01      | 2024-06-05  | 7        | 11.90       |

🔽 Archivo final ordenado por “Valor Total” (ventas_ordenadas.csv = out.csv)
| Producto | Fecha de Inicio | Fecha Final | Cantidad | Valor Total |
| -------- | --------------- | ----------- | -------- | ----------- |
| Peras    | 2024-06-01      | 2024-06-05  | 7        | 11.90       |
| Naranjas | 2024-06-10      | 2024-06-10  | 4        | 7.20        |
| Manzanas | 2024-06-03      | 2024-06-03  | 3        | 6.00        |

### (orden descendente por Valor Total)
---

💡 **Autor:** D. Colque Chura
📚 **Propósito:** Presentación académica (Universidad) y portafolio técnico para postulaciones en empresas de tecnología.
