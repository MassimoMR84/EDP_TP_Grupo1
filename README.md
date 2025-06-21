Estructura de Datos y Progrmación - Comisión C - Grupo 1
Sistema de Transporte

## Objeivo del proyecto

Encontrar un sistema que encuentre la mejor ruta para transportar carga entre ciudades de Argentina. La "mejor ruta" puede definirse de dos formas:
- La que se recorra en menos tiempo (optimización por tiempo)
- La que tenga el costo más bajo (optimización por costo)


## Funcionamiento

Paso 1: carga de datos desde los archivos CSV
Paso 2: Análisis de todas las rutas posibles entre ciudades
Paso 3: Encuentra la mejor opción usando algoritmos 
Paso 4: Muestra los resultados de la optimización de tiempo y costo


## Ejemplo de resultado

```
===== OPTIMIZACIÓN POR TIEMPO =====
Ruta: Zarate -> Buenos_Aires -> Mar_del_Plata
1. Zarate -> Buenos_Aires (Ferroviaria): 85km, 0h 51min, $180.00
2. Buenos_Aires -> Mar_del_Plata (Ferroviaria): 384km, 3h 50min, $779.60
TOTAL: Tiempo: 4h 41min | Costo: $959.60
```

## Clases principales
  - `Vehiculo` - abarca todos los comportamientos y atributos comúnes entre vehículos
    - `Tren` - hereda de la clase vehículo y contempla descuentos por distancia
    - `Camion` - hereda de la clase vehículo y contempla sobrecosto por peso
    - `Barco` - hereda de la clase vehículo y contempla la diferencia fluvial/marítimo
    - `Avion` - hereda de la clase vehículo y contempla los efectos adversos por clima

- `Nodo` - representa una ciudad, un punto en el mapa
- `Conexion` - representa una ruta entre nodos e incluye atributos como la distancia y la restricción (si la hay)
- `Planificador` - construye y compara las rutas posibles y encuentra las óptimas
- `Itinerario` - presenta el resultado final del viaje

## Restricciones posibles 
- Velocidad máxima en ciertos tramos de tren
- Peso máximo en puentes específicos que pueden recorrer los camiones 
- Tipo de navegación (diferencia entre marítimo y fluvial)
- Probabilidad de mal tiempo para aviones (afecta su velocidad)


## Aprendizajes del proyecto: problemas resueltos

1. ¿Cómo repartir una carga que no entra en un único vehículo? --> se reparte la carga
2. Algunos caminos tienen límites específicos --> aplicar restricciones para evitar problemas
3. Usar un mismo algoritmo para optimizar por tiempo y costo
4. Manejo de errores (falta de archivos o datos incorrectos)