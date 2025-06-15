def validar_positivo(numero):
    """Verifica que sea >= 0"""
    if not isinstance(numero, (int, float)):
        raise TypeError('Debe ser un número')
    if numero < 0:
        raise ValueError('Debe ser positivo')
    return numero


def validar_mayor_cero(numero):
    """Verifica que sea > 0"""
    validar_positivo(numero)
    if numero == 0:
        raise ValueError('Debe ser mayor a cero')
    return numero


def validar_texto(texto):
    """Verifica que sea texto válido"""
    if not isinstance(texto, str):
        raise TypeError('Debe ser texto')
    if not texto.strip():
        raise ValueError('No puede estar vacío')
    return texto.strip()


def validar_division_cero(denominador):
    """Previene divisiones por cero"""
    if denominador == 0:
        raise ValueError('No se puede dividir por cero')
    return denominador


def validar_vehiculo(vehiculo): 
    """Verifica que sea un vehículo válido"""
    from vehiculos import Vehiculo
    if not isinstance(vehiculo, Vehiculo):
        raise TypeError("Debe ser un vehículo")
    return vehiculo


def validar_origen_destino(origen, destino): 
    """Verifica que origen y destino sean diferentes"""
    if origen == destino:
        raise ValueError("Origen y destino no pueden ser iguales")
    return origen, destino


def validar_modo_transporte(modo):
    """Valida y normaliza modos de transporte"""
    modo = validar_texto(modo).lower()
    
    modos_validos = {
        'automotor': 'automotor',
        'ferroviaria': 'ferroviaria', 
        'aerea': 'aerea',
        'aereo': 'aerea',
        'fluvial': 'fluvial',
        'maritimo': 'maritimo',
        'marítimo': 'maritimo'
    }
    
    if modo not in modos_validos:
        raise ValueError(f'Modo inválido: {modo}. Usar: automotor, ferroviaria, aerea, fluvial, maritimo')
    
    return modos_validos[modo]


def validar_restriccion_conexion(restriccion, valor):
    """Validador simple para restricciones"""
    if not restriccion or not valor:
        return valor
        
    restriccion = restriccion.strip().lower()
    
    # Validaciones básicas según tipo
    if restriccion in ['velocidad_max', 'peso_max']:
        try:
            num = float(valor)
            if num <= 0:
                raise ValueError(f"{restriccion} debe ser positivo")
            return num
        except ValueError:
            raise ValueError(f"{restriccion} debe ser un número válido")
    
    elif restriccion == 'tipo':
        if valor.lower() not in ['fluvial', 'maritimo']:
            raise ValueError("Tipo debe ser 'fluvial' o 'maritimo'")
        return valor.lower()
    
    elif restriccion == 'prob_mal_tiempo':
        try:
            prob = float(valor)
            if not 0 <= prob <= 1:
                raise ValueError("Probabilidad debe estar entre 0 y 1")
            return prob
        except ValueError:
            raise ValueError("Probabilidad debe ser un número entre 0 y 1")
    
    # Para otras restricciones, solo devolver el valor
    return valor


# Prueba simple
if __name__ == "__main__":
    print("✅ Validaciones simplificadas")
    
    # Probar validaciones básicas
    try:
        print(f"Positivo: {validar_positivo(10)}")
        print(f"Mayor cero: {validar_mayor_cero(5)}")
        print(f"Texto: '{validar_texto('  Buenos Aires  ')}'")
        print(f"Modo: {validar_modo_transporte('Automotor')}")
        print("✅ Todas las validaciones funcionan")
    except Exception as e:
        print(f"❌ Error: {e}")