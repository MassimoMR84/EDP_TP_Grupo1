from sistema_transporte import SistemaTransporte
from planificador import Planificador
from datetime import datetime
import os

# Importar gráficos si matplotlib está disponible
try:
    from graficos import generar_todos_los_graficos, grafico_tiempo_vs_distancia_por_modo
    GRAFICOS_DISPONIBLES = True
except ImportError:
    print("Matplotlib no disponible - gráficos deshabilitados")
    GRAFICOS_DISPONIBLES = False

os.makedirs('output',exist_ok=True)

def procesar_solicitudes(sistema, planificador):
    """
    Procesa todas las solicitudes generando itinerarios optimizados por tiempo y costo.
    Genera gráficos comparativos si matplotlib está disponible.
    """
    print("\n" + "="*60)
    print("PROCESANDO SOLICITUDES")
    print("="*60)
    
    resultados_tiempo = {}
    resultados_costo = {}
    
    for i, solicitud in enumerate(sistema.solicitudes, 1):
        print(f"\n{'='*15} SOLICITUD {i}/{len(sistema.solicitudes)} {'='*15}")
        print(f"ID: {solicitud.id_carga}")
        print(f"Carga: {solicitud.peso_kg:,} kg")
        print(f"Ruta: {solicitud.origen.nombre} -> {solicitud.destino.nombre}")
        print("="*50)
        
        # Optimización por tiempo
        print(f"\nOPTIMIZACION POR TIEMPO:")
        print("-" * 30)
        try:
            itinerario_tiempo = planificador.generar_itinerario(solicitud, "tiempo")
            if itinerario_tiempo:
                print("Ruta encontrada:")
                print(itinerario_tiempo)
                resultados_tiempo[f"{solicitud.id_carga}_tiempo"] = itinerario_tiempo
                
                # Gráficos para primera solicitud
                if GRAFICOS_DISPONIBLES:
                    try:
                        print(f"\nGenerando gráficos por tiempo...")
                        generar_todos_los_graficos(itinerario_tiempo, f"{solicitud.id_carga} - Por Tiempo")
                    except Exception as e:
                        print(f"Error en gráficos: {e}")
                        
                # Gráfico de comparación entre modos
                if GRAFICOS_DISPONIBLES:
                    try:
                        print("\nGenerando gráfico comparativo de tiempo vs distancia por modo...")
                        mejor_it, itinerarios_por_modo = planificador.encontrar_ruta_optima(solicitud, kpi="costo")
                        grafico_tiempo_vs_distancia_por_modo(itinerarios_por_modo, mejor_it)
                    except Exception as e:
                        print(f"Error al generar gráfico comparativo de líneas: {e}")
                                      
            else:
                print("No se encontró ruta válida")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        # Optimización por costo
        print(f"\nOPTIMIZACION POR COSTO:")
        print("-" * 30)
        try:
            itinerario_costo = planificador.generar_itinerario(solicitud, "costo")
            if itinerario_costo:
                print("Ruta encontrada:")
                print(itinerario_costo)
                resultados_costo[f"{solicitud.id_carga}_costo"] = itinerario_costo
                
                # Gráficos para primera solicitud
                if GRAFICOS_DISPONIBLES:
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
        
        # Comparación directa entre ambas optimizaciones
        if (f"{solicitud.id_carga}_tiempo" in resultados_tiempo and 
            f"{solicitud.id_carga}_costo" in resultados_costo):
            
            print(f"\nCOMPARACION DE RESULTADOS:")
            print("-" * 40)
            tiempo_it = resultados_tiempo[f"{solicitud.id_carga}_tiempo"]
            costo_it = resultados_costo[f"{solicitud.id_carga}_costo"]
            
            # Mostrar en formato tabla
            print(f"{'CRITERIO':<15} {'TIEMPO':<25} {'COSTO':<25}")
            print("-" * 65)
            
            # Rutas
            ruta_tiempo = " -> ".join(tiempo_it.obtener_ruta_completa())
            ruta_costo = " -> ".join(costo_it.obtener_ruta_completa())
            print(f"{'Ruta:':<15} {ruta_tiempo:<25} {ruta_costo:<25}")
            
            # Vehículos
            vehiculos_tiempo = ", ".join(set(tiempo_it.obtener_vehiculos_utilizados()))
            vehiculos_costo = ", ".join(set(costo_it.obtener_vehiculos_utilizados()))
            print(f"{'Vehiculo:':<15} {vehiculos_tiempo:<25} {vehiculos_costo:<25}")
            
            # Métricas
            tiempo_formateado_tiempo = tiempo_it.obtener_tiempo_total_formateado()
            tiempo_formateado_costo = costo_it.obtener_tiempo_total_formateado()
            print(f"{'Tiempo:':<15} {tiempo_formateado_tiempo:<25} {tiempo_formateado_costo:<25}")
            
            costo_tiempo_str = f"${tiempo_it.costo_total:.2f}"
            costo_costo_str = f"${costo_it.costo_total:.2f}"
            print(f"{'Costo:':<15} {costo_tiempo_str:<25} {costo_costo_str:<25}")
            
            distancia_tiempo_str = f"{tiempo_it.obtener_distancia_total():.1f} km"
            distancia_costo_str = f"{costo_it.obtener_distancia_total():.1f} km"
            print(f"{'Distancia:':<15} {distancia_tiempo_str:<25} {distancia_costo_str:<25}")
            
            print(f"\nANALISIS:")
            print("-" * 20)
            
            # Determinar mejor opción
            if tiempo_it.tiempo_total < costo_it.tiempo_total:
                print(f"Más rápido: Optimización por TIEMPO ({tiempo_it.obtener_tiempo_total_formateado()})")
            else:
                print(f"Más rápido: Optimización por COSTO ({costo_it.obtener_tiempo_total_formateado()})")
                
            if tiempo_it.costo_total < costo_it.costo_total:
                print(f"Más barato: Optimización por TIEMPO (${tiempo_it.costo_total:.2f})")
            else:
                print(f"Más barato: Optimización por COSTO (${costo_it.costo_total:.2f})")
            
            # Análisis de diferencias para recomendación
            diferencia_tiempo = abs(tiempo_it.tiempo_total - costo_it.tiempo_total)
            diferencia_costo = abs(tiempo_it.costo_total - costo_it.costo_total)
            
            print(f"\nRECOMENDACION:")
            if diferencia_costo > tiempo_it.costo_total * 0.2:  # Diferencia mayor al 20%
                porcentaje_ahorro = (diferencia_costo / max(tiempo_it.costo_total, costo_it.costo_total)) * 100
                print(f"  Diferencia de costo significativa: ${diferencia_costo:.2f} ({porcentaje_ahorro:.1f}%)")
                print(f"  Recomendamos OPTIMIZACION POR COSTO para maximizar ahorro")
            elif diferencia_tiempo > 2:  # Diferencia mayor a 2 horas
                print(f"  Diferencia de tiempo significativa: {diferencia_tiempo:.1f} horas")
                print(f"  Recomendamos OPTIMIZACION POR TIEMPO para entregas urgentes")
            else:
                print(f"  Ambas opciones son similares")
                print(f"  Elegir según prioridad del cliente: rapidez vs economia")
        
        print("\n" + "="*60)
    
    '''
    # Gráficos comparativos finales
    if GRAFICOS_DISPONIBLES and (len(resultados_tiempo) > 1 or len(resultados_costo) > 1):
        try:
            print(f"\nGenerando gráficos comparativos...")
            if resultados_tiempo:
                grafico_comparacion_tiempos(resultados_tiempo)
            if resultados_costo:
                grafico_comparacion_caminos(resultados_costo)
        except Exception as e:
            print(f"Error en gráficos comparativos: {e}")
    '''

def mostrar_estadisticas_detalladas(sistema):
    """
    Muestra estadísticas detalladas del sistema cargado.
    """
    print(f"\nESTADISTICAS DETALLADAS:")
    print("-" * 40)
    
    stats = sistema.obtener_estadisticas()
    
    print(f"Red de transporte:")
    print(f"  - Nodos: {stats['total_nodos']}")
    print(f"  - Conexiones: {stats['total_conexiones']}")
    
    print(f"\nConexiones por modo de transporte:")
    for modo, cantidad in stats['conexiones_por_tipo'].items():
        porcentaje = (cantidad / stats['total_conexiones']) * 100
        print(f"  - {modo.capitalize()}: {cantidad} ({porcentaje:.1f}%)")
    
    print(f"\nSolicitudes de transporte:")
    print(f"  - Total: {stats['total_solicitudes']}")
    
    peso_stats = stats['solicitudes_por_peso']
    total_solicitudes = sum(peso_stats.values())
    if total_solicitudes > 0:
        print(f"  - Cargas ligeras (<10 ton): {peso_stats['ligeras']} ({(peso_stats['ligeras']/total_solicitudes)*100:.1f}%)")
        print(f"  - Cargas medianas (10-50 ton): {peso_stats['medianas']} ({(peso_stats['medianas']/total_solicitudes)*100:.1f}%)")
        print(f"  - Cargas pesadas (>50 ton): {peso_stats['pesadas']} ({(peso_stats['pesadas']/total_solicitudes)*100:.1f}%)")


def validar_sistema(sistema):
    """
    Valida la integridad del sistema y reporta posibles problemas.
    """
    print(f"\nVALIDACION DEL SISTEMA:")
    print("-" * 40)
    
    errores = sistema.validar_integridad()
    
    if not errores:
        print("Sistema validado correctamente")
        print("Todos los nodos están correctamente referenciados")
        print("Todas las conexiones son válidas")
        return True
    else:
        print(f"Se encontraron {len(errores)} problemas:")
        for error in errores:
            print(f"  - {error}")
        return False


def main():
    """
    Función principal: carga datos, crea planificador y procesa solicitudes.
    Maneja errores comunes como archivos faltantes.
    """
    print("="*50)
    print("SISTEMA DE TRANSPORTE - INICIANDO")
    print("="*50)
    print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    try:
        # Crear sistema y cargar datos
        print("Inicializando sistema de transporte...")
        sistema = SistemaTransporte()
        
        print("Cargando datos desde archivos CSV...")
        sistema.cargar_nodos('nodos.csv')
        sistema.cargar_conexiones('conexiones.csv')
        sistema.cargar_solicitudes('solicitudes.csv')
        
        # Mostrar información del sistema
        sistema.mostrar_resumen()
        mostrar_estadisticas_detalladas(sistema)
        
        # Validar integridad del sistema
        if not validar_sistema(sistema):
            print("\nSe detectaron problemas en el sistema.")
            print("El procesamiento continuará, pero algunos resultados pueden ser incorrectos.")
        
        # Verificar conectividad
        sistema.verificar_conectividad()
        
        # Crear planificador y procesar solicitudes
        print(f"\nCreando planificador...")
        planificador = Planificador(sistema)
        print(f"Planificador listo con {len(planificador.vehiculos_disponibles)} tipos de vehículos")
        
        # Exportar resumen detallado
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            sistema.exportar_resumen(f"output/resumen_ejecucion_{timestamp}.txt")
            print(f"Resumen exportado: resumen_ejecucion_{timestamp}.txt")
        except Exception as e:
            print(f"Advertencia: No se pudo exportar resumen: {e}")
        
        # Procesar todas las solicitudes
        procesar_solicitudes(sistema, planificador)
        
        print(f"\nPROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("="*50)
        
        # Mostrar resumen final
        print(f"\nRESUMEN FINAL:")
        print(f"- Nodos procesados: {len(sistema.nodos)}")
        print(f"- Conexiones cargadas: {len(sistema.conexiones)}")
        print(f"- Solicitudes procesadas: {len(sistema.solicitudes)}")
        if GRAFICOS_DISPONIBLES:
            print(f"- Gráficos generados: SÍ")
        else:
            print(f"- Gráficos generados: NO (instalar matplotlib)")
        
    except FileNotFoundError as e:
        print(f"\nERROR: No se encontró archivo requerido")
        print(f"Archivo faltante: {e.filename}")
        print("\nARCHIVOS NECESARIOS:")
        print("  - nodos.csv - Lista de ciudades/nodos")
        print("  - conexiones.csv - Rutas entre nodos con restricciones") 
        print("  - solicitudes.csv - Solicitudes de transporte")
        print("\nSOLUCION:")
        print("  1. Verificar que los archivos estén en el directorio actual")
        print("  2. Revisar que los nombres de archivo sean correctos")
        print("  3. Consultar la documentación para el formato requerido")
        
    except Exception as e:
        print(f"\nERROR INESPERADO: {e}")
        print("\nINFORMACION DEL ERROR:")
        import traceback
        traceback.print_exc()
        
        print("\nPOSIBLES CAUSAS:")
        print("  - Formato incorrecto en archivos CSV")
        print("  - Referencias inconsistentes entre nodos y conexiones")
        print("  - Datos numéricos inválidos (distancias, pesos, etc.)")
        print("  - Caracteres especiales en nombres de nodos")
        
        print("\nRECOMENDACIONES:")
        print("  - Revisar el formato de los archivos CSV")
        print("  - Validar que los nombres de nodos sean consistentes")
        print("  - Verificar que todos los valores numéricos sean válidos")


if __name__ == "__main__":
    main()