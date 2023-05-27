import re
import csv
import json 
import os

with open('C:\\Users\\Usuario\\Desktop\\CAROLINA\\PYL 1C 2023\\Semana 9\\dt.json') as archivo:
    data_nba = json.load(archivo)

lista_nba = data_nba["jugadores"]

def quick_sort(lista_original: list, flag_orden: bool) -> list:
    lista_de = []
    lista_iz = []
    if len(lista_original) <= 1:
        return lista_original
    else:
        pivot = lista_original[0]
        for elemento in lista_original[1:]:
            if (elemento > pivot and flag_orden) or (elemento < pivot and not flag_orden):
                lista_de.append(elemento)
            else:
                lista_iz.append(elemento)
    lista_iz = quick_sort(lista_iz, flag_orden)
    lista_iz.append(pivot)
    lista_de = quick_sort(lista_de, flag_orden)
    lista_iz.extend(lista_de)
    return lista_iz

def ingresar_opcion(opciones: list) -> str:
    opcion = input(f"Ingresar una de las siguientes opciones: {opciones} ")
    while opcion not in opciones:
        print("Opción no válida. Inténtalo de nuevo.")
        opcion = input(f"Ingresar una de las siguientes opciones *RECORDA UTILIZAR MAYUSCULAS!*: {opciones} ")
    else:
        return opcion

def es_numero(numero):
    if numero.isdigit():
        return True
    elif numero.replace('.', '', 1).isnumeric():
        return True
    elif numero.replace(',', '', 1).isnumeric():
        return True
    else:
        return False

def mostrar_jugadores(lista):
    for jugador in lista:
        print("{} - {}".format(jugador["nombre"], jugador["posicion"]))


def mostrar_estadisticas_guardar_csv(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    indice_ingresado = int(input("Ingresar indice del jugador para ver sus estadisticas: "))
    while not indice_ingresado <= cantidad and indice_ingresado >= 0:
        indice_ingresado = input("Ingresar indice VALIDO del jugador para ver sus estadisticas: ")
    jugador_seleccionado = lista[indice_ingresado]
    estadisticas = jugador_seleccionado["estadisticas"]
    lista_datos_para_guardar = []
    for key, value in estadisticas.items():
        key_modificada = re.sub("_", " ", key)
        dato = "{}: {}".format(key_modificada.capitalize(), value)
        print(dato)
        lista_datos_para_guardar.append(dato)
    nombre_archivo = "C:\\Users\\Usuario\\Desktop\\CAROLINA\\PYL 1C 2023\\Semana 9\\estadisticas.csv"
    with open(nombre_archivo, "w") as file:
        file.write(jugador_seleccionado["nombre"] + "\n")
        file.write(jugador_seleccionado["posicion"] + "\n")
        for dato in lista_datos_para_guardar:
            file.write(str(dato) + "\n")

def mostrar_logro_jugador(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    lista_nombres = []
    for jugador in lista:
        lista_nombres.append(jugador["nombre"])
    opcion_seleccionada = ingresar_opcion(lista_nombres)
    for jugador in lista:
        if jugador["nombre"] == opcion_seleccionada:
            jugador_seleccionado = jugador
    logros = jugador_seleccionado["logros"]
    for logro in logros:
        print(str(logro))

def mostrar_promedio_puntos_ordenado_ascendente(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    dict_nombre_puntos = {}
    for jugador in lista:
        promedio_puntos = jugador["estadisticas"]["promedio_puntos_por_partido"]
        nombre = jugador["nombre"]
        dict_nombre_puntos[nombre] = promedio_puntos
    jugadores_puntos_ordenados = quick_sort(list(dict_nombre_puntos.values()), True)
    nombres_ordenados = []
    for promedio_puntos in jugadores_puntos_ordenados:
        for jugador in lista:
            if jugador["estadisticas"]["promedio_puntos_por_partido"] == promedio_puntos:
                nombres_ordenados.append(jugador["nombre"])
    print(nombres_ordenados)

def mostrar_si_es_miembro_salon(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    lista_nombres = []
    for jugador in lista:
        lista_nombres.append(jugador["nombre"])
    opcion_seleccionada = ingresar_opcion(lista_nombres)
    for jugador in lista:
        if jugador["nombre"] == opcion_seleccionada:
            jugador_seleccionado = jugador
    logros = jugador_seleccionado["logros"]
    string_es_miembro = "Miembro del Salon de la Fama del Baloncesto"
    if string_es_miembro in logros:
        print("{} es miembro del Salon de la Fama del Baloncesto".format(jugador_seleccionado["nombre"]))
    else:
        print("{} no es miembro del Salon de la Fama del Baloncesto".format(jugador_seleccionado["nombre"]))

def nombrar_mayor_en_una_estadistica(lista, valor_buscado):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    lista_totales = []
    for jugador in lista:
        lista_totales.append(jugador["estadisticas"][valor_buscado])
    maximo_total_algo = max(lista_totales)
    jugadores_con_mayor_cantidad = []
    for jugador in lista:
        if jugador["estadisticas"][valor_buscado] == maximo_total_algo:
            jugadores_con_mayor_cantidad.append(jugador["nombre"])
    valor_buscado_para_imprimir = re.sub("_", " ", valor_buscado)
    if len(jugadores_con_mayor_cantidad) == 1:
        print("El jugador con mayor cantidad de {} es {}".format(valor_buscado_para_imprimir, jugadores_con_mayor_cantidad[0]))
    else:
        print("Los jugadores con mayor cantidad de {} son: ".format(valor_buscado))
        print(jugadores_con_mayor_cantidad)

def mostrar_promedios_mayores_en_una_estadistica(lista, valor_buscado):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    valor_ingresado = input("Ingrese un valor numerico: ")
    while not es_numero(valor_ingresado):
        valor_ingresado = input("Ingrese un valor NUMERICO: ")
    lista_jugadores_superando_valor = []
    if "," in valor_ingresado or "." in valor_ingresado:
        if "," in valor_ingresado:
            valor_ingresado = re.sub(",", ".", valor_ingresado)
        valor_ingresado = float(valor_ingresado)
    else:
        valor_ingresado = int(valor_ingresado)
    for jugador in lista:
        if jugador["estadisticas"][valor_buscado] > valor_ingresado:
            lista_jugadores_superando_valor.append(jugador["nombre"])
    valor_buscado_para_imprimir = re.sub("_", " ", valor_buscado)
    if len(lista_jugadores_superando_valor) == 1:
        print("El jugador que supera el valor ingresado en {} es {} ".format(valor_buscado_para_imprimir, lista_jugadores_superando_valor[0]))
    elif len(lista_jugadores_superando_valor) == 0:
            print("Ningun jugador supera ese valor en {}.".format(valor_buscado_para_imprimir))
    else:
        print("Los jugadores que superan el valor ingresado en {} son: ".format(valor_buscado_para_imprimir))
        print(lista_jugadores_superando_valor)

def mostrar_jugador_con_mas_logros(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    cantidades_logros = []
    for jugador in lista:
        cantidad_logros = len(jugador["logros"])
        cantidades_logros.append(cantidad_logros)
    mayor_cantidad_logros = max(cantidades_logros)
    jugadores_con_mas_logros = []
    for jugador in lista:
        if len(jugador["logros"]) == mayor_cantidad_logros:
            jugadores_con_mas_logros.append(jugador["nombre"])
    if len(jugadores_con_mas_logros) == 1:
        print("El jugador con mas logros es {}".format(jugadores_con_mas_logros[0]))
    else: 
        print("Los jugadores con mas logros son:")
        print(jugadores_con_mas_logros)

def mostrar_y_ordenar_jugadores_con_mas_tiros_campo(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    valor_ingresado = input("Ingrese un valor numerico: ")
    while not es_numero(valor_ingresado):
        valor_ingresado = input("Ingrese un valor NUMERICO: ")
    lista_jugadores_superando_valor = []
    if "," in valor_ingresado or "." in valor_ingresado:
        if "," in valor_ingresado:
            valor_ingresado = re.sub(",", ".", valor_ingresado)
        valor_ingresado = float(valor_ingresado)
    else:
        valor_ingresado = int(valor_ingresado)
    for jugador in lista:
        if jugador["estadisticas"]["porcentaje_tiros_de_campo"] > valor_ingresado:
            lista_jugadores_superando_valor.append(jugador["nombre"])
    jugadores_posicion = {}
    for jugador in lista_jugadores_superando_valor:
        nombre = jugador["nombre"]
        posicion = jugador["posicion"]
        jugadores_posicion[nombre] = posicion
    jugadores_por_posicion = {}
    for nombre, posicion in jugadores_posicion.items():
        if posicion in jugadores_por_posicion:
            jugadores_por_posicion[posicion].append(nombre)
        else:
            jugadores_por_posicion[posicion] = [nombre]

    if len(lista_jugadores_superando_valor) == 1:
        print("El jugador que supera el valor ingresado en porcentaje de tiros de campo es {} ".format(lista_jugadores_superando_valor[0]))
    elif len(lista_jugadores_superando_valor) == 0:
            print("Ningun jugador supera ese valor en porcentaje de tiros de campo.")
    else: 
        print("Los jugadores que superan el valor ingresado en porcentaje de tiros de campo ORDENADOS POR POSICION son: ")
        print(jugadores_por_posicion)

def calcular_promedio_puntos_sin_menor(lista):
    total_puntos = []
    for jugador in lista:
        promedio_puntos_jugador = jugador["estadisticas"]["promedio_puntos_por_partido"]
        total_puntos.append(promedio_puntos_jugador)
    menor_cantidad_puntos = min(total_puntos)
    suma_puntos_equipo = sum(total_puntos) - menor_cantidad_puntos
    promedio_puntos_equipo = suma_puntos_equipo / (len(total_puntos) - 1)
    print("El promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido es {}".format(promedio_puntos_equipo))

calcular_promedio_puntos_sin_menor(lista_nba)

def mostrar_menu():
    print("1. Mostrar todos los jugadores y su posicion.")
    print("2. Mostrar estadisticas de jugador.") 
    print("3. Buscar jugador por nombre y mostrar sus logros.") 
    print("4. Calcular y mostrar el promedio de puntos por partido de todo el equipo del Dream Team.")
    print("5. Ingresar el nombre de un jugador y mostrar si ese jugador es miembro del Salón de la Fama del Baloncesto.")
    print("6. Calcular y mostrar el jugador con la mayor cantidad de rebotes totales.")
    print("7. Calcular y mostrar el jugador con el mayor porcentaje de tiros de campo.")
    print("8. Calcular y mostrar el jugador con la mayor cantidad de asistencias totales.")
    print("9. Ingresar un valor y mostrar los jugadores que han promediado más puntos por partido que ese valor.")
    print("10. Ingresar un valor y mostrar los jugadores que han promediado más rebotes por partido que ese valor.")
    print("11. Ingresar un valor y mostrar los jugadores que han promediado más asistencias por partido que ese valor.")
    print("12. Mostrar el jugador con la mayor cantidad de robos totales.")
    print("13. Mostrar el jugador con la mayor cantidad de bloqueos totales.")
    print("14. Ingresar un valor y mostrar los jugadores que hayan tenido un porcentaje de tiros libres superior.")
    print("15. Mostrar el promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido.")#
    print("16. Mostrar el jugador con la mayor cantidad de logros obtenidos.")
    print("17. Ingresar un valor y mostrar los jugadores que hayan tenido un porcentaje de tiros triples superior a ese valor.")
    print("18. Mostrar el jugador con la mayor cantidad de temporadas jugadas.")
    print("19. Ingresar un valor y mostrar los jugadores , ordenados por posición en la cancha, que hayan tenido un porcentaje de tiros de campo superior a ese valor.")
    print("0. SALIR.")

def utilizar_app():
    mostrar_menu()
    while True:
        opcion = input("Ingrese una opcion valida del menu principal: ")
        patron = r"^(0|[1-9]|1[0-9])$"
        while not re.match(patron, opcion):
            opcion = input("Ingrese una opcion valida del menu principal: ")
        if opcion == "0":
            os.system('cls')
            break
        elif opcion == "1":
            mostrar_jugadores(lista_nba)
        elif opcion == "2":
            mostrar_estadisticas_guardar_csv(lista_nba)
        elif opcion == "3":
            mostrar_logro_jugador(lista_nba)
        elif opcion == "4":
            mostrar_promedio_puntos_ordenado_ascendente(lista_nba)
        elif opcion == "5":
            mostrar_si_es_miembro_salon(lista_nba)
        elif opcion == "6":
            nombrar_mayor_en_una_estadistica(lista_nba, "rebotes_totales")
        elif opcion == "7":
            nombrar_mayor_en_una_estadistica(lista_nba, "porcentaje_tiros_de_campo")
        elif opcion == "8":
            nombrar_mayor_en_una_estadistica(lista_nba, "asistencias_totales")
        elif opcion == "9":
            mostrar_promedios_mayores_en_una_estadistica(lista_nba, "promedio_puntos_por_partido")
        elif opcion == "10":
            mostrar_promedios_mayores_en_una_estadistica(lista_nba, "promedio_rebotes_por_partido")
        elif opcion == "11":
            mostrar_promedios_mayores_en_una_estadistica(lista_nba, "promedio_asistencias_por_partido")
        elif opcion == "12":
            nombrar_mayor_en_una_estadistica(lista_nba, "robos_totales")
        elif opcion == "13":
            nombrar_mayor_en_una_estadistica(lista_nba, "bloqueos_totales")
        elif opcion == "14":
            mostrar_promedios_mayores_en_una_estadistica(lista_nba, "porcentaje_tiros_libres")
        elif opcion == "15":
            calcular_promedio_puntos_sin_menor(lista_nba)
        elif opcion == "16":
            mostrar_jugador_con_mas_logros(lista_nba)
        elif opcion == "17":
            mostrar_promedios_mayores_en_una_estadistica(lista_nba, "porcentaje_tiros_triples")
        elif opcion == "18":
            nombrar_mayor_en_una_estadistica(lista_nba, "temporadas")
        elif opcion == "19":
            mostrar_y_ordenar_jugadores_con_mas_tiros_campo(lista_nba)

utilizar_app()