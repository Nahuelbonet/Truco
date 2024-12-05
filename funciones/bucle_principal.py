import pygame
from funciones.mazo import *
from funciones.botones import *
from funciones.puntuacion import *
from funciones.juego import *
from funciones.colores import *

def bucle_principal(pantalla, imagenes_cartas, fondo, mazo, mano_jugador, mano_maquina, imagenes, seleccion, nombre):
    """
    Ejecuta el bucle principal del juego, gestionando los turnos, los clics en los botones, y el estado del juego.
    
    :param pantalla: La superficie de Pygame donde se dibujan los elementos.
    :param imagenes_cartas: Las imágenes de las cartas para mostrarlas en pantalla.
    :param fondo: La imagen de fondo que se dibuja en la pantalla.
    :param mazo: El mazo de cartas del juego.
    :param mano_jugador: Las cartas que tiene el jugador.
    :param mano_maquina: Las cartas que tiene la máquina.
    :param imagenes: Las imágenes utilizadas en el juego.
    :param seleccion: El número de puntos necesarios para ganar el juego.
    :param nombre: El nombre del jugador.
    """
    # Colocando los botones uno encima del otro en el lado inferior izquierdo
    boton_envido = Boton(50, 650, 120, 50, "Envido", color_boton=(0, 0, 255))  # Primer botón (Envido)
    boton_truco = Boton(50, 550, 120, 50, "Truco", color_boton=(255, 0, 0))   # Segundo botón (Truco)
    boton_mazo = Boton(50, 450, 120, 50, "Mazo", color_boton=(0, 255, 0))    # Tercer botón (Mazo)

    # Variables para gestionar el juego
    puntos_jugador, puntos_maquina = 0, 0
    jugando = True
    turno_actual = "jugador"
    cartas_jugadas = []
    puntos_truco = 0
    envido_jugado = False
    ronda_activa = True
    manos_ganadas = {"jugador": 0, "maquina": 0}
    inicia_ronda = "jugador"
    cartas_maquina = []
    inicio_ronda = True
    empate = 0
    ganador_primera = ""
    canto_actual = ""
    respuesta = False
    turno_truco = "jugador"

    # Bucle principal
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

            # Detectar clic en cartas solo si la ronda está activa y es el turno del jugador
            if evento.type == pygame.MOUSEBUTTONDOWN and ronda_activa and turno_actual == "jugador":
                carta_seleccionada = mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 600, es_jugador=True)

                if carta_seleccionada and carta_seleccionada in mano_jugador:
                    # El jugador juega su carta
                    mano_jugador.remove(carta_seleccionada)
                    if len(cartas_maquina) == 0:
                        carta_maquina = jugar_maquina(mano_maquina, carta_seleccionada)
                        mano_maquina.remove(carta_maquina)
                        cartas_jugadas.append((carta_seleccionada, carta_maquina))
                        print(f"Jugaste: {carta_seleccionada}, La máquina jugó: {carta_maquina}")
                    else:
                        cartas_jugadas.append((carta_seleccionada, cartas_maquina[0]))
                        print(f"Jugaste: {carta_seleccionada}, La máquina jugó: {cartas_maquina[0]}")

                    # Mover carta seleccionada al centro de la pantalla
                    mover_carta(pantalla, carta_seleccionada, imagenes_cartas, 50, 400, 450, 300)

                    # Evaluar quién ganó la mano
                    ganador_mano = evaluar_mano(cartas_jugadas[-1], valores_truco)
                    if ganador_mano == "jugador":
                        print("Ganaste esta mano.")
                        manos_ganadas["jugador"] += 1
                        turno_actual = "jugador"
                        if inicio_ronda == True or empate > 0:
                            ganador_primera = "jugador"
                    elif ganador_mano == "maquina":
                        print("La máquina ganó esta mano.")
                        manos_ganadas["maquina"] += 1
                        turno_actual = "maquina"
                        if inicio_ronda == True or empate > 0:
                            ganador_primera = "maquina"
                    else:
                        print("Empate en esta mano.")
                        turno_actual = "jugador"
                        empate += 1
                    cartas_maquina = []
                    inicio_ronda = False

        # Verificar si alguien ganó dos manos
        if manos_ganadas["jugador"] == 2 or manos_ganadas["maquina"] == 2 or (empate > 0 and (manos_ganadas["jugador"] == 1 or manos_ganadas["maquina"] == 1)):
            ronda_activa = False
            if canto_actual != "" and turno_truco == "maquina":
                if respuesta == True:
                    puntos_truco = 2
                else: 
                    puntos_truco = 1
            elif canto_actual != "" and turno_truco == "jugador":
                if respuesta == True:
                    puntos_truco = 2
                else: 
                    puntos_maquina = 1
            puntos_jugador, puntos_maquina = determinar_ganador_final(
            puntos_jugador, puntos_maquina, ganador_primera, manos_ganadas, puntos_truco)
            reiniciar_ronda(mazo, mano_jugador, mano_maquina, cartas_jugadas, manos_ganadas, inicia_ronda)
            inicio_ronda = True
            inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"
            turno_actual = inicia_ronda
            ronda_activa = True
            envido_jugado = False
            empate = 0
            canto_actual = ""
            turno_truco = "jugador"
            puntos_truco = 0
        else:
            # Turno de la máquina
            if (turno_actual == "maquina" or (inicia_ronda == "maquina" and inicio_ronda == True)) and ronda_activa:
                turno_actual = manejar_turno_maquina(mano_maquina, cartas_jugadas, valores_truco, turno_actual, manos_ganadas, cartas_maquina)
                inicio_ronda = False

        # Dibujar fondo y elementos
        pantalla.blit(fondo, (0, 0))
        mostrar_puntajes(pantalla, puntos_jugador, puntos_maquina)

        # Mostrar cartas del jugador y la máquina
        mostrar_cartas(pantalla, mano_jugador, imagenes_cartas, 600, es_jugador=True)
        mostrar_cartas(pantalla, mano_maquina, imagenes_cartas, 100, es_jugador=False)

        # Dibujar los botones
        boton_truco.dibujar(pantalla)
        boton_envido.dibujar(pantalla)
        boton_mazo.dibujar(pantalla)

        # Detectar clic en el botón Envido
        if boton_envido.detectar_clic() and turno_actual == "jugador" and not envido_jugado:
            print("Botón Envido presionado")
            puntos_jugador, puntos_maquina, envido_jugado = manejar_envido_completo(puntos_jugador, puntos_maquina, mano_jugador, mano_maquina, turno_actual, seleccion)
            envido_jugado = True

        # Detectar clic en el botón Truco
        if boton_truco.detectar_clic() and turno_actual == "jugador":
            print("Botón Truco presionado")
            canto_actual, respuesta, turno_truco = gestionar_truco_interfaz(pantalla, turno_truco, canto_actual, respuesta)

       # Detectar clic en el botón Mazo
        if boton_mazo.detectar_clic() and ronda_activa:
            print("Clic en el botón Mazo detectado")
            ronda_activa = False
            puntos_jugador, puntos_maquina = manejar_irse_al_mazo(turno_actual, envido_jugado, inicio_ronda, puntos_jugador, puntos_maquina)

            reiniciar_ronda(mazo, mano_jugador, mano_maquina, cartas_jugadas, manos_ganadas, inicia_ronda)
            inicio_ronda = True
            inicia_ronda = "maquina" if inicia_ronda == "jugador" else "jugador"
            turno_actual = inicia_ronda
            ronda_activa = True
            envido_jugado = False
            empate = 0

        # Verificar fin del juego
        if puntos_jugador >= seleccion or puntos_maquina >= seleccion:
            print("¡Juego finalizado!")
            if puntos_jugador > puntos_maquina:
                print(f"{nombre} ha ganado el juego!")
                guardar_ranking(nombre, manos_ganadas["jugador"])
            else:
                print("La máquina ha ganado el juego!")
                guardar_ranking("Máquina", manos_ganadas["maquina"])
            jugando = False

        # Actualizar la pantalla
        pygame.display.update()

def mover_carta(pantalla, carta, imagenes_cartas, x_destino, y_destino, x_inicial, y_inicial):
    """
    Mueve la carta seleccionada de su posición inicial a la nueva posición.
    
    :param pantalla: La superficie de Pygame donde se dibujarán las cartas.
    :param carta: La carta a mover.
    :param imagenes_cartas: Las imágenes de las cartas.
    :param x_destino: La posición X de destino.
    :param y_destino: La posición Y de destino.
    :param x_inicial: La posición X inicial (antes de moverla).
    :param y_inicial: La posición Y inicial (antes de moverla).
    """
    # Actualizar la posición de la carta
    carta_rect = imagenes_cartas[carta].get_rect()
    carta_rect.topleft = (x_inicial, y_inicial)
    
    # Dibujar la carta en la nueva posición
    pantalla.blit(imagenes_cartas[carta], (x_destino, y_destino))
    pygame.display.update()

def cargar_valores_truco(ruta_archivo):
    """
    Carga los valores del truco desde un archivo de texto y los guarda en un diccionario.
    
    :param ruta_archivo: La ruta al archivo de texto que contiene los valores de las cartas.
    :return: Un diccionario con los valores de las cartas, o un diccionario vacío si no se encuentra el archivo.
    """
    valores_truco = {}
    try:
        # Abrimos el archivo en modo de lectura
        with open(ruta_archivo, 'r') as archivo:
            for linea in archivo:
                # Limpiamos los espacios en blanco y dividimos la línea en nombre de carta y valor
                carta, valor = linea.strip().split(', ')
                # Guardamos el valor en el diccionario
                valores_truco[carta] = int(valor)
        return valores_truco
    except FileNotFoundError:
        print("El archivo no se encuentra en la ruta especificada.")
        return {}

# Usar la función para cargar los valores
valores_truco = cargar_valores_truco("archivos/valores_truco.txt")