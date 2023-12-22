import pygame
import player
import enemy
import items
import gameobjects
import random
from pygame import mixer
from player import *

pygame.init()
WIDTH = 800
HEIGHT = 500
FPS = 60

buttonPlay_x = 350
buttonPlay_y = 250
buttonPlay_width = 100
buttonPlay_height = 50
buttonPlay_color = (0, 255, 0)

buttonQuit_x = 350
buttonQuit_y = 350
buttonQuit_width = 100
buttonQuit_height = 50
buttonQuit_color = (255,0,0)
import levelManager
pygame.init()

pageNumber = 0

maliceDown = False


screen = pygame.display.set_mode((800,500))
screen_rect=screen.get_rect()
pygame.display.set_caption("Joe's Adventure")

back = pygame.image.load("TutoralBG.jpg")
back =pygame.transform.scale(back, (800,500))
back_rect = back.get_rect()
back_rect.center=screen_rect.center

# mixer.music.load("Clarx - Zig Zag [NCS Release].mp3")
# mixer.music.set_volume(0.1)
# mixer.music.play(bdMusic, loop=-1)

Block1 = gameobjects.GameObject(0,400,'grass chain.png')


coin = 0 # variable for number of coins that the player has
time = 0

player= Player(70,50,'Warrior_1\idle.png',gameobjects.speed, 0)

levelTesting = levelManager.LevelManager()

npc_group = pygame.sprite.Group()
        
inventory = items.Inventory(50,screen_rect.centery,player,screen)

item_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

font = pygame.font.Font(None, 26)

def render():
    screen.blit(back,back_rect)

    info_text = font.render("Level: "+str(levelTesting.level)+"    Health: "+str(player.health)+"    Coins: "+str(coin), True, (255, 255, 255))
    info_text_rect = info_text.get_rect()
    info_text_rect.center = (screen_rect.centerx,25)
    screen.blit(info_text,info_text_rect)

    screen.blit(Block1.image,Block1.rect)
    player.render(screen)

    for item in item_group:
        item.update(screen,player)

    for character in enemy_group:
        character.update(screen,player)

    for npc in npc_group:
        if str(type(npc)) == "<class 'npc.Shopkeeper'>":
            npc.update(screen,player)
        else:
            npc.update(screen)

    player.render(screen)
    inventory.update(screen,player)

    pygame.display.flip()

def game_intro():
    intro_back = pygame.image.load("introBG.jpg")
    intro_back =pygame.transform.scale(intro_back, (800,500))
    intro_back_rect = intro_back.get_rect()
    intro_back_rect.center=screen_rect.center

    font = pygame.font.Font('Raleway-Bold.ttf', 36)
    text = font.render("Welcome to Joe's Adventure", True, (255, 255, 255))

    buttonFont = pygame.font.Font('Raleway-Bold.ttf', 18)
    buttonEnterText = font.render("Play", True, (255, 255, 255))
    buttonQuitText = font.render("Quit", True, (255, 255, 255))

    intro = True
    while intro:
        screen.blit(intro_back,intro_back_rect)
        screen.blit(text,(200,100))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if buttonPlay_x < mouse_pos[0] < buttonPlay_x + buttonPlay_width and buttonPlay_y < mouse_pos[1] < buttonPlay_y + buttonPlay_height:
                    # Button Click
                    intro = False
                if buttonQuit_x < mouse_pos[0] < buttonQuit_x + buttonQuit_width and buttonQuit_y < mouse_pos[1] < buttonQuit_y + buttonQuit_height:
                    # Button Click
                    pygame.quit()
        pygame.draw.rect(screen, buttonPlay_color, (buttonPlay_x, buttonPlay_y, buttonPlay_width, buttonPlay_height))
        pygame.draw.rect(screen, buttonQuit_color, (buttonQuit_x, buttonQuit_y, buttonQuit_width, buttonQuit_height))
        screen.blit(buttonEnterText, (buttonPlay_x+10, buttonPlay_y))
        screen.blit(buttonQuitText, (buttonQuit_x+10, buttonQuit_y))
        pygame.display.flip()

def endScreen():
    end_back = pygame.image.load("introBG.jpg")
    end_back =pygame.transform.scale(end_back, (800,500))
    end_back_rect = end_back.get_rect()
    end_back_rect.center=screen_rect.center

    font = pygame.font.Font('Raleway-Bold.ttf', 36)
    text = font.render("Congratulations you beat Joe's Adventure", True, (255, 255, 255))

    buttonFont = pygame.font.Font('Raleway-Bold.ttf', 18)
    buttonQuitText = font.render("Quit", True, (255, 255, 255))

    end = True
    while end:
        screen.blit(end_back,end_back_rect)
        screen.blit(text,(25,100))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if buttonQuit_x < mouse_pos[0] < buttonQuit_x + buttonQuit_width and buttonQuit_y < mouse_pos[1] < buttonQuit_y + buttonQuit_height:
                    # Button Click
                    pygame.quit()

        pygame.draw.rect(screen, buttonQuit_color, (buttonQuit_x, buttonQuit_y, buttonQuit_width, buttonQuit_height))
        screen.blit(buttonQuitText, (buttonQuit_x+10, buttonQuit_y))
        pygame.display.flip()
    
game_intro()

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        # Handle events for all NPCs
        for npc in npc_group:
            if str(type(npc)) == "<class 'npc.Shopkeeper'>":
                possible_coin = npc.handle_event(event,screen,item_group,player,inventory,coin)
                if possible_coin != None:
                    coin = possible_coin
            elif str(type(npc)) == "<class 'npc.NPC'>":
                npc.handle_event(event,player)
            else:
                npc.handle_event(event,inventory,player,item_group)
        # Handle events for all items
        for item in item_group:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if inventory.shop_open == False:
                        if item.inv == None:
                            if item.rect.colliderect(player.rect):
                                inventory.add_item(item)
                                break
                elif event.key == pygame.K_r:
                    if item.rect.collidepoint(pygame.mouse.get_pos()):
                        if item.inv == inventory:
                            inventory.remove_item(item)
                            item.kill()
                            break

        inventory.handle_event(event,item_group)

    render()
    if player.pos.x>=750:
        if enemy_group.__len__() > 0:
            player.pos.x = 750
        else:
            levelTesting.nextLevel(player,item_group,enemy_group,npc_group,screen)
    elif player.pos.x <= 0:
        player.pos.x = 0
        
    for enemy in enemy_group:
        if enemy.health<=0:
            if levelTesting.level==1:
                enemy.die(levelTesting.level_1_items,item_group)
                coin += random.randint(1,2)
            if levelTesting.level==2:
                enemy.die(levelTesting.level_2_items,item_group)
                coin += random.randint(2,4)
            if levelTesting.level==3:
                enemy.die(levelTesting.level_3_items,item_group)
                coin += random.randint(3,6)
            if enemy.is_dr_malice:
                running = False
                endScreen()
            print(levelTesting.room) 

        enemy.collision()

    if player.health<=0:

        coin -= int(coin/2) # Half of player's coins are removed upon death

        if levelTesting.level==1:
            levelTesting.room=0
        if levelTesting.level==2:
            levelTesting.room=8
        if levelTesting.level==3:
            levelTesting.room=17
        levelTesting.nextLevel(player,item_group,enemy_group,npc_group,screen)
        player.health=player.max_health

    if levelTesting.room == 25:
        if pygame.time.get_ticks() - time > 5000:
            levelTesting.spawn_enemy(enemy_group,levelTesting.level_3_enemies)
            time = pygame.time.get_ticks()
    


    player.update(enemy_group)

    pygame.time.Clock().tick(60)

pygame.quit()
