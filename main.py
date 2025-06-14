from nodo import Nodo
from conexion import Conexion
from solicitud_transporte import SolicitudTransporte
from planificador import Planificador
import csv

# Importar gráficos si están disponibles
try:
    from graficos import generar_todos_los_graficos, grafico_comparacion_caminos, grafico_comparacion_tiempos
    GRAFICOS_DISPONIBLES = True
except ImportError:
    print("Matplotlib no disponible - gráficos deshabilitados")
    GRAFICOS_DISPONIBLES = False

class SistemaTransporte:
    def __init__(self):
        self.nodos = {}
        self.conexiones = []
        self.solicitudes = []

    def cargar_nodos(self, archivo_csv):
        """Carga nodos desde archivo CSV"""
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
        """Carga conexiones desde archivo CSV"""
        print(f"Cargando conexiones desde {archivo_csv}...")
        try:
            with open(archivo_csv, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                conexiones_agregadas = 0
                for row in reader:
                    origen_nombre = row['origen'].strip()
                    destino_nombre = row['destino'].strip()
                    tipo = row['tipo'].strip()
                    distancia = float(row['distancia_km'])
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
        """Carga solicitudes desde archivo CSV"""
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
        """Muestra resumen del sistema cargado"""
        print("\n" + "="*60)
        print("RESUMEN DEL SISTEMA DE TRANSPORTE")
        print("="*60)
        print(f"Nodos: {len(self.nodos)}")
        print(f"Conexiones: {len(self.conexiones)}")
        print(f"Solicitudes: {len(self.solicitudes)}")
        
        print("\nNODOS Y CONEXIONES:")
        for nombre, nodo in self.nodos.items():
            conexiones_por_tipo = {}
            restricciones_especiales = []
            
            for conexion in nodo.conexiones:
                tipo = conexion.tipo.lower()
                if tipo not in conexiones_por_tipo:
                    conexiones_por_tipo[tipo] = 0
                conexiones_por_tipo[tipo] += 1
                
                # Detectar restricciones especiales
                if conexion.restriccion and conexion.valorRestriccion is not None:
                    info_restriccion = conexion.obtener_info_restriccion()
                    restricciones_especiales.append(f"{conexion.destino.nombre}: {info_restriccion}")
            
            tipos_str = ", ".join([f"{tipo}: {count}" for tipo, count in conexiones_por_tipo.items()])
            print(f"  {nombre}: {len(nodo.conexiones)} conexiones ({tipos_str})")
            
            # Mostrar algunas restricciones
            if restricciones_especiales:
                for restriccion in restricciones_especiales[:3]:
                    print(f"    Restricción: {restriccion}")
                if len(restricciones_especiales) > 3:
                    print(f"    ... y {len(restricciones_especiales) - 3} más")
        
        print(f"\nSOLICITUDES:")
        for solicitud in self.solicitudes:
            print(f"  {solicitud}")

    def verificar_conectividad(self):
        """Verifica conectividad básica del grafo"""
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

def procesar_solicitudes(sistema, planificador):
    """Procesa todas las solicitudes del sistema"""
    print("\n" + "="*60)
    print("PROCESANDO SOLICITUDES")
    print("="*60)
    
    resultados_tiempo = {}
    resultados_costo = {}
    
    for i, solicitud in enumerate(sistema.solicitudes, 1):
        print(f"\n{'='*20} SOLICITUD {i}/{len(sistema.solicitudes)} {'='*20}")
        print(f"ID: {solicitud.id_carga}")
        print(f"Carga: {solicitud.peso_kg} kg")
        print(f"Ruta: {solicitud.origen.nombre} -> {solicitud.destino.nombre}")
        
        # Optimizar por tiempo
        print(f"\nOPTIMIZACIÓN POR TIEMPO:")
        print("-" * 40)
        try:
            itinerario_tiempo = planificador.generar_itinerario(solicitud, "tiempo")
            if itinerario_tiempo:
                print("Ruta encontrada:")
                print(itinerario_tiempo)
                resultados_tiempo[f"{solicitud.id_carga}_tiempo"] = itinerario_tiempo
                
                # Generar gráficos para primera solicitud
                if i == 1 and GRAFICOS_DISPONIBLES:
                    try:
                        print(f"\nGenerando gráficos por tiempo...")
                        generar_todos_los_graficos(itinerario_tiempo, f"{solicitud.id_carga} - Por Tiempo")
                    except Exception as e:
                        print(f"Error en gráficos: {e}")
            else:
                print("No se encontró ruta válida")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Optimizar por costo
        print(f"\nOPTIMIZACIÓN POR COSTO:")
        print("-" * 40)
        try:
            itinerario_costo = planificador.generar_itinerario(solicitud, "costo")
            if itinerario_costo:
                print("Ruta encontrada:")
                print(itinerario_costo)
                resultados_costo[f"{solicitud.id_carga}_costo"] = itinerario_costo
                
                # Generar gráficos para primera solicitud
                if i == 1 and GRAFICOS_DISPONIBLES:
                    try:
                        print(f"\nGenerando gráficos por costo...")
                        generar_todos_los_graficos(itinerario_costo, f"{solicitud.id_carga} - Por Costo")
                    except Exception as e:
                        print(f"Error en gráficos: {e}")
            else:
                print("No se encontró ruta válida")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Comparación directa
        if (f"{solicitud.id_carga}_tiempo" in resultados_tiempo and 
            f"{solicitud.id_carga}_costo" in resultados_costo):
            
            print(f"\nCOMPARACIÓN:")
            print("-" * 40)
            tiempo_it = resultados_tiempo[f"{solicitud.id_carga}_tiempo"]
            costo_it = resultados_costo[f"{solicitud.id_carga}_costo"]
            
            print(f"TIEMPO  - Duración: {tiempo_it.obtener_tiempo_total_formateado()}, Costo: ${tiempo_it.costo_total:.2f}")
            print(f"COSTO   - Duración: {costo_it.obtener_tiempo_total_formateado()}, Costo: ${costo_it.costo_total:.2f}")
            
            # Determinar mejor opción
            if tiempo_it.tiempo_total < costo_it.tiempo_total:
                print(f"Más rápido: Optimización por TIEMPO ({tiempo_it.obtener_tiempo_total_formateado()})")
            else:
                print(f"Más rápido: Optimización por COSTO ({costo_it.obtener_tiempo_total_formateado()})")
                
            if tiempo_it.costo_total < costo_it.costo_total:
                print(f"Más barato: Optimización por TIEMPO (${tiempo_it.costo_total:.2f})")
            else:
                print(f"Más barato: Optimización por COSTO (${costo_it.costo_total:.2f})")
        
        print("\n" + "="*60)
    
    # Gráficos comparativos
    if GRAFICOS_DISPONIBLES and (len(resultados_tiempo) > 1 or len(resultados_costo) > 1):
        try:
            print(f"\nGenerando gráficos comparativos...")
            if resultados_tiempo:
                grafico_comparacion_tiempos(resultados_tiempo)
            if resultados_costo:
                grafico_comparacion_caminos(resultados_costo)
        except Exception as e:
            print(f"Error en gráficos comparativos: {e}")

def main():
    """Función principal del sistema"""
    print("="*50)
    print("SISTEMA DE TRANSPORTE - INICIANDO")
    print("="*50)
    
    try:
        # Crear sistema
        sistema = SistemaTransporte()
        
        # Cargar datos
        sistema.cargar_nodos('nodos.csv')
        sistema.cargar_conexiones('conexiones.csv')
        sistema.cargar_solicitudes('solicitudes.csv')
        
        # Mostrar resumen
        sistema.mostrar_resumen()
        
        # Verificar conectividad
        sistema.verificar_conectividad()
        
        # Crear planificador
        print(f"\nCreando planificador...")
        planificador = Planificador(sistema)
        print(f"Planificador listo con {len(planificador.vehiculos_disponibles)} tipos de vehículos")
        
        # Procesar solicitudes
        procesar_solicitudes(sistema, planificador)
        
        print(f"\nPROCESAMIENTO COMPLETADO")
        print("="*50)
        
    except FileNotFoundError as e:
        print(f"Error: No se encontró archivo requerido")
        print(f"Archivo faltante: {e.filename}")
        print("\nArchivos necesarios:")
        print("  - nodos.csv")
        print("  - conexiones.csv") 
        print("  - solicitudes.csv")
        print("\nVerificar que estén en el directorio actual")
    except Exception as e:
        print(f"Error inesperado: {e}")
        print("\nInformación del error:")
        import traceback
        traceback.print_exc()
        print("\nVerificar:")
        print("  - Formato de archivos CSV")
        print("  - Referencias entre nodos y conexiones")
        print("  - Datos numéricos válidos")

if __name__ == "__main__":
    main()