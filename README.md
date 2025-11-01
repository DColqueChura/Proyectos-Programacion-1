
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

---

## 🧠 Tecnologías y conceptos aplicados

* **Python 3.11+**
* Estructuras `try / except`
* Manejo de archivos (`.txt`, `.csv`, `.json`, `.toml`)
* Testing con `unittest`
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
```

---

💡 **Autor:** D. Colque Chura
📚 **Propósito:** Presentación académica (Universidad) y portafolio técnico para postulaciones en empresas de tecnología.
