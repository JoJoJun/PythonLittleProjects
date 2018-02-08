'''
pygame python3.6 鼠标控制的打飞机
Bullet子弹类  Enemy敌机类 Plane主控飞机
bullets 子弹列表 每隔一段间隔发射一次 到最上方失效
'''
import pygame
from pygame.locals import *
from sys import exit
import random

score = 0
class Bullet():
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active = False #击中敌机以及飞出窗外的失效
    def move(self):
        x,y = pygame.mouse.get_pos()
        if self.active: #只有尚有效的可以向上移动
            self.y-=3
        if self.y<0: #飞出界外的失效
            self.active=False
    def restart(self):#失效子弹重新利用
        mx,my = pygame.mouse.get_pos() #鼠标位置
        self.x = mx - self.image.get_width()/2
        self.y = my - self.image.get_height()/2

        self.active = True


class Enemy():
    def restart(self):#随机出现位置和速度
        self.x = random.randrange(0,420)
        self.y = random.randrange(-200,-50)
        self.speed = random.random()+0.2
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()
    def move(self):
        if self.y<800:
            self.y += self.speed
        else:
            self.restart()
class Plane():
    def restart(self):
        self.x = 200
        self.y = 600

    def __init__(self):
        self.image = pygame.image.load('plane.jpg').convert_alpha()
        self.restart()
    def move(self):
        #飞机移动到鼠标位置
        x, y = pygame.mouse.get_pos()

        x -= plane.image.get_width() / 2
        y -= plane.image.get_height() / 2
        self.x = x
        self.y = y
#检测子弹是否碰撞敌机
def checkHit(bullet,enemy):
    if (bullet.x>=enemy.x and bullet.x<enemy.x+enemy.image.get_width()) and (bullet.y>enemy.y and bullet.y < enemy.y+enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    else: return False
#碰撞检测 敌机与飞机
def checkCrash(enemy, plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False


pygame.init()
screen = pygame.display.set_mode((450,800),0,32) #界面
pygame.display.set_caption("plane")
bg = pygame.image.load('back.jpg')
go = pygame.image.load('gameover.png').convert()
#子弹列表
bullets = []
for i in range(5):
    bullets.append(Bullet())
bull_count = len(bullets)
index_bu = 0 #下一个子弹的索引
interval_bu = 0 #间隔
#敌机列表
enemies = []
for i in range(5):
    enemies.append(Enemy())
plane = Plane()

gameOver = False
scoreFont = pygame.font.Font(None, 32)

while True:
    for event in pygame.event.get():
        #退出
            if event.type == pygame.QUIT:
                exit()
        #gameover状态下 点击鼠标重新开始
            if gameOver and event.type == pygame.MOUSEBUTTONUP:
                plane.restart()
                for e in enemies:
                    e.restart()
                for b in bullets:
                    b.active = False
                score = 0
                gameOver = False


    if not gameOver:
        screen.blit(bg,(0,0))#背景图
        interval_bu -=1
        if interval_bu<0:#间隔时间到 重新发射子弹
            bullets[index_bu].restart()
            interval_bu = 100
            index_bu = (index_bu+1)%bull_count
        for b in bullets:
            if b.active == True:
                b.move()
                screen.blit(b.image,(b.x,b.y))
                for e in enemies:
                    if checkHit(b,e):#碰撞检测
                        score+=10

        for e in enemies:
            if checkCrash(e,plane):
                gameOver = True
                screen.blit(go,(0,0))#gameover背景
            else :
                e.move()
                screen.blit(e.image, (e.x, e.y))#敌机背景
        if gameOver:
            screen.blit(go,(0,0))
        #显示分数
        scoreText= scoreFont.render('Score:%d'%score,1,(0,0,0))
        screen.blit(scoreText,(225,0))
        plane.move()
        screen.blit(plane.image,(plane.x,plane.y))
        pygame.display.update()






