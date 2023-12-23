import pygame

image = pygame.image.load('/home/zoso/Desktop/invader/assets/exp.png')

rows = 4
cols = 4
height = 64
width = 64

movinglens = pygame.Rect(0, 0, width, height)

for i in range(rows):
    for j in range(cols):
        movinglens = pygame.Rect(width*j, height*i, width, height)
        pygame.image.save(image.subsurface(movinglens), f"/home/zoso/Desktop/invader/seperated/frame{i}{j}.png")