import re
import csv
import json 
import os

"""
En esta instancia, se abre el archivo con los datos del Dream Team, y la lista se guarda en la variable 'data_nba'
"""
with open('dt.json') as archivo:
    data_nba = json.load(archivo)

lista_nba = data_nba["jugadores"]

"""
Recibe por parametro la lista que querramos ordenar, y un booleano que determina la forma de ordenamiento (True para ascendente y False para descendente).
Ordena la lista pasada por parametro con el algoritmo Quick Sort, que divide la lista original en dos listas teniendo en cuenta si cada elemento es mayor
o menor al elemento pivote, sucesivamente, hasta que cada sublista contenga solo un elemento.
Arma y devuelve una nueva version de la lista original dependiendo de la forma de ordenamiento pasada como parámetro.
"""

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

"""
Recibe como parámetro una lista con opciones a elegir por el usuario.
Ofrece las opciones al usuario y la posibilidad de elegir una de ellas, y valida que haya ingresado un elemento válido.
Devuelve la opción válida elegida.
"""
def ingresar_opcion(opciones: list) -> str:
    opcion = input(f"Ingresar una de las siguientes opciones: {opciones} ")
    while opcion not in opciones:
        print("Opción no válida. Inténtalo de nuevo.")
        opcion = input(f"Ingresar una de las siguientes opciones *RECORDA UTILIZAR MAYUSCULAS!*: {opciones} ")
    else:
        return opcion

"""
Recibe por parámetro un elemento, y valida que este sea un número. Funciona con numeros enteros o decimales, y valida decimales
tanto con coma como con punto.
Devuelve True si es número, False si no lo es.
"""
def es_numero(numero):
    if numero.isdigit():
        return True
    elif numero.replace('.', '', 1).isnumeric():
        return True
    elif numero.replace(',', '', 1).isnumeric():
        return True
    else:
        return False


"""
Recibe por parametro una lista con el formato del JSON trabajado e imprime en consola el nombre y la posición de cada jugador. Retorna 0 
si la lista está vacía.
"""
def mostrar_jugadores(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    for jugador in lista:
        print("{} - {}".format(jugador["nombre"], jugador["posicion"]))

"""
Recibe por parametro una lista con el formato del JSON trabajado, retorna 0 si la lista está vacía. De lo contrario, pide al usuario que ingrese el
índice de un elemento (jugador) en la lista, y valida que este sea mayor a 0 y menor o igual a la cantidad de elementos de la lista.
Acomoda de forma estética la clave de cada estadística (reemplazando los _ por espacios), y lo imprime en consola junto a su respectivo valor.
Guarda en un archivo CSV el nombre y la posición del jugador ingresado por el usuario, y sus estadísticas. Reescribe los datos si la función
se vuelve a llamar.
"""
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
    nombre_archivo = "estadisticas.csv"
    with open(nombre_archivo, "w") as file:
        file.write(jugador_seleccionado["nombre"] + "\n")
        file.write(jugador_seleccionado["posicion"] + "\n")
        for dato in lista_datos_para_guardar:
            file.write(str(dato) + "\n")


"""
Recibe por parametro una lista con el formato del JSON trabajado, crea una lista con los nombres de cada jugador y la pasa por parámetro a la hora
de llamar a la función ingresar_opcion. Una vez validado el jugador ingresado por el usuario, imprime en pantalla los logros del mismo, de manera estética
en forma de listado. Retorna 0 si la lista está vacía.
"""
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


"""
Recibe por parametro una lista con el formato del JSON trabajado. Retorna 0 si la lista está vacía. Crea un diccionario que contiene como clave
el nombre de cada jugador, y el promedio de puntos por partido del mismo como valor. Ordena de forma ascendente el puntaje de cada jugador con la
funcion quicksort, y luego, con dos bucles for, busca el nombre de cada jugador que coincide con cada puntaje ya ordenado, para agregarlos a una lista de
manera ordenada. Imprime dicha lista por consola.
"""
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

"""
Recibe por parametro una lista con el formato del JSON trabajado. Retorna 0 si la lista está vacía, sino crea una lista con los nombres de cada jugador
y la pasa por parámetro a la hora de llamar a la función ingresar_opcion. Una vez validado el jugador ingresado por el usuario, 
lo busca en la lista, e imprime una leyenda que especifica si tal jugador es o no es miembro del Salon de la Fama del Baloncesto.
"""
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


"""
Recibe por parametro una lista con el formato del JSON trabajado y una estadística a buscar dentro de los datos del jugador. 
Retorna 0 si la lista está vacía. Busca al jugador que mayor valor tiene en esa estadística que se especifica por parametro, y lo o los imprime por consola,
dependiendo si hay más de uno con un mismo valor (el mayor de todos).
"""
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

"""
Recibe por parametro una lista con el formato del JSON trabajado y una estadística a buscar dentro de los datos del jugador.
Retorna 0 si la lista está vacía. Pide al usuario ingresar un valor y valida si el mismo es un numero. Si el numero es decimal, y está escrito
con coma en vez de punto, lo reemplaza por punto para que la consola lo entienda como un decimal. Imprime por pantalla el nombre del jugador que supere
el valor ingresado por el usuario en la estadística pasada por parámetro, los enlista si son más de un jugador, y aclara en el caso de no haber ninguno
que cumpla con dicha condición.
"""
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


"""
Recibe por parametro una lista con el formato del JSON trabajado. Retorna 0 si la lista está vacía. Crea una lista con la cantidad de logros de cada jugador,
busca el número mayor en la lista, e imprime el nombre del jugador o de los jugadores cuya cantidad de logros coincida con ese número máximo.
"""
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


"""
Recibe por parametro una lista con el formato del JSON trabajado. Retorna 0 si la lista está vacía. Pide al usuario ingresar un valor y valida 
si el mismo es un numero. Si el numero es decimal, y está escrito con coma en vez de punto, lo reemplaza por punto 
para que la consola lo entienda como un decimal. Busca el jugador o los jugadores que superen el valor ingresado por el usuario en la estadistica
"porcentaje tiros de campo", y luego, si son más de un jugador, los imprime por consola, categorizándolos por posición en la cancha. Aclara si es un
solo jugador quien supera el valor, o si no hay ninguno que cumpla dicha condición.
"""
def mostrar_y_ordenar_jugadores_con_mas_tiros_campo(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    valor_ingresado = input("Ingrese un valor numérico: ")
    while not es_numero(valor_ingresado):
        valor_ingresado = input("Ingrese un valor NUMÉRICO: ")
    dict_jugadores_superando_valor = {}
    if "," in valor_ingresado or "." in valor_ingresado:
        if "," in valor_ingresado:
            valor_ingresado = re.sub(",", ".", valor_ingresado)
        valor_ingresado = float(valor_ingresado)
    else:
        valor_ingresado = int(valor_ingresado)
    for jugador in lista:
        if jugador["estadisticas"]["porcentaje_tiros_de_campo"] > valor_ingresado:
            nombre = jugador["nombre"]
            posicion = jugador["posicion"]
            dict_jugadores_superando_valor[nombre] = posicion
    jugadores_por_posicion = {}
    for nombre, posicion in dict_jugadores_superando_valor.items():
        if posicion in jugadores_por_posicion:
            jugadores_por_posicion[posicion].append(nombre)
        else:
            jugadores_por_posicion[posicion] = [nombre]

    if len(dict_jugadores_superando_valor) == 1:
        print("El jugador que supera el valor ingresado en porcentaje de tiros de campo es: {}".format(list(dict_jugadores_superando_valor.keys())[0]))
    elif len(dict_jugadores_superando_valor) == 0:
        print("Ningún jugador supera ese valor en porcentaje de tiros de campo.")
    else:
        print("Los jugadores que superan el valor ingresado en porcentaje de tiros de campo, ORDENADOS POR POSICIÓN, son:")
        for posicion, jugadores in jugadores_por_posicion.items():
            print("Posición: {}".format(posicion))
            for jugador in jugadores:
                print("- {}".format(jugador))

"""
Recibe por parametro una lista con el formato del JSON trabajado. Retorna 0 si la lista está vacía. Calcula el promedio de puntos por partido de 
todo el equipo, pero restando al jugador que menos valor tiene en dicha estadística. Imprime por pantalla el dato calculado.
"""
def calcular_promedio_puntos_sin_menor(lista):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    total_puntos = []
    for jugador in lista:
        promedio_puntos_jugador = jugador["estadisticas"]["promedio_puntos_por_partido"]
        total_puntos.append(promedio_puntos_jugador)
    menor_cantidad_puntos = min(total_puntos)
    suma_puntos_equipo = sum(total_puntos) - menor_cantidad_puntos
    promedio_puntos_equipo = suma_puntos_equipo / (len(total_puntos) - 1)
    print("El promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido es {}".format(promedio_puntos_equipo))

"""
Imprime por pantalla cada opción que el usuario puede elegir.
"""
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

"""
Imprime la funcion para mostrar el menú y pide al usuario un valor numérico válido, que coincida con alguna opción. Luego de la validación, llama
a la función correspondiente dependiendo de la opción ingresada por el usuario, y luego de llamar a la función elegida, pide al usuario que de nuevo
ingrese una opción por si quiere llamar a otra función del menú. Sale del programa si el usuario elige la opción 0.
"""
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

# 23 - BONUS

"""
Recibe por parametro una lista con el formato del JSON trabajado, el nombre del jugador a buscar y la estadística a buscar del jugador. 
Retorna 0 si la lista está vacía. Busca el nombre del jugador en la lista y calcula qué posición en un ranking del 1 a 12 
tiene el mismo, en la estadística pasada como tercer parámetro. Retorna un entero que representa a dicha posición.
"""
def calcular_posicion_en_ranking(lista, nombre_jugador, ranking):
    cantidad = len(lista)
    if cantidad <= 0:
        return 0
    lista_puntajes = []
    for jugador in lista:
        jugador_puntaje = jugador["estadisticas"][ranking]
        lista_puntajes.append(jugador_puntaje)
    puntajes_ordenados = quick_sort(lista_puntajes, False)
    posicion_jugador = 0
    for puntos in puntajes_ordenados:
        for jugador in lista:
            if jugador["nombre"] == nombre_jugador and jugador["estadisticas"][ranking] == puntos:
                posicion_jugador = puntajes_ordenados.index(puntos) + 1
    return posicion_jugador

"""
Recibe por parametro una lista con el formato del JSON trabajado y el nombre del jugador a buscar. Utilizando la función calcular_posicion_en_ranking,
busca el nombre del jugador en la lista y crea cuatro variables que guardan la posicion del jugador en las estadisticas seleccionadas.
crea un string en el que se enseña de forma estética los datos de las variables creadas y el nombre del jugador.
Retorna dicho string.
"""

def enlistar_ranking_por_jugador(lista, nombre_jugador):
    for jugador in lista:
        if jugador["nombre"] == nombre_jugador:
            nombre = nombre_jugador
    ranking_en_puntos_totales = calcular_posicion_en_ranking(lista, nombre, "puntos_totales")
    ranking_en_rebotes_totales = calcular_posicion_en_ranking(lista, nombre, "rebotes_totales")
    ranking_en_asistencias_totales = calcular_posicion_en_ranking(lista, nombre, "asistencias_totales")
    ranking_en_robos_totales = calcular_posicion_en_ranking(lista, nombre, "robos_totales")
    datos = "{}\t\t{}\t\t{}\t\t\t{}\t  {}".format(ranking_en_puntos_totales, ranking_en_rebotes_totales,
                                              ranking_en_asistencias_totales, ranking_en_robos_totales, nombre)
    return datos

"""
Recibe por parametro una lista con el formato del JSON trabajado. Crea una lista en la que se guardarán los nombres de las categorías y los datos
extraídos de la función anterior enlistar_ranking_por_jugador, pasando por parámetro la lista a trabajar, y el nombre del jugador que se buscó en las líneas
anteriores. Guarda en el archivo CSV linea por línea los datos de la lista_con_datos, agregando un salto de línea luego de cada iteración, para enseñarlo
de forma estética.
"""
def crear_csv_con_posiciones_en_ranking(lista):
    lista_con_datos = []
    categorias = "Puntos Rebotes Asistencias Robos  Jugador"
    lista_con_datos.append(categorias)
    for jugador in lista:
        nombre = jugador["nombre"]
        lista_con_datos.append(enlistar_ranking_por_jugador(lista, nombre))
    nombre_archivo = "ranking_jugadores.csv"
    with open(nombre_archivo, "w") as file:
        for linea in lista_con_datos:
            file.write(str(linea))
            file.write("\n")

crear_csv_con_posiciones_en_ranking(lista_nba)
utilizar_app()
