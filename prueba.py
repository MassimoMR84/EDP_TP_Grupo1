import matplotlib.pyplot as plt
from planificador import *
def grafico_tiempos():
    a=[2,3,4,4]
    b=[4,5,6,7]
    c=[3,4,5,6]
    d=[6,7,8,9]
    plt.title('')
    plt.xlabel('Tiempo Acumulado (horas)')
    plt.ylabel('Distancia Acumulada (km)')

    plt.plot(a,b,color='green')
    plt.plot(c,d,color='red')

    plt.show()
grafico_tiempos()


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
    
grafico_tiempo_vs_distancia_por_modo()