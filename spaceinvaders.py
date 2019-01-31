#!/usr/bin/python

import pygame, sys, time, random, math

#set screen, create variables, and inits
playerhp = 9
DEHP = 2
want_star_color = (180, 180, 180)
star_color = (180, 180, 180)
ENEMY_HTW_RATIO = 1.35
MAX_ROCKETS = 3
timeleft = 1
speed = [100, 1]
black = 0, 0, 0
SPEED = 0.5
xvel = 0
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()
size = height, width
screenrect = pygame.Rect(-350, -350, width+350, height+350)
xpos = int(width/2)
pygame.init()
prevtime = time.time() * 1000
stars = []
bullets = []
particles = []
enemysize = 55
swarmsize = [int(width/3/(enemysize*ENEMY_HTW_RATIO)), int(height/3/enemysize)]
gamefont = pygame.font.Font('SPACEBOY.TTF', 30)
changestarcolor = 100
blind = 0

def draw():
    healthtxt = gamefont.render(str(playerhp)+'hp', True, (255, 255, 255), None)
    screen.fill(black)
    for particle in particles:
        particle.Draw()
    for bullet in bullets:
        bullet.Draw()
    if blind == 0:
        for enemy in Enemy.enemies:
            enemy.Draw()
    screen.blit(player, playerrect)
    screen.blit(healthtxt, pygame.Rect((0, 0), gamefont.size(str(playerhp)+'hp')))

def cSwarm(size1, size2=0, shape = 'rect'):
    Enemy.enemies = []
    if shape == 'rect':
        for enemyx in xrange(0, size1):
            for enemyy in xrange(0, size2):
                Enemy.enemies.append(Enemy(pygame.Rect((int(10+(enemysize*ENEMY_HTW_RATIO)*enemyx), int(10+enemysize*enemyy)), enemyrect.size), DEHP))
    if shape == 'circ':
        enemy_per_layer_increase = 10
        Enemy.enemies.append(Enemy(pygame.Rect((width/2, height/2), enemyrect.size), DEHP))
        for layer in xrange(1, size1+1):
            for rot in xrange(0, layer*enemy_per_layer_increase):
                Enemy.enemies.append(Enemy(pygame.Rect((math.cos(rot*(360.0/(layer*enemy_per_layer_increase))/180.0*math.pi)*layer*(enemysize*ENEMY_HTW_RATIO)+width/2, math.sin(rot*(360.0/(layer*enemy_per_layer_increase))/180.0*math.pi)*layer*enemysize+height/2), enemyrect.size), DEHP))
    ready = False
    while not ready:
        for enemy in Enemy.enemies:
            enemy.rect.left -= 10
        for enemy in Enemy.enemies:
            if enemy.rect.left < 0:
                for enemy in Enemy.enemies:
                    enemy.rect.left += 20
                ready = True
    ready = False
    while not ready:
        for enemy in Enemy.enemies:
            enemy.rect.top -= 10
        for enemy in Enemy.enemies:
            if enemy.rect.top < 0:
                for enemy in Enemy.enemies:
                    enemy.rect.top += 20
                ready = True

class Enemy(object):
    enemies = []
    direction = 1
    speed = 2
    def __init__(self, rect, hp):
        self.hp = hp
        self.dead = False
        self.rect = rect
    def Update(self):
        self.rect.left += Enemy.direction * Enemy.speed
        if random.random()<0.1 and random.random()<0.1 and random.random()<0.1 and random.random() < 0.1:
            bullets.append(Enemybullet((self.rect.left+self.rect.right)/2, self.rect.bottom))
    def Draw(self):
        screen.blit(enemy_sprite, self.rect)
    def Damage(self, hp):
        self.hp -= hp
        if hp == 0:
            self.dead = True

class Particle(object):
    def __init__(self, x, y, color, size, colorplus = (0, 0, 0), colortimes = (1, 1, 1), xvel = 0, yvel = 0, sizeinc = 0, lifespan = 1000, showblind = True):
        self.x = x
        self.y = y
        self.color = color
        self.colorplus = colorplus
        self.colortimes = colortimes
        self.xvel = xvel
        self.yvel = yvel
        self.size = size
        self.sizeinc = sizeinc
        self.lifespan = lifespan
        self.showblind = showblind
    def Update(self):
        self.size += self.sizeinc
        self.x += self.xvel
        self.y += self.yvel
        self.color = (
            self.color[0] * self.colortimes[0],
            self.color[1] * self.colortimes[1],
            self.color[2] * self.colortimes[2])
        self.color = (
            self.color[0] + self.colorplus[0],
            self.color[1] + self.colorplus[1],
            self.color[2] + self.colorplus[2])
        self.color = (
                max(0, min(self.color[0], 255)),
                max(0, min(self.color[1], 255)),
                max(0, min(self.color[2], 255))
                )
        self.lifespan -= 1
    def Draw(self):
        if blind == 0 or self.showblind:
            pygame.draw.circle(screen,
                    (int(self.color[0]), int(self.color[1]), int(self.color[2])),
                    (int(self.x), int(self.y)), int(self.size), 0)

class Bullet(object):
    def __init__(self, x, y):
        self.xspd = 0
        self.yspd = -10
        self.damage = 2
        self.color = (0, 255, 255)
        self.typ = 'bullet'
        self.dead = False
        self.SetCoord(x, y)

    def SetCoord(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect((x, y), (5, 30))

    def Move(self, x, y):
        self.SetCoord(self.x + x, self.y + y)

    def Update(self):
        self.Move(0, self.yspd)

    def Draw(self):
        pygame.draw.line(screen, self.color, (self.rect.centerx, self.rect.centery), (self.rect.centerx-self.xspd*5, self.rect.centery-self.yspd*5), 10)
    
    def Damage(self, hp):
        if self.damage > hp:
            self.damage -= hp
            return hp
        else:
            self.dead = True
            return self.damage
    
    def Cankillenemy(self):
        return True
    def Cankillplayer(self):
        return False

class Rocket(Bullet):
    rocket_count = 0
    def __init__(self, x, y):
        Bullet.__init__(self, x, y)
        self.xspd = 0
        self.yspd = -1
        self.color = (255, 10, 10)
        self.typ = 'rocket'
        Rocket.rocket_count += 1
    def __del__(self):
        Rocket.rocket_count -= 1
    def Update(self):
        Bullet.Update(self)
        particle = Particle(
                x=(self.rect.right+self.rect.left)/2,
                y=self.rect.bottom,
                size = 2,
                sizeinc = 0.1,
                color = (255, 128, 1),
                colortimes = (0.9, 0.9, 1),
                colorplus = (0, 0, 0.9),
                lifespan = 75,
                xvel = random.randint(0, 500)/100*(random.randint(0, 2)-1),
                yvel = random.randint(3, 7))
        particles.append(particle)

    def Destroy(self):
        self.dead = True
    
    def Cankillenemy(self):
        return False

class Minibullet(Bullet):
    def __init__(self, rot, x, y):
        Bullet.__init__(self, x, y)
        self.damage = 1
        self.xspd = math.cos(rot/180.0*math.pi)
        self.yspd = math.sin(rot/180.0*math.pi)
        self.color = (0, 225, 0)
    def Update(self):
        self.Move(self.xspd, self.yspd)
    def Cankillenemy(self):
        return True

class Enemybullet(Bullet):
    def __init__(self, x, y):
        Bullet.__init__(self, x, y)
        self.damage = 1
        self.typ = 'enemy'
        self.xspd = random.randint(-5, 5)/5
        self.yspd = 5
        self.color = (255, 255, 0)
    def Update(self):
        self.Move(self.xspd, self.yspd)
    def Cankillenemy(self):
        return False
    def Cankillplayer(self):
        return True
    def Draw(self):
        if blind>0 and math.sqrt((playerrect.centerx-self.x)**2+(playerrect.centery-self.y)**2) > 500:
            return
        Bullet.Draw(self)

def make_star():
    global changestarcolor
    global star_color
    global want_star_color
    changestarcolor -= 1
    if changestarcolor == 0:
        changestarcolor = 100
        want_star_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    sr = star_color[0]
    sg = star_color[1]
    sb = star_color[2]
    if sr < want_star_color[0]:
        sr += 1
    elif sr > want_star_color[0]:
        sr -= 1
    if sg < want_star_color[1]:
        sg += 1
    elif sg > want_star_color[1]:
        sg -= 1
    if sb < want_star_color[2]:
        sb += 1
    elif sb > want_star_color[2]:
        sb -= 1
    star_color = (sr, sg, sb)
    if random.random() < 0.5:
        r = random.randint(3, 8)/2
        particles.append(Particle(x=random.randint(0, width), y=0, size=r*3, color=star_color, yvel=r+0.5, lifespan=0, showblind=False))
#Create starting stars
for i in xrange(0, 1000):
    for particle in particles:
        particle.Update()
    make_star()

#load the images and create coordinates
player = pygame.image.load("Space Invader Models/playership.png")
player = pygame.transform.scale(player, (100, 100))
playerrect = player.get_rect()
enemy_sprite = pygame.image.load("Space Invader Models/invader.png")
enemy_sprite = pygame.transform.scale(enemy_sprite, (int(ENEMY_HTW_RATIO * enemysize), int(enemysize)))
enemyrect = enemy_sprite.get_rect()

# make enemies
cSwarm(shape = 'circ', size1 = 4)
#cSwarm(shape = 'rect', size1 = swarmsize[0], size2 = swarmsize[1])

while True:
    timeleft += time.time()*1000 - prevtime
    prevtime = time.time()*1000

    #Input
    if len(Enemy.enemies) == 0 or playerhp <= 0:
        if playerhp <= 0:
            text = 'YOU LOSE'
        elif len(Enemy.enemies) == 0:
            text = 'YOU WIN'
        elif len(Enemy.enemies) == 0 and playerhp <= 0:
            text = 'YOU ARE THE EPIC GAMER OF THE YEAR'
        txt = gamefont.render(text, True, (255, 255, 255), None)
        textsize = gamefont.size(text)
        draw()
        screen.blit(txt, pygame.Rect((width/2-textsize[0]/2, height/2-textsize[1]/2), textsize))
        pygame.display.flip()
        time.sleep(1.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                for bullet in bullets:
                    pos = [(bullet.rect.left+bullet.rect.right)/2, (bullet.rect.top+bullet.rect.bottom)/2]
                    if bullet.typ != 'rocket':
                        continue
                    for i in xrange(0, 24):
                        bullet1 = Minibullet(i*15, pos[0], pos[1])
                        bullets.append(bullet1)
                    bullet.Destroy()
            if event.key == pygame.K_SPACE:
                bullet = Bullet((playerrect.left+playerrect.right)/2, playerrect.top)
                bullets.append(bullet)
                bullet = None
            if event.key == pygame.K_r:
                if Rocket.rocket_count < MAX_ROCKETS:
                    bullet = Rocket((playerrect.left+playerrect.right)/2, playerrect.top)
                    bullets.append(bullet)
                    bullet = None
    #movement
    while timeleft - 5 > 0:
        timeleft -= 5
        blind = max(0, blind-1)
        for bullet in bullets:
            bullet.Update()
        make_star() 
        for particle in particles:
            particle.Update()
        for bullet in bullets:
            if bullet.dead:
                continue
            if not bullet.rect.colliderect(screenrect):
                bullet.dead = True
            if bullet.Cankillplayer():
                if bullet.rect.colliderect(playerrect):
                    playerhp -= bullet.damage
                    bullet.dead = True
                    blind = 550
            if not bullet.Cankillenemy():
                continue
            for enemy in Enemy.enemies:
                if enemy.dead:
                    continue
                if bullet.rect.colliderect(enemy.rect):
                    enemy.Damage(bullet.Damage(enemy.hp))
        bullets = [bullet for bullet in bullets if not bullet.dead]
        particles = [particle for particle in particles if particle.lifespan != 0 and particle.x > 0 and particle.x < width and particle.y > 0 and particle.y < height]
        stars = [star for star in stars if star[1] < height]
        Enemy.enemies = [enemy for enemy in Enemy.enemies if not enemy.dead]
        xvel *= 0.9
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            xvel -= SPEED
        if pressed[pygame.K_d]:
            xvel += SPEED
        xpos += xvel
        playerrect.left = xpos
        playerrect.bottom = height - 75

        #check boundaries and stop ship if it passes boundaries
        if playerrect.left < 0:
            playerrect.left = 0
            xvel *= -1.35
        if playerrect.right > width:
            playerrect.right = width
            xvel *= -1.35
        particles.append(Particle(x=playerrect.left+15, y=playerrect.bottom, size=4, color=(1, 255, 255), lifespan=200, yvel=2, xvel=random.random()-0.5/2, colorplus=(0, -3, 0), colortimes=(1.5, 1, 0.9)))
        particles.append(Particle(x=playerrect.right-15, y=playerrect.bottom, size=4, color=(1, 255, 255), lifespan=200, yvel=2, xvel=random.random()-0.5/2, colorplus=(0, -3, 0), colortimes=(1.5, 1, 0.9)))
        # Move Enemies
        for enemy in Enemy.enemies:
            enemy.Update()
        for enemy in Enemy.enemies:    
            if enemy.rect.left < 0:
                enemy.rect.left = 0
                Enemy.direction = 1
                for enemy in Enemy.enemies:
                    enemy.rect.bottom += 25
                break
            if enemy.rect.right > width:
                enemy.rect.right = width
                Enemy.direction = -1
                for enemy in Enemy.enemies:
                    enemy.rect.bottom += 25
                break
    #draw objects and flip
    draw()
    pygame.display.flip()
