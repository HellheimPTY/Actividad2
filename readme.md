# 📂 Asignación: Estructura de Datos y Algoritmos (Registro Civil)

## 📜 Descripción del Proyecto
Este proyecto resuelve una asignación de Estructura de Datos y Algoritmos implementando un sistema de gestión simplificado para un Registro Civil. El objetivo principal es modelar eficientemente los registros de personas y eventos de casamiento utilizando estructuras de datos avanzadas.

El proyecto se centra en:

- Modelar el registro de varones en un Árbol Binario de Búsqueda (ABB), ordenado por DNI.

- Implementar el algoritmo para la modificación de datos de una persona en el ABB.

- Desarrollar un algoritmo para corregir masivamente el estado civil de todas las personas, consultando el registro de casamientos.

## 🛠️ Requisitos del Sistema
Para ejecutar el script es necesario tener instalado Python y las siguientes bibliotecas:

pandas: Para la extracción y manipulación de datos desde el archivo Excel.

openpyxl: Motor necesario para que pandas pueda leer archivos .xlsx.

Puedes instalar las dependencias con el siguiente comando:

Bash

pip install pandas openpyxl

## ⚙️ Estructura de Archivos
El proyecto consta de los siguientes archivos clave:

Archivo	Función
registro_civil.py	Contiene el código fuente en Python, incluyendo las clases Nodo, la construcción del ABB, y los algoritmos de modificación y corrección.
registro_civil.xlsx	Archivo de entrada de datos. Debe contener las tres hojas especificadas.
README.md	Este archivo de documentación.


## 📊 Preparación de los Datos (Excel)
El script espera encontrar un archivo llamado registro_civil.xlsx en el mismo directorio de ejecución. Este archivo debe contener tres hojas (tabs) con las siguientes estructuras:

Hoja	Columnas Requeridas	Estructura de Datos Asociada	Clave de Búsqueda
Mujeres	DNI, Apellido, Nombre, EstadoCivil	Diccionario (Tabla Hash)	DNI
Varones	DNI, Apellido, Nombre, EstadoCivil	Árbol Binario de Búsqueda (ABB)	DNI
Casamientos	DNI_Femenino, DNI_Masculino, FechaCasamiento	DataFrame (Lista)	N/A (Se itera)

Asegúrate de que los encabezados de las columnas coincidan exactamente con los nombres especificados, respetando mayúsculas y minúsculas.

## 🚀 Uso del Programa
Para ejecutar el script principal, abre tu terminal o línea de comandos, navega hasta el directorio del proyecto y ejecuta:

Bash

python registro_civil.py
El programa ejecutará las siguientes acciones en secuencia:

Extracción de Datos desde registro_civil.xlsx.

Construcción del ABB de Varones.

Demostración del procedimiento de Modificación de Datos (ejemplo: cambia el estado civil de una persona).

Ejecución del algoritmo de Corrección Masiva (corregir_estado_civil).

Muestra la Verificación Final de los estados civiles corregidos.

## 💻 Algoritmos Clave Implementados
1. Modelado: Árbol Binario de Búsqueda (ABB)
Estructura: Implementado mediante la clase Nodo y la función construir_abb_varones.

Clave: DNI (Entero).

Eficiencia: La búsqueda de un varón por DNI es O(logn) en el caso promedio.

2. Modificación de Datos
Función: modificar_datos_persona(raiz, dni, nuevos_datos).

Mecanismo: Utiliza la función recursiva buscar_nodo_por_dni para localizar el nodo en el ABB. Una vez encontrado el nodo, sus atributos se actualizan directamente.

3. Corrección del Estado Civil (Post-Virus)
Función: corregir_estado_civil(registro_mujeres, raiz_varones, df_casamientos).

Proceso:

Reinicia el estado civil de todas las personas a "Soltero/a" (recorrido O(n)).

Itera sobre cada registro en la lista de casamientos.

Busca a la mujer en la Tabla Hash (diccionario), O(1).

Busca al varón en el ABB, O(logn).

Si ambos cónyuges son encontrados, su estado civil se actualiza a "Casado/a".

Complejidad Asintótica: El proceso total de corrección es altamente eficiente, con una complejidad dominada por O(klogn) donde k es el número de casamientos.

Autor: Hellheim
Asignatura: Estructura de Datos y Algoritmos