# Sistema de Transporte - Grupo 1

## 🚛 ¿Qué hace este proyecto?

Este sistema encuentra la **mejor ruta** para transportar carga entre ciudades de Argentina. Puedes optimizar por:
- **⏱️ Tiempo más rápido** (para envíos urgentes)
- **💰 Costo más barato** (para maximizar ganancias)

El sistema considera diferentes tipos de transporte: camiones, trenes, barcos y aviones.

## 🚀 Cómo ejecutar el programa

### Requisitos
- Python 3.6 o superior
- Archivos CSV con los datos (incluidos en el proyecto)

### Ejecución básica
```bash
python main.py
```

### Para ver gráficos (opcional)
```bash
pip install matplotlib
python main.py
```

## 📁 Archivos importantes

- **`main.py`** - Ejecuta todo el sistema
- **`nodos.csv`** - Lista de ciudades
- **`conexiones.csv`** - Rutas entre ciudades con restricciones
- **`solicitudes.csv`** - Qué cargas transportar

## 🎯 Cómo funciona

1. **Carga los datos** desde los archivos CSV
2. **Analiza todas las rutas** posibles entre ciudades
3. **Encuentra la mejor opción** usando algoritmos inteligentes
4. **Muestra el resultado** con detalles de tiempo y costo

## 🚗 Tipos de vehículos

| Vehículo | Velocidad | Capacidad | Mejor para |
|----------|-----------|-----------|------------|
| 🚛 Camión | 80 km/h | 30,000 kg | Flexibilidad |
| 🚂 Tren | 100 km/h | 150,000 kg | Cargas pesadas |
| 🚢 Barco | 40 km/h | 100,000 kg | Costo bajo |
| ✈️ Avión | 600 km/h | 5,000 kg | Urgente |

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
- **`Vehiculo`** - Comportamiento común (tiempo, costo)
  - `Tren` - Descuentos por distancia
  - `Camion` - Sobrecosto por peso
  - `Barco` - Diferencia fluvial/marítimo
  - `Avion` - Afectado por clima

- **`Nodo`** - Representa una ciudad
- **`Conexion`** - Ruta entre ciudades con restricciones
- **`Planificador`** - Encuentra rutas óptimas
- **`Itinerario`** - Resultado final del viaje

### Restricciones que maneja
- **Velocidad máxima** en ciertos tramos de tren
- **Peso máximo** en puentes específicos
- **Tipo de navegación** (río vs océano)
- **Probabilidad de mal tiempo** para aviones

## 🎨 Gráficos (si tienes matplotlib)

El sistema puede generar gráficos para visualizar:
- Progreso del viaje (distancia vs tiempo)
- Costo acumulado por kilómetro
- Comparación entre diferentes rutas

## ⚠️ Casos especiales que resuelve

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

## 🎓 Lo que aprendimos haciendo este proyecto

### Problemas que resolvimos
1. **Múltiples vehículos** - ¿Cómo repartir carga que no entra en uno solo?
2. **Restricciones por ruta** - Algunos caminos tienen límites específicos
3. **Optimización dual** - Mismo algoritmo para tiempo y costo
4. **Manejo de errores** - ¿Qué pasa si faltan archivos o datos incorrectos?

### Decisiones técnicas importantes
- Usamos **Dijkstra** porque garantiza la mejor solución
- **Llenar vehículos** al máximo antes de agregar otro (más realista)
- **Validar todo** antes de procesar (evita errores raros)
- **Gráficos opcionales** (funciona sin matplotlib)

## 🏃‍♂️ Empezar rápido

1. Descargar el proyecto
2. Ejecutar `python main.py`
3. Ver los resultados en pantalla
4. (Opcional) Instalar matplotlib para gráficos

¡Eso es todo! El sistema hace el resto automáticamente.

---

**Hecho con 💻 por Grupo 1 - Estructura de Datos y Programación**