def horas_a_hs_y_min(tiempo_en_horas):
    '''
    Convierte un valor en horas decimales a una tupla (horas, minutos)
    '''
    horas = int(tiempo_en_horas)
    minutos = int((tiempo_en_horas-horas)*60)
    return horas, minutos
      