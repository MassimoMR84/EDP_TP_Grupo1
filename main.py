import csv
def leer_csv(file):
    with open(file,'r',encoding='utf-8') as archivo:
        lector=csv.DictReader(archivo)
        return list(lector)

print(leer_csv('conexiones.csv'))
