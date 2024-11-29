import pygame
import constants
from character import Character
from weapon import Weapon
from items import Item

pygame.init()

class PauseMenu:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 10)

    def display(self, screen):
        screen.fill(constants.BG)
        draw_text("PAUSA", self.font, constants.WIDTH, constants.SCREEM_WIDTH // 2 - 50, constants.SCREEN_HEIGHT // 2 - 50)
        draw_text("Presiona P para continuar", self.font, constants.WIDTH, constants.SCREEM_WIDTH // 2 - 150, constants.SCREEN_HEIGHT // 2)
        draw_text("Presiona ESC para salir", self.font, constants.WIDTH, constants.SCREEM_WIDTH // 2 - 150, constants.SCREEN_HEIGHT // 2 + 30)
        pygame.display.update()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

screen = pygame.display.set_mode((constants.SCREEM_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Crear reloj para mantener la tasa principal
clock = pygame.time.Clock()

# Definir variables de movimiento
moving = {'left': False, 'right': False, 'up': False, 'down': False}

# Definir fuente
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

# Función ayudante para escalar imágenes
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# Cargar imágenes de corazón
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# Cargar imágenes de monedas
coin_images = [scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE) for x in range(4)]

# Cargar imagen de poción
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

# Cargar imágenes de armas
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

# Cargar imágenes de personajes
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
animations_types = ["idle", "run"]

for mob in mob_types:
    animation_list = []
    for animation in animations_types:
        temp_list = [scale_img(pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha(), constants.SCALE) for i in range(4)]
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

# Función para mostrar información del juego
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEM_WIDTH, 50))
    pygame.draw.line(screen, constants.WIDTH, (0, 50), (constants.SCREEM_WIDTH, 50))
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and not half_heart_drawn:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
    draw_text(f"PUNTAJE: {player.score}", font, constants.WIDTH, constants.SCREEM_WIDTH - 250, 15)

# Clase para texto de daño
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        super().__init__()
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.counter = 0

    def update(self):
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
            self.kill()

# Crear jugador
player = Character(100, 100, 100, mob_animations, 0)
enemy = Character(200, 300, 100, mob_animations, 1)
bow = Weapon(bow_image, arrow_image)

# Crear lista de enemigos
enemy_list = [enemy]

# Crear grupos de sprites
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

# Crear objetos de ítem
score_coin = Item(100, 100, 0, coin_images)
potion = Item(200, 200, 1, [red_potion])
item_group.add(potion)
coin = Item(400, 400, 0, coin_images)
item_group.add(coin)

# Bucle principal del juego
run = True
paused = False
pause_menu = PauseMenu()

while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BG)

    # Calcular movimiento del jugador
    dx = constants.SPPED * (moving['right'] - moving['left'])
    dy = constants.SPPED * (moving['down'] - moving['up'])

    # Mover jugador
    player.move(dx, dy)

    # Actualizar enemigos y jugador
    for enemy in enemy_list:
        enemy.update()
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.centery, str(damage), constants.RED)
            damage_text_group.add(damage_text)

    damage_text_group.update()
    item_group.update(player)

    # Dibujar elementos en pantalla
    arrow_group.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_ESCAPE:
                run = False
            if not paused:
                if event.key == pygame.K_a:
                    moving['left'] = True
                if event.key == pygame.K_d:
                    moving['right'] = True
                if event.key == pygame.K_w:
                    moving['up'] = True
                if event.key == pygame.K_s:
                    moving['down'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving['left'] = False
            if event.key == pygame.K_d:
                moving['right'] = False
            if event.key == pygame.K_w:
                moving['up'] = False
            if event.key == pygame.K_s:
                moving['down'] = False

    if paused:
        pause_menu.display(screen)

    pygame.display.update()

pygame.quit()