import pygame
import math
import random

class R_Bar:
    rh = 80
    rw = 20
    rot_speed = 2
    vel = 5

    def __init__(self,x,y,color) -> None:
        self.rot = 0
        self.image = pygame.Surface((self.rw,self.rh))
        self.image.set_colorkey(Color.BLACK)
        self.image.fill(color)
        self.image_copy = self.image.copy()
        self.image_copy.set_colorkey(Color.BLACK)
        self.rect = self.image_copy.get_rect()
        self.rect.center = (x,y)
        self.new_image = self.image

    def draw(self,game):
        game.WIN.blit(self.new_image,self.rect)
    
    def rotate(self,right):
        if right:
            self.rot = (self.rot + self.rot_speed) % 360
        else:
            if self.rot_speed > self.rot:
                self.rot = 360 - self.rot_speed
            else:
                self.rot = (self.rot - self.rot_speed)
        old = self.rect.center
        self.new_image = pygame.transform.rotate(self.image,self.rot)
        self.rect = self.new_image.get_rect()
        self.rect.center = old

    def move(self,up):
        if up:
            self.rect.centery -= self.vel
        else:    
            self.rect.centery += self.vel
        
class Ball:
    ballRadius = 10
    ballVel = 5

    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.x_vel = random.choice([-self.ballVel,self.ballVel])
        self.y_vel = random.randint(-self.ballVel,self.ballVel)
        self.color = color

    def draw(self,game):
        pygame.draw.circle(game.WIN,self.color,(self.x,self.y),self.ballRadius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self,game):
        self.x = game.WIDTH//2
        self.y = game.HEIGHT//2
        self.x_vel = random.choice([-self.ballVel,self.ballVel])
        self.y_vel = random.randint(-self.ballVel,self.ballVel)
    
class Color:
    BLACK = (0,0,0)
    ORANGE = (255,127,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)

class Game:
    def __init__(self,height,width,fps) -> None:
        pygame.init()
        self.HEIGHT = height
        self.WIDTH = width
        self.WIN = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption('Pong Game')
        pygame.mouse.set_visible(False)
        self.FPS = fps
        self.run = True
        self.clock = pygame.time.Clock()
        self.leftBar = R_Bar(R_Bar.rh,self.HEIGHT//2,Color.BLUE)
        self.rightBar = R_Bar(self.WIDTH-R_Bar.rh-10,self.HEIGHT//2,Color.RED)
        self.ball = Ball(self.WIDTH//2,self.HEIGHT//2,Color.ORANGE)

    def start(self):
        while self.run:
            self.clock.tick(self.FPS)
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.run = False
            self.keys = pygame.key.get_pressed()
            self.handleMovement(self.keys,self.leftBar,self.rightBar)
            self.handleCollision(self.ball,self.leftBar,self.rightBar)
            self.ball.move()
            self.update(self.WIN,self.leftBar,self.rightBar,self.ball)
        pygame.quit()

    def update(self,win,leftBar,rightBar,ball):
        win.fill(Color.WHITE)
        leftBar.draw(self)
        rightBar.draw(self)
        ball.draw(self)
        pygame.display.update()

    def handleCollision(self,ball,lbar,rbar):

        if self.ball.x_vel < 0:
            if self.handlePoint(ball.x,ball.y - ball.ballRadius + 1,ball.y + ball.ballRadius - 1,lbar.rect,True,ball.ballRadius):
                ball.y_vel = int(math.atan(ball.y_vel/ball.x_vel) * ball.ballVel) if ball.y_vel != 0 else int(math.atan(ball.x_vel) * ball.ballVel)
                ball.x_vel *= -1
        else:
            if self.handlePoint(ball.x,ball.y - ball.ballRadius + 1,ball.y + ball.ballRadius - 1,rbar.rect,False,ball.ballRadius):
                ball.y_vel = int(math.atan(ball.y_vel/ball.x_vel) * ball.ballVel) if ball.y_vel != 0 else int(math.atan(ball.x_vel) * ball.ballVel)
                ball.x_vel *= -1
        
        if ball.y + ball.ballRadius + ball.y_vel > self.HEIGHT or ball.y - ball.ballRadius + ball.y_vel < 0:
            ball.y_vel *= -1
        
        if ball.x - ball.ballRadius + ball.x_vel <= 0 or ball.x + ball.ballRadius + ball.ballVel >= self.WIDTH:
            ball.reset(self)
            pygame.time.wait(3000)

    def handlePoint(self,x,yStart,yEnd,bar,flag,midValue):
        i = 0
        f = False
        for j in range(yStart,yEnd+1):
            if i == midValue + 1:
                f = True
                i -= 2
            if (flag and bar.collidepoint(x-i,j)) or (not flag and bar.collidepoint(x+i,j)):
                return True
            else:
                if f:
                    i -= 1
                else:
                    i += 1
        return False

    def handleMovement(self,keys,lbar,rbar):
        if keys[pygame.K_w] and lbar.rect.centery - lbar.rh//2 - lbar.vel > 0:
            lbar.move(True)
        elif keys[pygame.K_s] and lbar.rect.centery + lbar.rh//2 + lbar.vel < self.HEIGHT:
            lbar.move(False)

        if keys[pygame.K_a]:
            lbar.rotate(True)
        elif keys[pygame.K_d]:
            lbar.rotate(False)

        if keys[pygame.K_i] and rbar.rect.centery - rbar.rh//2 - rbar.vel > 0:
            rbar.move(True)
        elif keys[pygame.K_k] and rbar.rect.centery + rbar.rh//2 + rbar.vel < self.HEIGHT:
            rbar.move(False)

        if keys[pygame.K_j]:
            rbar.rotate(True)
        elif keys[pygame.K_l]:
            rbar.rotate(False)