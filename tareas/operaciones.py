"""
Modulo 'operaciones': logica del programa sobre la lista de tareas.
Contiene las operaciones principales del sistema (agregar, completar y filtrar).
"""

from tareas.modelo import crear_tarea, PESO_PRIORIDAD


def calcular_nuevo_id(tareas):
    """
    Calcula el proximo id disponible.

    Recorre la lista buscando el id mas alto y le suma 1. Si la lista esta
    vacia, el primer id es 1. Asi cada tarea tiene un identificador unico.
    """
    mayor_id = 0
    # Recorrido con 'for' para encontrar el id maximo.
    for tarea in tareas:
        if tarea["id"] > mayor_id:
            mayor_id = tarea["id"]
    return mayor_id + 1


def agregar_tarea(tareas, descripcion, prioridad, vencimiento, horas_estimadas=0.0):
    """
    Crea una tarea nueva y la agrega a la lista.

    Usa PARAMETRO OPCIONAL 'horas_estimadas' (0.0 por defecto). Devuelve la
    tarea creada para poder mostrarla.
    """
    nuevo_id = calcular_nuevo_id(tareas)
    tarea = crear_tarea(
        id_tarea=nuevo_id,
        descripcion=descripcion,
        prioridad=prioridad.strip().lower(),
        vencimiento=vencimiento,
        horas_estimadas=horas_estimadas,
    )
    tareas.append(tarea)
    return tarea


def completar_tarea(tareas, id_tarea):
    """
    Marca como completada la tarea cuyo id coincide con 'id_tarea'.

    Devuelve True si encontro y actualizo la tarea, o False si no existe
    ninguna con ese id.
    """
    for tarea in tareas:
        if tarea["id"] == id_tarea:
            tarea["completada"] = True  # se modifica el campo booleano
            return True
    return False


def filtrar_tareas(tareas, prioridad=None, estado=None):
    """
    Devuelve una lista nueva con las tareas que cumplen los filtros.

    Los dos filtros son PARAMETROS OPCIONALES:
        - prioridad: 'alta', 'media' o 'baja'. Si es None no filtra por prioridad.
        - estado   : 'completada' o 'pendiente'. Si es None no filtra por estado.

    Cuando ambos son None, devuelve todas las tareas.
    """
    resultado = []

    for tarea in tareas:
        # Por defecto la tarea entra, y se descarta si falla algun filtro.
        coincide = True

        # Filtro por prioridad (solo si se paso el parametro).
        if prioridad is not None:
            if tarea["prioridad"] != prioridad.strip().lower():
                coincide = False

        # Filtro por estado (solo si se paso el parametro).
        if estado is not None:
            estado_pedido = estado.strip().lower()
            if estado_pedido == "completada" and not tarea["completada"]:
                coincide = False
            elif estado_pedido == "pendiente" and tarea["completada"]:
                coincide = False

        if coincide:
            resultado.append(tarea)

    return resultado


def ordenar_por_prioridad(tareas):
    """
    Devuelve una copia de la lista ordenada por prioridad (alta primero).
    """
    return sorted(tareas, key=lambda t: PESO_PRIORIDAD.get(t["prioridad"], 99))


def contar_por_estado(tareas):
    """
    Cuenta cuantas tareas hay completadas y cuantas pendientes.
    Devuelve una tupla (completadas, pendientes) con dos enteros.
    """
    completadas = 0
    pendientes = 0
    for tarea in tareas:
        if tarea["completada"]:
            completadas += 1
        else:
            pendientes += 1
    return (completadas, pendientes)
