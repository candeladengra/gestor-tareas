"""
Modulo 'modelo': define la estructura de datos de una tarea.

Decision de diseno: cada tarea se representa como un DICCIONARIO, porque
permite acceder a cada dato por un nombre claro. El conjunto de todas las
tareas se maneja como una lista de diccionarios.

Las prioridades y los estados se definen como tuplas, porque son valores
fijos que no deben modificarse durante la ejecucion del programa.
"""

# Tupla con las prioridades validas, ordenadas de mayor a menor importancia.
PRIORIDADES = ("alta", "media", "baja")

# Tupla con los dos estados posibles de una tarea.
ESTADOS = ("pendiente", "completada")

# Peso numerico de cada prioridad, usado para ordenar las tareas.
# Cuanto mas bajo el numero, mas urgente es la tarea.
PESO_PRIORIDAD = {"alta": 1, "media": 2, "baja": 3}


def crear_tarea(
    id_tarea, descripcion, prioridad, vencimiento, horas_estimadas=0.0, completada=False
):
    """
    Construye y devuelve una tarea como diccionario.

    PARAMETROS OPCIONALES: 'horas_estimadas' (por defecto 0.0) y 'completada'
    (por defecto False).

    Parametros:
        id_tarea (int)        : identificador unico de la tarea.
        descripcion (str)     : texto que describe la tarea.
        prioridad (str)       : 'alta', 'media' o 'baja'.
        vencimiento (str)     : fecha de vencimiento en formato dd/mm/aaaa.
        horas_estimadas (float): horas estimadas de trabajo (opcional).
        completada (bool)     : True si la tarea ya esta hecha (opcional).

    Devuelve:
        dict: la tarea con todos sus campos.
    """
    return {
        "id": id_tarea,  # int
        "descripcion": descripcion,  # str
        "prioridad": prioridad,  # str
        "vencimiento": vencimiento,  # str
        "horas_estimadas": horas_estimadas,  # float
        "completada": completada,  # bool
    }


def estado_de(tarea):
    """
    Devuelve el estado de una tarea ('completada' o 'pendiente') como texto,
    a partir del campo booleano 'completada'.
    """
    if tarea["completada"]:
        return "completada"
    return "pendiente"


def formatear_tarea(tarea):
    """
    Arma una linea de texto legible para mostrar una tarea por pantalla.

    Ejemplo de salida:
        [ ] #3  (alta )  vence 15/09/2026  5.0h  -> Terminar el TP
    """
    # Marca visual segun el booleano 'completada'.
    marca = "X" if tarea["completada"] else " "

    # ljust/str.format se usan solo para alinear las columnas al imprimir.
    return "[{}] #{}  ({})  vence {}  {}h  -> {}".format(
        marca,
        tarea["id"],
        tarea["prioridad"].ljust(5),
        tarea["vencimiento"],
        tarea["horas_estimadas"],
        tarea["descripcion"],
    )
