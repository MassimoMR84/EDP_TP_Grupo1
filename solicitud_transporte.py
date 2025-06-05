from main import leer_csv
from validaciones import validar_numero_mayor_a_cero,validar_numero_positivo

class SolicitudTransporte:
    '''Clase que representa una solicitud de carga'''
    def __init__(self,id_carga,peso_kg,origen,destino):
        self.id_carga=id_carga
        self.peso_kg=validar_numero_mayor_a_cero(peso_kg)
        self.origen=origen
        self.destino=destino

    

    def __eq__(self, other):
        if not isinstance(other,SolicitudTransporte):
            raise TypeError ('Ambos objetos deben ser de la clase SolicitudTransporte')
        if self.id_carga == other.id_carga:
            return True
        else:
            return False

if __name__ == '__main__':
    dicc = leer_csv('solicitudes.csv')
    for elem in dicc:
        Nuevo=SolicitudTransporte(**elem)

    print(Nuevo.id_carga)
