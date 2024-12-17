import pygame
import csv
import random

def load_data(file_path):
    """Carga los datos del archivo CSV."""
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def main():
    # Inicialización de pygame
    pygame.init()

    # Cargar la imagen
    image = pygame.image.load(IMAGE_PATH)
    image_width, image_height = image.get_size()

    # Dimensiones del lienzo con espacio adicional
    extra_space = 30
    screen_width = image_width
    screen_height = image_height + extra_space

    # Configuración del lienzo
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Detectar clic en píxeles")

    # Colores
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)

    # Cargar los datos
    data = load_data(DATA_FILE)
    available_data = data.copy()
    correct_attempts = []

    # Seleccionar un objetivo aleatorio inicialmente
    current_target = random.choice(data)
    attempts_left = 3
    message = ""
    message_color = black
    draw_circle = False
    target_circle_position = (0, 0)

    # Fuente para mostrar texto
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20)

    # Bucle principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detectar clic del ratón
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print(x,y)
                if y <= image_height:  # Solo verificar si se hace clic en la imagen
                    if message in ["CORRECTO", "INCORRECTO"]:
                        message = ""
                        draw_circle = False
                        if not available_data:
                            available_data = data.copy()
                            correct_attempts = []

                        current_target = random.choice(data)
                        attempts_left = 3
                    else:
                        target_x = int(current_target['x'])
                        target_y = int(current_target['y'])
                        margin_x = int(current_target['marginx'])
                        margin_y = int(current_target['marginy'])

                        if (target_x - margin_x <= x <= target_x + margin_x) and \
                           (target_y - margin_y <= y <= target_y + margin_y):
                            message = "CORRECTO"
                            message_color = green
                            draw_circle = True
                            target_circle_position = (target_x, target_y)
                            circle_color = green
                            if attempts_left == 3:
                                available_data.remove(current_target)
                                correct_attempts.append(current_target)
                        else:
                            attempts_left -= 1
                            if attempts_left > 0:
                                message = f"Intentos restantes: {attempts_left}"
                                message_color = black
                            else:
                                message = "INCORRECTO"
                                message_color = red
                                draw_circle = True
                                target_circle_position = (target_x, target_y)
                                circle_color = red

        # Dibujar la imagen
        screen.fill(white)
        screen.blit(image, (0, 0))

        # Dibujar el texto del objetivo
        target_text = font.render(current_target['name'], True, black)
        screen.blit(target_text, (10, image_height + 5))

        # Dibujar el mensaje en el espacio adicional
        if message:
            message_surface = font.render(message, True, message_color)
            screen.blit(message_surface, (300, image_height + 5))

        # Dibujar el círculo en caso de fallo
        if draw_circle:
            pygame.draw.circle(screen, circle_color, target_circle_position, 10, 0)

        # Actualizar pantalla
        pygame.display.flip()

    # Salir de pygame
    pygame.quit()

if __name__ == "__main__":
    # Replace these paths with your own
    RUTA_MAPAS = "./"
    MAPA       = 'asia'
    IMAGE_PATH = f"{RUTA_MAPAS}/{MAPA}.png"  # Path to your map image
    DATA_FILE  = f"{RUTA_MAPAS}/{MAPA}.csv"  # Path to your data file
    main()