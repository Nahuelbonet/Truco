import pygame
from funciones.mazo import *
from funciones.botones import *
from funciones.puntuacion import *
from funciones.juego import *
from funciones.colores import *
from funciones.bucle_principal import *

# Inicialización de pygame
pygame.init()
pygame.mixer.init()

# Configuración de pantalla
ancho, alto = 1000, 800
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Truco")

pygame.mixer.music.load("sonidos/musica.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

fondo_menu = pygame.image.load("imagenes/cartas/fondo.jpg")
fondo_menu = pygame.transform.smoothscale(fondo_menu, (ancho, alto))

# Mostrar el menú principal
mostrar_menu_principal(pantalla, fondo_menu)

# Llamar a la función al inicio del juego
nombre = pedir_nombre(pantalla, ancho, alto)

# Selección de puntos antes de iniciar el juego
seleccion = seleccionar_puntos(pantalla, ancho, alto)

# Cargar la imagen de fondo
fondo = pygame.image.load("imagenes/cartas/fondo.jpg")
fondo = pygame.transform.smoothscale(fondo, (ancho, alto))

# Variables iniciales
mazo, rutas_imagenes, valores_truco = crear_mazo(PALOS, VALORES)
imagenes_cartas = cargar_imagenes_cartas(rutas_imagenes)
mano_jugador, mano_maquina = repartir_cartas(mazo)

# Llamar al bucle principal
bucle_principal(pantalla, imagenes_cartas, fondo, mazo, mano_jugador, mano_maquina, imagenes_cartas, seleccion, nombre)

pygame.quit()
