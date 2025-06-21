# EDP_TP_Grupo1
Sistema de Transporte
# Sistema de Transporte - Grupo 1

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





### Cargas muy pesadas
Si una carga es muy pesada para un solo vehículo, automáticamente usa varios:
- 70,000 kg en camiones → usa 3 camiones de 30,000 kg cada uno

### Restricciones de peso
Si un puente no soporta el peso, busca rutas alternativas:
- Puente límite 15,000 kg → carga de 20,000 kg busca otra ruta

### Mal clima
Los aviones pueden ir más lento si hay mal tiempo:
- Velocidad normal: 600 km/h
- Con mal tiempo: 400 km/h

## Lo que aprendimos haciendo este proyecto

### Problemas que resolvimos
1. **Múltiples vehículos** - ¿Cómo repartir carga que no entra en uno solo?
2. **Restricciones por ruta** - Algunos caminos tienen límites específicos
3. **Optimización dual** - Mismo algoritmo para tiempo y costo
4. **Manejo de errores** - ¿Qué pasa si faltan archivos o datos incorrectos?




**Hecho con por Grupo 1 - Estructura de Datos y Programación**