import pygame
from invaderlib import *
import os
import random

pygame.init()

#GAME CONSTANTS
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

#GAME VARIABLES
DIFFICULTY = 1
SCORE = 0
SPEED = 10
exp_path = '/home/zoso/Desktop/invader/assets/exp'
exp_list = [file for file in os.listdir(exp_path)]
exp_list = ['/home/zoso/Desktop/invader/assets/exp/' + str(file) for file in exp_list]



ship = Ship(Position(SCREEN_WIDTH/2,SCREEN_HEIGHT/1.5), Velocity(0,0))
enemylist = []
starlist = []
bullets = []
healthlist = []

# Start Screen Loop
start_screen = StartScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
start_run = True
while start_run:
    clock.tick(30)
    screen.fill((0, 0, 0))

    start_screen.draw(screen)

    pygame.display.update()
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start_run = False  # Exit the start screen loop


run = True
while run:
    clock.tick(30)  # limits FPS to 60
    screen.fill((0,0,0))

    if SCORE >= 100 and SCORE % 100 == 0:
        DIFFICULTY += 1
    if SCORE >= 200 and SCORE % 200 == 0:
        SPEED += 1

    if len(starlist) < 1000:
        starlist.append(Star(SCREEN_WIDTH))
    
    for star in starlist:
        star.move(40)

    if len(enemylist) <= DIFFICULTY:
        enemylist.append(Alien(SCREEN_WIDTH))
    
    if len(healthlist) < 1 and random.random() > 0.99:
        healthlist.append(Health(SCREEN_WIDTH))

    for enemy in enemylist:
        enemy.move(SPEED)
    
    for bullet in bullets:
        bullet.move()
    
   
    for health in healthlist:
        health.move(SPEED)

    ship.move(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    fireweapon(ship, bullets)
    
    for health in healthlist:
        if detectHealthup(ship, health):
            ship.health += 10

    for enemy in enemylist:
        if detectCollision(ship, enemy):
            for explosion in exp_list:
                exp_image = pygame.image.load(explosion)
                if ship.health <= 10:
                    screen.blit(exp_image, (ship.position.x, ship.position.y))
                    screen.blit(exp_image, (enemy.position.x, enemy.position.y))
                else:
                    screen.blit(exp_image, (enemy.position.x, enemy.position.y))
            ship.health -= 10
    
    if ship.health == 0:
        run = False
            

    for enemy in enemylist:
        for bullet in bullets:
            if detectHit(bullet, enemy):
                for explosion in exp_list:
                    exp_image = pygame.image.load(explosion)
                    screen.blit(exp_image, (enemy.position.x, enemy.position.y))

    for bullet in bullets:
        enemylist = [enemy for enemy in enemylist if not (detectHit(bullet, enemy))]
        bullets = [bullet for bullet in bullets if not (detectHit(bullet, enemy))]
    
    healthlist = [health for health in healthlist if not detectHealthup(ship, health)]
    enemylist = [enemy for enemy in enemylist if not (detectCollision(ship, enemy))]

    SCORE += (DIFFICULTY + 1) - len(enemylist)
    
    ship.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

    for enemy in enemylist:
        enemy.draw(screen)

    for star in starlist:
        star.draw(screen)
    
    for health in healthlist:
        health.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    enemylist = [enemy for enemy in enemylist if enemy.position.y <= SCREEN_HEIGHT+100]
    healthlist = [health for health in healthlist if health.position.y <= SCREEN_HEIGHT+100]
    starlist = [star for star in starlist if star.position.y <= SCREEN_HEIGHT+10]
    bullets = [bullet for bullet in bullets if bullet.position.y >= 0]

    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {SCORE-1}", True, (255, 255, 255))
    screen.blit(score_text, (25, 20))
    pygame.draw.rect(screen, (0,0,255), (SCREEN_WIDTH - 225, 20, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (SCREEN_WIDTH - 225 + 200 - (ship.health / 100) * 200, 20, (ship.health / 100) * 200, 20))



    pygame.display.update()
    

# Game Over Screen Loop
game_over_screen = GameOverScreen(SCREEN_WIDTH,SCREEN_HEIGHT)
game_over_run = True
while game_over_run:
    clock.tick(30)
    screen.fill((0, 0, 0))

    game_over_screen.draw(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_over_run = False  # Exit the game over screen loop and restart the game

pygame.quit()