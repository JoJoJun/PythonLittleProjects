'''
pygame 简单入门
load一张背景图 随机位置画雪（圆） 并不断刷新位置
'''
import random
import pygame
from pygame.locals import *
from sys import exit
size=(1024,768)
bg = pygame.image.load('snow.jpg')
screen = pygame.display.set_mode(size)
pygame.display.set_caption("snowing")

snow_list=[]
for i in range(500):
    x = random.randrange(0,size[0])
    y = random.randrange(0,size[1])
    sx = random.randrange(-3,3)
    sy = random.randrange(5,9)
    snow_list.append([x,y,sx,sy])

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    screen.blit(bg,(0,0))
    for i in range(len(snow_list)):
        pygame.draw.circle(screen,(255,255,255),snow_list[i][:2],snow_list[i][3]-5)
        snow_list[i][0]+=snow_list[i][2]
        snow_list[i][1]+=snow_list[i][3]
        if snow_list[i][1]>size[1]:
            snow_list[i][0]=random.randrange(0,size[0])
            snow_list[i][1]=random.randrange(-20,-10)
    pygame.display.flip()
    clock.tick(10)

pygame.quit()