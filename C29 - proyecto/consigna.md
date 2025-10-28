Ejercicio: 

Escriba un proyecto que desarrolle un artefacto de software 
que tome por parámetro un archivo en formato csv, 
cuyo encabezado esté formado por nombres: 
‘Fecha’,’Producto’,’Cantidad’,‘ValorUnitario’

El programa debe acumular las ventas por producto. 

Ayuda: crear un diccionario cuya clave sea el producto y 
        use el valor asociado para almacenar:

a. la fecha de inicio de las ventas de ese producto: la fecha de la primera venta del producto,
b. la fecha de finalización de las ventas: la fecha de la última venta del producto,
c. acumular la cantidad vendida y
d. el valor total vendido

Finalmente se debe almacenar los datos del diccionario en un archivo en formato csv.

Observación: ¡usar todo lo que saben: excepciones, testing, parámetros de programa y 
manejo de archivos en formato csv usando csv!

Tarea adicional: usar la biblioteca datetime para el manejo de fechas. 
        DeepSeek: Can you provide a summary of the date time library?

------------
Desarrollo

Archivo inicial: Fecha,Producto,Cantidad,ValorUnitario
Archivo final: Producto, Fecha de Inicio, Fecha Final, Cantidad, Valor Total
