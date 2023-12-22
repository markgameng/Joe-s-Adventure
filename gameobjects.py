import pygame
speed = 4
# GameObject class contains basic info regarding in-game sprites
class GameObject(pygame.sprite.Sprite):
    def __init__(self,x,y,img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


