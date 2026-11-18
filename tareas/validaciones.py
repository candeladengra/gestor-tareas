"""
Modulo 'validaciones': valida los datos ingresados por el usuario
mediante expresiones regulares.
"""

import re  # modulo estandar de expresiones regulares

from tareas.modelo import PRIORIDADES

# Expresion regular para una fecha con formato dd/mm/aaaa.
# ^        -> inicio del texto
# \d{2}    -> exactamente dos digitos (dia)
# /        -> barra separadora literal
# \d{2}    -> dos digitos (mes)
# \d{4}    -> cuatro digitos (anio)
# $        -> fin del texto
# Se compila una sola vez para reutilizarla en cada validacion.
PATRON_FECHA = re.compile(r"^\d{2}/\d{2}/\d{4}$")

# Expresion regular para las horas: un numero entero o decimal.
# Acepta "5", "5.0" o "2.5"; no acepta letras ni valores vacios.
PATRON_HORAS = re.compile(r"^\d+(\.\d+)?$")


def validar_fecha(texto):
    """
    Valida que 'texto' sea una fecha real en formato dd/mm/aaaa.

    Primero comprueba el FORMATO con una expresion regular y despues
    verifica que el dia y el mes existan de verdad (por ejemplo, rechaza
    32/13/2026). Devuelve True o False (bool).
    """
    # Paso 1: el formato debe coincidir con el patron dd/mm/aaaa.
    if PATRON_FECHA.match(texto) is None:
        return False

    # Paso 2: separar los numeros y comprobar que formen una fecha valida.
    dia, mes, anio = texto.split("/")
    dia = int(dia)
    mes = int(mes)
    anio = int(anio)

    # Cantidad de dias por mes (indice 0 no se usa; enero = posicion 1).
    dias_por_mes = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    # El mes debe estar entre 1 y 12.
    if mes < 1 or mes > 12:
        return False

    # El dia debe estar entre 1 y el maximo del mes correspondiente.
    if dia < 1 or dia > dias_por_mes[mes]:
        return False

    # El anio se limita a un rango razonable
    if anio < 2000 or anio > 2100:
        return False

    return True


def validar_prioridad(texto):
    """
    Devuelve True si 'texto' es una prioridad valida ('alta', 'media' o
    'baja'), sin importar mayusculas o espacios sobrantes.
    """
    return texto.strip().lower() in PRIORIDADES


def validar_horas(texto):
    """
    Valida que 'texto' represente un numero de horas valido (entero o
    decimal) usando una expresion regular. Devuelve True o False.
    """
    return PATRON_HORAS.match(texto.strip()) is not None


def descripcion_es_valida(texto):
    """
    Comprueba que la descripcion no este vacia y no contenga el caracter
    '|', que se reserva como separador del archivo plano. Esta decision de
    diseno evita que una descripcion rompa el formato del archivo.
    """
    if texto.strip() == "":
        return False
    if "|" in texto:
        return False
    return True
