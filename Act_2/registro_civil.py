# actividad2.py
import pandas as pd

# =============================================================================
# 0. CONFIGURACIÓN Y EXTRACCIÓN DE DATOS DESDE EXCEL
# =============================================================================

NOMBRE_ARCHIVO_EXCEL = 'registro_civil.xlsx'

def extraer_datos(nombre_archivo):
    """
    Extrae los datos de las tres hojas del archivo Excel.
    
    PRECONDICIÓN: El archivo Excel debe contener 3 hojas (tabs) llamadas:
    'Mujeres', 'Varones', y 'Casamientos'.
    """
    try:
        # 1. Extracción de los DataFrames
        df_mujeres = pd.read_excel(nombre_archivo, sheet_name='Mujeres')
        df_varones = pd.read_excel(nombre_archivo, sheet_name='Varones')
        df_casamientos = pd.read_excel(nombre_archivo, sheet_name='Casamientos')
        
        # 2. Preparación del registro de mujeres para búsquedas O(1)
        # Se convierte el DataFrame a un diccionario usando DNI como clave.
        registro_mujeres = df_mujeres.set_index('DNI').to_dict('index')

        print(f"✅ Datos cargados exitosamente de '{nombre_archivo}'.")
        return registro_mujeres, df_varones, df_casamientos
    
    except FileNotFoundError:
        print(f"❌ Error: El archivo '{nombre_archivo}' no se encontró. Asegúrate de que esté en la misma carpeta.")
        return None, None, None
    except ValueError as e:
        print(f"❌ Error al leer las hojas del Excel. Verifica los nombres de las hojas: Mujeres, Varones, Casamientos. Detalles: {e}")
        return None, None, None


# =============================================================================
# 1. MODELADO: CLASE NODO Y ÁRBOL BINARIO DE BÚSQUEDA (ABB)
# =============================================================================

class Nodo:
    """Clase para representar un nodo en el ABB (Varón)."""
    def __init__(self, dni, apellido, nombre, estado_civil):
        self.DNI = dni  # Clave de ordenamiento
        self.Apellido = apellido
        self.Nombre = nombre
        self.EstadoCivil = estado_civil
        self.izquierdo = None
        self.derecho = None

def construir_abb_varones(df_varones):
    """Crea el ABB insertando cada varón del DataFrame."""
    raiz = None
    if df_varones is None:
        return None
        
    for _, fila in df_varones.iterrows():
        dni, apellido, nombre, estado_civil = fila['DNI'], fila['Apellido'], fila['Nombre'], fila['EstadoCivil']
        nuevo_nodo = Nodo(dni, apellido, nombre, estado_civil)
        
        if raiz is None:
            raiz = nuevo_nodo
            continue
        
        actual = raiz
        while True:
            if dni < actual.DNI:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo_nodo
                    break
                actual = actual.izquierdo
            elif dni > actual.DNI:
                if actual.derecho is None:
                    actual.derecho = nuevo_nodo
                    break
                actual = actual.derecho
            # Si DNI es igual, no se inserta (se ignora duplicado)
            else:
                break 
    return raiz

# =============================================================================
# 2. ACTIVIDAD: MODIFICACIÓN DE DATOS (Búsqueda y Actualización en ABB)
# =============================================================================

def buscar_nodo_por_dni(raiz, dni_buscado):
    """Busca un nodo en el ABB por DNI de forma recursiva (O(log n))."""
    if raiz is None or raiz.DNI == dni_buscado:
        return raiz
    
    if dni_buscado < raiz.DNI:
        return buscar_nodo_por_dni(raiz.izquierdo, dni_buscado)
    else:
        return buscar_nodo_por_dni(raiz.derecho, dni_buscado)

def modificar_datos_persona(raiz_varones, dni_modificar, nuevos_datos):
    """Modifica los datos de un varón dado su DNI en el ABB."""
    if raiz_varones is None:
        print("❌ Error: El ABB de varones está vacío.")
        return
        
    nodo_a_modificar = buscar_nodo_por_dni(raiz_varones, dni_modificar)
    
    if nodo_a_modificar:
        # Aplicar la modificación solo si el campo existe en nuevos_datos
        nodo_a_modificar.Apellido = nuevos_datos.get('Apellido', nodo_a_modificar.Apellido)
        nodo_a_modificar.Nombre = nuevos_datos.get('Nombre', nodo_a_modificar.Nombre)
        nodo_a_modificar.EstadoCivil = nuevos_datos.get('EstadoCivil', nodo_a_modificar.EstadoCivil)
            
        print(f"✅ DNI {dni_modificar} (Varón): Datos modificados. Nuevo Estado Civil: {nodo_a_modificar.EstadoCivil}")
    else:
        print(f"❌ Error: DNI {dni_modificar} no encontrado en el registro de varones (ABB).")

# =============================================================================
# 3. ACTIVIDAD: CORRECCIÓN DEL ESTADO CIVIL
# =============================================================================

def establecer_estado_soltero_abb(nodo):
    """Recorrido InOrden para establecer todos los varones a 'Soltero'."""
    if nodo:
        establecer_estado_soltero_abb(nodo.izquierdo)
        nodo.EstadoCivil = "Soltero"
        establecer_estado_soltero_abb(nodo.derecho)

def corregir_estado_civil(registro_mujeres, raiz_varones, df_casamientos):
    """
    Algoritmo para corregir el Estado Civil basándose en el registro de casamientos.
    """
    if raiz_varones is None:
        print("⚠️ Advertencia: No hay varones para corregir.")
        return

    # PASO 1: Resetear todos a Soltero/a
    establecer_estado_soltero_abb(raiz_varones)
    for dni in registro_mujeres:
        registro_mujeres[dni]['EstadoCivil'] = "Soltera"
    print("✅ Estado civil reiniciado a 'Soltero/a' para todos (limpieza post-virus simulada).")
    
    # PASO 2: Procesar Casamientos y establecer "Casado/a"
    print("--- Proceso de corrección: Casamientos ---")
    
    for _, evento in df_casamientos.iterrows():
        dni_f = evento['DNI_Femenino']
        dni_m = evento['DNI_Masculino']

        # A. Corregir Mujer (uso del diccionario O(1))
        if dni_f in registro_mujeres:
            registro_mujeres[dni_f]['EstadoCivil'] = "Casada"
        
        # B. Corregir Varón (uso de la búsqueda en ABB O(log n))
        nodo_varon = buscar_nodo_por_dni(raiz_varones, dni_m)
        if nodo_varon:
            nodo_varon.EstadoCivil = "Casado"
    
    print("✅ Corrección de estados civiles a 'Casado/a' completada.")

    # --- FUNCIÓN DE VERIFICACIÓN (Opcional: Muestra los resultados) ---
    def abb_a_lista(nodo, resultado):
        if nodo:
            abb_a_lista(nodo.izquierdo, resultado)
            resultado.append({'DNI': nodo.DNI,'Nombre': nodo.Nombre, 'Apellido': nodo.Apellido, 'EstadoCivil': nodo.EstadoCivil})
            abb_a_lista(nodo.derecho, resultado)
            
    varones_final = []
    abb_a_lista(raiz_varones, varones_final)
    
    print("\n--- VERIFICACIÓN DE VARONES ---")
    print(pd.DataFrame(varones_final)[['DNI','Nombre', 'Apellido', 'EstadoCivil']])
    
    print("\n--- VERIFICACIÓN DE MUJERES ---")
    df_mujeres_final = pd.DataFrame.from_dict(registro_mujeres, orient='index').reset_index().rename(columns={'index': 'DNI'})
    print(df_mujeres_final[['DNI', 'Nombre','Apellido', 'EstadoCivil']])


# =============================================================================
# 5. EJECUCIÓN PRINCIPAL
# =============================================================================

# 1. Extraer datos del Excel
registro_mujeres, df_varones, df_casamientos = extraer_datos(NOMBRE_ARCHIVO_EXCEL)

if df_varones is not None:
    # 2. Construir el ABB de Varones
    raiz_varones = construir_abb_varones(df_varones)

    # 3. Demostración de Modificación de Datos
    print("\n--- DEMOSTRACIÓN: MODIFICACIÓN DE DATOS ---")
    # Intentamos cambiar el estado civil de un varón a "Unión Libre"
    modificar_datos_persona(raiz_varones, 21789423, {'EstadoCivil': 'Unión Libre'})
    
    # 4. Corregir los Estados Civiles (Esto anulará la modificación anterior, 
    # ya que 21789423 no está en casamientos y volverá a 'Soltero')
    corregir_estado_civil(registro_mujeres, raiz_varones, df_casamientos)
