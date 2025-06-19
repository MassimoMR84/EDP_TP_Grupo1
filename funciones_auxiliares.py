def horas_a_hs_y_min(tiempo_en_horas):
    """
    Convierte horas decimales a tupla (horas, minutos).
    Ejemplo: 2.75 -> (2, 45)
    """
    horas = int(tiempo_en_horas)
    minutos = int((tiempo_en_horas - horas) * 60)
    return (horas, minutos)


def tiempo_a_string(tiempo_en_horas):
    """
    Convierte horas decimales a string legible.
    Ejemplo: 2.75 -> "2hs, 45min"
    """
    horas, minutos = horas_a_hs_y_min(tiempo_en_horas)
    return f'{horas}hs, {minutos}min'