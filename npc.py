import pygame
import gameobjects
import items

class NPC(gameobjects.GameObject):
    def __init__(self,x,y,img,*txt):
        super().__init__(x,y,img)
        self.active = False

        self.font = pygame.font.Font(None, 14)

        self.pages = list(txt)
        self.current_page = 1

        self.text = self.font.render(self.pages[0], True, (0, 0, 0))
        self.text_rect = self.text.get_rect()

        self.text_box = pygame.Surface((self.font.size(self.pages[0])[0] + 40, 50))
        self.text_box.fill((255, 255, 255))
        self.text_box_rect = self.text_box.get_rect()
        self.text_box_rect.midbottom = (self.rect.centerx,self.rect.top - 10)
        
        self.text_rect.center = self.text_box_rect.center

    # Blits NPC to screen, as well as their textbox if they are active
    def update(self,screen):
        screen.blit(self.image, self.rect)

        if self.active:
            screen.blit(self.text_box, self.text_box_rect)
            screen.blit(self.text, self.text_rect)

    def text_resize(self,text,pos):
        #update text box based on new text size
        self.text_box = pygame.Surface((self.font.size(text)[0] + 40, 50))
        self.text_box.fill((255, 255, 255))
        self.text_box_rect = self.text_box.get_rect()
        self.text_box_rect.midbottom = pos

    # While active, if the player presses Enter, the NPC will move to their next page of dialogue, and will
    # close if there are no pages left. While inactive, if the player is touching the NPC and presses Enter,
    # the NPC will activate
    def handle_event(self,event,player):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.current_page < self.pages.__len__():
                        self.text = self.font.render(self.pages[self.current_page], True, (0, 0, 0))
                        self.text_rect = self.text.get_rect()
                        self.text_resize(self.pages[self.current_page],(self.rect.centerx,self.rect.top - 10))
                        self.text_rect.center = self.text_box_rect.center
                        self.current_page += 1
                    else:
                        self.active = False
                        self.current_page = 1
        elif self.rect.colliderect(player.rect):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.text = self.font.render(self.pages[0], True, (0, 0, 0))
                    self.text_rect = self.text.get_rect()
                    self.text_resize(self.pages[0],(self.rect.centerx,self.rect.top - 10))
                    self.text_rect.center = self.text_box_rect.center
                    self.active = True

        

class Shopkeeper(NPC):
    def __init__(self,x,y,img,txt,screen,*stored_items):
        super().__init__(x,y,img,txt)
        self.text_box_rect.center = (screen.get_rect().center)  
        self.text_rect.center = self.text_box_rect.center
        self.inventory = items.Inventory(screen.get_rect().right - 50,screen.get_rect().centery,None,screen)
        self.inventory.shop_open = True
        for item in stored_items:
            item.in_shop = True
            self.inventory.add_item(item)

    def update(self,screen,player):
        super().update(screen)

        if self.active:
            self.inventory.update(screen,player)

    def handle_event(self,event,screen,group,player,player_inv,coin):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.active == False
                    player_inv.shop_open = False
                    self.kill()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    for item in self.inventory.items:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            if coin >= item.cost:
                                self.inventory.remove_item(item)
                                player_inv.add_item(item)
                                self.text = self.font.render("You bought a " + item.name + "!", True, (0, 0, 0))
                                self.text_rect = self.text.get_rect()
                                self.text_resize("You bought a " + item.name + "!",screen.get_rect().center)
                                self.text_rect.center = self.text_box_rect.center
                                item.in_shop = False
                                group.add(item)
                                return coin - item.cost
                            else:
                                self.text = self.font.render("You can't afford that.", True, (0, 0, 0))
                                self.text_rect = self.text.get_rect()
                                self.text_resize("You can't afford that.",screen.get_rect().center)
                                self.text_rect.center = self.text_box_rect.center
                            break
                    for item in player_inv.items:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            player_inv.remove_item(item)
                            item.in_shop = True
                            self.inventory.add_item(item)
                            self.text = self.font.render("You sold a " + item.name + "!", True, (0, 0, 0))
                            self.text_rect = self.text.get_rect()
                            self.text_resize("You sold a " + item.name + "!",screen.get_rect().center)
                            self.text_rect.center = self.text_box_rect.center
                            return coin + item.cost
        elif self.rect.colliderect(player.rect):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.active = True
                    player_inv.shop_open = True


class QuestionNPC(NPC):
    def __init__(self,x,y,img,answer,reward,*txt):
        super().__init__(x,y,img,*txt)
        self.answer = answer
        self.reward = reward
        self.has_answered = False
        self.input = ""

    def handle_event(self,event,player_inv,player,group):
        if self.active:
            if self.has_answered == False:
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isprintable():
                        self.input += event.unicode
                        self.pages[0] += event.unicode
                        self.text = self.font.render(self.pages[0], True, (0, 0, 0))
                        self.text_rect = self.text.get_rect()
                        self.text_resize(self.pages[0],(self.rect.centerx,self.rect.top - 10))
                        self.text_rect.center = self.text_box_rect.center
                    elif event.key == pygame.K_BACKSPACE:
                        self.input = self.input[:-1]
                        self.pages[0] = self.pages[0][:-1]
                        self.text = self.font.render(self.pages[0], True, (0, 0, 0))
                        self.text_rect = self.text.get_rect()
                        self.text_resize(self.pages[0],(self.rect.centerx,self.rect.top - 10))
                        self.text_rect.center = self.text_box_rect.center
                    elif event.key == pygame.K_RETURN:
                        self.has_answered = True
                        if self.input.lower() == self.answer:
                            self.text = self.font.render(self.pages[1], True, (0, 0, 0))
                            self.text_rect = self.text.get_rect()
                            self.text_resize(self.pages[1],(self.rect.centerx,self.rect.top - 10))
                            self.text_rect.center = self.text_box_rect.center
                            player_inv.add_item(self.reward)
                            group.add(self.reward)
                        else:
                            self.text = self.font.render(self.pages[2], True, (0, 0, 0))
                            self.text_rect = self.text.get_rect()
                            self.text_resize(self.pages[2],(self.rect.centerx,self.rect.top - 10))
                            self.text_rect.center = self.text_box_rect.center
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.active = False
        elif self.rect.colliderect(player.rect):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.active = True