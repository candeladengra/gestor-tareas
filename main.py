"""
Programa principal.

Este archivo es el PUNTO DE ENTRADA del sistema. Se encarga de la interaccion
con el usuario (menu, entradas por teclado y salidas por pantalla) y delega
la logica en los modulos del paquete 'tareas'.
"""

from tareas.modelo import ESTADOS, formatear_tarea
from tareas.validaciones import (
    descripcion_es_valida,
    validar_fecha,
    validar_horas,
    validar_prioridad,
)
from tareas.almacenamiento import cargar_tareas, guardar_tareas
from tareas.operaciones import (
    agregar_tarea,
    completar_tarea,
    contar_por_estado,
    filtrar_tareas,
    ordenar_por_prioridad,
)


# ---------------------------------------------------------------------------
# Funciones auxiliares de entrada por teclado (con control de errores)
# ---------------------------------------------------------------------------


def pedir_texto(mensaje):
    """
    Pide un texto por teclado y no acepta una respuesta vacia.

    Repite la pregunta con un 'while' hasta que el usuario escriba algo.
    """
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("  ! No podes dejar este campo vacio. Intenta de nuevo.")


def pedir_entero(mensaje):
    """
    Pide un numero entero por teclado, controlando errores de conversion.

    Si el usuario escribe algo que no es un numero, se captura la excepcion
    ValueError y se vuelve a preguntar
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            return int(entrada)
        except ValueError:
            print("  ! Tenes que ingresar un numero entero valido.")


def pedir_fecha(mensaje):
    """
    Pide una fecha de vencimiento y la valida con la expresion regular
    del modulo de validaciones. Repite hasta que sea una fecha correcta.
    """
    while True:
        fecha = input(mensaje).strip()
        if validar_fecha(fecha):
            return fecha
        print("  ! Fecha invalida. Usa el formato dd/mm/aaaa (ej: 15/09/2026).")


def pedir_prioridad(mensaje):
    """
    Pide una prioridad y la valida contra las prioridades permitidas.
    Devuelve siempre la prioridad en minusculas.
    """
    while True:
        prioridad = input(mensaje).strip().lower()
        if validar_prioridad(prioridad):
            return prioridad
        print("  ! Prioridad invalida. Opciones: alta, media, baja.")


def pedir_horas(mensaje):
    """
    Pide las horas estimadas (numero decimal). Es un dato OPCIONAL: si el
    usuario presiona Enter sin escribir nada, se asume 0.0 horas.
    """
    while True:
        entrada = input(mensaje).strip()

        # Si el usuario no ingresa nada, usamos el valor por defecto.
        if entrada == "":
            return 0.0

        # Validamos el formato con expresion regular antes de convertir.
        if validar_horas(entrada):
            return float(entrada)
        print("  ! Ingresa un numero valido (ej: 3 o 2.5) o Enter para 0.")


# ---------------------------------------------------------------------------
# Funciones de presentacion (salida por pantalla)
# ---------------------------------------------------------------------------


def mostrar_tareas(tareas, titulo="Tareas"):
    """
    Muestra por pantalla una lista de tareas ya ordenada por prioridad.

    Si la lista esta vacia, avisa que no hay tareas para mostrar.
    """
    print("\n=== {} ===".format(titulo))

    if len(tareas) == 0:
        print("  (no hay tareas para mostrar)")
        return

    # Recorremos la lista ordenada e imprimimos cada tarea formateada.
    for tarea in ordenar_por_prioridad(tareas):
        print("  " + formatear_tarea(tarea))


def mostrar_resumen(tareas):
    """Muestra un resumen con la cantidad de tareas por estado."""
    completadas, pendientes = contar_por_estado(tareas)
    total = len(tareas)
    print(
        "\nResumen: {} tarea(s) en total | {} pendiente(s) | {} completada(s).".format(
            total, pendientes, completadas
        )
    )


# ---------------------------------------------------------------------------
# Acciones del menu
# ---------------------------------------------------------------------------


def accion_agregar(tareas):
    """Pide los datos de una tarea nueva y la agrega a la lista."""
    print("\n--- Agregar tarea nueva ---")

    # Pedimos la descripcion y la validamos (no vacia, sin el caracter '|').
    while True:
        descripcion = pedir_texto("Descripcion: ")
        if descripcion_es_valida(descripcion):
            break
        print("  ! La descripcion no puede contener el caracter '|'.")

    prioridad = pedir_prioridad("Prioridad (alta/media/baja): ")
    vencimiento = pedir_fecha("Vencimiento (dd/mm/aaaa): ")
    horas = pedir_horas("Horas estimadas (Enter = 0): ")

    tarea = agregar_tarea(tareas, descripcion, prioridad, vencimiento, horas)
    print("  -> Tarea #{} agregada correctamente.".format(tarea["id"]))


def accion_completar(tareas):
    """Marca una tarea como completada segun su id."""
    print("\n--- Completar tarea ---")

    if len(tareas) == 0:
        print("  (no hay tareas cargadas todavia)")
        return

    # Mostramos primero las pendientes para que el usuario elija.
    pendientes = filtrar_tareas(tareas, estado="pendiente")
    mostrar_tareas(pendientes, "Tareas pendientes")

    if len(pendientes) == 0:
        return

    id_tarea = pedir_entero("Id de la tarea a completar: ")
    if completar_tarea(tareas, id_tarea):
        print("  -> Tarea #{} marcada como completada.".format(id_tarea))
    else:
        print("  ! No existe ninguna tarea con id #{}.".format(id_tarea))


def accion_filtrar(tareas):
    """
    Permite filtrar las tareas por prioridad o por estado.

    Muestra un submenu y arma los filtros que se pasan como parametros
    opcionales a la funcion filtrar_tareas.
    """
    print("\n--- Filtrar tareas ---")
    print("  1) Por prioridad")
    print("  2) Por estado (pendiente/completada)")
    print("  3) Volver")

    opcion = input("Elegi una opcion: ").strip()

    if opcion == "1":
        prioridad = pedir_prioridad("Prioridad a mostrar (alta/media/baja): ")
        resultado = filtrar_tareas(tareas, prioridad=prioridad)
        mostrar_tareas(resultado, "Tareas de prioridad " + prioridad)

    elif opcion == "2":
        # Validamos el estado con un 'while' hasta que sea correcto.
        while True:
            estado = input("Estado (pendiente/completada): ").strip().lower()
            if estado in ESTADOS:
                break
            print("  ! Estado invalido. Opciones: pendiente, completada.")
        resultado = filtrar_tareas(tareas, estado=estado)
        mostrar_tareas(resultado, "Tareas " + estado + "s")

    elif opcion == "3":
        return

    else:
        print("  ! Opcion invalida.")


def mostrar_menu():
    """Imprime el menu principal en pantalla."""
    print("\n" + "=" * 40)
    print("     GESTOR DE TAREAS CON PRIORIDADES")
    print("=" * 40)
    print("  1) Agregar tarea")
    print("  2) Ver todas las tareas")
    print("  3) Completar una tarea")
    print("  4) Filtrar tareas")
    print("  5) Guardar y salir")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------


def main():
    """
    Funcion principal: carga los datos, muestra el menu y ejecuta las
    acciones elegidas hasta que el usuario decide salir.
    """
    # Al iniciar, cargamos las tareas guardadas en el archivo plano.
    tareas = cargar_tareas()
    print("Se cargaron {} tarea(s) desde el archivo.".format(len(tareas)))

    # Bandera booleana que controla la continuidad del programa.
    seguir = True

    while seguir:
        mostrar_menu()
        opcion = input("Elegi una opcion (1-5): ").strip()

        if opcion == "1":
            accion_agregar(tareas)

        elif opcion == "2":
            mostrar_tareas(tareas, "Todas las tareas")
            mostrar_resumen(tareas)

        elif opcion == "3":
            accion_completar(tareas)

        elif opcion == "4":
            accion_filtrar(tareas)

        elif opcion == "5":
            # Guardamos en el archivo plano antes de cerrar.
            if guardar_tareas(tareas):
                print("\nTareas guardadas. Hasta la proxima!")
            else:
                print("\n! No se pudieron guardar las tareas (error de archivo).")
            seguir = False

        else:
            print("  ! Opcion invalida. Elegi un numero del 1 al 5.")


# Esta condicion asegura que main() se ejecute solo si corremos este archivo
# directamente (python main.py) y no cuando se importa desde otro modulo.
if __name__ == "__main__":
    main()
