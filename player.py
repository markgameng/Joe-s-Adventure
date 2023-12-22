import pygame
from pygame.locals import*

vec = pygame.math.Vector2

#animation images
warrioranimation_right = [pygame.image.load("Warrior_1\warrior1_sprite1.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite2.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite3.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite4.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite5.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite6.png")]

warrioranimation_left = [pygame.image.load("Warrior_1\warrior1_sprite1L.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite2L.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite3L.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite4L.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite5L.png"),
                          pygame.image.load("Warrior_1\warrior1_sprite6L.png")]

#image when not running
idle = pygame.image.load("Warrior_1\idle.png") 



class Player(pygame.sprite.Sprite):
    def __init__(self,x,y,img,speed,jump):
        super().__init__()
        self.img = pygame.image.load(img) 
        self.rect = self.img.get_rect()
        

        #player info
        self.pos= vec(x,y)
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.weapon = None
        self.armor = None
        self.max_health = 100
        self.health = self.max_health
        self.coins = 0
        self.jumping = False
        self.hops = jump
        self.speed = speed
        
        self.move_frame = 0

        #player constants
        self.acceleration = 7.4

    def render(self, screen):
        self.rect.topleft = self.pos
        screen.blit(self.img, self.pos) #main screen

    #changing player health when enemy hits
    def change_health(self,amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    

    def change_max_health(self,amount):
        self.max_health += amount

    
    def move(self):
        #sets acceleration of y to 0.5 which is gravity
        self.acc = vec(0,0.5)

        #when animation list is done return to first animation
        if self.move_frame > 5:
            self.move_frame = 0
            return

        keys = pygame.key.get_pressed()

        
        
        if keys[K_d] or keys[K_RIGHT]: 
            self.pos.x += self.acceleration #add acceleration, to his position making him move to the right
            self.img = warrioranimation_right[self.move_frame] #set image to animation image 
            
            self.move_frame+=1 # allows interation through list

        elif keys[K_a] or keys[K_LEFT]:
            self.pos.x -= self.acceleration #minus acceleration, to his position making him move to the left
            self.img = warrioranimation_left[self.move_frame] #need moving sprites
            
            self.move_frame+=1  # allows interation through list
        else:
            self.img = idle 
        if keys[K_w] or keys[K_UP]:
            self.jump()


       
        self.vel += self.acc # add acceleration into speed
        self.pos += self.vel +0.5*self.acc

    def update(self,enemy_group):
        self.move()
        self.collision()
        self.attack(enemy_group)
        
    
    def jump(self):
        if self.jumping == False:
            self.jumping = True
            self.vel.y = -12

    def attack(self, enemy_group):
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            for enemy in enemy_group:
                if enemy.rect.colliderect(self.rect):
                    time =0
                    if (pygame.time.get_ticks()-time)>500:   
                        if self.weapon:
                            enemy.change_health(-5-self.weapon.amount)
                        else:
                            enemy.change_health(-5)
                        time=pygame.time.get_ticks()




    def collision(self): #create ground group in ground
        if self.vel.y > 0: 
            if self.pos.y >= 400-self.rect.height:
                self.pos.y = 400 - self.rect.height
                self.rect.y = 400 - self.rect.height
                self.vel.y = 0
                self.jumping = False



        
    



