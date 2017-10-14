import sys, os, pygame,time,math,random
from queue import PriorityQueue 
pygame.init()

clock = pygame.time.Clock()

size = width, height = 1200, 800
black = 0, 0, 0
#ball = pygame.image.load('C:/users/imadw/Desktop/game/ball.bmp')
screen = pygame.display.set_mode(size)
class Ball:
    def __init__(self, image):
        self.type = "ball"
        self.image =  image
        self.rect = self.image.get_rect()
        self.pos = [0,0]
        self.vel = [-3,-3]
    def average_pos(self):
        self.pos = [(self.rect.left+self.rect.right)/2,(self.rect.top+self.rect.bottom)/2]
    def random_bounce(self):
        return random.uniform(0.95,1.06)
    def fix_pos(self):
        if self.rect.left<= 0 or self.rect.right>width:
            self.vel[0] = -self.random_bounce()*self.vel[0]
        if self.rect.top<=0 or self.rect.bottom>height:
            self.vel[1] = -self.random_bounce()*self.vel[1]
    def update_pos(self):
        self.fix_pos()
        self.rect = self.rect.move(self.vel)
        self.average_pos()
class Seeker(Ball):
    def __init__(self):
        Ball.__init__(self, pygame.image.load('C:/users/imadw/Desktop/game/seeker.bmp').convert())
        self.type = "seeker"
        self.speed = 3
    def seek(self,player):
        self.average_pos()
        player.average_pos()
        dx = player.pos[0]-self.pos[0]
        dy = player.pos[1]-self.pos[1]
        dist = (dx**2+dy**2)**0.5
        self.vel[0] = self.speed*dx/dist
        self.vel[1] = self.speed*dy/dist 
    def update_pos(self):
        self.rect = self.rect.move(self.vel)
        self.average_pos()
class Target(Ball):
    def __init__(self):
        Ball.__init__(self, pygame.image.load('C:/users/imadw/Desktop/game/target.bmp').convert())
        self.rect = self.image.get_rect()
        self.targetblock = pygame.image.load('C:/users/imadw/Desktop/game/targetblock.bmp').convert()
        self.type = "target"
        self.speed = 3
        self.active = 0 
        self.spawn_dict={0:([30,30],[self.speed/2,self.speed/2]),1:([width-30,30],[-self.speed/2,self.speed/2]),2:([30,height-30],[self.speed/2,-self.speed/2]),3:([width-20,height-20],[-self.speed/2,-self.speed/2])}
    def destroy(self):
        self.vel = [0,0]
        self.active = 0 
        screen.blit(self.targetblock,self.rect)
        self.rect.move_ip(width,height)
        self.average_pos()
    def spawn(self):
        self.active = 1
        temppos, self.vel = self.spawn_dict[random.randint(0,3)]
        self.average_pos()
        movex = temppos[0]-self.pos[0]
        movey = temppos[1]-self.pos[1]
        self.rect.move_ip((movex,movey))
        screen.blit(self.image,self.rect)
        pygame.display.flip()
class Bullet(Ball):
    def __init__(self):
        Ball.__init__(self, pygame.image.load('C:/users/imadw/Desktop/game/bullet.bmp').convert())
        self.rect = self.image.get_rect()
        self.rect.move([20,20])
        self.type = "bullet"
        self.speed = 10
        self.active = 0 
    def fix_pos(self):
        if self.rect.left<= 0 or self.rect.right>width:
            self.destroy()
        if self.rect.top<=0 or self.rect.bottom>height:
            self.destroy()
    def destroy(self):
        self.active = 0 
        self.rect.move(2*width,2*height)
        self.vel = [0,0]
        print("bullet gone")
    def fire_bullet(self, player_pos, position):
        self.active = 1
        self.average_pos()
        movex = player_pos[0]-self.pos[0]
        movey = player_pos[1]-self.pos[1]
        self.rect.move_ip((movex,movey))
        self.average_pos()
        print(self.pos)
        deltax = position[0]-self.pos[0]
        deltay = position[1]-self.pos[1]
        delta = max(1,(deltax**2+deltay**2)**0.5)
        
        propx = deltax/delta
        propy = deltay/delta 
        self.vel = [self.speed*propx,self.speed*propy]
        self.rect.move_ip(self.vel)
        screen.blit(self.image,self.rect)
        pygame.display.flip()
class Player(Ball):
    def __init__(self):
        Ball.__init__(self, pygame.image.load('C:/users/imadw/Desktop/game/player.bmp').convert())
        self.speed = 6
        self.pos = [600,400]
        self.rect.move_ip(self.pos)
    def follow_click(self, position):
        self.average_pos()
        deltax = position[0]-self.pos[0]
        deltay = position[1]-self.pos[1]
        delta = (deltax**2+deltay**2)**0.5
        if delta<20:
            self.stop()
        else:
            propx = deltax/delta
            propy = deltay/delta 
            self.vel = [self.speed*propx,self.speed*propy]
            self.rect.move(self.vel)
            
    def get_position(self):
        position = pygame.mouse.get_pos()
        print(position)
        self.follow_click(position)
    def stop(self):
        self.vel=[0,0]
        self.rect.move([0,0])
class Hlaser:
    def __init__(self):
        self.image = pygame.image.load('C:/users/imadw/Desktop/game/greenlaser.bmp').convert()
        self.rect = self.image.get_rect()
        self.type = "laser"
        self.danger = 0 
        self.duration = 60
        self.warning = 40
        self.horizontal = random.randint(100,height-100)
        self.vertical = 0
    def on_danger(self):
        self.danger = 1
        self.image = pygame.image.load('C:/users/imadw/Desktop/game/redlaser.bmp').convert()
    def safe(self):
        self.danger = 0 
        self.image = pygame.image.load('C:/users/imadw/Desktop/game/greenlaser.bmp').convert()
        self.change_location()
    def change_location(self):
        self.horizontal = random.randint(100,height-100)
class Vlaser:
    def __init__(self):
        self.image = pygame.image.load('C:/users/imadw/Desktop/game/greenlaserv.bmp').convert()
        self.rect = self.image.get_rect()
        self.type = "laser"
        self.danger = 0 
        self.duration = 60
        self.warning = 40
        self.horizontal = 0
        self.vertical = random.randint(100,width-100)
    def on_danger(self):
        self.image = pygame.image.load('C:/users/imadw/Desktop/game/redlaserv.bmp').convert()
        self.danger = 1
    def safe(self):
        self.image = pygame.image.load('C:/users/imadw/Desktop/game/greenlaserv.bmp').convert()
        self.danger = 0 
        self.change_location()
    def change_location(self):
        self.vertical = random.randint(100,width-100)
class Game:
    def __init__(self, balls):
        self.events_dict = {"seeker": self.generate_seeker,"balls": self.generate_enemy,"vlaser":self.generate_vlaser, "hlaser":self.generate_hlaser, "vlaseron":self.vlaseron, "hlaseron":self.hlaseron, "hlaseroff":self.hlaser_off, "vlaseroff":self.vlaser_off,"flashcd": self.flashcd, "ghostoff": self.ghostoff, "ghostcd": self.ghostcd, "speedup": self.speedup,"bulletcd":self.bulletcd,"spawntarg":self.spawntarg}
        self.abilities = {"flash":1,"ghost":1, "shoot":1}
        self.cooldowns = {"flash":-1,"ghost":-1}
        self.bullet_count = 2 
        self.targnum = 2
        self.bullets = []
        self.target = [Target(),Target()]
        self.game_over = False
        self.high_score = 0
        self.count = 0 
        self.enemies = []
        self.balls = balls 
        self.player = Player() 
        self.vlaser = Vlaser()
        self.vlaser_on = 0
        self.hlaser = Hlaser() 
        self.hlaser_on = 0 
        self.background = pygame.image.load('C:/users/imadw/Desktop/game/block.bmp').convert()
        self.events = PriorityQueue()
    def get_high_score(self):
        if os.path.isfile('C:/users/imadw/Desktop/game/score.txt'):
            f = open('C:/users/imadw/Desktop/game/score.txt','r')
            self.high_score = int(f.read())
            f.close()
    def distance(self, x1,y1,x2,y2):
        return ((x1-x2)**2+(y1-y2)**2)**0.5
        
    def collide(self, object1, object2):
        if object1.rect.colliderect(object2.rect):
              return True
        else:
            return False
    def bullet_collide(self):
        for target in self.target:
            if target.active == 1:
                for item in self.bullets:
                    if item.rect.colliderect(target.rect) and item.active==1:
                        target.destroy()
                        self.events.put((random.randint(100,300)+self.count,"spawntarg"))
                        item.destroy()
                        self.score += 200
    def check_collide(self):
        xval = {self.player.pos[0]:self.player}
        for enemy in self.enemies:
            xval[enemy.pos[0]] = enemy
        xkeys = sorted(xval.keys())
        for i in range(1,len(xkeys)):
            if xkeys[i]-xkeys[i-1]<40:
                object1 = xval[xkeys[i]]
                object2 = xval[xkeys[i-1]]
                if self.collide(object1, object2):
                    if object1==self.player or object2==self.player:
                        self.game_over = True 
                        print("gameover")
                    else:
                        pass
                        #self.enemy_bounce(object1, object2)
        self.bullet_collide()
        if self.vlaser.danger == 1:
            if self.player.rect.left<self.vlaser.vertical and self.player.rect.right>self.vlaser.vertical:
                self.game_over = True 
                print("gameover")
        if self.hlaser.danger == 1:
            if self.player.rect.top<self.hlaser.horizontal and self.player.rect.bottom>self.hlaser.horizontal:
                self.game_over = True 
                print("gameover")
    def speedup(self):
        if self.player.speed < 7:
            self.player.speed += 0.2
        for item in self.target:
            if item.speed <4:
                item.speed += 0.2
        print("Speedup"+str(self.player.speed))
        self.events.put((self.count+500,"speedup"))
    def enemy_bounce(self, object1, object2):
        temp = object2.vel
        object2.vel = object1.vel
        object1.vel = temp
        
    def generate_enemy(self):
        self.enemies.append(Ball(pygame.image.load('C:/users/imadw/Desktop/game/enemy.bmp').convert()))
        
    def generate_seeker(self):
        self.enemies.append(Seeker())
    
    def generate_bullet(self):
        for i in range(0,self.bullet_count):
            self.bullets.append(Bullet())
            
    def update_bullet(self):
        for item in self.bullets:
            if item.active == 1:
                item.update_pos()
                screen.blit(item.image,item.rect)
    def generate_target(self):
        for i in range(0,self.targnum):
            for target in self.target:
                self.enemies.append(target)
                target.spawn()
    def spawntarg(self):
        for item in self.target:
            if item.active == 0:
                item.spawn()
                break 
    def generate_hlaser(self):
        self.hlaser_on = 1
        self.events.put((self.count+self.hlaser.warning,"hlaseron"))
        
    def generate_vlaser(self):
        self.vlaser_on = 1
        self.events.put((self.count+self.vlaser.warning,"vlaseron"))
        
    def vlaseron(self):
        self.vlaser.on_danger()
        self.events.put((self.count+self.vlaser.duration,"vlaseroff"))
        
    def hlaseron(self):
        self.hlaser.on_danger()
        self.events.put((self.count+self.hlaser.duration,"hlaseroff"))
        
    def vlaser_off(self):
        self.vlaser_on = 0
        self.vlaser.safe()
        self.events.put((self.count+random.randint(100,300),"vlaser"))
        
    def hlaser_off(self):
        self.hlaser_on = 0
        self.hlaser.safe()
        self.events.put((self.count+random.randint(100,300),"hlaser"))
        
    def display_vlaser(self):
        screen.blit(self.vlaser.image,(self.vlaser.vertical,self.vlaser.horizontal))
        
    def display_hlaser(self):
        screen.blit(self.hlaser.image,(self.hlaser.vertical,self.hlaser.horizontal))
        
    def update_game(self):
        screen.fill(black)
        screen.blit(self.background, self.player.rect)
        for enemy in self.enemies:
            enemy.average_pos()
            screen.blit(self.background, enemy.rect)
        self.player.average_pos()
        self.player.update_pos()
        screen.blit(self.player.image,self.player.rect )
        self.update_bullet()
        for enemy in self.enemies:
            if enemy.type == "ball":
                enemy.update_pos()
            elif enemy.type == "seeker":
                enemy.seek(self.player)
                enemy.update_pos()
            elif enemy.type == "bullet" or enemy.type == "target": 
                if enemy.active == 1:
                    enemy.update_pos()
            screen.blit(enemy.image, enemy.rect)
        if self.vlaser_on == 1:
            self.display_vlaser()
        if self.hlaser_on == 1:
            self.display_hlaser()
        self.print_score(self.score)
        self.print_flash()
        self.print_ghost()
        pygame.display.flip()
        
    def print_score(self,score):
        white = (255, 255, 255)
        
        font = pygame.font.Font(None, 40)
        text = font.render(str(score), 1, white)
        screen.blit(self.background, (1100,750))
        screen.blit(text, (1100,750))
        text = font.render(str("Highest:")+str(self.high_score),1,white)
        screen.blit(self.background, (1000,700))
        screen.blit(text, (1000, 700))

        if score>self.high_score:
            self.high_score = score
    def print_flash(self):
        cooldown = max(0,self.cooldowns["flash"]-self.count)
        if cooldown == 0:
            flash = pygame.image.load('C:/users/imadw/Desktop/game/flash.bmp').convert()
        else:
            flash = pygame.image.load('C:/users/imadw/Desktop/game/flashcd.bmp').convert()
        screen.blit(flash, (1000,650))
        white = (255, 255, 255)
        
        font = pygame.font.Font(None, 24)
        text = font.render("%2d" %(cooldown), 1, white)
#        screen.blit(self.background, (1050,650))
        screen.blit(text, (1050,650))
    def print_ghost(self):
        #show the abilities here 
        #maybe create classes for flash and ghost
        cooldown = max(0,self.cooldowns["ghost"]-self.count)
        if cooldown == 0:
            ghost = pygame.image.load('C:/users/imadw/Desktop/game/ghost.bmp').convert()
        else:
            ghost = pygame.image.load('C:/users/imadw/Desktop/game/ghostcd.bmp').convert()
        screen.blit(ghost, (1100,650))
        
        white = (255, 255, 255)
        font = pygame.font.Font(None, 24)
        text = font.render("%2d" %(cooldown), 1, white)
#        screen.blit(self.background, (1150,650))
        screen.blit(text, (1150,650))
        
    def aiplayer(self):
        decision_array = []
        for enemy in self.enemies:
            dx = 600-enemy.pos[0]
            dy = 400-enemy.pos[1]
            if dy > 0:
                if enemy.vel[1] >0:
                    #compute
                    t = (400-enemy.pos[1])/enemy.vel[1]
                    x2 = enemy.pos[0]+enemy.vel[0]*t
                    decision_array.append((x2-20,x2+20))
            else:
                if enemy.vel[1] <0:
                    #compute
                    t = (400-enemy.pos[1])/enemy.vel[1]
                    x2 = enemy.pos[0]+enemy.vel[0]*t
                    decision_array.append((x2-20,x2+20))
        temp_pos = self.player.pos[0]
        for location in decision_array:
            if temp_pos>location[0] and temp_pos<location[1]:
                temp_pos = location[1]+20
        if temp_pos > width:
            temp_pos = width-40
        if temp_pos < 0:
            temp_pos = 40
        self.player.follow_click([temp_pos,400])
    def flash(self, position):
        self.abilities["flash"] = 0
        position = [position[0],position[1]]
        if position[0]>1170:
            position[0] = 1170
        elif position[0]<30:
            position[0] = 30
        if position[1]>770:
            position[1] = 770
        elif position[1]<30:
            position[1] = 30
        deltax = position[0]-self.player.pos[0]
        deltay = position[1]-self.player.pos[1]
        screen.blit(self.background, self.player.rect)
        self.player.rect.move_ip([deltax,deltay])
        self.player.average_pos()
        screen.blit(self.player.image,self.player.rect )
        pygame.display.flip()
        self.events.put((self.count+200, "flashcd"))
        self.cooldowns["flash"] = self.count+200
    def flashcd(self):
        self.abilities["flash"] = 1
    def ghost(self):
        self.abilities["ghost"] = 0
        self.player.speed *= 2
        self.player.vel[0] *= 2
        self.player.vel[1] *= 2
        self.events.put((self.count+50,"ghostoff"))
        self.cooldowns["ghost"] = self.count+50
    def ghostoff(self):
        self.player.speed *= 0.5
        self.player.vel[0] *= 0.5
        self.player.vel[1] *=0.5
        self.events.put((self.count+200, "ghostcd"))
        self.cooldowns["ghost"] = self.count+200
    def ghostcd(self):
        self.abilities["ghost"] = 1
    def bulletcd(self):
        self.abilities["shoot"] = 1
    def game_events_start(self):
        self.generate_bullet()
        self.events.put((100,"seeker"))
        for i in range(2,self.balls+2):
            self.events.put((100*i,"balls"))
        self.events.put((200,"vlaser"))
        self.events.put((300, "hlaser"))
        self.events.put((500, "speedup"))
        
    def game_events_check(self,count):
        if self.events.queue[0][0]<=count:
            event = self.events.get()[1]
            self.events_dict[event]()
    
    def run_game(self):
        self.get_high_score()
        self.count = 0 
        self.score = 0
        self.game_over = False 
        screen.fill(black)
        self.game_events_start()
        self.generate_target()
        while self.game_over==False:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.get_position()
                elif event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_s:
                        self.player.vel=[0,0]
                    elif event.key==pygame.K_d and self.abilities["flash"]==1:
                        print("Flash")
                        self.flash(pygame.mouse.get_pos())
                        self.player.vel=[0,0]
                    elif event.key==pygame.K_f and self.abilities["ghost"]==1: 
                        print("Ghost")
                        self.ghost()
                    elif event.key==pygame.K_a and self.abilities["shoot"]==1:
                        fired = False 
                        self.player.average_pos()
                        for item in self.bullets:
                            if item.active ==0 and fired == False:
                                print("Fired")
                                item.fire_bullet(self.player.pos,pygame.mouse.get_pos())
                                fired = True 
                                self.abilities["shoot"] =0
                                self.events.put((self.count+20,"bulletcd"))
            self.check_collide()
            self.update_game()
            self.count += 1 
            self.score += 1
            clock.tick(60)
            if self.events.qsize()!=0:
                self.game_events_check(self.count)
            if self.game_over==True:
                time.sleep(0.5)
                self.score -=1
                f = open('C:/users/imadw/Desktop/game/score.txt','w')
                f.write(str(self.high_score))
                f.close()
        return self.score 

class GUI:
    def __init__(self):
        self.title = pygame.image.load('C:/users/imadw/Desktop/game/titlescreen.bmp').convert()
        self.lost = pygame.image.load('C:/users/imadw/Desktop/game/losemenu.bmp').convert()
    def wait_for_click(self):
        game_start = False 
        while game_start == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game_start = True 
    def menu(self):
        screen.blit(self.title,(0,0))
        self.get_score()
        pygame.display.flip()
        self.wait_for_click()
    def youlose(self,score):
        screen.fill(black)
        screen.blit(self.lost, (200,200))
        white = (255, 255, 255)
        font = pygame.font.Font(None, 70)
        text = font.render("YOU LOSE, your score was:"+str(score), 1, white)
        screen.blit(text, (200,750))

        pygame.display.flip()
        self.wait_for_click()
    def get_score(self):
        if os.path.isfile('C:/users/imadw/Desktop/game/score.txt'):
            #get score
            f = open('C:/users/imadw/Desktop/game/score.txt','r')
            score = f.read()
            white = (255, 255, 255)
            
            font = pygame.font.Font(None, 72)
            text = font.render(str("High Score:")+score,1,white)
            screen.blit(text, (600, 700))
            f.close()
            
        
        
try: 
    start = GUI()
    while(1):
        start.menu()
        newgame = Game(5)
        score = newgame.run_game()
        start.youlose(score)
finally: 
    pygame.quit()