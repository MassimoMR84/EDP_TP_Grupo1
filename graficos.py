import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]             #necesitaria puntos medios entre nodos y todo en listas
y = [2, 3, 5, 7, 11]            #si no pueden hacerlo yo veo como hago

plt.plot(x, y, color='blue', marker='o')      
plt.title('Distancia Acumulada vs Tiempo Acumulado')
plt.xlabel('Tiempo Acumulado')
plt.ylabel('Distancia Acumulada')
plt.legend()
plt.show()


plt.plot([2,3,4,5],[1,3,6,7],color='purple', marker='X')
plt.title('Costo Acumulado vs Distancia Acumulada')
plt.xlabel('Distancia Acumulada')
plt.ylabel('Costo Acumulado')
plt.show()


costos=[234000,250000,275000,300000]
caminos=['Camino A','Camino B','Camino C','Camino D']
plt.title(label='Grafico posibles caminos', fontsize=16, color= 'black')
plt.xlabel('Caminos')
plt.ylabel('Costos')
plt.bar(caminos,costos,color='green', width=0.5)
plt.show()