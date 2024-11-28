import pygame
import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEM_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

#create clock for maintaining main rate 
clock = pygame.time.Clock()

#define player movement variables
moving_left = False
moving_rigth = False
moving_up = False
moving_down = False

#define font
font = pygame.font.Font("assets/fonts/AtariClassic.ttf", 20)

#helped function to scale image
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale ))

#load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)

#load character images
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]

animations_types = ["idle", "run"]
for mob in mob_types:
    #load images
    animation_list = []
    for animation in animations_types:
        #list temporary list of images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

#damage text class
class DamageText(pygame.sprite.Sprite):
  def __init__(self, x, y, damage, color):
    pygame.sprite.Sprite.__init__(self)
    self.image = font.render(damage, True, color)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.counter = 0

  def update(self):
    #move damage text up
    self.rect.y -= 1
    #delete the damage text after a few seconds
    self.counter += 1
    if self.counter > 30:
      self.kill()

#create player
player = Character(100, 100, 100, mob_animations, 0)
enemy = Character(200, 300, 100,  mob_animations, 1)

#create player`s weapon
bow = Weapon(bow_image, arrow_image)

#create empty enemy list
enemy_list = []
enemy_list.append(enemy)

#create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()



#main game loop
run = True
while run:

    clock.tick(constants.FPS)
    screen.fill(constants.BG)

    #calculate player movement
    dx = 0
    dy = 0
    if moving_rigth == True:
        dx = constants.SPPED
    if moving_left == True:
        dx = -constants.SPPED
    if moving_up == True:
        dy = -constants.SPPED
    if moving_down == True:
        dy = constants.SPPED

    print(str(dx) + ", " + str(dy) )
    #move player
    player.move(dx, dy)
    
    #update player
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

    print(arrow_group)
    arrow_group.draw(screen)

    #draw player on screen
    for enemy in enemy_list:
        enemy.draw(screen)
    player.draw(screen)
    bow.draw(screen)
    damage_text_group.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    
    print(enemy.health)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_rigth = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_rigth = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    pygame.display.update()

pygame.quit()
