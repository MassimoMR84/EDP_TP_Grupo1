from planificador import *
# Manejo de dependencias opcionales
try:
    import matplotlib.pyplot as plt
    from datetime import datetime
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
    print("Matplotlib no disponible. Gráficos deshabilitados.")

# Mapeo de nombres descriptivos por modo de transporte
NOMBRES_VEHICULOS = {
    'ferroviaria': 'Tren',
    'automotor': 'Camión', 
    'fluvial': 'Barco',
    'maritimo': 'Barco',
    'aerea': 'Avión'
}

def verificar_matplotlib():
    """Verifica disponibilidad de matplotlib con instrucciones de instalación"""
    if not MATPLOTLIB_DISPONIBLE:
        print("Matplotlib no instalado. Instalar con: pip install matplotlib")
        return False
    return True

def _crear_nombre_archivo(prefijo, sufijo=""):
    """Crea nombres de archivo descriptivos con timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre = f"{prefijo}"
    if sufijo:
        nombre += f"_{sufijo}"
    nombre += f"_{timestamp}"
    return f"output/{nombre}.png"

def grafico_distancia_vs_tiempo(itinerario):
    """
    Gráfico de progreso: muestra cómo avanza la distancia a lo largo del tiempo.
    Incluye marcas en cambios de tramo y etiquetas con información.
    """
    if not verificar_matplotlib():
        return
        
    if not itinerario.tramos:
        print("No hay tramos para graficar")
        return
        
    # Preparar datos acumulados (empezar en 0,0)
    tiempos_acumulados = [0]
    distancias_acumuladas = [0]
    
    tiempo_acum = 0
    distancia_acum = 0
    
    for tramo in itinerario.tramos:
        tiempo_acum += tramo.tiempo
        distancia_acum += tramo.distancia
        tiempos_acumulados.append(tiempo_acum)
        distancias_acumuladas.append(distancia_acum)
    
    # Crear gráfico
    plt.figure(figsize=(12, 7))
    plt.plot(tiempos_acumulados, distancias_acumuladas, 
             color='blue', marker='o', linewidth=2, markersize=8)
    
    # Agregar marcas en puntos de cambio de tramo
    for i, tramo in enumerate(itinerario.tramos, 1):
        nombre_vehiculo = NOMBRES_VEHICULOS.get(tramo.vehiculo.modo_de_transporte, 'Vehículo')
        plt.scatter(tiempos_acumulados[i], distancias_acumuladas[i], 
                   s=200, color='red', marker='X', zorder=5)
        
        # Etiqueta con información del tramo
        plt.annotate(f'{nombre_vehiculo}: ${tramo.costo:.0f}', 
                    (tiempos_acumulados[i], distancias_acumuladas[i]),
                    xytext=(10, 10), textcoords='offset points', 
                    fontsize=10, bbox=dict(boxstyle='round,pad=0.3', 
                    facecolor='yellow', alpha=0.7))
    
    plt.title(f'Progreso del Viaje - Optimización por {itinerario.kpi_usado.upper()}\n'
              f'Ruta: {" -> ".join(itinerario.obtener_ruta_completa())}', fontsize=16)
    plt.xlabel('Tiempo Acumulado (horas)', fontsize=12)
    plt.ylabel('Distancia Acumulada (km)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Información adicional en el gráfico
    info_text = (f'KPI: {itinerario.kpi_usado.upper()}\n'
                f'Tiempo total: {itinerario.obtener_tiempo_total_formateado()}\n'
                f'Costo total: ${itinerario.costo_total:.2f}')
    
    plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
            facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    
    # Guardar con nombre descriptivo
    ruta_nombre = "_".join(itinerario.obtener_ruta_completa())
    nombre_archivo = _crear_nombre_archivo(f"progreso_{ruta_nombre}_{itinerario.kpi_usado}")
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"Gráfico de progreso guardado: {nombre_archivo}")
    
    plt.show()

def grafico_costo_vs_distancia(itinerario):
    """
    Gráfico de eficiencia económica con marcas en cambios de tramo.
    """
    if not verificar_matplotlib():
        return
        
    if not itinerario.tramos:
        print("No hay tramos para graficar")
        return
        
    # Preparar datos acumulados
    distancias_acumuladas = [0]
    costos_acumulados = [0]
    
    distancia_acum = 0
    costo_acum = 0
    
    for tramo in itinerario.tramos:
        distancia_acum += tramo.distancia
        costo_acum += tramo.costo
        distancias_acumuladas.append(distancia_acum)
        costos_acumulados.append(costo_acum)
    
    # Crear gráfico
    plt.figure(figsize=(12, 7))
    plt.plot(distancias_acumuladas, costos_acumulados, 
             color='purple', marker='o', linewidth=2, markersize=8)
    
    # Agregar marcas en puntos de cambio de tramo
    for i, tramo in enumerate(itinerario.tramos, 1):
        nombre_vehiculo = NOMBRES_VEHICULOS.get(tramo.vehiculo.modo_de_transporte, 'Vehículo')
        plt.scatter(distancias_acumuladas[i], costos_acumulados[i], 
                   s=200, color='red', marker='X', zorder=5)
        
        # Etiqueta con información del tramo
        plt.annotate(f'{nombre_vehiculo}: {tramo.distancia}km', 
                    (distancias_acumuladas[i], costos_acumulados[i]),
                    xytext=(10, 10), textcoords='offset points', 
                    fontsize=10, bbox=dict(boxstyle='round,pad=0.3', 
                    facecolor='lightgreen', alpha=0.7))
    
    plt.title(f'Análisis de Costos - Optimización por {itinerario.kpi_usado.upper()}\n'
              f'Ruta: {" -> ".join(itinerario.obtener_ruta_completa())}', fontsize=16)
    plt.xlabel('Distancia Acumulada (km)', fontsize=12)
    plt.ylabel('Costo Acumulado ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Información adicional
    if itinerario.obtener_distancia_total() > 0:
        costo_promedio_km = itinerario.costo_total / itinerario.obtener_distancia_total()
        info_text = (f'KPI: {itinerario.kpi_usado.upper()}\n'
                    f'Costo total: ${itinerario.costo_total:.2f}\n'
                    f'Costo promedio: ${costo_promedio_km:.2f}/km')
    else:
        info_text = (f'KPI: {itinerario.kpi_usado.upper()}\n'
                    f'Costo total: ${itinerario.costo_total:.2f}')
    
    plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', 
            facecolor='lightcoral', alpha=0.8))
    
    plt.tight_layout()
    
    # Guardar con nombre descriptivo
    ruta_nombre = "_".join(itinerario.obtener_ruta_completa())
    nombre_archivo = _crear_nombre_archivo(f"costos_{ruta_nombre}_{itinerario.kpi_usado}")
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"Gráfico de costos guardado: {nombre_archivo}")
    
    plt.show()

def grafico_costo_vs_distancia_por_modo(itinerarios_optimos_por_modo, mejor_itinerario):
    """
    NUEVO: Gráfico que muestra cómo varía el costo total según la distancia 
    recorrida para cada tipo de vehículo (modo de transporte).
    """
    if not verificar_matplotlib():
        return
        
    if not itinerarios_optimos_por_modo:
        print("No hay itinerarios para graficar.")
        return

    plt.figure(figsize=(12, 8))
    
    # Colores y marcadores específicos para cada modo
    estilos_modo = {
        'ferroviaria': {'color': 'blue', 'marker': 's', 'linestyle': '-'},      # Cuadrado
        'automotor': {'color': 'green', 'marker': '^', 'linestyle': '--'},     # Triángulo
        'fluvial': {'color': 'cyan', 'marker': 'd', 'linestyle': '-.'},        # Diamante
        'maritimo': {'color': 'navy', 'marker': 'd', 'linestyle': '-.'},       # Diamante
        'aerea': {'color': 'red', 'marker': 'v', 'linestyle': ':'}             # Triángulo invertido
    }

    for modo, itinerario in itinerarios_optimos_por_modo.items():
        costos = [0]
        distancias = [0]
        costo_acumulado = 0
        distancia_acumulada = 0

        for tramo in itinerario.tramos:
            costo_acumulado += tramo.costo
            distancia_acumulada += tramo.distancia
            costos.append(costo_acumulado)
            distancias.append(distancia_acumulada)

        # Obtener estilo para este modo
        estilo = estilos_modo.get(modo, {'color': 'gray', 'marker': 'o', 'linestyle': '-'})
        nombre_vehiculo = NOMBRES_VEHICULOS.get(modo, 'Vehículo')
        
        # Resaltar el mejor itinerario
        if itinerario == mejor_itinerario:
            plt.plot(distancias, costos, 
                    label=f"★ {nombre_vehiculo.upper()} (ÓPTIMO)", 
                    linewidth=5, color='gold', marker='*', markersize=15,
                    linestyle='-', markeredgecolor='orange', markeredgewidth=2)
        else:
            plt.plot(distancias, costos, 
                    label=f"{nombre_vehiculo}", 
                    linewidth=3, color=estilo['color'], 
                    marker=estilo['marker'], markersize=10,
                    linestyle=estilo['linestyle'], alpha=0.8)

    plt.xlabel("Distancia Acumulada (km)", fontsize=12)
    plt.ylabel("Costo Acumulado ($)", fontsize=12)
    plt.title("Comparación de Costos por Modo de Transporte", fontsize=16)
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Guardar
    nombre_archivo = _crear_nombre_archivo("costo_vs_distancia_por_modo")
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"Gráfico costo vs distancia por modo guardado: {nombre_archivo}")
    
    plt.show()

def grafico_tiempo_vs_distancia_por_modo(itinerarios_optimos_por_modo, mejor_itinerario):
    """Gráfico mejorado con diferentes marcadores y mejor diferenciación visual"""
    if not itinerarios_optimos_por_modo:
        print("No hay itinerarios para graficar.")
        return

    plt.figure(figsize=(12, 8))
    
    # Colores y marcadores específicos para cada modo
    estilos_modo = {
        'ferroviaria': {'color': 'blue', 'marker': 's', 'linestyle': '-'},      # Cuadrado
        'automotor': {'color': 'green', 'marker': '^', 'linestyle': '--'},     # Triángulo
        'fluvial': {'color': 'cyan', 'marker': 'd', 'linestyle': '-.'},        # Diamante
        'maritimo': {'color': 'navy', 'marker': 'd', 'linestyle': '-.'},       # Diamante
        'aerea': {'color': 'red', 'marker': 'v', 'linestyle': ':'}             # Triángulo invertido
    }

    for modo, itinerario in itinerarios_optimos_por_modo.items():
        tiempos = [0]
        distancias = [0]
        tiempo_acumulado = 0
        distancia_acumulada = 0

        for tramo in itinerario.tramos:
            tiempo_acumulado += tramo.tiempo * 60  # pasa a minutos
            distancia_acumulada += tramo.distancia
            tiempos.append(tiempo_acumulado)
            distancias.append(distancia_acumulada)

        # Obtener estilo para este modo
        estilo = estilos_modo.get(modo, {'color': 'gray', 'marker': 'o', 'linestyle': '-'})
        nombre_vehiculo = NOMBRES_VEHICULOS.get(modo, 'Vehículo')
        
        # Resaltar el mejor itinerario
        if itinerario == mejor_itinerario:
            plt.plot(tiempos, distancias, 
                    label=f"★ {nombre_vehiculo.upper()} (ÓPTIMO)", 
                    linewidth=5, color='gold', marker='*', markersize=15,
                    linestyle='-', markeredgecolor='orange', markeredgewidth=2)
        else:
            plt.plot(tiempos, distancias, 
                    label=f"{nombre_vehiculo}", 
                    linewidth=3, color=estilo['color'], 
                    marker=estilo['marker'], markersize=10,
                    linestyle=estilo['linestyle'], alpha=0.8)

    plt.xlabel("Tiempo Acumulado (min)", fontsize=12)
    plt.ylabel("Distancia Acumulada (km)", fontsize=12)
    plt.title("Comparación de Tiempo vs Distancia por Modo", fontsize=16)
    plt.legend(fontsize=11, loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Guardar
    nombre_archivo = _crear_nombre_archivo("tiempo_vs_distancia_por_modo")
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"Gráfico tiempo vs distancia por modo guardado: {nombre_archivo}")
    
    plt.show()

def generar_todos_los_graficos(itinerario, nombre_itinerario="Itinerario"):
    """
    Genera conjunto completo de gráficos para un itinerario.
    """
    if not verificar_matplotlib():
        return
        
    print(f"Generando gráficos para: {nombre_itinerario}")
    
    try:
        grafico_distancia_vs_tiempo(itinerario)
        grafico_costo_vs_distancia(itinerario)
        print("Gráficos generados correctamente")
    except Exception as e:
        print(f"Error generando gráficos: {e}")