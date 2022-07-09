import pygame
from game import Color,Game
import sys

class Button:
    def __init__(self,text,color,ind,selected) -> None:
        self.text = text
        self.color = color
        self.ind = ind
        self.selected = selected

    def render(self,mp,textFont):
        if self.selected:
            index = 0
        else:
            index = 1
        self.button = textFont.render(self.text,True,self.color,mp[index])

    def blit(self,game):
        game.WIN.blit(self.button,(game.WIDTH//2 - (self.button.get_width()//2),self.ind*game.HEIGHT//3))

def check(keys,button_1,button_2,mp,textFont):
    if keys[pygame.K_UP] and not button_1.selected:
        button_1.selected = True
        button_2.selected = False
    elif keys[pygame.K_DOWN] and not button_2.selected:
        button_1.selected = False
        button_2.selected = True
    elif keys[pygame.K_RETURN] and button_1.selected:
        print('Buton 1')
        return True
    elif keys[pygame.K_RETURN] and button_2.selected:
        pygame.quit()
        sys.exit()
    button_1.render(mp,textFont)
    button_2.render(mp,textFont)
    return False

def update(game,button_1,button_2):
    game.WIN.fill(Color.BLACK)
    button_1.blit(game)
    button_2.blit(game)
    pygame.display.update()

def main():
    game = Game(600,1000,20)
    mp = [Color.BLUE,None]
    textFont = pygame.font.SysFont("comicsans",50)
    firstButton = Button('Start Game',Color.GREEN,1,True)
    secondButton = Button('Exit',Color.GREEN,2,False)
    while game.run:
        game.clock.tick(game.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.run = False
        keys = pygame.key.get_pressed()
        flag = check(keys,firstButton,secondButton,mp,textFont)
        update(game,firstButton,secondButton)
        if flag:
            break
    #pygame.quit()
    game.FPS = 60
    game.start()

if __name__ == "__main__":
    main()