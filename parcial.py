import re
import csv
import json 

with open('C:\\Users\\Usuario\\Desktop\\CAROLINA\\PYL 1C 2023\\Semana 9\\dt.json') as archivo:
    data_nba = json.load(archivo)

lista_nba = data_nba["jugadores"]

def mostrar_jugadores(lista):
    for jugador in lista:
        print("{} - {}".format(jugador["nombre"], jugador["posicion"]))

mostrar_jugadores(lista_nba)