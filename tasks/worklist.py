from argparse import ArgumentError
from enum import Enum

DayActions = Enum('DayActions', 'empty job')

class Elem():
    def __init__(self, state : DayActions, start_date : int, end_date : int) -> None:
        self.state = state
        self.start_date = start_date
        self.end_date = end_date
    
    def clone(self):
        return Elem(self.state, self.start_date, self.end_date)
    
    def __str__(self) -> str:
        return "{}, {} to {}".format(self.state, self.start_date, self.end_date)


def maping_emptys(list : [Elem]) -> [Elem]:
    """
        Mapea una lista uniendo los elementos vacios consecutivos y devuelve la lista resultante

        list --> lista de elementos
    """
    new_list = [] # nueva lista
    empty_elem = None # elemento vacio encontrado
    for item in list:
        # si el elemento es vacio tenemos 2 opciones, creamos en caso de 
        # que sea el primer subconjunto de elementos vacios consecutivos
        # o vamos cambiando la fecha final si es consecutivo
        if item.state is DayActions.empty:
            if empty_elem is None:
                empty_elem = item.clone()
            else:
                empty_elem.end_date = item.end_date
            continue

        # en caso de no ser vacio pues comprobamos que no tengamos pendiente
        # la acumulacion de elementos vacios y añadimos el siguiente valor
        if empty_elem is not None:
            new_list += [empty_elem]
            empty_elem = None
        new_list += [item]
    
    # este caso es porque puede darse el caso que se acumulen vacios y se acabe la lista
    if empty_elem is not None:
        new_list += [empty_elem]
        empty_elem = None
    
    return new_list

def emptys_gen(list : [Elem], perc : int = 1) -> [Elem]:
    """
        Mapea una lista separando los elementos vacios por un percentil y devuelve la lista resultante

        list --> lista de elementos
        perc --> perceptil para generar espacios

        raise --> si el perc es negativo
    """
    if 0 > perc: raise ArgumentError("el parametro perc no puede ser negativo")

    new_list = [] # nueva lista
    delta_date = list[-1].end_date - list[0].start_date # es la diferencia entre la mayor h y la menor
    perc_date = delta_date * perc / 100 # usando el delta se calcula cual es la h correspondiente al percentil
    for item in list:
        # en caso de ser vacio ese elemento añadiremos vacios a la nueva lista 
        # hasta que llene las h del elemento, si no lo es pues se añade el elemento
        if item.state is DayActions.empty:
            acum = item.start_date # fecha acumulada
            err = (item.end_date - acum) % perc_date # margen de error del percentil con respecto a la distacia horaria a recorrer
            # la idea es ir añadiendo percentiles mientras la acumulacion actual mas el margen de error sea menor que el tiempo final
            while item.end_date > acum + err:
                new_list += [Elem(DayActions.empty, acum, acum + perc_date)]
                acum += perc_date
            # si el margen es distinto de 0 pues se añade un vacio de esa distancia horaria
            if err > 0:
                new_list += [Elem(DayActions.empty, acum, acum + err)]
        else:
            new_list += [item]
    
    return new_list

def fill_emptys(list : [Elem], h1 : int = 0, h2 : int = 24) -> [Elem]:
    """
        Mapea una lista rellenando los horarios vacios entre elementos y devuelve la lista resultante

        h1 --> cota menor
        h2 --> cota superior

        raise --> si los h son negativos o si h1 > h2
    """
    if 0 > min(h1, h2): raise ArgumentError("no se aceptan horarios negativos")
    if h1 > h2: raise ArgumentError("h1 tiene que ser menor que h2")

    # inicio con al menos un elemento
    new_list = [list[0]]
    # si el menor de todos es mas grande que la h1 se añade un vacio
    if h1 < list[0].start_date:
        new_list = [Elem(DayActions.empty, h1, list[0].start_date)] + new_list

    for item in list[1:]:
        # se añaden vacios si hay espacio entre horarios, sino se añade directo el elemento
        if new_list[-1].end_date is not item.start_date:
            new_list += [Elem(DayActions.empty, new_list[-1].end_date, item.start_date)]
        new_list += [item]

    # si el mayor de todos es mas pequeño que la h2 se añade un vacio
    if h2 > list[-1].end_date:
        new_list += [Elem(DayActions.empty, new_list[-1].end_date, h2)]

    return new_list