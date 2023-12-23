### this file contains all the classes and functions for invader game
import pygame
import random
import os

### Start screen
class StartScreen:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.font = pygame.font.Font(None, 60)
        self.title_text = self.font.render("SPACE FIGHTER", True, (0, 255, 255))
        self.start_text = self.font.render("Press ENTER to start", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.start_rect = self.start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    def draw(self, screen):
        self.image = pygame.image.load('/home/zoso/Desktop/invader/assets/bg/1.jpeg')
        screen.blit(self.image, (0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)

### game over screen
        
class GameOverScreen:
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.font = pygame.font.Font(None, 60)
        self.game_over_text = self.font.render("Game Over", True, (255, 0, 255))
        self.restart_text = self.font.render("Press ENTER to exit", True, (255, 255, 255))
        self.game_over_rect = self.game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.restart_rect = self.restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    def draw(self, screen):
        self.image = pygame.image.load('/home/zoso/Desktop/invader/assets/bg/2.jpeg')
        screen.blit(self.image, (0, 0))
        screen.blit(self.game_over_text, self.game_over_rect)
        screen.blit(self.restart_text, self.restart_rect)

### velocity class
class Velocity():
    def __init__(self, x, y):
        self.x = x
        self.y = y

### position class
class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

### bullet class
class Bullet():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.radius = 5
    
    def draw(self, screen):
        pygame.draw.circle(screen, (0,255,255),(self.position.x,self.position.y), self.radius)

    def move(self):
        self.position.y -= self.velocity.y
        


### ship class
class Ship():
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.width = 40
        self.height = 60
        self.health = 100

        # Load ship image
        self.image = pygame.image.load("/home/zoso/Desktop/invader/assets/ship.png")

    def draw(self, screen):
        #pygame.draw.rect(screen, (0,255,0),(self.position.x,self.position.y,self.width,self.height))
        screen.blit(self.image, (self.position.x, self.position.y))

    def move(self, screen_width, screen_height):
        key = pygame.key.get_pressed()
        SPEED = 10
        self.velocity.x = 0
        self.velocity.y = 0

        if key[pygame.K_UP]:
            self.velocity.y = -SPEED
        if key[pygame.K_DOWN]:
            self.velocity.y = SPEED
        if key[pygame.K_LEFT]:
            self.velocity.x = -SPEED
        if key[pygame.K_RIGHT]:
            self.velocity.x = SPEED

        if (self.position.x + self.velocity.x >= 0) and ((self.position.x + self.width + self.velocity.x) <= screen_width):
            self.position.x += self.velocity.x
        if (self.position.y + self.velocity.y >= 0) and ((self.position.y + self.height + self.velocity.y) <= screen_height):
            self.position.y += self.velocity.y

### alien calss
class Alien():
    def __init__(self, screen_width):
        
        self.width = 40
        self.height = 40
        self.position = Position(random.randint(0+self.width, screen_width-self.width),-100)

        #alien image
        self.image = pygame.image.load("/home/zoso/Desktop/invader/assets/alien.png")  

    def draw(self, screen):
        #pygame.draw.rect(screen, (255,0,0),(self.position.x,self.position.y, self.height,self.width))
        screen.blit(self.image, (self.position.x, self.position.y))
    
    def move(self, SPEED):
        self.position.y += SPEED

### healthpack calss
class Health():
    def __init__(self, screen_width):
        
        self.width = 40
        self.height = 40
        self.position = Position(random.randint(0+self.width, screen_width-self.width),-100)

        #alien image
        self.image = pygame.image.load("/home/zoso/Desktop/invader/assets/healthpack.png")  

    def draw(self, screen):
        #pygame.draw.rect(screen, (255,0,0),(self.position.x,self.position.y, self.height,self.width))
        screen.blit(self.image, (self.position.x, self.position.y))
    
    def move(self, SPEED):
        self.position.y += SPEED*2

class Star():
    def __init__(self, screen_width):
        self.position = Position(random.randint(0, screen_width),-100)

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255),(self.position.x,self.position.y,2,2))
    
    def move(self, SPEED):
        self.position.y += SPEED



    def update(self):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update

        if elapsed_time > 1000 / self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = now


### game functions

### collision detection
def detectCollision(ship, alien):
    return (
        ship.position.x < alien.position.x + alien.width and
        ship.position.x + ship.width > alien.position.x and
        ship.position.y < alien.position.y + alien.height and
        ship.position.y + ship.height > alien.position.y
    )

### hit detection
def detectHit(bullet, alien):
    return (
        bullet.position.x < (alien.position.x + alien.width) and
        (bullet.position.x + 2*bullet.radius) > alien.position.x and
        (bullet.position.y + 2*bullet.radius) > alien.position.y and
        bullet.position.y < (alien.position.y + alien.height)
    )


### health pack detection
def detectHealthup(ship, health):
    return (
        ship.position.x < health.position.x + health.width and
        ship.position.x + ship.width > health.position.x and
        ship.position.y < health.position.y + health.height and
        ship.position.y + ship.height > health.position.y
    )

## fire weapon
def fireweapon(ship, bullets):
    firespeed = 20
    key = pygame.key.get_pressed()      
    if key[pygame.K_SPACE]:
        newbullet = Bullet(Position(ship.position.x + ship.width/2,ship.position.y), Velocity(0,firespeed))
        bullets.append(newbullet)




### game functionality
        
