# Sistema de Transporte - Grupo 1

## Qué hace este proyecto

Básicamente es un sistema que calcula la mejor ruta para transportar carga entre ciudades usando diferentes tipos de vehículos (trenes, camiones, barcos, aviones). Podés optimizar por tiempo (más rápido) o por costo (más barato).

## Cómo funciona

El sistema lee tres archivos CSV:
- `nodos.csv`: las ciudades
- `conexiones.csv`: las rutas entre ciudades con sus restricciones
- `solicitudes.csv`: qué querés transportar y adónde

Después usa el algoritmo de Dijkstra para encontrar el mejor camino según lo que elijas.

## Ejecutar el programa

```bash
python main.py
```

Si querés gráficos (opcional):
```bash
pip install matplotlib
```

## Estructura del código

### Clases principales

**Vehiculo**: Clase base para todos los vehículos
- `Tren`: Para vías de ferrocarril (alta capacidad, a veces limitado por velocidad)
- `Camion`: Para rutas/autopistas (flexible, limitado por peso en algunos puentes)
- `Barco`: Para rutas marítimas/fluviales (capacidad alta, costos diferentes)
- `Avion`: Para rutas aéreas (rápido, afectado por mal tiempo)

**Nodo**: Representa una ciudad o punto en la red

**Conexion**: Una ruta entre dos nodos. Puede tener restricciones como:
- Velocidad máxima (para trenes)
- Peso máximo (para camiones en ciertos puentes)
- Tipo de navegación (fluvial vs marítimo)
- Probabilidad de mal tiempo (para aviones)

**Planificador**: El cerebro del sistema. Usa Dijkstra para encontrar rutas óptimas.

**Itinerario**: El resultado final con todos los tramos del viaje.

## Problemas que nos encontramos desarrollando

### Restricciones por tipo de transporte

Al principio pensamos en poner las restricciones en cada vehículo, pero nos dimos cuenta que era mejor ponerlas en las conexiones. Por ejemplo, un tren puede ir a 100 km/h normalmente, pero en cierta vía específica está limitado a 80 km/h. Eso es más fácil de manejar si está en la conexión.

### Manejo de múltiples vehículos

Cuando la carga es muy pesada para un solo vehículo, el sistema automáticamente calcula cuántos necesitás. Primero llena cada vehículo al máximo antes de agregar otro. Esto complicó los cálculos de costo porque hay que considerar el costo fijo de cada vehículo extra.

### Algoritmo de optimización

Usar Dijkstra para dos KPIs diferentes (tiempo vs costo) fue medio complicado. Terminamos haciendo que el algoritmo cambie la función de costo según lo que querés optimizar. Para tiempo usa `distancia/velocidad`, para costo usa la fórmula completa de costos.

### Validaciones

Nos fuimos un poco al pasto con las validaciones al principio. Ahora están más simplificadas pero siguen cubriendo los casos importantes.

## Archivos importantes

- `main.py`: Punto de entrada, carga todo y ejecuta el procesamiento
- `planificador.py`: Contiene el algoritmo de Dijkstra y la lógica de optimización
- `vehiculos.py`: Definiciones de todos los tipos de vehículos
- `conexion.py`: Maneja las rutas y sus restricciones
- `validaciones.py`: Funciones para validar datos de entrada

## Ejemplo de uso

El sistema puede manejar solicitudes como:
- Transportar 70,000 kg de Zárate a Mar del Plata
- Optimizar por tiempo: probablemente use tren (rápido, alta capacidad)
- Optimizar por costo: probablemente use camión (más barato)

## Limitaciones conocidas

- Los gráficos son opcionales (requieren matplotlib)
- Solo maneja rutas de ida (no considera regreso)
- No considera horarios específicos de partida
- Las probabilidades de mal tiempo se calculan al azar

## Para extender el proyecto

Si querés agregar nuevos tipos de vehículos:
1. Crear nueva clase que herede de `Vehiculo`
2. Agregar el tipo al mapeo en `planificador.py`
3. Definir nuevas restricciones en `validaciones.py` si es necesario

El código está pensado para ser extensible, así que debería ser relativamente fácil agregar funcionalidad nueva.