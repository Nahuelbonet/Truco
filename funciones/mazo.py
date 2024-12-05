import random
import os
import pygame

PALOS = ("espada", "basto", "oro", "copa")
VALORES = (1, 2, 3, 4, 5, 6, 7, 10, 11, 12)

def crear_mazo(palos, valores) -> tuple:
    mazo = []
    rutas_imagenes = {}

    for palo in palos:
        for valor in valores:
            carta = (valor, palo)
            ruta_imagen = os.path.join(os.path.dirname(__file__), "..", "imagenes", "cartas", f"{valor} {palo}.jpg")
            mazo.append(carta)
            rutas_imagenes[carta] = ruta_imagen

    random.shuffle(mazo)
    valores_truco = cargar_valores_truco("archivos/valores_truco.txt")
    return mazo, rutas_imagenes, valores_truco

def cargar_imagenes_cartas(rutas_imagenes: dict) -> dict:
    '''
    Carga las imágenes de las cartas desde las rutas proporcionadas.
    '''
    imagenes = {}
    for carta, ruta in rutas_imagenes.items():
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, (99, 160))  # Escalar las cartas a un tamaño fijo
        imagenes[carta] = imagen
    
    ruta_boca_abajo = os.path.join(os.path.dirname(__file__), "..", "imagenes", "cartas", "dorso.jpg")
    imagenes["dorso"] = pygame.transform.scale(pygame.image.load(ruta_boca_abajo), (99, 160))

    return imagenes

def repartir_cartas(mazo: list) -> tuple:
    '''
    Reparte tres cartas para el jugador y tres para la máquina.
    '''
    jugador = [mazo.pop() for _ in range(3)]  # Extraer 3 cartas para el jugador
    maquina = [mazo.pop() for _ in range(3)]  # Extraer 3 cartas para la máquina
    return jugador, maquina

def cargar_valores_truco(archivo: str) -> dict:
    '''
    Carga los valores de las cartas del truco desde un archivo de texto.
    '''
    valores_truco = {}
    ruta = os.path.join(os.path.dirname(__file__), "..", archivo)
    with open(ruta, "r") as f:
        for linea in f:
            carta, valor = linea.strip().split(",")
            valores_truco[carta] = int(valor)
    return valores_truco

def mostrar_cartas(pantalla: pygame.Surface, mano: list, imagenes: dict, y: int, es_jugador: bool) -> tuple:
    '''
    Dibuja las cartas en pantalla y permite la selección de una carta si es del jugador.
    '''
    # Calcular el centro de la pantalla para las cartas
    x_inicio = (pantalla.get_width() - 99 * len(mano)) // 2  # Centrar las cartas
    carta_seleccionada = None

    for i, carta in enumerate(mano):
        carta_rect = pygame.Rect(x_inicio + i * 110, y, 99, 160)  # Espaciado entre cartas
        
        if es_jugador:
            pantalla.blit(imagenes[carta], (x_inicio + i * 110, y)) 
        else:
            pantalla.blit(imagenes["dorso"], (x_inicio + i * 110, y))

        # Detectar clic
        if es_jugador and carta_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, (255, 0, 0), carta_rect, 2)  # Resaltar la carta con un borde rojo
            if pygame.mouse.get_pressed()[0]:  # Si se hace clic con el botón izquierdo
                carta_seleccionada = carta

    return carta_seleccionada

def arrastrar_carta(pantalla: pygame.Surface, carta_seleccionada: tuple, imagenes: dict, posicion_final: tuple) -> None:
    """
    Permite al jugador arrastrar una carta al centro de la pantalla.

    Parámetros:
        pantalla (pygame.Surface): La superficie donde se dibuja la carta.
        carta_seleccionada (tuple): La carta seleccionada por el jugador.
        imagenes (dict): Diccionario con las imágenes de las cartas.
        posicion_final (tuple): Coordenadas finales donde se colocará la carta.
    """
    x, y = pygame.mouse.get_pos()  # Posición actual del ratón

    # Dibujar la carta mientras se arrastra
    pantalla.fill((0, 128, 0))  # Fondo
    pantalla.blit(imagenes[carta_seleccionada], (x - 50, y - 75))  # Ajustar para centrar la carta
    pygame.display.flip()

    # Esperar a que el jugador suelte la carta en la posición final
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONUP:  # Al soltar el botón del mouse
                pantalla.blit(imagenes[carta_seleccionada], posicion_final)  # Dibujar en la posición final
                pygame.display.flip()
                return

def mostrar_ganador(pantalla: pygame.Surface, carta_ganadora: tuple, imagenes: dict, posicion: tuple) -> None:
    """
    Muestra la carta ganadora en el centro de la pantalla.

    Parámetros:
        pantalla (pygame.Surface): La superficie donde se dibuja la carta.
        carta_ganadora (tuple): La carta ganadora.
        imagenes (dict): Diccionario con las imágenes de las cartas.
        posicion (tuple): Coordenadas donde se mostrará la carta ganadora.
    """
    pantalla.blit(imagenes[carta_ganadora], posicion)  # Dibujar la carta ganadora en la posición
    pygame.display.flip()
