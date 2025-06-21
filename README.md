# EDP_TP_Grupo1
Sistema de Transporte
# Sistema de Transporte - Grupo 1

## ¿Qué hace nuestro proyecto?

Este sistema encuentra la ruta más rápida y la más barata para transportar carga entre nodos que representan algunas ciudades de Argentina. 

El sistema considera los siguientes modos de transporte: camiones, trenes, barcos y aviones.

Priorizamos la legibilidad y la modularidad del proyecto, por esto armamos una gran cantidad de archivos, intentando separar o seccionar el código lo más posible, acorde a los principios de la programación orientada a objetos.

## Funcionamiento

Paso 1: carga de datos desde los archivos CSV
Paso 2: Análisis de todas las rutas posibles entre ciudades
Paso 3: Encuentra la mejor opción usando algoritmos 
Paso 4: Muestra los resultados de la optimización de tiempo y costo



## 📋 Ejemplo de resultado

```
===== OPTIMIZACIÓN POR TIEMPO =====
Ruta: Zarate -> Buenos_Aires -> Mar_del_Plata
1. Zarate -> Buenos_Aires (Ferroviaria): 85km, 0h 51min, $180.00
2. Buenos_Aires -> Mar_del_Plata (Ferroviaria): 384km, 3h 50min, $779.60
TOTAL: Tiempo: 4h 41min | Costo: $959.60
```

## 🔧 Estructura del código

### Clases principales
  - `Vehiculo` - abarca todos los comportamientos y atributos comúnes entre vehículos
    - `Tren` - hereda de la clase vehículo y contempla descuentos por distancia
    - `Camion` - hereda de la clase vehículo y contempla sobrecosto por peso
    - `Barco` - hereda de la clase vehículo y contempla la diferencia fluvial/marítimo
    - `Avion` - hereda de la clase vehículo y contempla los efectos adversos por clima

- `Nodo` - representa una ciudad, un punto en el mapa
- `Conexion` - representa una ruta entre nodos e incluye atributos como la distancia y la restricción (si la hay)
- **`Planificador`** - construye y compara las rutas posibles y encuentra las óptimas
- **`Itinerario`** - presenta el resultado final del viaje

### Restricciones que maneja
- **Velocidad máxima** en ciertos tramos de tren
- **Peso máximo** en puentes específicos
- **Tipo de navegación** (río vs océano)
- **Probabilidad de mal tiempo** para aviones





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