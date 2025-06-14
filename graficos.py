try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False
    print("Matplotlib no disponible. Gráficos deshabilitados.")

def verificar_matplotlib():
    """Verifica si matplotlib está disponible"""
    if not MATPLOTLIB_DISPONIBLE:
        print("Matplotlib no instalado. Instalar con: pip install matplotlib")
        return False
    return True

def grafico_distancia_vs_tiempo(itinerario):
    """Genera gráfico de Distancia Acumulada vs Tiempo Acumulado"""
    if not verificar_matplotlib():
        return
        
    if not itinerario.tramos:
        print("No hay tramos para graficar")
        return
        
    tiempos_acumulados = [0]
    distancias_acumuladas = [0]
    
    tiempo_acum = 0
    distancia_acum = 0
    
    for tramo in itinerario.tramos:
        tiempo_acum += tramo.tiempo
        distancia_acum += tramo.distancia
        tiempos_acumulados.append(tiempo_acum)
        distancias_acumuladas.append(distancia_acum)
    
    plt.figure(figsize=(10, 6))
    plt.plot(tiempos_acumulados, distancias_acumuladas, color='blue', marker='o', linewidth=2)
    plt.title('Distancia Acumulada vs Tiempo Acumulado', fontsize=16)
    plt.xlabel('Tiempo Acumulado (horas)', fontsize=12)
    plt.ylabel('Distancia Acumulada (km)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Anotar puntos
    for i, tramo in enumerate(itinerario.tramos, 1):
        plt.annotate(f'Tramo {i}', 
                    (tiempos_acumulados[i], distancias_acumuladas[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.show()

def grafico_costo_vs_distancia(itinerario):
    """Genera gráfico de Costo Acumulado vs Distancia Acumulada"""
    if not verificar_matplotlib():
        return
        
    if not itinerario.tramos:
        print("No hay tramos para graficar")
        return
        
    distancias_acumuladas = [0]
    costos_acumulados = [0]
    
    distancia_acum = 0
    costo_acum = 0
    
    for tramo in itinerario.tramos:
        distancia_acum += tramo.distancia
        costo_acum += tramo.costo
        distancias_acumuladas.append(distancia_acum)
        costos_acumulados.append(costo_acum)
    
    plt.figure(figsize=(10, 6))
    plt.plot(distancias_acumuladas, costos_acumulados, color='purple', marker='X', linewidth=2)
    plt.title('Costo Acumulado vs Distancia Acumulada', fontsize=16)
    plt.xlabel('Distancia Acumulada (km)', fontsize=12)
    plt.ylabel('Costo Acumulado ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Anotar puntos
    for i, tramo in enumerate(itinerario.tramos, 1):
        plt.annotate(f'Tramo {i}', 
                    (distancias_acumuladas[i], costos_acumulados[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    plt.tight_layout()
    plt.show()

def grafico_comparacion_caminos(itinerarios_dict):
    """Genera gráfico de barras comparando costos"""
    if not verificar_matplotlib():
        return
        
    if not itinerarios_dict:
        print("No hay itinerarios para comparar")
        return
        
    nombres = list(itinerarios_dict.keys())
    costos = [itinerario.costo_total for itinerario in itinerarios_dict.values()]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(nombres, costos, color='green', width=0.6, alpha=0.7)
    
    # Valores sobre barras
    for bar, costo in zip(bars, costos):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(costos)*0.01, 
                f'${costo:.2f}', ha='center', va='bottom', fontsize=10)
    
    plt.title('Comparación de Costos por Camino', fontsize=16)
    plt.xlabel('Caminos', fontsize=12)
    plt.ylabel('Costo Total ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

def grafico_comparacion_tiempos(itinerarios_dict):
    """Genera gráfico de barras comparando tiempos"""
    if not verificar_matplotlib():
        return
        
    if not itinerarios_dict:
        print("No hay itinerarios para comparar")
        return
        
    nombres = list(itinerarios_dict.keys())
    tiempos = [itinerario.tiempo_total for itinerario in itinerarios_dict.values()]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(nombres, tiempos, color='orange', width=0.6, alpha=0.7)
    
    # Valores sobre barras
    for bar, tiempo in zip(bars, tiempos):
        horas = int(tiempo)
        minutos = int((tiempo - horas) * 60)
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(tiempos)*0.01, 
                f'{horas}h {minutos}m', ha='center', va='bottom', fontsize=10)
    
    plt.title('Comparación de Tiempos por Camino', fontsize=16)
    plt.xlabel('Caminos', fontsize=12)
    plt.ylabel('Tiempo Total (horas)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

def generar_todos_los_graficos(itinerario, nombre_itinerario="Itinerario"):
    """Genera todos los gráficos para un itinerario"""
    if not verificar_matplotlib():
        return
        
    print(f"Generando gráficos para: {nombre_itinerario}")
    
    try:
        grafico_distancia_vs_tiempo(itinerario)
        grafico_costo_vs_distancia(itinerario)
        print("Gráficos generados correctamente")
    except Exception as e:
        print(f"Error generando gráficos: {e}")

if __name__ == "__main__":
    print("MÓDULO DE GRÁFICOS")
    print("="*40)
    print("Funciones disponibles:")
    print("- grafico_distancia_vs_tiempo(itinerario)")
    print("- grafico_costo_vs_distancia(itinerario)")
    print("- grafico_comparacion_caminos(itinerarios_dict)")
    print("- grafico_comparacion_tiempos(itinerarios_dict)")
    print("- generar_todos_los_graficos(itinerario, nombre)")
    
    if MATPLOTLIB_DISPONIBLE:
        print("matplotlib disponible - gráficos habilitados")
    else:
        print("matplotlib NO disponible - gráficos deshabilitados")
        print("Para habilitar: pip install matplotlib")