"""
Modulo 'almacenamiento': gestiona el repositorio de datos en ARCHIVO PLANO.

Las tareas se guardan en un archivo de texto (datos/tareas.txt), donde cada
linea es una tarea y los campos se separan con el caracter '|'.

Formato de cada linea:
    id|descripcion|prioridad|vencimiento|horas_estimadas|completada

Ejemplo:
    1|Terminar el TP de Programacion II|alta|15/09/2026|5.0|0

El campo 'completada' se guarda como '1' (True) o '0' (False).
"""

import os  # para construir rutas y comprobar si el archivo existe

from tareas.modelo import crear_tarea

# Separador de campos dentro de cada linea del archivo.
SEPARADOR = "|"

# Ruta del archivo de datos, relativa a la carpeta de este modulo.
CARPETA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_ARCHIVO = os.path.join(CARPETA_BASE, "datos", "tareas.txt")


def guardar_tareas(tareas):
    """
    Escribe la lista completa de tareas en el archivo plano.

    Recorre la lista con un 'for' y arma una linea de texto por cada tarea.
    Devuelve True si pudo guardar y False si ocurrio un error de escritura
    (control de errores con try/except).
    """
    try:
        # 'with' asegura que el archivo se cierre aunque ocurra un error.
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as archivo:
            for tarea in tareas:
                # Convertir el booleano a '1' o '0' para el texto plano.
                completada = "1" if tarea["completada"] else "0"

                # Unir todos los campos con el separador '|'.
                linea = SEPARADOR.join(
                    [
                        str(tarea["id"]),
                        tarea["descripcion"],
                        tarea["prioridad"],
                        tarea["vencimiento"],
                        str(tarea["horas_estimadas"]),
                        completada,
                    ]
                )
                archivo.write(linea + "\n")
        return True
    except OSError:
        # Si el sistema no puede escribir (permisos, disco, etc.)
        return False


def cargar_tareas():
    """
    Lee el archivo plano y devuelve una lista de tareas (diccionarios).

    Si el archivo todavia no existe (primera ejecucion), devuelve una lista
    vacia. Las lineas mal formadas se ignoran para no cortar el programa.
    """
    tareas = []

    # Si el archivo aun no fue creado, no hay nada que cargar.
    if not os.path.exists(RUTA_ARCHIVO):
        return tareas

    try:
        with open(RUTA_ARCHIVO, "r", encoding="utf-8") as archivo:
            # Recorremos el archivo linea por linea.
            for linea in archivo:
                linea = linea.strip()

                # Saltar lineas vacias.
                if linea == "":
                    continue

                partes = linea.split(SEPARADOR)

                # Una linea valida debe tener exactamente 6 campos.
                if len(partes) != 6:
                    continue

                # Reconstruir la tarea convirtiendo cada campo a su tipo.
                tarea = crear_tarea(
                    id_tarea=int(partes[0]),
                    descripcion=partes[1],
                    prioridad=partes[2],
                    vencimiento=partes[3],
                    horas_estimadas=float(partes[4]),
                    completada=(partes[5] == "1"),
                )
                tareas.append(tarea)
    except OSError:
        # Ante un error de lectura devolvemos lo que se haya podido cargar.
        return tareas

    return tareas
