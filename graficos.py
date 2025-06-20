from planificador import *
# Manejo de dependencias opcionales
try:
    import matplotlib.pyplot as plt
    from datetime import datetime
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
    print("Matplotlib no disponible. Gráficos deshabilitados.")


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
    Útil para visualizar eficiencia temporal de la ruta.
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
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos_acumulados, distancias_acumuladas, 
             color='blue', marker='o', linewidth=2)
    plt.title(f'Progreso del Viaje - Optimización por {itinerario.kpi_usado.upper()}\n'
              f'Ruta: {" -> ".join(itinerario.obtener_ruta_completa())}', fontsize=16)
    plt.xlabel('Tiempo Acumulado (horas)', fontsize=12)
    plt.ylabel('Distancia Acumulada (km)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Anotar tramos
    for i, tramo in enumerate(itinerario.tramos, 1):
        plt.annotate(f'Tramo {i}\n{tramo.vehiculo.modo_de_transporte}', 
                    (tiempos_acumulados[i], distancias_acumuladas[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
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
    Gráfico de eficiencia económica: cómo se acumula el costo por distancia.
    Útil para identificar tramos más costosos.
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
    plt.figure(figsize=(10, 6))
    plt.plot(distancias_acumuladas, costos_acumulados, 
             color='purple', marker='X', linewidth=2)
    plt.title(f'Análisis de Costos - Optimización por {itinerario.kpi_usado.upper()}\n'
              f'Ruta: {" -> ".join(itinerario.obtener_ruta_completa())}', fontsize=16)
    plt.xlabel('Distancia Acumulada (km)', fontsize=12)
    plt.ylabel('Costo Acumulado ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Anotar tramos
    for i, tramo in enumerate(itinerario.tramos, 1):
        plt.annotate(f'Tramo {i}\n${tramo.costo:.2f}', 
                    (distancias_acumuladas[i], costos_acumulados[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
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


'''def grafico_comparacion_caminos(itinerarios_optimos_por_modo):
    """
    Gráfico de barras comparando costos entre diferentes rutas.
    Permite evaluar rápidamente qué itinerarios son más económicos.
    """
    if not verificar_matplotlib():
        return
        
    if not itinerarios_optimos_por_modo:
        print("No hay itinerarios para comparar")
        return
        
    # Extraer datos
    nombres = list(itinerarios_optimos_por_modo.keys())
    costos = [itinerario.costo_total for itinerario in itinerarios_optimos_por_modo.values()]
    
    # Crear gráfico de barras
    plt.figure(figsize=(12, 6))
    bars = plt.bar(nombres, costos, color='green', width=0.6, alpha=0.7)
    
    # Etiquetas con valores sobre las barras
    for bar, costo in zip(bars, costos):
        plt.text(bar.get_x() + bar.get_width()/2, 
                bar.get_height() + max(costos)*0.01, 
                f'${costo:.2f}', 
                ha='center', va='bottom', fontsize=10)
    
    # Resaltar el mejor (más barato)
    if costos:
        min_index = costos.index(min(costos))
        bars[min_index].set_color('gold')
        bars[min_index].set_edgecolor('orange')
        bars[min_index].set_linewidth(2)
    
    plt.title('Comparación de Costos por Camino', fontsize=16)
    plt.xlabel('Caminos', fontsize=12)
    plt.ylabel('Costo Total ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Guardar con nombre descriptivo
    nombre_archivo = _crear_nombre_archivo("comparativo_costos")
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"Gráfico comparativo de costos guardado: {nombre_archivo}")
    
    plt.show()

def grafico_comparacion_tiempos(itinerarios_optimos_por_modo):
    """
    Gráfico de barras comparando tiempos entre diferentes rutas.
    Útil para optimización temporal.
    """
    if not verificar_matplotlib():
        return
        
    if not itinerarios_optimos_por_modo:
        print("No hay itinerarios para comparar")
        return
        
    # Extraer datos
    nombres = list(itinerarios_optimos_por_modo.keys())
    tiempos = [itinerario.tiempo_total for itinerario in itinerarios_optimos_por_modo.values()]
    
    # Crear gráfico
    plt.figure(figsize=(12, 6))
    bars = plt.bar(nombres, tiempos, color='orange', width=0.6, alpha=0.7)
    
    # Etiquetas con formato tiempo legible
    for bar, tiempo in zip(bars, tiempos):
        horas = int(tiempo)
        minutos = int((tiempo - horas) * 60)
        plt.text(bar.get_x() + bar.get_width()/2, 
                bar.get_height() + max(tiempos)*0.01, 
                f'{horas}h {minutos}m', 
                ha='center', va='bottom', fontsize=10)
    
    # Resaltar el mejor (más rápido)
    if tiempos:
        min_index = tiempos.index(min(tiempos))
        bars[min_index].set_color('gold')
        bars[min_index].set_edgecolor('orange')
        bars[min_index].set_linewidth(2)
    
    plt.title('Comparación de Tiempos por Camino', fontsize=16)
    plt.xlabel('Caminos', fontsize=12)
    plt.ylabel('Tiempo Total (horas)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    
    # Guardar con nombre descriptivo
    nombre_archivo = _crear_nombre_archivo("comparativo_tiempos")
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"Gráfico comparativo de tiempos guardado: {nombre_archivo}")
    
    plt.show()

'''

def grafico_tiempo_vs_distancia_por_modo(itinerarios_optimos_por_modo, mejor_itinerario):
    if not itinerarios_optimos_por_modo:
        print("No hay itinerarios para graficar.")
        return

    plt.figure(figsize=(12, 6))

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

        if itinerario == mejor_itinerario:
            plt.plot(tiempos, distancias, label=f"{modo} (óptimo)", linewidth=3, color='gold')
        else:
            plt.plot(tiempos, distancias, label=modo, linewidth=1.8)

    plt.xlabel("Tiempo Acumulado (min)")
    plt.ylabel("Distancia Acumulada (km)")
    plt.title("Comparación de Itinerarios Óptimos por Modo")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()



def generar_todos_los_graficos(itinerario, nombre_itinerario="Itinerario"):
    """
    Genera conjunto completo de gráficos para un itinerario.
    Función de conveniencia para análisis integral.
    """
    if not verificar_matplotlib():
        return
        
    print(f"Generando gráficos para: {nombre_itinerario}")
    
    try:
        grafico_distancia_vs_tiempo(itinerario)
        grafico_costo_vs_distancia(itinerario)
        grafico_tiempo_vs_distancia_por_modo(Planificador.optimos_por_modo(), Planificador.generar_itinerario())
        print("Gráficos generados correctamente")
    except Exception as e:
        print(f"Error generando gráficos: {e}")