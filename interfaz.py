"""
MODULO: interfaz.py

Este módulo es la "interfaz" (la ventana) del programa. Es sencillo:
tiene un botón que dice "Generar y resolver laberinto" y, cuando lo
apretás, se genera un laberinto nuevo de 50x50 y después se ve, EN VIVO,
cómo el "ratón" lo va recorriendo paso a paso (incluyendo cuando
retrocede), hasta que llega a la salida.

Toda la lógica del laberinto (generarlo y resolverlo) está en el otro
módulo, laberinto.py. Acá solo la usamos e importamos. Este módulo lo
único que hace es dibujar y animar.
"""

import tkinter as tk
import laberinto   # este es el otro módulo (laberinto.py)


# ------------------------------------------------------------------
# Datos generales de la ventana y del laberinto
# ------------------------------------------------------------------
numero_de_filas = 50
numero_de_columnas = 50

tamaño_de_cada_celda = 11   # en píxeles, para dibujar en el canvas

ancho_del_canvas = numero_de_columnas * tamaño_de_cada_celda
alto_del_canvas = numero_de_filas * tamaño_de_cada_celda

# cada cuántos milisegundos avanzamos un paso de la animación
milisegundos_entre_pasos = 15

# cuántos pasos del recorrido dibujamos en cada "cuadro" de la animación
# (con 1 se ve más lento y prolijo, con un número más alto se ve más rápido)
pasos_por_cuadro = 3

# variable para acordarnos en qué paso de la animación vamos
indice_del_paso_actual = 0

# variable para acordarnos del camino completo que hay que animar
camino_completo_para_animar = []


# ------------------------------------------------------------------
# Función que se ejecuta cuando apretamos el botón
# ------------------------------------------------------------------
def generar_y_resolver():

    global camino_completo_para_animar, indice_del_paso_actual

    # mientras se genera y se calcula el recorrido, desactivamos el botón
    # para que no lo puedan apretar de nuevo en el medio de una animación
    boton_generar["state"] = "disabled"

    etiqueta_de_estado["text"] = "Generando el laberinto..."
    ventana.update()

    pared_norte, pared_sur, pared_este, pared_oeste = laberinto.generar_laberinto(
        numero_de_filas, numero_de_columnas
    )

    fila_entrada = 0
    columna_entrada = 0
    fila_salida = numero_de_filas - 1
    columna_salida = numero_de_columnas - 1

    etiqueta_de_estado["text"] = "Calculando el recorrido..."
    ventana.update()

    camino_completo, camino_final = laberinto.resolver_laberinto(
        numero_de_filas, numero_de_columnas,
        pared_norte, pared_sur, pared_este, pared_oeste,
        fila_entrada, columna_entrada, fila_salida, columna_salida
    )

    # guardamos estos datos para poder usarlos al final de la animación
    global longitud_del_camino_final
    longitud_del_camino_final = len(camino_final)

    # dibujamos el laberinto vacío (solo las paredes, entrada y salida)
    dibujar_paredes_en_canvas(pared_norte, pared_sur, pared_este, pared_oeste,
                               fila_entrada, columna_entrada,
                               fila_salida, columna_salida)

    # preparamos la animación: todavía no dibujamos ningún paso
    camino_completo_para_animar = camino_completo
    indice_del_paso_actual = 0

    etiqueta_de_estado["text"] = "Recorriendo el laberinto..."

    # arrancamos la animación (esto llama a dibujar_siguiente_paso más
    # adelante, sin trabar la ventana)
    dibujar_siguiente_paso()


# ------------------------------------------------------------------
# Función que dibuja únicamente las paredes, la entrada y la salida
# ------------------------------------------------------------------
def dibujar_paredes_en_canvas(pared_norte, pared_sur, pared_este, pared_oeste,
                               fila_entrada, columna_entrada,
                               fila_salida, columna_salida):

    canvas.delete("all")   # borramos todo lo que estaba dibujado antes

    for fila in range(numero_de_filas):
        for columna in range(numero_de_columnas):

            x_izquierda = columna * tamaño_de_cada_celda
            x_derecha = x_izquierda + tamaño_de_cada_celda
            y_arriba = fila * tamaño_de_cada_celda
            y_abajo = y_arriba + tamaño_de_cada_celda

            if pared_norte[fila][columna] == True:
                canvas.create_line(x_izquierda, y_arriba, x_derecha, y_arriba)

            if pared_sur[fila][columna] == True:
                canvas.create_line(x_izquierda, y_abajo, x_derecha, y_abajo)

            if pared_este[fila][columna] == True:
                canvas.create_line(x_derecha, y_arriba, x_derecha, y_abajo)

            if pared_oeste[fila][columna] == True:
                canvas.create_line(x_izquierda, y_arriba, x_izquierda, y_abajo)

    # marcamos la entrada (verde) y la salida (azul)
    x_entrada = columna_entrada * tamaño_de_cada_celda
    y_entrada = fila_entrada * tamaño_de_cada_celda
    canvas.create_rectangle(x_entrada, y_entrada,
                             x_entrada + tamaño_de_cada_celda,
                             y_entrada + tamaño_de_cada_celda,
                             fill="green", outline="")

    x_salida = columna_salida * tamaño_de_cada_celda
    y_salida = fila_salida * tamaño_de_cada_celda
    canvas.create_rectangle(x_salida, y_salida,
                             x_salida + tamaño_de_cada_celda,
                             y_salida + tamaño_de_cada_celda,
                             fill="blue", outline="")


# ------------------------------------------------------------------
# Función que dibuja un pedacito del recorrido y se vuelve a llamar
# a sí misma más adelante, para ir animando paso a paso
# ------------------------------------------------------------------
def dibujar_siguiente_paso():

    global indice_del_paso_actual

    ya_llegamos_a_la_ultima_posicion = indice_del_paso_actual >= len(camino_completo_para_animar) - 1

    if ya_llegamos_a_la_ultima_posicion:
        # terminó la animación
        texto_final = "Listo. Pasos del camino final: " + str(longitud_del_camino_final)
        texto_final = texto_final + " (el ratón dio " + str(len(camino_completo_para_animar)) + " pasos en total, contando los retrocesos)"
        etiqueta_de_estado["text"] = texto_final
        boton_generar["state"] = "normal"
        return

    # dibujamos varios pasos en este mismo "cuadro" para que la animación
    # avance más rápido (si pasos_por_cuadro = 1, se dibuja de a un paso)
    for numero_de_paso in range(pasos_por_cuadro):

        if indice_del_paso_actual >= len(camino_completo_para_animar) - 1:
            break

        fila_1, columna_1 = camino_completo_para_animar[indice_del_paso_actual]
        fila_2, columna_2 = camino_completo_para_animar[indice_del_paso_actual + 1]

        x_1 = columna_1 * tamaño_de_cada_celda + tamaño_de_cada_celda / 2
        y_1 = fila_1 * tamaño_de_cada_celda + tamaño_de_cada_celda / 2
        x_2 = columna_2 * tamaño_de_cada_celda + tamaño_de_cada_celda / 2
        y_2 = fila_2 * tamaño_de_cada_celda + tamaño_de_cada_celda / 2

        canvas.create_line(x_1, y_1, x_2, y_2, fill="orange", width=2)

        indice_del_paso_actual = indice_del_paso_actual + 1

    # dibujamos un punto que muestra dónde está el "ratón" ahora mismo
    fila_actual, columna_actual = camino_completo_para_animar[indice_del_paso_actual]
    x_centro = columna_actual * tamaño_de_cada_celda + tamaño_de_cada_celda / 2
    y_centro = fila_actual * tamaño_de_cada_celda + tamaño_de_cada_celda / 2
    radio = tamaño_de_cada_celda / 3

    canvas.delete("raton")   # borramos el punto del paso anterior
    canvas.create_oval(x_centro - radio, y_centro - radio,
                        x_centro + radio, y_centro + radio,
                        fill="red", outline="", tags="raton")

    # programamos el próximo "cuadro" de la animación
    ventana.after(milisegundos_entre_pasos, dibujar_siguiente_paso)


# ------------------------------------------------------------------
# Armado de la ventana (interfaz)
# ------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Laberinto 50x50")

titulo = tk.Label(ventana, text="Laberinto que se resuelve solo", font=("Arial", 16))
titulo.pack(pady=10)

boton_generar = tk.Button(ventana, text="Generar y recorrer laberinto",
                           font=("Arial", 12), command=generar_y_resolver)
boton_generar.pack(pady=5)

etiqueta_de_estado = tk.Label(ventana, text="Apretá el botón para empezar", font=("Arial", 10))
etiqueta_de_estado.pack(pady=5)

canvas = tk.Canvas(ventana, width=ancho_del_canvas, height=alto_del_canvas, bg="white")
canvas.pack(padx=10, pady=10)


# ------------------------------------------------------------------
# Si ejecutamos este archivo directamente, abrimos la ventana
# ------------------------------------------------------------------
if __name__ == "__main__":
    ventana.mainloop()
