# Manejo de dependencias opcionales
try:
    import matplotlib.pyplot as plt
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
    plt.title('Distancia Acumulada vs Tiempo Acumulado', fontsize=16)
    plt.xlabel('Tiempo Acumulado (horas)', fontsize=12)
    plt.ylabel('Distancia Acumulada (km)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Anotar tramos
    for i, tramo in enumerate(itinerario.tramos, 1):
        plt.annotate(f'Tramo {i}', 
                    (tiempos_acumulados[i], distancias_acumuladas[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
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
    plt.title('Costo Acumulado vs Distancia Acumulada', fontsize=16)
    plt.xlabel('Distancia Acumulada (km)', fontsize=12)
    plt.ylabel('Costo Acumulado ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Anotar tramos
    for i, tramo in enumerate(itinerario.tramos, 1):
        plt.annotate(f'Tramo {i}', 
                    (distancias_acumuladas[i], costos_acumulados[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.show()


def grafico_comparacion_caminos(itinerarios_dict):
    """
    Gráfico de barras comparando costos entre diferentes rutas.
    Permite evaluar rápidamente qué itinerarios son más económicos.
    """
    if not verificar_matplotlib():
        return
        
    if not itinerarios_dict:
        print("No hay itinerarios para comparar")
        return
        
    # Extraer datos
    nombres = list(itinerarios_dict.keys())
    costos = [itinerario.costo_total for itinerario in itinerarios_dict.values()]
    
    # Crear gráfico de barras
    plt.figure(figsize=(12, 6))
    bars = plt.bar(nombres, costos, color='green', width=0.6, alpha=0.7)
    
    # Etiquetas con valores sobre las barras
    for bar, costo in zip(bars, costos):
        plt.text(bar.get_x() + bar.get_width()/2, 
                bar.get_height() + max(costos)*0.01, 
                f'${costo:.2f}', 
                ha='center', va='bottom', fontsize=10)
    
    plt.title('Comparación de Costos por Camino', fontsize=16)
    plt.xlabel('Caminos', fontsize=12)
    plt.ylabel('Costo Total ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()


def grafico_comparacion_tiempos(itinerarios_dict):
    """
    Gráfico de barras comparando tiempos entre diferentes rutas.
    Útil para optimización temporal.
    """
    if not verificar_matplotlib():
        return
        
    if not itinerarios_dict:
        print("No hay itinerarios para comparar")
        return
        
    # Extraer datos
    nombres = list(itinerarios_dict.keys())
    tiempos = [itinerario.tiempo_total for itinerario in itinerarios_dict.values()]
    
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
    
    plt.title('Comparación de Tiempos por Camino', fontsize=16)
    plt.xlabel('Caminos', fontsize=12)
    plt.ylabel('Tiempo Total (horas)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
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
        print("Gráficos generados correctamente")
    except Exception as e:
        print(f"Error generando gráficos: {e}")