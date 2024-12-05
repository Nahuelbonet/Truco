import pygame
import csv
import os
from funciones.colores import *
from funciones.botones import *


def calcular_puntos_envido(tipo_envido: str, puntos_jugador: int = 0, maquina_puntos: int = 0,
                            puntos_victoria: int = 30) -> int:
    '''
    Calcula los puntos del envido comparando los
    puntos del jugador y de la maquina
    '''
    # Solo manejamos el "envido"
    if tipo_envido == "envido":
        return 2
    return 0  # Si no es uno de estos, no se da ningún puntaje

def mostrar_puntajes(pantalla: pygame.Surface, puntos_jugador: int, puntos_maquina: int) -> None:
    '''
    Muestra los puntajes del jugador y la máquina en la pantalla, centrado en la pantalla de 1000x800.
    '''
    fuente = pygame.font.Font(None, 36)
    texto_jugador = fuente.render(f"Jugador: {puntos_jugador}", True, BLANCO)
    texto_maquina = fuente.render(f"Máquina: {puntos_maquina}", True, BLANCO)
    
    # Centrado de texto
    pantalla.blit(texto_jugador, (500 - texto_jugador.get_width() // 2, 20))  # Centrado horizontal
    pantalla.blit(texto_maquina, (500 - texto_maquina.get_width() // 2, 60))  # Centrado horizontal

def guardar_ranking(nombre: str, puntaje: int, archivo: str = "ranking.csv") -> None:
    """
    Guarda el puntaje del jugador en un archivo CSV.
    Si el jugador ya existe, actualiza su puntaje si es mayor al anterior.
    """
    ranking = []
    archivo_completo = os.path.join("archivos/ranking.csv")

    # Leer el archivo existente
    if os.path.exists(archivo_completo):
        with open(archivo_completo, "r", newline="", encoding="utf-8") as file:
            lector = csv.reader(file)
            ranking = list(lector)

    # Actualizar o agregar al ranking
    actualizado = False
    for fila in ranking:
        if fila[0] == nombre:
            fila[1] = str(int(fila[1]) + 1)
            actualizado = True
            break
    if not actualizado:
        ranking.append([nombre, str(puntaje)])

    # Guardar los datos actualizados
    with open(archivo_completo, "w", newline="", encoding="utf-8") as file:
        escritor = csv.writer(file)
        escritor.writerows(ranking)


def mostrar_ranking(pantalla: pygame.Surface, fondo: pygame.Surface, archivo: str = "ranking.csv") -> None:
    """
    Muestra el ranking en la pantalla, centrado en 1000x800.
    """
    fuente = pygame.font.Font(None, 36)
    archivo_completo = os.path.join("archivos/ranking.csv")

    # Leer el ranking
    if os.path.exists(archivo_completo):
        with open(archivo_completo, "r", newline="", encoding="utf-8") as file:
            lector = csv.reader(file)
            ranking = sorted(lector, key=lambda x: int(x[1]), reverse=True)  # Ordenar por puntaje descendente
    else:
        ranking = []

    # Bucle para mostrar el ranking
    mostrando = True
    while mostrando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:  # Salir con Enter
                mostrando = False

        pantalla.blit(fondo, (0, 0))  # Dibuja el fondo

        # Mostrar título y ranking
        titulo = fuente.render("Puntaje historico", True, OCRE)
        pantalla.blit(titulo, (300, 50))
        y = 100
        for i, (nombre, puntaje) in enumerate(ranking[:10], start=1):  # Mostrar solo el top 10
            texto = fuente.render(f"{i}. {nombre} - {puntaje}", True, BLANCO)
            pantalla.blit(texto, (200, y))
            y += 40
          
        volver_a_menu = Boton(300, 500, 200, 50, "Volver a menu", VERDE_OLIVA)
        volver_a_menu.dibujar(pantalla)
        if volver_a_menu.detectar_clic():
            break

        pygame.display.flip()

def pedir_nombre(pantalla: pygame.Surface, ancho: int, alto: int) -> str:
    """
    Solicita al usuario ingresar su nombre mediante una interfaz gráfica, centrado en 1000x800.
    """
    pygame.font.init()
    pantalla.fill(BLANCO)
    fuente = pygame.font.Font(None, 36)

    # Renderizar el título
    texto_titulo = fuente.render("Nombre jugador:", True, (255, 255, 255))  # BLANCO
    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))

    # Variables para el nombre
    nombre = ""
    continuar = True
    input_rect = pygame.Rect(ancho // 2 - 70, 200, 140, 32)  # Centrado de la caja de texto

    while continuar:
        for evt in pygame.event.get():
            if evt.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evt.type == pygame.KEYDOWN:
                if evt.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evt.key == pygame.K_RETURN or evt.key == pygame.K_KP_ENTER:
                    continuar = False
                else:
                    nombre += evt.unicode

        # Actualizar pantalla
        pantalla.fill(VINO)  # Fondo
        pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))  # Título

        # Rectángulo de entrada
        pygame.draw.rect(pantalla, (GRIS_OSCURO), input_rect) 
        if  input_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(pantalla, (AZUL_NEON), input_rect, 2)
        text_surface = fuente.render(nombre, True, (255, 255, 255))  # Texto en blanco
        pantalla.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

    return nombre

def seleccionar_puntos(pantalla: pygame.Surface, ancho: int, alto: int) -> int:
    """
    Muestra una pantalla para seleccionar la cantidad de puntos a jugar (15 o 30), centrado en 1000x800.
    """
    pantalla.fill((0, 128, 0))
    fuente = pygame.font.Font(None, 50)
    texto_titulo = fuente.render("¿A cuánto querés jugar?", True, (255, 255, 255)) 
    pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))

    boton_quince = Boton(ancho // 2 - 150, 200, 300, 50, "Jugar a 15 puntos", (189, 183, 107))  
    boton_treinta = Boton(ancho // 2 - 150, 300, 300, 50, "Jugar a 30 puntos", (189, 183, 107))  

    seleccion = 0

    while seleccion == 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return 0  # Devuelve 0 para indicar que se desea salir

        # Redibujar pantalla
        pantalla.fill((0, 128, 0))
        pantalla.blit(texto_titulo, (ancho // 2 - texto_titulo.get_width() // 2, 100))
        boton_quince.dibujar(pantalla)
        boton_treinta.dibujar(pantalla)

        # Detectar clics
        if boton_quince.detectar_clic():
            seleccion = 15
        if boton_treinta.detectar_clic():
            seleccion = 30

        pygame.display.flip()

    return seleccion


def mostrar_menu_principal(pantalla: pygame.Surface, fondo: pygame.Surface) -> None:
    """
    Muestra el menú principal con las opciones de Jugar, Ver Ranking o Salir, centrado en 1000x800.
    """
    mostrar_menu = True
    while mostrar_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        pantalla.blit(fondo, (0, 0))  # Fondo del menú
        titulo = pygame.font.Font(None, 48).render("Menú Principal", True, (255, 255, 255))
        pantalla.blit(titulo, (500 - titulo.get_width() // 2, 100))  # Centrado horizontal

        boton_jugar = Boton(400, 300, 200, 50, "Jugar")
        boton_ranking = Boton(400, 380, 200, 50, "Ver Ranking")
        boton_salir = Boton(400, 460, 200, 50, "Salir")  # Botón Salir

        boton_jugar.dibujar(pantalla)
        boton_ranking.dibujar(pantalla)
        boton_salir.dibujar(pantalla)

        if boton_ranking.detectar_clic():
            mostrar_ranking(pantalla, fondo)  # Llama a la función del ranking

        if boton_jugar.detectar_clic():
            mostrar_menu = False  # Sal del menú para iniciar el juego

        if boton_salir.detectar_clic():  # Acción para el botón Salir
            pygame.quit()
            exit()

        pygame.display.flip()


def actualizar_ranking(nombre, puntos):
    archivo = "ranking.csv"
    # Asegúrate de que la ruta sea correcta
    archivo_completo = os.path.join(os.getcwd(), "archivos/ranking.csv")

    try:
        with open(archivo_completo, "a", newline="", encoding="utf-8") as file:
            escritor = csv.writer(file)
            escritor.writerow([nombre, puntos, 1])  # Se registra una victoria por partida
    except Exception as e:
        print(f"Error al actualizar el ranking: {e}")
