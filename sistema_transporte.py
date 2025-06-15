from nodo import Nodo
from conexion import Conexion
from solicitud_transporte import SolicitudTransporte
import csv


class SistemaTransporte:
    """
    Clase principal que maneja la red de transporte completa.
    Carga datos desde CSV y coordina el procesamiento de solicitudes.
    """
    
    def __init__(self):
        self.nodos = {}          # {nombre: objeto_Nodo}
        self.conexiones = []     # Lista de conexiones
        self.solicitudes = []    # Lista de solicitudes

    def cargar_nodos(self, archivo_csv):
        """Carga nodos desde archivo CSV con columna 'nombre'"""
        print(f"Cargando nodos desde {archivo_csv}...")
        try:
            with open(archivo_csv, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    nombre = row['nombre'].strip()
                    if nombre not in self.nodos:
                        self.nodos[nombre] = Nodo(nombre)
            print(f"Cargados {len(self.nodos)} nodos")
        except Exception as e:
            print(f"Error cargando nodos: {e}")
            raise

    def cargar_conexiones(self, archivo_csv):
        """Carga conexiones con restricciones opcionales desde CSV"""
        print(f"Cargando conexiones desde {archivo_csv}...")
        try:
            with open(archivo_csv, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                conexiones_agregadas = 0
                
                for row in reader:
                    # Extraer datos básicos
                    origen_nombre = row['origen'].strip()
                    destino_nombre = row['destino'].strip()
                    tipo = row['tipo'].strip()
                    distancia = float(row['distancia_km'])
                    
                    # Restricciones opcionales
                    restriccion = row.get('restriccion', '').strip() or None
                    valor_restriccion = row.get('valor_restriccion', '').strip() or None
                    
                    # Verificar que existan los nodos
                    if origen_nombre in self.nodos and destino_nombre in self.nodos:
                        nodo_origen = self.nodos[origen_nombre]
                        nodo_destino = self.nodos[destino_nombre]
                        
                        conexion = Conexion(
                            origen=nodo_origen,
                            destino=nodo_destino,
                            tipo=tipo,
                            distancia=distancia,
                            restriccion=restriccion,
                            valorRestriccion=valor_restriccion
                        )
                        
                        nodo_origen.agregarConexiones(conexion)
                        self.conexiones.append(conexion)
                        conexiones_agregadas += 1
                    else:
                        print(f"Nodos no encontrados: {origen_nombre} -> {destino_nombre}")
                
                print(f"Cargadas {conexiones_agregadas} conexiones")
        except Exception as e:
            print(f"Error cargando conexiones: {e}")
            raise

    def cargar_solicitudes(self, archivo_csv):
        """Carga solicitudes de transporte desde CSV"""
        print(f"Cargando solicitudes desde {archivo_csv}...")
        try:
            with open(archivo_csv, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                solicitudes_agregadas = 0
                
                for row in reader:
                    try:
                        id_carga = row['id_carga'].strip()
                        peso_kg = float(row['peso_kg'])
                        origen_nombre = row['origen'].strip()
                        destino_nombre = row['destino'].strip()
                        
                        if origen_nombre in self.nodos and destino_nombre in self.nodos:
                            solicitud = SolicitudTransporte(
                                id_carga=id_carga,
                                peso_kg=peso_kg,
                                origen=self.nodos[origen_nombre],
                                destino=self.nodos[destino_nombre]
                            )
                            self.solicitudes.append(solicitud)
                            solicitudes_agregadas += 1
                        else:
                            print(f"Nodos no encontrados para {id_carga}: {origen_nombre} -> {destino_nombre}")
                            
                    except Exception as e:
                        print(f"Error procesando solicitud {row}: {e}")
                
                print(f"Cargadas {solicitudes_agregadas} solicitudes")
        except Exception as e:
            print(f"Error cargando solicitudes: {e}")
            raise

    def mostrar_resumen(self):
        """Muestra resumen del sistema cargado con estadísticas"""
        print("\n" + "="*60)
        print("RESUMEN DEL SISTEMA DE TRANSPORTE")
        print("="*60)
        print(f"Nodos: {len(self.nodos)}")
        print(f"Conexiones: {len(self.conexiones)}")
        print(f"Solicitudes: {len(self.solicitudes)}")
        
        print("\nNODOS Y CONEXIONES:")
        for nombre, nodo in self.nodos.items():
            # Contar conexiones por tipo
            conexiones_por_tipo = {}
            restricciones_especiales = []
            
            for conexion in nodo.conexiones:
                tipo = conexion.tipo.lower()
                conexiones_por_tipo[tipo] = conexiones_por_tipo.get(tipo, 0) + 1
                
                # Detectar restricciones para mostrar
                if conexion.restriccion and conexion.valorRestriccion is not None:
                    info_restriccion = conexion.obtener_info_restriccion()
                    restricciones_especiales.append(f"{conexion.destino.nombre}: {info_restriccion}")
            
            tipos_str = ", ".join([f"{tipo}: {count}" for tipo, count in conexiones_por_tipo.items()])
            print(f"  {nombre}: {len(nodo.conexiones)} conexiones ({tipos_str})")
            
            # Mostrar algunas restricciones (máximo 3)
            for restriccion in restricciones_especiales[:3]:
                print(f"    Restricción: {restriccion}")
            if len(restricciones_especiales) > 3:
                print(f"    ... y {len(restricciones_especiales) - 3} más")
        
        print(f"\nSOLICITUDES:")
        for solicitud in self.solicitudes:
            print(f"  {solicitud}")

    def verificar_conectividad(self):
        """Verifica qué modos de transporte están disponibles para cada solicitud"""
        print(f"\nVERIFICANDO CONECTIVIDAD...")
        
        for solicitud in self.solicitudes:
            origen = solicitud.origen.nombre
            destino = solicitud.destino.nombre
            peso = solicitud.peso_kg
            print(f"\nRuta: {origen} -> {destino} (Carga: {peso} kg)")
            
            # Verificar cada modo
            modos = ['Ferroviaria', 'Automotor', 'Fluvial', 'Aerea']
            for modo in modos:
                conexiones_disponibles = []
                conexiones_bloqueadas = []
                
                for conexion in solicitud.origen.conexiones:
                    if conexion.tipo.lower() == modo.lower():
                        if conexion.es_compatible_con_carga(peso):
                            conexiones_disponibles.append(conexion.destino.nombre)
                        else:
                            info_restriccion = conexion.obtener_info_restriccion()
                            conexiones_bloqueadas.append(f"{conexion.destino.nombre} ({info_restriccion})")
                
                if conexiones_disponibles:
                    destinos_str = ", ".join(conexiones_disponibles)
                    print(f"  OK {modo}: conecta a {destinos_str}")
                else:
                    print(f"  NO {modo}: no disponible desde {origen}")
                
                if conexiones_bloqueadas:
                    bloqueados_str = ", ".join(conexiones_bloqueadas)
                    print(f"    Bloqueadas: {bloqueados_str}")

    def obtener_estadisticas(self):
        """Retorna estadísticas básicas del sistema"""
        estadisticas = {
            'total_nodos': len(self.nodos),
            'total_conexiones': len(self.conexiones),
            'total_solicitudes': len(self.solicitudes),
            'conexiones_por_tipo': {},
            'solicitudes_por_peso': {
                'ligeras': 0,    # < 10,000 kg
                'medianas': 0,   # 10,000 - 50,000 kg
                'pesadas': 0     # > 50,000 kg
            }
        }
        
        # Estadísticas de conexiones por tipo
        for conexion in self.conexiones:
            tipo = conexion.tipo.lower()
            estadisticas['conexiones_por_tipo'][tipo] = estadisticas['conexiones_por_tipo'].get(tipo, 0) + 1
        
        # Estadísticas de solicitudes por peso
        for solicitud in self.solicitudes:
            peso = solicitud.peso_kg
            if peso < 10000:
                estadisticas['solicitudes_por_peso']['ligeras'] += 1
            elif peso <= 50000:
                estadisticas['solicitudes_por_peso']['medianas'] += 1
            else:
                estadisticas['solicitudes_por_peso']['pesadas'] += 1
        
        return estadisticas

    def buscar_nodo(self, nombre):
        """Busca un nodo por nombre (case-insensitive)"""
        nombre_normalizado = nombre.strip().lower()
        for nodo_nombre, nodo in self.nodos.items():
            if nodo_nombre.lower() == nombre_normalizado:
                return nodo
        return None

    def validar_integridad(self):
        """Valida la integridad de los datos cargados"""
        errores = []
        
        # Verificar que todas las conexiones tienen nodos válidos
        for i, conexion in enumerate(self.conexiones):
            if conexion.origen.nombre not in self.nodos:
                errores.append(f"Conexión {i}: Nodo origen '{conexion.origen.nombre}' no existe")
            if conexion.destino.nombre not in self.nodos:
                errores.append(f"Conexión {i}: Nodo destino '{conexion.destino.nombre}' no existe")
        
        # Verificar que todas las solicitudes tienen nodos válidos
        for i, solicitud in enumerate(self.solicitudes):
            if solicitud.origen.nombre not in self.nodos:
                errores.append(f"Solicitud {i} ({solicitud.id_carga}): Nodo origen '{solicitud.origen.nombre}' no existe")
            if solicitud.destino.nombre not in self.nodos:
                errores.append(f"Solicitud {i} ({solicitud.id_carga}): Nodo destino '{solicitud.destino.nombre}' no existe")
        
        # Verificar nodos aislados (sin conexiones)
        nodos_aislados = []
        for nombre, nodo in self.nodos.items():
            if len(nodo.conexiones) == 0:
                # También verificar si llegan conexiones de otros nodos
                conexiones_entrantes = [c for c in self.conexiones if c.destino.nombre == nombre]
                if len(conexiones_entrantes) == 0:
                    nodos_aislados.append(nombre)
        
        if nodos_aislados:
            errores.append(f"Nodos aislados (sin conexiones): {', '.join(nodos_aislados)}")
        
        return errores

    def exportar_resumen(self, archivo_salida="resumen_sistema.txt"):
        """Exporta un resumen detallado del sistema a un archivo de texto"""
        try:
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("RESUMEN DEL SISTEMA DE TRANSPORTE\n")
                f.write("=" * 50 + "\n\n")
                
                # Estadísticas generales
                stats = self.obtener_estadisticas()
                f.write("ESTADÍSTICAS GENERALES:\n")
                f.write(f"  Nodos: {stats['total_nodos']}\n")
                f.write(f"  Conexiones: {stats['total_conexiones']}\n")
                f.write(f"  Solicitudes: {stats['total_solicitudes']}\n\n")
                
                # Conexiones por tipo
                f.write("CONEXIONES POR TIPO:\n")
                for tipo, cantidad in stats['conexiones_por_tipo'].items():
                    f.write(f"  {tipo.capitalize()}: {cantidad}\n")
                f.write("\n")
                
                # Solicitudes por peso
                f.write("SOLICITUDES POR CATEGORÍA DE PESO:\n")
                for categoria, cantidad in stats['solicitudes_por_peso'].items():
                    f.write(f"  {categoria.capitalize()}: {cantidad}\n")
                f.write("\n")
                
                # Detalles de nodos
                f.write("DETALLE DE NODOS:\n")
                for nombre, nodo in self.nodos.items():
                    f.write(f"\n{nombre}:\n")
                    if nodo.conexiones:
                        for conexion in nodo.conexiones:
                            restriccion_info = ""
                            if conexion.restriccion:
                                restriccion_info = f" [{conexion.obtener_info_restriccion()}]"
                            f.write(f"  -> {conexion.destino.nombre} ({conexion.tipo}, {conexion.distancia}km){restriccion_info}\n")
                    else:
                        f.write("  Sin conexiones salientes\n")
                
                # Solicitudes
                f.write(f"\nSOLICITUDES:\n")
                for solicitud in self.solicitudes:
                    f.write(f"  {solicitud}\n")
                
            print(f"Resumen exportado a: {archivo_salida}")
            
        except Exception as e:
            print(f"Error exportando resumen: {e}")


# Código de prueba
if __name__ == "__main__":
    print("Probando SistemaTransporte...")
    
    try:
        # Crear y cargar sistema
        sistema = SistemaTransporte()
        
        # Intentar cargar archivos de prueba
        try:
            sistema.cargar_nodos('nodos.csv')
            sistema.cargar_conexiones('conexiones.csv')
            sistema.cargar_solicitudes('solicitudes.csv')
            
            sistema.mostrar_resumen()
            sistema.verificar_conectividad()
            
            # Validar integridad
            errores = sistema.validar_integridad()
            if errores:
                print(f"\nERRORES DE INTEGRIDAD:")
                for error in errores:
                    print(f"  - {error}")
            else:
                print(f"\n✓ Sistema validado correctamente")
            
            # Exportar resumen
            sistema.exportar_resumen()
            
        except FileNotFoundError as e:
            print(f"Archivo no encontrado: {e}")
            print("Creando sistema de prueba...")
            
            # Crear datos de prueba en memoria
            sistema.nodos = {
                'TestA': Nodo('TestA'),
                'TestB': Nodo('TestB')
            }
            print("Sistema de prueba creado con 2 nodos")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nPruebas completadas")