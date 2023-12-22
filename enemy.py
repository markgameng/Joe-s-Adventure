import pygame
import random 
import gameobjects
import levelManager

vec = pygame.math.Vector2

class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,img_left,img_right,type,health,attack,projectile_speed,delay):
        super().__init__()
        self.x_value = x
        self.y_value = y
        self.img_left_src = img_left
        self.img_right_src = img_right
        self.img = pygame.image.load(img_left) 
        self.rect = self.img.get_rect()
        self.type = type
        self.health = health
        self.attack = attack
        self.projectiles = pygame.sprite.Group()
        self.projectile_speed = projectile_speed
        self.delay = delay
        self.last_attack_time = 0
        self.is_boss1 = False
        self.is_dr_malice = False

        self.pos= vec(x,y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.friction = -0.1
        self.ACC = round(random.uniform(0.1, 0.2), 2)

        self.direction = 1 #move left towards player

    def copy(self):
        return Enemy(self.x_value,self.y_value,self.img_left_src,self.img_right_src,self.type,self.health,self.attack,self.projectile_speed,self.delay)

    def move(self,player):
        self.acc = vec(0, 0.5)

        if self.direction == 0: #right
            self.acc.x = self.ACC
        elif self.direction == 1:#left
            self.acc.x = -self.ACC

        if self.type == 'melee':
            self.acc.x += self.vel.x * self.friction
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        elif self.type == 'projectile':
            self.acc.x = 0
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc

        if self.rect.centerx > player.rect.centerx:
            self.direction = 1 
            self.img = pygame.image.load(self.img_left_src) 
        else:
            self.direction = 0
            self.img = pygame.image.load(self.img_right_src) 

        self.rect.topleft = self.pos

        if self.rect.top < player.rect.bottom:
            if self.rect.centerx >= player.rect.centerx - 5 and self.rect.centerx <= player.rect.centerx + 5:
                if self.type == 'melee':
                    if pygame.time.get_ticks() - self.last_attack_time >= 1000:
                        if player.armor:
                            attack_amount = player.armor.amount - self.attack
                            if attack_amount > 0:
                                attack_amount = 0
                        else:
                            attack_amount = -self.attack

                        player.change_health(attack_amount)
                        self.last_attack_time = pygame.time.get_ticks()

        if self.type == 'projectile':
            for projectile in self.projectiles:
                if projectile.direction == 'left':
                    projectile.rect.move_ip(-self.projectile_speed,0)
                elif projectile.direction == 'right':
                    projectile.rect.move_ip(self.projectile_speed,0)

                if self.is_boss1 or self.is_dr_malice:
                        if player.rect.centery+10 > projectile.rect.centery:
                            projectile.rect.move_ip(0,2)
                        else:
                            projectile.rect.move_ip(0,-2)

                if projectile.rect.collidepoint(player.rect.centerx,player.rect.centery+20):
                    time = 0
                    if (pygame.time.get_ticks()-time)>500:
                        if player.armor:
                            attack_amount = player.armor.amount - self.attack
                            if attack_amount > 0:
                                attack_amount = 0
                        else:
                            attack_amount = -self.attack

                        player.change_health(attack_amount)
                        projectile.kill()
                        time=pygame.time.get_ticks()
                    

    def update(self,screen,player):
        self.move(player)

        screen.blit(self.img,self.rect)
        for projectile in self.projectiles:
            screen.blit(projectile.image,projectile.rect)

        if self.type == 'projectile':
                if pygame.time.get_ticks() - self.last_attack_time > self.delay:
                    self.shoot_projectile(player)
                    self.last_attack_time = pygame.time.get_ticks()


    def collision(self): #create ground group in ground
        if self.vel.y > 0: 
            if self.pos.y >= 400-self.rect.height:
                    self.pos.y = 400 - self.rect.height
                    self.rect.y = 400 - self.rect.height
                    self.vel.y = 0

    def change_health(self,amount):
        self.health += amount

    def die(self,possible_items,item_group):
        drop_chance = random.randint(1,10)
        index = random.randint(1,10)

        if index < 7:
            new_item = possible_items[0].copy()
        elif index < 9:
            new_item = possible_items[1].copy()
        else:
            new_item = possible_items[2].copy()

        if drop_chance > 6:
            item_group.add(new_item)
            new_item.rect.midbottom = self.rect.midbottom
            
        self.kill()

    def shoot_projectile(self,player):
        if self.is_boss1 or self.is_dr_malice:
            if player.pos.x < self.pos.x:
                projectile = gameobjects.GameObject(self.pos.x,player.rect.centery,'Enemy_Assets\projectile_left.png')
                projectile.direction = 'left'
            else:
                projectile = gameobjects.GameObject(self.pos.x,player.rect.centery,'Enemy_Assets\projectile_right.png')
                projectile.direction = 'right'
            self.projectiles.add(projectile)
        else:
            if player.pos.x < self.pos.x:
                projectile = gameobjects.GameObject(self.pos.x,350,'Enemy_Assets\projectile_left.png')
                projectile.direction = 'left'
            else:
                projectile = gameobjects.GameObject(self.pos.x,350,'Enemy_Assets\projectile_right.png')
                projectile.direction = 'right'
            self.projectiles.add(projectile)

