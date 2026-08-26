

import random


# ------------------------------------------------------------------
# PASO 1: función para crear una matriz de filas x columnas
# ------------------------------------------------------------------
def crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, valor_inicial):
    matriz = []
    for fila in range(numero_de_filas):
        fila_nueva = []
        for columna in range(numero_de_columnas):
            fila_nueva.append(valor_inicial)
        matriz.append(fila_nueva)
    return matriz


# ------------------------------------------------------------------
# PASO 2: función para generar el laberinto
# ------------------------------------------------------------------
def generar_laberinto(numero_de_filas, numero_de_columnas, semilla_aleatoria=None):
    """
    Devuelve 4 matrices (pared_norte, pared_sur, pared_este, pared_oeste).
    Cada una dice, celda por celda, si hay pared de ese lado (True) o si
    se puede pasar (False).
    """

    if semilla_aleatoria is not None:
        random.seed(semilla_aleatoria)

    visitada = crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, False)
    pared_norte = crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, True)
    pared_sur = crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, True)
    pared_este = crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, True)
    pared_oeste = crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, True)

    # Usamos 2 listas como si fueran una pila, para ir recordando el
    # camino que vamos recorriendo mientras armamos el laberinto.
    pila_filas = [0]
    pila_columnas = [0]
    visitada[0][0] = True

    while len(pila_filas) > 0:

        fila_actual = pila_filas[-1]
        columna_actual = pila_columnas[-1]

        # buscamos los vecinos de la celda actual que todavía no visitamos
        vecinos_fila = []
        vecinos_columna = []
        vecinos_direccion = []

        if fila_actual - 1 >= 0:
            if visitada[fila_actual - 1][columna_actual] == False:
                vecinos_fila.append(fila_actual - 1)
                vecinos_columna.append(columna_actual)
                vecinos_direccion.append("norte")

        if fila_actual + 1 < numero_de_filas:
            if visitada[fila_actual + 1][columna_actual] == False:
                vecinos_fila.append(fila_actual + 1)
                vecinos_columna.append(columna_actual)
                vecinos_direccion.append("sur")

        if columna_actual + 1 < numero_de_columnas:
            if visitada[fila_actual][columna_actual + 1] == False:
                vecinos_fila.append(fila_actual)
                vecinos_columna.append(columna_actual + 1)
                vecinos_direccion.append("este")

        if columna_actual - 1 >= 0:
            if visitada[fila_actual][columna_actual - 1] == False:
                vecinos_fila.append(fila_actual)
                vecinos_columna.append(columna_actual - 1)
                vecinos_direccion.append("oeste")

        if len(vecinos_fila) > 0:
            indice_elegido = random.randint(0, len(vecinos_fila) - 1)
            nueva_fila = vecinos_fila[indice_elegido]
            nueva_columna = vecinos_columna[indice_elegido]
            direccion_elegida = vecinos_direccion[indice_elegido]

            if direccion_elegida == "norte":
                pared_norte[fila_actual][columna_actual] = False
                pared_sur[nueva_fila][nueva_columna] = False
            elif direccion_elegida == "sur":
                pared_sur[fila_actual][columna_actual] = False
                pared_norte[nueva_fila][nueva_columna] = False
            elif direccion_elegida == "este":
                pared_este[fila_actual][columna_actual] = False
                pared_oeste[nueva_fila][nueva_columna] = False
            elif direccion_elegida == "oeste":
                pared_oeste[fila_actual][columna_actual] = False
                pared_este[nueva_fila][nueva_columna] = False

            visitada[nueva_fila][nueva_columna] = True
            pila_filas.append(nueva_fila)
            pila_columnas.append(nueva_columna)

        else:
            # no hay vecinos sin visitar -> retrocedemos en la pila
            pila_filas.pop()
            pila_columnas.pop()

    return pared_norte, pared_sur, pared_este, pared_oeste


# ------------------------------------------------------------------
# PASO 3: funciones para resolver el laberinto solo
# ------------------------------------------------------------------
def direccion_a_la_derecha(direccion):
    if direccion == "norte":
        return "este"
    elif direccion == "este":
        return "sur"
    elif direccion == "sur":
        return "oeste"
    elif direccion == "oeste":
        return "norte"


def direccion_a_la_izquierda(direccion):
    if direccion == "norte":
        return "oeste"
    elif direccion == "oeste":
        return "sur"
    elif direccion == "sur":
        return "este"
    elif direccion == "este":
        return "norte"


def se_puede_avanzar(fila, columna, direccion, pared_norte, pared_sur, pared_este, pared_oeste):
    # Devuelve: (True/False si hay camino libre, fila vecina, columna vecina)
    if direccion == "norte":
        if pared_norte[fila][columna] == False:
            return True, fila - 1, columna
    elif direccion == "sur":
        if pared_sur[fila][columna] == False:
            return True, fila + 1, columna
    elif direccion == "este":
        if pared_este[fila][columna] == False:
            return True, fila, columna + 1
    elif direccion == "oeste":
        if pared_oeste[fila][columna] == False:
            return True, fila, columna - 1

    return False, fila, columna


def resolver_laberinto(numero_de_filas, numero_de_columnas,
                        pared_norte, pared_sur, pared_este, pared_oeste,
                        fila_entrada, columna_entrada,
                        fila_salida, columna_salida):
    """
    Hace que un "ratón" recorra el laberinto solo, siguiendo esta regla
    en cada celda:
        1) intenta seguir DERECHO
        2) si no puede, intenta ir a la DERECHA
        3) si no puede, intenta ir a la IZQUIERDA
        4) si ninguna funciona, RETROCEDE

    Devuelve:
        camino_completo -> TODOS los pasos que dio el ratón (con retrocesos)
        camino_final     -> el camino final, desde la entrada hasta la salida
    """

    visitada_recorrido = crear_matriz_de_booleanos(numero_de_filas, numero_de_columnas, False)
    visitada_recorrido[fila_entrada][columna_entrada] = True

    pila_filas_recorrido = [fila_entrada]
    pila_columnas_recorrido = [columna_entrada]
    pila_direcciones_recorrido = ["este"]   # dirección inicial al entrar

    camino_completo = [(fila_entrada, columna_entrada)]

    while True:

        fila_actual = pila_filas_recorrido[-1]
        columna_actual = pila_columnas_recorrido[-1]
        direccion_actual = pila_direcciones_recorrido[-1]

        if fila_actual == fila_salida and columna_actual == columna_salida:
            break

        direccion_derecha = direccion_a_la_derecha(direccion_actual)
        direccion_izquierda = direccion_a_la_izquierda(direccion_actual)

        # orden de prioridad pedido: derecho, derecha, izquierda
        orden_de_intentos = [direccion_actual, direccion_derecha, direccion_izquierda]

        se_pudo_avanzar = False

        for direccion_a_probar in orden_de_intentos:
            hay_camino, fila_vecina, columna_vecina = se_puede_avanzar(
                fila_actual, columna_actual, direccion_a_probar,
                pared_norte, pared_sur, pared_este, pared_oeste
            )

            if hay_camino and visitada_recorrido[fila_vecina][columna_vecina] == False:
                visitada_recorrido[fila_vecina][columna_vecina] = True
                pila_filas_recorrido.append(fila_vecina)
                pila_columnas_recorrido.append(columna_vecina)
                pila_direcciones_recorrido.append(direccion_a_probar)
                camino_completo.append((fila_vecina, columna_vecina))
                se_pudo_avanzar = True
                break

        if se_pudo_avanzar == False:
            # no se pudo ni derecho, ni derecha, ni izquierda -> retrocedemos
            pila_filas_recorrido.pop()
            pila_columnas_recorrido.pop()
            pila_direcciones_recorrido.pop()

            fila_anterior = pila_filas_recorrido[-1]
            columna_anterior = pila_columnas_recorrido[-1]
            camino_completo.append((fila_anterior, columna_anterior))

    camino_final = []
    for i in range(len(pila_filas_recorrido)):
        camino_final.append((pila_filas_recorrido[i], pila_columnas_recorrido[i]))

    return camino_completo, camino_final