# PyGame

Juego de accion

# Explicación del Código de un Juego en Pygame

## Menu basico de Pausa

![Descripción de la imagen](https://i.ibb.co/yNdYGH1/juegito-2.png)

## Vista inicial del juego

![Descripción de la imagen](https://i.ibb.co/WDFBkNJ/juegito-1.png)

## personaje principal lanzando flechas

![Descripción de la imagen](https://i.ibb.co/P6k0cgL/juego-4.png)

## personaje principal flecha en el monstruo

![Descripción de la imagen](https://i.ibb.co/jb47R9y/juego-5.png)

## personaje principal puntos salud monstruo

![Descripción de la imagen](https://i.ibb.co/KyDSHjN/juego-3.png)

## puntaje luego de tomar las monedas

![Descripción de la imagen](https://i.ibb.co/Bqy9jpb/juego-6.png)

## Como iniciar el juego

Se debe descargar el repositorio
una vez dentro de la carpeta se inicializa por medio de una terminal con el comando python main.py

Este código es una implementación básica de un juego en Pygame que incluye un menú de pausa, manejo de personajes, enemigos y elementos del juego. A continuación se detalla cada parte del código.

## Importaciones y Inicialización

- Se importan las bibliotecas necesarias, incluyendo `pygame` y módulos personalizados (`constants`, `Character`, `Weapon`, `Item`).
- Se inicializa Pygame.

## Clase PauseMenu

- **`__init__`**: Inicializa la fuente para el texto del menú de pausa.
- **`display`**: Dibuja el menú de pausa en la pantalla, mostrando opciones para continuar o salir del juego.

## Función draw_text

- Esta función renderiza texto en la pantalla utilizando la fuente y el color proporcionados.

## Configuración de la Ventana del Juego

- Se establece el tamaño de la ventana del juego y se le asigna un título.

## Reloj y Variables de Movimiento

- Se crea un objeto de reloj para controlar la tasa de fotogramas.
- Se definen las variables de movimiento del jugador.

## Carga de Recursos

El código carga imágenes para diferentes elementos del juego, como corazones, monedas, pociones, armas y personajes:

- Se utilizan funciones para escalar las imágenes a un tamaño adecuado.

## Función draw_info

- Dibuja un panel en la parte superior de la pantalla que muestra la salud del jugador y su puntaje.

## Clase DamageText

- Esta clase se utiliza para mostrar el daño infligido a los enemigos en la pantalla.

## Bucle Principal del Juego

- Se ejecuta el bucle principal del juego, donde se manejan los eventos, se actualizan las posiciones de los personajes y se dibujan en la pantalla.
- Si el juego está pausado, se muestra el menú de pausa.
