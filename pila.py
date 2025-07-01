from validaciones import *

class NodoPila():
    def __init__(self, km, origen, destino, sig=None):
        validar_mayor_cero(km)
        validar_texto(origen)
        validar_texto(destino)
        
        self.dato= {
            'km': (round(km, 2)),
            'desde': origen,
            'hasta': destino}
        self.sig=sig

    def __str__(self):
        return (f"Km de la recarga: {self.dato['km']}; se encuentra en el tramo entre {self.dato['desde']} y {self.dato['hasta']}")


class Pila:
    def __init__(self):
        self.cima = None
        self.longitud = 0

    def apilar(self, nodo: NodoPila): #agregar a la pila
        nodo.sig = self.cima #nuevo nodo ahora tiene la referencia al nodo que antes estaba último
        self.cima = nodo #nuevo nodo ahora es el último
        self.longitud += 1

    def esVacia(self):
        if self.cima==None:
            return True
        else:
            return False

    def visualizarPila(self):
        """Imprime directamente el contenido de la pila de cima a base."""
        if self.esVacia():
            print("Pila vacía, no se realizaron recargas.")
        else:
            actual = self.cima
            while actual:
                print(actual)
                actual = actual.sig
