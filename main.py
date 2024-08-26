import pygame, random, math
from pygame.locals import *
pygame.init()
#screen variables
global clock, winS, screen, bg, life, score
clock = pygame.time.Clock()
winS = [1000, 1000]
screen = pygame.display.set_mode(winS, 0, 32)
pygame.display.set_caption("SPACE DODGE")
bg = pygame.transform.rotate(pygame.image.load("sprites/bg.png"), 90)
tiles = math.ceil(bg.get_width()/2) + 1
scroll = 0
i = 0
#MUSIC
pygame.mixer.init()
#colors
global black
black = (0,0,0)
#fonts
global font, welcome_text, welcome_render, welcome_rect, over_text, over_render, over_rect, a
font = pygame.font.Font("fonts/ARDESTINE.ttf", 30)
welcome_text = "SPACE DODGE, DODGE ENEMY WARCRAFTS"
welcome_render = font.render(welcome_text, True, (255, 0, 0), (0,0,0))
welcome_rect = welcome_render.get_rect()
welcome_rect.center = [screen.get_width() // 2, 40]
a = 1
score_text = "0"
#gameover function 
def gameover(score, reason):
    if reason == "collision":
        over_text = f"YOU COLLIDED WITH AN ENEMY SPACE CRAFT !! SCORE : {str(score)}"
    if reason == "passby":
        over_text = f"ENEMY TOOK CONTROL OVER EARTH, WE LOSE!! SCORE : {str(score)}"
    over_render = font.render(over_text, True, (255,255,255), (0,0,0))
    over_rect = over_render.get_rect()
    over_rect.center = [screen.get_width() // 2, 500]
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("music/gameover.wav"))
    while True: 
        screen.fill((0,0,0))
        screen.blit(over_render, over_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_x:
                    pygame.quit()
        pygame.display.update()
#setup
def setup():
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("music/bg.mp3"))
    screen.fill(black)
    while True:
        screen.blit(welcome_render, welcome_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game()
        pygame.display.flip()
def game():
    #player variables
    global score_text, score_render, score_rect, player_sprite, player_location, player_rect, move_up, move_down, move_left, move_right, fire, player_speed
    player_sprite = pygame.image.load("sprites/pl.png")
    player_location = [350, screen.get_height() - 100]
    player_rect = pygame.Rect(player_location, [player_sprite.get_width(), player_sprite.get_height()])
    move_up = False
    move_down = False
    move_right = False
    move_left = False
    fire = False
    score = 0
    life = 3
    score_text = "0"
    player_speed = 6
    scroll = 0
    #explosion
    explosion_image = pygame.image.load("sprites/exp.png")
    #enemy variables
    global enemy_sprite, enemy_location, enemy_rect, enemy_speed
    enemy_sprite = pygame.image.load("sprites/enemy1.png")
    enemy_sprite = pygame.transform.rotate(enemy_sprite, 180)
    enemy_location = [screen.get_height() // 2, 0]
    enemy_rect = pygame.Rect(enemy_location, [enemy_sprite.get_width(), enemy_sprite.get_height()])
    enemy_speed = 7
    while True:
        if enemy_speed % 10 == 0:
            player_speed += 2
        screen.fill(black)
        i = 0
        for i in range(0, tiles):
            screen.blit(bg, (0 , -i * bg.get_height() - scroll))
        scroll -= 4
        if abs(scroll) > screen.get_height():
            scroll = 0
        score_render = font.render(score_text, True, (255, 255, 255), (0,0,0))
        score_rect = score_render.get_rect()
        bullet = pygame.draw.circle(screen, (255, 0, 255), [player_location[0] + 30, player_location[1] + 10], 5)
        screen.blit(player_sprite, player_location)
        screen.blit(enemy_sprite, enemy_location)
        enemy_location[1] += enemy_speed
        enemy_rect.y = enemy_location[1]
        enemy_rect.x = enemy_location[0]
        player_rect.y = player_location[1]
        player_rect.x = player_location[0]
        score_text = f"TAKEDOWNS :{str(score)} FLEW PAST : {str(3 - life)}" if life > 1 else f"TAKEDOWNS :{str(score)} FLEW PAST : {str(3 - life)}, ONE MORE PASSBY AND WE LOSE!"
        score_render = font.render(score_text, True, (255, 255, 255), (0,0,0))
        if player_rect.colliderect(enemy_rect):
            screen.blit(explosion_image, [player_rect.x - 490, player_rect.y - 490])
            enemy_speed = 0
            player_speed = 0
            pygame.mixer.Channel(0).pause()
            pygame.mixer.Channel(1).pause()
            gameover(score, "collision")
        if enemy_location[1] > screen.get_height():
            screen.blit(explosion_image, [enemy_location[0] - 480, enemy_location[1] - 530])
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("music/explosion.wav"))
            life -= 1
            enemy_location[1] = 0
            enemy_location[0] = random.randint(0, 600)
            if life == 0:
                pygame.mixer.Channel(0).pause()
                pygame.mixer.Channel(1).pause()
                gameover(score, "passby")
        if move_up and player_location[1] > 0:
            player_location[1] -= player_speed
        if move_left and player_location[0] > 0:
            player_location[0] -= player_speed
        if move_right and player_location[0] < screen.get_width() - 53:
            player_location[0] += player_speed
        if move_down and player_location[1] < screen.get_height() - 50:
            player_location[1] += player_speed
        if fire:
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("music/fire.mp3"))
            while bullet.y > 0:
                if enemy_rect.colliderect(bullet):
                    screen.blit(explosion_image, [enemy_location[0] - 480, enemy_location[1] - 490])
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("music/explosion.wav"))
                    fire = False
                    enemy_location[1] = 0
                    enemy_location[0] = random.randint(0, 600)
                    enemy_speed += 0.1  
                    score += 1
                    score_text = f"TAKEDOWNS :{str(score)} FLEW PAST : {str(3 - life)}" if life > 1 else f"TAKEDOWNS :{str(score)} FLEW PAST : {str(3 - life)}, ONE MORE PASSBY AND WE LOSE!"
                    score_render = font.render(score_text, True, (255, 255, 255), (0,0,0))
                    break
                bullet.y -= 5
                bullet = pygame.draw.circle(screen, (255, 128, 0), [player_location[0] + 30,bullet.y + 10], 6)
            fire = False
        screen.blit(score_render, score_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    move_left = True
                if event.key == K_s or event.key == K_DOWN:
                    move_down = True
                if event.key == K_d or event.key == K_RIGHT:
                    move_right = True
                if event.key == K_w or event.key == K_UP:
                    move_up = True
                if event.key == K_SPACE:
                    fire = True
            if event.type == KEYUP:
                if event.key == K_a or event.key == K_LEFT:
                    move_left = False 
                if event.key == K_s or event.key == K_DOWN:
                    move_down = False
                if event.key == K_d or event.key == K_RIGHT:
                    move_right = False
                if event.key == K_w or event.key == K_UP:
                    move_up = False
                if event.key == K_SPACE:
                    fire = False
        clock.tick(60)
        pygame.display.flip()
setup()
