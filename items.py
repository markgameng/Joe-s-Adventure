import pygame
import gameobjects

class Item(gameobjects.GameObject):
    def __init__(self,x,y,img,name,type,amount,cost):
        super().__init__(x,y,img)
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (32,32))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.img = img
        self.name = name
        self.type = type
        self.amount = amount
        self.cost = cost
        self.picked_up = False
        self.in_shop = False
        self.inv = None

        self.font = pygame.font.Font(None, 14)

        self.text = name + "            "

        if self.type == 'weapon':
            self.text += 'Damage: ' + str(self.amount)
        elif self.type == 'armor':
            self.text += 'Protection: ' + str(self.amount)
        elif self.type == 'consumable':
            self.text += 'Healing: ' + str(self.amount)

        self.text += '          Cost: ' + str(self.cost) + ' coins'

        self.description = self.font.render(self.text, True, (0, 0, 0))
        self.desc_rect = self.description.get_rect()

        self.desc_box = pygame.Surface((self.font.size(self.text)[0] + 40, 50))
        self.desc_box.fill((255, 255, 255))
        self.desc_box_rect = self.desc_box.get_rect()
        self.desc_box_rect.center = (self.rect.center)

        self.desc_rect.center = self.desc_box_rect.center

    def update(self,screen,player):
        screen.blit(self.image,self.rect)

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.in_shop:
                self.desc_box_rect.midright = (self.rect.left,self.rect.centery)
            elif self.picked_up:
                self.desc_box_rect.midleft = (self.rect.right,self.rect.centery)
            else:
                self.desc_box_rect.midbottom = (self.rect.centerx,self.rect.top - 20)
            screen.blit(self.desc_box, self.desc_box_rect)
            self.desc_rect.center = self.desc_box_rect.center
            screen.blit(self.description, self.desc_rect)

    def use(self,item_group):
        if self.picked_up == False:
            pass
        elif self.type == 'consumable':
            self.inv.player.change_health(self.amount)
            self.inv.remove_item(self)
        elif self.type == 'weapon' or self.type == 'armor':
            self.inv.equip_item(self,item_group)

    def pickup(self):
        self.inv.add_item(self)

    def copy(self):
        return Item(self.rect.centerx,self.rect.centery,self.img,self.name,self.type,self.amount,self.cost)



class Inventory(pygame.sprite.Sprite):
    def __init__(self,x,y,player,screen):
        super().__init__()
        self.image = pygame.Surface((90,screen.get_rect().height - 10))
        self.image.fill((140,140,140))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.player = player
        self.shop_open = False
        self.items = pygame.sprite.Group()

    def update(self,screen,player):
        screen.blit(self.image,self.rect)
        self.items.update(screen,player)

    # Adds item to inventory if the inventory limit has not been reached
    def add_item(self,item):
        if self.items.sprites().__len__() > 8:
            pass
        else:
            item.picked_up = True
            item.inv = self
            self.items.add(item)
            item.rect.midtop = (self.rect.centerx, int((self.rect.height / 8) * (self.items.sprites().__len__() - 1))  + 10)

    # Removes item from inventory, then removes and re-adds all remaining items
    def remove_item(self,item):
        item.kill()
        temp_group = self.items.copy()
        
        for other_item in self.items:
            self.items.remove(other_item)

        for other_item in temp_group:
            self.add_item(other_item)

    # Equips item to player, placing their previously equipped item in the inventory
    def equip_item(self,item,item_group):
            if item.type == 'armor':
                if self.player.armor:
                    temp = self.player.armor
                    self.player.armor = item
                    self.remove_item(item)
                    self.add_item(temp)
                    item_group.add(temp)
                else:
                    self.player.armor = item
                    self.remove_item(item)
            elif item.type == 'weapon':
                if self.player.weapon:
                    temp = self.player.weapon
                    self.player.weapon = item
                    self.remove_item(item)
                    self.add_item(temp)
                    item_group.add(temp)
                else:
                    self.player.weapon = item
                    self.remove_item(item)

    def handle_event(self,event,item_group):
        for item in self.items:
            if self.shop_open == False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            item.use(item_group)
                            break