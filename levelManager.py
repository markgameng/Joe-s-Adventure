import pygame
import gameobjects
import player
import enemy
import items
import npc
import random



class LevelManager:
    def __init__(self):
        self.minor_health = items.Item(0,0,'Item_Assets\minor_health.png','Minor Potion of Health','consumable',10,5)
        self.medium_health = items.Item(0,0,'Item_Assets\medium_health.png','Potion of Health','consumable',25,15)
        self.strong_health = items.Item(0,0,'Item_Assets\strong_health.png','Major Potion of Health','consumable',50,30)
        self.cloth_armor = items.Item(0,0,'Item_Assets\cloth_armor.png','Cloth Armor','armor',5,10)
        self.leather_armor = items.Item(0,0,'Item_Assets\leather_armor.png','Leather Armor','armor',10,30)
        self.iron_armor = items.Item(0,0,'Item_Assets\iron_armor.png','Iron Armor','armor',20,60)
        self.iron_sword = items.Item(0,0,'Item_Assets\iron_sword.png','Iron Sword','weapon',5,15)
        self.magic_sword = items.Item(0,0,'Item_Assets\magic_sword.png','Magic Sword','weapon',10,30)
        self.flaming_sword = items.Item(0,0,'Item_Assets\\flaming_sword.png','Flaming Sword','weapon',20,60)
        self.malice_sword = items.Item(0,0,'Item_Assets\dr_malice_sword.png',"Dr. Malice's Prototype",'weapon',40,100)
        self.level_1_items = (self.minor_health,self.cloth_armor,self.iron_sword)
        self.level_2_items = (self.medium_health,self.leather_armor,self.magic_sword)
        self.level_3_items = (self.strong_health,self.iron_armor,self.flaming_sword)

        self.level_1_melee = enemy.Enemy(0,350,'Enemy_Assets\melee_1_left.png','Enemy_Assets\melee_1_right.png','melee',15,5,None,4000)
        self.level_1_projectile = enemy.Enemy(0,350,'Enemy_Assets\projectile_1_left.png','Enemy_Assets\projectile_1_right.png','projectile',20,25,1,4000)
        self.level_2_melee = enemy.Enemy(0,350,'Enemy_Assets\melee_2_left.png','Enemy_Assets\melee_2_right.png','melee',70,20,None,3000)
        self.level_2_projectile = enemy.Enemy(0,350,'Enemy_Assets\projectile_2_left.png','Enemy_Assets\projectile_2_right.png','projectile',60,30,2,2000)
        self.level_3_melee = enemy.Enemy(0,350,'Enemy_Assets\melee_3_left.png','Enemy_Assets\melee_3_right.png','melee',100,30,None,3000)
        self.level_3_projectile = enemy.Enemy(0,350,'Enemy_Assets\projectile_3_left.png','Enemy_Assets\projectile_3_right.png','projectile',120,40,4,1000)
        self.level_1_enemies = (self.level_1_melee,self.level_1_projectile)
        self.level_2_enemies = (self.level_2_melee,self.level_2_projectile)
        self.level_3_enemies = (self.level_3_melee,self.level_3_projectile)
        self.enemy_group = pygame.sprite.Group()

        self.possible_npc_dialogue = (("If your health is ever low, use a potion!","Minions sometimes drop them,","or you can buy them from the merchant!"),
                                      ("It is rumored that sages wander nearby,","and that they will reward travellers for their wisdom."),
                                      ("Is it true that you're Dr. Malice's son?","It's a good thing you aren't like him."),
                                      ("Dr. Malice's 'cure' is turning people into monsters.","There's even rumors some plants are transforming too!"),
                                      ("Dr. Malice used to be a great doctor,","But his most recent 'cure' is worse than the disease it was made for.","It's the reason everyone has turned into monsters."),
                                      ("If your inventory gets too full, just remove an item.","You can do this by pressing 'R'.","You can also sell items to the merchant for coins!"))
        
        self.possible_question_dialogue = (("What is your name: ","joe","Correct! Here is a reward.","Incorrect. How do you not know your own name?"),
                                           ("What is 36 + 17: ","53","Impressive! Take this as a reward for your wisdom.","Incorrect. Your math needs some work."),
                                           ("Who is terrorizing our world: ","dr. malice","Correct. Hopefully he will be driven away soon.","Incorrect."),
                                           ("What is the course this game was developed for: ","se2250","Correct. Wait, game?","Incorrect. That's concerning, you should know this."))
        
        self.level = 1
        self.room=0
    
        #Title Page
        # tutorial and exit

        #Level 0
        #Tutorial Level with NPC and explain the games

        #Level 0.1
        # Tutorial Level with mobs fight some stuff

        #Level 1
        # Kill a bunch of mobs and move to the end

        #Level 1.1
        # Boss battle one 

        #Level 2
        # Kill bunch of mobs

        #Level 2.1
        # Final Boss battle 2


    def nextLevel(self,player,item_group,enemy_group,npc_group,screen):
        self.room += 1
        print (self.room)
        if self.room==8:
            self.level=2
        if self.room==17:
            self.level=3
        player.pos.x=70
        player.pos.y=400-player.rect.height
        for item in item_group:
            if item.inv == None:
                item_group.remove(item)
        enemy_group.empty()
        npc_group.empty()
        self.whatSpawns(self.room,enemy_group,npc_group,item_group,screen)
        
    def spawn_npc(self,x,npc_group,dialogue):
        new_npc = npc.NPC(x,336,'NPC_Assets\\npc.png',*dialogue)
        npc_group.add(new_npc)

    # IMPORTANT: the dialogue argument must be a tuple of strings with a size of 4 that follows the order:
    # question, answer, dialogue when answer is correct, dialogue when answer is incorrect.
    def spawn_question_npc(self,x,npc_group,dialogue,possible_items):
        new_npc = npc.QuestionNPC(x,338,'NPC_Assets\questionNPC.png',dialogue[1],random.choice(possible_items).copy(),dialogue[0],dialogue[2],dialogue[3])
        npc_group.add(new_npc)

    def spawn_shopkeeper(self,x,npc_group,screen,possible_items):
        item_list = []
        for i in range(random.randint(2,5)):
            index = random.randint(1,10)
            if index < 7:
                new_item = possible_items[0].copy()
            elif index < 9:
                new_item = possible_items[1].copy()
            else:
                new_item = possible_items[2].copy()
            item_list.append(new_item)

        new_npc = npc.Shopkeeper(x,338,'NPC_Assets\shopkeeper.png','Welcome to my shop!',screen,*item_list)
        npc_group.add(new_npc)

    def spawn_enemy(self,enemy_group,possible_enemies):
        new_enemy = random.choice(possible_enemies).copy()
        enemy_group.add(new_enemy)
        new_enemy.pos.x = random.randint(100,700) 

    def spawn_boss1(self,enemy_group):
        boss1 = enemy.Enemy(700,350,'Enemy_Assets\\boss_1_left.png','Enemy_Assets\\boss_1_right.png','projectile',200,40,5,1500)
        boss1.is_boss1 = True
        enemy_group.add(boss1)

    def spawn_dr_malice(self,enemy_group):
        dr_malice = enemy.Enemy(675,350,'Enemy_Assets\dr_malice_left.png','Enemy_Assets\dr_malice_right.png','projectile',3000,200,5,5000)
        dr_malice.is_dr_malice = True
        enemy_group.add(dr_malice)

    def whatSpawns(self,room,enemy_group,npc_group,item_group,screen):
        if room==1:
            self.spawn_npc(400,npc_group,("Welcome to Earth Joe, we have been expecting you","Dr. Malice has taken over our planet and only you can save us.","In order to save our world you must destroy Dr. Malice.","Along the way you will no doubt encounter many of his minions.","They have been 'treated' with his 'cures'."))
        
        elif room ==2:
            self.spawn_npc(250,npc_group,("Over there is an item","you can pick it up by getting near and pressing 'E'","Once it's in your inventory, you can use it by pressing 'E' too!","Give it a try!"))
            self.spawn_npc(600,npc_group,("One of Dr. Malice's minions is in the next room","you can defeat minions by getting close and attacking with 'SPACE'","Be careful though, if you get too close, they can attack you too!"))
            tutorial_item = self.minor_health.copy()
            item_group.add(tutorial_item)
            tutorial_item.rect.midbottom = (450,400)
        
        elif room ==3:
            tutorial_enemy = self.level_1_melee.copy()
            enemy_group.add(tutorial_enemy)
            tutorial_enemy.pos.x = 600
        
        elif room ==4:
            self.spawn_npc(300,npc_group,("Good work defeating that minion!","You might have noticed that it dropped some coins.","You can use them to buy items from the merchant","You can also sell your items to him to get more coins.","Make sure to trade as much as you need when you first talk to him,","He'll leave after you're done trading.","press 'E' to buy or sell items, then press 'ESC' to leave."))
            self.spawn_shopkeeper(500,npc_group,screen,self.level_1_items)
            self.spawn_npc(600,npc_group,("There's some more minions up ahead,","Try beating them to reach the next safe zone."))
        
        elif room ==5:
            for  i in range(random.randint(2,3)):
                self.spawn_enemy(enemy_group,(self.level_1_melee.copy(),self.level_1_melee.copy()))
        elif room ==6:
            for  i in range(random.randint(3,4)):
                self.spawn_enemy(enemy_group,(self.level_1_melee.copy(),self.level_1_melee.copy()))

        elif room ==7:
            self.spawn_npc(300,npc_group,random.choice(self.possible_npc_dialogue))
            self.spawn_shopkeeper(600,npc_group,screen,self.level_1_items)
                
        elif room ==8:
            self.spawn_npc(200,npc_group,("Some of Dr. Malice's minions shoot fireballs.","Make sure to jump over them, or you'll get hit!"))
            projectile_tutorial = self.level_1_projectile.copy()
            enemy_group.add(projectile_tutorial)
            projectile_tutorial.pos.x = 600

        elif room ==9:
            for  i in range(random.randint(2,3)):
                self.spawn_enemy(enemy_group,self.level_2_enemies)
        elif room ==10:
            for  i in range(random.randint(2,3)):
                self.spawn_enemy(enemy_group,self.level_2_enemies)     
        elif room ==11:
            self.spawn_npc(300,npc_group,random.choice(self.possible_npc_dialogue))
            self.spawn_shopkeeper(600,npc_group,screen,self.level_2_items)
        elif room ==12:
            for  i in range(random.randint(4,5)):
                self.spawn_enemy(enemy_group,self.level_2_enemies)        
        elif room ==13:
            for  i in range(random.randint(4,5)):
                self.spawn_enemy(enemy_group,self.level_2_enemies)   
        elif room ==14:
            self.spawn_npc(300,npc_group,random.choice(self.possible_npc_dialogue))
            self.spawn_shopkeeper(600,npc_group,screen,self.level_2_items)   

        elif room ==15:
            self.spawn_npc(400,npc_group,("Dr. Malice's assistant is just up ahead.","Be careful, the 'cure' has made him very strong","His powerful fireballs are said to follow their targets."))
        elif room ==16:
            self.spawn_boss1(enemy_group)
        
        elif room ==17:
            self.spawn_npc(300,npc_group,("One of the rumored sages is over there.","They will ask you a question to test your wisdom.","If you're correct, it is said they will reward you."))
            self.spawn_question_npc(600,npc_group,random.choice(self.possible_question_dialogue),self.level_3_items)
        
        elif room ==18:
            for  i in range(random.randint(2,4)):
                self.spawn_enemy(enemy_group,self.level_3_enemies)
        elif room ==19:
            for  i in range(random.randint(2,4)):
                self.spawn_enemy(enemy_group,self.level_3_enemies)     
        elif room ==20:
            self.spawn_npc(200,npc_group,random.choice(self.possible_npc_dialogue))
            self.spawn_shopkeeper(400,npc_group,screen,self.level_3_items)
            self.spawn_question_npc(600,npc_group,random.choice(self.possible_question_dialogue),self.level_3_items)
        elif room ==21:
            for  i in range(random.randint(5,7)):
                self.spawn_enemy(enemy_group,self.level_3_enemies)        
        elif room ==22:
            for  i in range(random.randint(5,7)):
                self.spawn_enemy(enemy_group,self.level_3_enemies)   
        elif room ==23:
            self.spawn_npc(200,npc_group,random.choice(self.possible_npc_dialogue))
            self.spawn_shopkeeper(400,npc_group,screen,self.level_3_items)  
            self.spawn_question_npc(600,npc_group,random.choice(self.possible_question_dialogue),self.level_3_items)

        elif room ==24:
            self.spawn_npc(400,npc_group,("This is it, Dr. Malice is just up ahead","Be careful, when he sees you he'll summon all the minions at his disposal.","He can also shoot fireballs as hot as the surface of the sun,","so make sure not to get hit.","It's going to be hard, but you can do it Joe!"))
        elif room ==25:
            self.spawn_dr_malice(enemy_group)