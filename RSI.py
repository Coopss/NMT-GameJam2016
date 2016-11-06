import sys, pygame, random, string, math, os

width, height = 1920, 1080
size = width, height
speed = [10, 10]
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
white = (255,255,255)
FPS = 30
SPAWNROOMY = 300
SPAWNROOMX = 400
SCORE = 0
FIRING_SPEED = 0
DAMAGE = 0
ACCURACY = 0
HEALTH_MULTIPLIER = 0
EFFECTIVE_HEALING = 0
PASSIVE_MONEY_MULTIPLIER = 0
STATE = True
SHIP_STATE= [['Fighter', False], ['Shield', False], ['Healer', False], ['Laser', False], ['Missile', False]]

# Initalize pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size, 0, 32)

# Graphics and Sounds
pygame.display.set_caption("Reverse Space Invaders")
clock = pygame.time.Clock()
bg = pygame.image.load("assets/background1.png")
smallfont = pygame.font.SysFont("monospace", 15)
largefont = pygame.font.SysFont("monospace", 60)

# menu_bar = pygame.draw.rect(screen, white, (400, 0, 5, height))

buttons = ['Damage' ,'Accuracy', 'Firing Speed', 'Health Multiplier', 'Healing Effectiveness', 'Passive Income Multiplier']
buttonDict = {}

cur_height = 200
for button in buttons:
    buttonDict[button] = [smallfont.render(button, True, white)]
    buttonDict[button].append(buttonDict[button][0].get_rect())
    pygame.draw.rect(buttonDict[button][0], white, buttonDict[button][1], 1)
    buttonDict[button][1].bottom = cur_height
    buttonDict[button][1].left = 0
    cur_height += 20

bg_music = 'space.ogg'
shooting_sounds = ['assets/', 'assets/']
fighter_death_sound = pygame.mixer.Sound('assets/fighterdead.wav')
fighter_death_sound.set_volume(0.5)
ship_shoot = pygame.mixer.Sound('assets/laser5.wav')
ship_shoot.set_volume(0.1)
missile_shoot = pygame.mixer.Sound('assets/missilelaunch.wav')
missile_shoot.set_volume(0.1)
laser_shoot = pygame.mixer.Sound('assets/laser.wav')
laser_shoot.set_volume(0.1)
low_hp = pygame.mixer.Sound('assets/hullalarm.wav')
low_hp.set_volume(0.1)
button_press = pygame.mixer.Sound('assets/option1.wav')
button_press.set_volume(0.1)
error_sound = pygame.mixer.Sound('assets/option2.wav')
error_sound.set_volume(0.5)
ship_place = pygame.mixer.Sound('assets/shipplace.wav')
ship_place.set_volume(0.3)
heal_sound = pygame.mixer.Sound('assets/healthship.wav')
heal_sound.set_volume(0.3)

fighter_img = 'assets/fightership.png'
healer_img = 'assets/healship.png'
shield_img = 'assets/wallship.png'
laser_img = 'assets/lasership.png'
missile_img = 'assets/missileship.png'
shield_station_img = 'assets/shield.png'
enemy_fighter_img = 'assets/enemyfighter.png'
enemy_turret_img = 'assets/turret.png'
enemy_missile_turret_img = 'assets/missileturret.png'

explosions = []
for i in range (1,4):
    expl = pygame.mixer.Sound('assets/explosion' + str(i) + '.wav')
    expl.set_volume(0.5)
    explosions.append(expl)
explosions.append(fighter_death_sound)
pygame.mixer.music.load('assets/space.ogg')
pygame.mixer.music.play(loops = -1)
pygame.mixer.music.set_volume(0.3)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['lg2'] = []
explosion_anim['sm2'] = []
for i in range(1,9):
    filename = 'assets/boom{}.png'.format(i)
    img = pygame.image.load(filename)
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
for i in range(9):
    filename = 'assets/regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename)
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg2'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm2'].append(img_sm)

all_sprites = pygame.sprite.Group()
ship_sprites = pygame.sprite.Group()
heal_ship_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
heal_bullet_sprites = pygame.sprite.Group()
friendly_ship_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
enemy_station_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
enemy_planet_sprite = pygame.sprite.Group()
enemy_shield_sprites = pygame.sprite.Group()
death_sprites = pygame.sprite.Group()

def get_dist(x1, y1, x2, y2):
    return math.sqrt(((x2 - x1)**2) + ((y2 - y1)**2))

#Sprites
class Earth(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, 100))
        self.image.fill((255,255,255))
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height)
        self.last_update = pygame.time.get_ticks()
        #Attributes
        self.health = 0
        self.level = 0

    def spawn(self):
        if len(enemy_station_sprites) == 0:
            player.money += 2000 * self.level
            self.level += 1
            for i in range(0, int(self.level)):
                enemy = EnemyGun(self.level)
                enemy.rect.center = (random.randint(400,width-100), height - 100)
                enemy_sprites.add(enemy)
                enemy_station_sprites.add(enemy)
                all_sprites.add(enemy)

                if (self.level % 2 == 0):
                    enemy = EnemyFighter(self.level)
                    enemy.rect.center = (random.randint(400,width-100), height - 100)
                    enemy_sprites.add(enemy)
                    all_sprites.add(enemy)

            for i in range(0, int(self.level / 2)):
                enemy = EnemyGun(self.level)
                enemy2 = EnemyShieldStation(self.level)
                w = (random.randint(400,width - 100))
                enemy.rect.center = (w, height - 100)
                enemy2.rect.center = (w, height - 175)
                enemy_sprites.add(enemy)
                enemy_sprites.add(enemy2)
                enemy_shield_sprites.add(enemy2)
                enemy_station_sprites.add(enemy)
                enemy_station_sprites.add(enemy2)
                all_sprites.add(enemy)
                all_sprites.add(enemy2)

            if self.level >= 5:
                for i in range(0, self.level - 4):
                    enemy = EnemyMissileTurret(self.level)
                    enemy2 = EnemyShieldStation(self.level)
                    w = (random.randint(400,width - 100))
                    enemy.rect.center = (w, height - 100)
                    enemy2.rect.center = (w, height - 175)
                    enemy_sprites.add(enemy)
                    enemy_sprites.add(enemy2)
                    enemy_shield_sprites.add(enemy2)
                    enemy_station_sprites.add(enemy)
                    enemy_station_sprites.add(enemy2)
                    all_sprites.add(enemy)
                    all_sprites.add(enemy2)
        # if progressionlevel

    def update(self):
        global SCORE
        self.spawn()
        hits = pygame.sprite.spritecollide(self, ship_sprites, False)
        for hit in hits:
            self.health = hit.health
            SCORE += hit.health
            hit.kill()
            self.kill()
        hits = pygame.sprite.spritecollide(self, heal_ship_sprites, False)
        for hit in hits:
            self.health = hit.health
            SCORE += hit.health
            hit.kill()
            self.kill()
class Bullet(pygame.sprite.Sprite):
    def __init__(self, damage):
        global ACCURACY
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/fighterbullet.png")
        self.rect = self.image.get_rect()
        self.speedy = 25
        # Attributes
        self.bulletaccuracy = int(5 - (ACCURACY / 2))
        if self.bulletaccuracy < 1:
            self.bulletaccuracy = 1
        self.speedx = random.randint(-self.bulletaccuracy,self.bulletaccuracy)
        self.damage = damage
        self.last_update = pygame.time.get_ticks()
        self.death_time = 99999

    def death(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.death_time:
            self.last_update = now
            self.kill()

    def check_bounds(self):
        global SPAWNROOMX
        if self.rect.center[0] <= SPAWNROOMX:
            self.kill()

    def update(self):
        global SCORE
        self.check_bounds()
        self.death()
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.damage
            SCORE += self.damage
            self.kill()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
class Laser(pygame.sprite.Sprite):
    def __init__(self, damage, lifetime):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/laser2.png")
        self.rect = self.image.get_rect()
        self.speedy = 1
        # Attributes
        self.speedx = 0
        self.damage = damage
        self.last_update = pygame.time.get_ticks()
        self.lifetime = lifetime

    def do_damage(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, enemy_shield_sprites, False)
        for hit in hits:
            hit.health -= self.damage
            SCORE += self.damage

    def death(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.lifetime:
            self.last_update = now
            self.kill()

    def update(self):
        self.death()
        self.do_damage()
        self.rect.y += self.speedy
class Missile(pygame.sprite.Sprite):
    def __init__(self, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/missile.png")
        self.rect = self.image.get_rect()
        # Attributes
        self.damage = damage
        self.last_update = pygame.time.get_ticks()
        self.death_time = 99999
        self.speedx = 5
        self.speedy = 5
        self.offsetx = 0
        self.offsety = 0

    def death(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.death_time:
            self.last_update = now
            self.kill()

    def check_bounds(self):
        global SPAWNROOMX
        if self.rect.center[0] <= SPAWNROOMX:
            self.kill()


    def find_nearest_enemy(self):
        closest_sprite = [0,0]
        for sprite in enemy_sprites:
            distl = get_dist(sprite.rect.center[0], sprite.rect.center[1], self.rect.center[0], self.rect.center[0])

            if distl < get_dist(closest_sprite[0], closest_sprite[1], self.rect.center[0], self.rect.center[1]):
                closest_sprite[0] = sprite.rect.center[0]
                closest_sprite[1] = sprite.rect.center[1]

        self.offsetx = (closest_sprite[0] - self.rect.center[0])
        self.offsety = (closest_sprite[1] - self.rect.center[1])

        if self.offsetx == 0:
            self.offsetx += 0.0000001
        if self.offsety == 0:
            self.offsety += 0.0000001
        # return (math.atan((closest_sprite[0] - self.rect.center[0]) / (closest_sprite[1] - self.rect.center[1])) * (180 / 3.1415))

    def move(self):
        self.find_nearest_enemy()
        try:
            self.rect.y += self.speedy * abs(self.offsety / self.offsetx)
            self.rect.x += self.speedx * self.offsetx / self.offsety
        except:
            pass

    def update(self):
        global SCORE
        self.check_bounds()
        self.death()
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.damage
            SCORE += self.damage
            self.kill()
        self.move()
class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/enemymissile.png")
        self.rect = self.image.get_rect()
        # Attributes
        self.damage = 400 + (100 * level)
        self.last_update = pygame.time.get_ticks()
        self.death_time = 10000
        self.speedx = 5
        self.speedy = -5
        self.offsetx = 0
        self.offsety = 0

    def death(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.death_time:
            self.last_update = now
            self.kill()

    def check_bounds(self):
        global SPAWNROOMX
        if self.rect.center[0] <= SPAWNROOMX:
            self.kill()


    def find_nearest_enemy(self):
        closest_sprite = [0,0]
        for sprite in friendly_ship_sprites:
            distl = get_dist(sprite.rect.center[0], sprite.rect.center[1], self.rect.center[0], self.rect.center[0])

            if distl < get_dist(closest_sprite[0], closest_sprite[1], self.rect.center[0], self.rect.center[1]):
                closest_sprite[0] = sprite.rect.center[0]
                closest_sprite[1] = sprite.rect.center[1]

        self.offsetx = -(closest_sprite[0] - self.rect.center[0])
        self.offsety = (closest_sprite[1] - self.rect.center[1])

        if self.offsetx == 0:
            self.offsetx += 0.000001
        if self.offsety == 0:
            self.offsety += 0.000001


        # return (math.atan((closest_sprite[0] - self.rect.center[0]) / (closest_sprite[1] - self.rect.center[1])) * (180 / 3.1415))

    def move(self):
        self.find_nearest_enemy()
        try:
            self.rect.y += self.speedy * abs(self.offsety / self.offsetx)
            self.rect.x += self.speedx * (self.offsetx / self.offsety)
        except:
            pass

    def update(self):
        self.check_bounds()
        self.death()
        hits = pygame.sprite.spritecollide(self, friendly_ship_sprites, False)
        for hit in hits:
            hit.health -= self.damage
            self.kill()
        self.move()
class HealBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        global EFFECTIVE_HEALING
        self.image = pygame.Surface((5, 5))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.center
        self.speedy = y
        self.speedx = x

        # Attributes
        self.last_update = pygame.time.get_ticks()
        self.bulletaccuracy = 30
        self.damagerep = 25 + EFFECTIVE_HEALING*5
        self.decay_time = 300

    def check_bounds(self):
        global SPAWNROOMX
        if self.rect.center[0] <= SPAWNROOMX:
            self.kill()

    def decay(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.decay_time:
            self.last_update = now
            self.kill()

    def check_collision(self):
        hits = pygame.sprite.spritecollide(self, ship_sprites, False)
        for hit in hits:
            if hit.health < hit.max_health:
                hit.health += self.damagerep
                self.kill()

    def update(self):
        self.check_bounds()
        self.decay()
        self.check_collision()
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top == height - 200:
            self.kill()
class DeathAnim(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.sound = explosions[random.randint(0,3)]
        self.sound.play()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
class Healthbar(pygame.sprite.Sprite):
    def __init__(self, boss):
        pygame.sprite.Sprite.__init__(self)
        self.boss = boss
        self.image = pygame.Surface((self.boss.rect.width,2))
        self.image.set_colorkey((0,0,0)) # black transparent
        pygame.draw.rect(self.image, (0,255,0), (0,0,self.boss.rect.width,2),1)
        self.rect = self.image.get_rect()
        self.oldpercent = 0


    def update(self):
        self.percent = self.boss.health / self.boss.max_health * 1.0
        if self.percent != self.oldpercent:
            pygame.draw.rect(self.image, (0,0,0), (1,0,self.boss.rect.width-1,3)) # fill black
            pygame.draw.rect(self.image, (0,255,0), (1,1,
                int(self.boss.rect.width * self.percent),5),0) # fill green
        self.oldpercent = self.percent
        self.rect.centerx = self.boss.rect.centerx
        self.rect.centery = self.boss.rect.centery - self.boss.rect.height /2 - 10
        #check if boss is still alive
        if (self.boss not in all_sprites):
            self.kill()
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, damage):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/enemybullet.png")
        self.rect = self.image.get_rect()
        self.rect.center
        self.speedy = -25
        # Attributes
        self.bulletaccuracy = 10
        self.speedx = random.randint(-self.bulletaccuracy,self.bulletaccuracy)
        self.damage = damage

    def check_bounds(self):
        global SPAWNROOMX
        if self.rect.center[0] <= SPAWNROOMX:
            self.kill()

    def update(self):
        self.check_bounds()
        hits = pygame.sprite.spritecollide(self, ship_sprites, False)
        for hit in hits:
            hit.health -= self.damage
            self.kill()
        hits = pygame.sprite.spritecollide(self, heal_ship_sprites, False)
        for hit in hits:
            hit.health -= self.damage
            self.kill()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top == height - 200:
            self.kill()
class EnemyFighter(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(enemy_fighter_img)
        self.rect = self.image.get_rect()
        # Attributes
        self.speedy = -1
        self.max_health = 100
        self.health = self.max_health
        self.killValue = 250
        self.firingspeed = 500
        self.damage = 15 + level*5
        self.last_shot = pygame.time.get_ticks()
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def check_collision(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, friendly_ship_sprites, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            self.last_shot = now
            new_bullet = EnemyBullet(self.damage)
            ship_shoot.play()
            new_bullet.rect.center = (self.rect.midtop)
            all_sprites.add(new_bullet)
            bullet_sprites.add(new_bullet)

    def check_death(self):
        self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'sm2')
            all_sprites.add(death)
            player.money += self.killValue
            self.kill()

    def move(self):
        self.rect.y += self.speedy

    def update(self):
        self.move()
        self.check_death()
        self.shoot()
class FighterShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global FIRING_SPEED, HEALTH_MULTIPLIER, SPAWNROOMY, DAMAGE, SPAWNROOMX
        self.image_pre = pygame.image.load(fighter_img)
        self.image = pygame.transform.rotate(self.image_pre, 180)
        self.rect = self.image.get_rect()

        mouse = pygame.mouse.get_pos()
        if mouse[1] > SPAWNROOMY and mouse[0] > SPAWNROOMX:
            self.rect.center = (mouse[0], SPAWNROOMY)
        elif mouse[0] < SPAWNROOMX and mouse[1] < SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, mouse[1])
        elif mouse[0] < SPAWNROOMX and mouse[1] > SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, SPAWNROOMY)
        else:
            self.rect.center = (mouse)

        # Attributes
        self.speedy = 1
        self.max_health = 100 + HEALTH_MULTIPLIER*15
        self.health = self.max_health
        self.price = 150 + (earth.level-1) * 45
        self.unlock_price = 300
        self.firingspeed = 500 - FIRING_SPEED * 25
        self.damage = 25 + DAMAGE * 5
        self.last_shot = pygame.time.get_ticks()
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def check_collision(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

        hits = pygame.sprite.spritecollide(self, enemy_planet_sprite, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            self.last_shot = now
            new_bullet = Bullet(self.damage)
            ship_shoot.play()
            new_bullet.rect.center = (self.rect.midbottom)
            all_sprites.add(new_bullet)
            bullet_sprites.add(new_bullet)

    def check_death(self):
        self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'sm2')
            all_sprites.add(death)
            self.kill()

    def move(self):
        self.rect.y += self.speedy

    def update(self):
        self.move()
        self.check_death()
        self.shoot()
class MissileShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global FIRING_SPEED, HEALTH_MULTIPLIER, SPAWNROOMY, DAMAGE, SPAWNROOMX
        self.image_pre = pygame.image.load(missile_img)
        self.image = pygame.transform.rotate(self.image_pre, 180)
        self.rect = self.image.get_rect()

        mouse = pygame.mouse.get_pos()
        if mouse[1] > SPAWNROOMY and mouse[0] > SPAWNROOMX:
            self.rect.center = (mouse[0], SPAWNROOMY)
        elif mouse[0] < SPAWNROOMX and mouse[1] < SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, mouse[1])
        elif mouse[0] < SPAWNROOMX and mouse[1] > SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, SPAWNROOMY)
        else:
            self.rect.center = (mouse)

        # Attributes
        self.speedy = 1
        self.max_health = 200 + HEALTH_MULTIPLIER*20
        self.health = self.max_health
        self.price = 600 + (earth.level-5) * 180
        self.unlock_price = 1200
        self.firingspeed = 1333 - FIRING_SPEED * 20
        self.damage = 150 + DAMAGE * 30
        self.last_shot = pygame.time.get_ticks()
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def check_collision(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

        hits = pygame.sprite.spritecollide(self, enemy_planet_sprite, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            missile_shoot.play()
            self.last_shot = now
            new_bullet = Missile(self.damage)
            new_bullet.rect.center = (self.rect.midbottom)
            all_sprites.add(new_bullet)
            bullet_sprites.add(new_bullet)

    def check_death(self):
        self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'sm2')
            all_sprites.add(death)
            self.kill()

    def move(self):
        self.rect.y += self.speedy

    def update(self):
        self.move()
        self.check_death()
        self.shoot()
class LaserShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global FIRING_SPEED, HEALTH_MULTIPLIER, SPAWNROOMX, SPAWNROOMY, DAMAGE
        self.image = pygame.image.load(laser_img)
        self.rect = self.image.get_rect()

        mouse = pygame.mouse.get_pos()
        if mouse[1] > SPAWNROOMY and mouse[0] > SPAWNROOMX:
            self.rect.center = (mouse[0], SPAWNROOMY)
        elif mouse[0] < SPAWNROOMX and mouse[1] < SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, mouse[1])
        elif mouse[0] < SPAWNROOMX and mouse[1] > SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, SPAWNROOMY)
        else:
            self.rect.center = (mouse)
        # Attributes
        self.speedy = 1
        self.max_health = 100 + HEALTH_MULTIPLIER
        self.health = self.max_health
        self.price = 1000 + (earth.level-4) * 100
        self.unlock_price = 2000
        self.firingspeed = 4000 - FIRING_SPEED * 600
        self.laserlifetime = 500
        self.damage = 75 + DAMAGE * 7
        self.last_shot = pygame.time.get_ticks()
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def check_collision(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

        hits = pygame.sprite.spritecollide(self, enemy_planet_sprite, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            self.last_shot = now
            new_bullet = Laser(self.damage, self.laserlifetime)
            laser_shoot.play()
            new_bullet.rect.midtop = (self.rect.center)
            all_sprites.add(new_bullet)
            bullet_sprites.add(new_bullet)
            self.health -= 5

    def check_death(self):
        self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'sm2')
            all_sprites.add(death)
            self.kill()

    def move(self):
        self.rect.y += self.speedy

    def update(self):
        self.move()
        self.check_death()
        self.shoot()
class ShieldShip(pygame.sprite.Sprite):
    def __init__(self):
        global HEALTH_MULTIPLIER, SPAWNROOMY, SPAWNROOMX
        pygame.sprite.Sprite.__init__(self)
        self.image_pre = pygame.image.load(shield_img)
        self.image = pygame.transform.rotate(self.image_pre, 180)
        self.rect = self.image.get_rect()

        mouse = pygame.mouse.get_pos()
        if mouse[1] > SPAWNROOMY and mouse[0] > SPAWNROOMX:
            self.rect.center = (mouse[0], SPAWNROOMY)
        elif mouse[0] < SPAWNROOMX and mouse[1] < SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, mouse[1])
        elif mouse[0] < SPAWNROOMX and mouse[1] > SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, SPAWNROOMY)
        else:
            self.rect.center = (mouse)
        # Attributes
        self.speedy = 1
        self.max_health = 600 + HEALTH_MULTIPLIER*200
        self.health = self.max_health
        self.price = 350 + (earth.level-2) * 75
        self.unlock_price = 700
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)


    def check_collision(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

        hits = pygame.sprite.spritecollide(self, enemy_planet_sprite, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()


    def check_death(self):
        self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

    def update(self):
        self.rect.y += self.speedy
        self.check_death()
class HealShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global HEALTH_MULTIPLIER, SPAWNROOMY, SPAWNROOMX, FIRING_SPEED
        self.image = pygame.image.load(healer_img)
        self.rect = self.image.get_rect()
        mouse = pygame.mouse.get_pos()
        if mouse[1] > SPAWNROOMY and mouse[0] > SPAWNROOMX:
            self.rect.center = (mouse[0], SPAWNROOMY)
        elif mouse[0] < SPAWNROOMX and mouse[1] < SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, mouse[1])
        elif mouse[0] < SPAWNROOMX and mouse[1] > SPAWNROOMY:
            self.rect.center = (SPAWNROOMX, SPAWNROOMY)
        else:
            self.rect.center = (mouse)
        # Attributes
        self.speedy = 1
        self.max_health = 25 + HEALTH_MULTIPLIER*4
        self.health = self.max_health
        self.price = 600 + (earth.level-3) * 180
        self.unlock_price = 1200
        self.firingspeed = 1500 - FIRING_SPEED*30
        self.last_shot = pygame.time.get_ticks()

        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def check_collision(self):
        global SCORE
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

        hits = pygame.sprite.spritecollide(self, enemy_planet_sprite, False)
        for hit in hits:
            hit.health -= self.health
            SCORE += self.health
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            self.kill()

    def check_death(self):
        self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'sm2')
            all_sprites.add(death)
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            self.last_shot = now
            inac = 18
            heal_sound.play()
            for i in range(0,3):
                new_bullet = HealBullet(-inac if i == 0 else 0 if i == 1 else inac, 25)
                new_bullet.rect.center = (self.rect.midbottom)
                all_sprites.add(new_bullet)
                heal_bullet_sprites.add(new_bullet)
            for i in range(0,3):
                new_bullet = HealBullet(-inac if i == 0 else 0 if i == 1 else inac, -25)
                new_bullet.rect.center = (self.rect.midtop)
                all_sprites.add(new_bullet)
                heal_bullet_sprites.add(new_bullet)
            for i in range(0,3):
                new_bullet = HealBullet(25, -inac if i == 0 else 0 if i == 1 else inac)
                new_bullet.rect.center = (self.rect.midright)
                all_sprites.add(new_bullet)
                heal_bullet_sprites.add(new_bullet)
            for i in range(0,3):
                new_bullet = HealBullet(-25, -inac if i == 0 else 0 if i == 1 else inac)
                new_bullet.rect.center = (self.rect.midleft)
                all_sprites.add(new_bullet)
                heal_bullet_sprites.add(new_bullet)

    def update(self):
        self.rect.y += self.speedy
        self.check_death()
        self.shoot()
class EnemyGun(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(enemy_turret_img)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height - 100)
        # Attributes
        self.level = level
        self.firingspeed = 250
        self.damage = 45 + level * 5
        self.max_health = 400 + level * 100
        self.health = self.max_health
        self.killValue = 1300 + level * 200
        self.last_shot = pygame.time.get_ticks()

        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            self.last_shot = now
            i = random.randint(0,1)
            new_bullet = EnemyBullet(self.damage)
            if i == 0:
                new_bullet.rect.center = (self.rect.topright)
            else:
                new_bullet.rect.center = (self.rect.topleft)
            all_sprites.add(new_bullet)
            enemy_bullet_sprites.add(new_bullet)

    def check_death(self):
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'lg')
            all_sprites.add(death)
            player.money += self.killValue
            self.kill()

    def update(self):
        self.check_death()
        self.shoot()
class EnemyShieldStation(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        global DAMAGE
        self.image = pygame.image.load(shield_station_img)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height - 200)
        # Attributes
        if level >= 10:
            self.max_health = 2000 + 2000 * (level + DAMAGE)
        else:
            self.max_health = 2000 + level * 200
        self.health = self.max_health
        self.killValue = 2000  + level * 150
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def check_death(self):
        # self.check_collision()
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'lg2')
            all_sprites.add(death)
            player.money += self.killValue
            self.kill()

    def update(self):
        self.check_death()
class EnemyMissileTurret(pygame.sprite.Sprite):
    def __init__(self, level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(enemy_missile_turret_img)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height - 100)
        # Attributes
        self.level = level
        self.firingspeed = 2000
        self.max_health = 500 + (level-5) * 50
        self.health = self.max_health
        self.killValue = 2500 + (level-5) * 200
        self.last_shot = pygame.time.get_ticks()

        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.firingspeed:
            self.last_shot = now
            new_bullet = EnemyMissile(self.level)
            new_bullet.rect.center = self.rect.midtop
            all_sprites.add(new_bullet)
            enemy_bullet_sprites.add(new_bullet)

    def check_death(self):
        if (self.health <= 0):
            death = DeathAnim(self.rect.center, 'lg')
            all_sprites.add(death)
            player.money += self.killValue
            self.kill()

    def update(self):
        self.check_death()
        self.shoot()
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        global HEALTH_MULTIPLIER, PASSIVE_MONEY_MULTIPLIER
        self.image = pygame.image.load("assets/mothership3.png")
        # self.image = pygame.transform.scale(self.image, (1028, 67))
        self.rect = self.image.get_rect()
        # self.rect.center = (width / (48/29), 50)
        self.rect.center = (width / (48/29), 85)

        # Attributes
        self.max_health = 20000
        self.health = self.max_health
        self.healthbar = Healthbar(self)
        all_sprites.add(self.healthbar)
        self.prevhm = HEALTH_MULTIPLIER
        self.money = 2000
        self.last_money = pygame.time.get_ticks()
        self.last_heal = pygame.time.get_ticks()
        self.heal_rate = 100 #4 heals per sec

    def self_heal(self):
        global EFFECTIVE_HEALING
        now = pygame.time.get_ticks()
        if now - self.last_heal > self.heal_rate:
            self.last_heal = now
            self.health += 5 + EFFECTIVE_HEALING

    def health_fix(self):
        global HEALTH_MULTIPLIER
        self.max_health += HEALTH_MULTIPLIER*5000
        self.health += HEALTH_MULTIPLIER*5000
        self.prevhm = HEALTH_MULTIPLIER

    def get_money(self):
        global PASSIVE_MONEY_MULTIPLIER
        now = pygame.time.get_ticks()
        if now - self.last_money > 100:
            self.last_money = now
            self.money += 5 + PASSIVE_MONEY_MULTIPLIER*2

    def update(self):
        global HEALTH_MULTIPLIER
        self.get_money()
        if self.prevhm != HEALTH_MULTIPLIER:
            self.health_fix()
        if (self.health / self.max_health <= 0.10):
            low_hp.play()
        if self.health < self.max_health:
            self.self_heal()

# Init enemy_planet_sprite
earth = Earth()
all_sprites.add(earth)
enemy_planet_sprite.add(earth)

not_enough_money = smallfont.render("NOT ENOUGH MONEY", 1, (255,0,0))
not_high_enough_level2 = smallfont.render("REQUIRES LEVEL 2 TO PURCHASE", 1, (255,0,0))
not_high_enough_level3 = smallfont.render("REQUIRES LEVEL 3 TO PURCHASE", 1, (255,0,0))
not_high_enough_level4 = smallfont.render("REQUIRES LEVEL 4 TO PURCHASE", 1, (255,0,0))
not_high_enough_level5 = smallfont.render("REQUIRES LEVEL 5 TO PURCHASE", 1, (255,0,0))
game_is_paused = smallfont.render("GAME PAUSED (PRESS P TO PAUSE/UNPAUSE)", 1, (255,255,255))
no_error = smallfont.render("", 1, (0,0,0))
cur_error = smallfont.render("", 1, (0,0,0))
cur_status = smallfont.render("", 1, (0,0,0))
err_time = FPS # 1 sec
cur_time = 0
old_level = 0
error = False
status = False

#Game loop
running = True
player = Player()
all_sprites.add(player)
ship_sprites.add(player)

while running:
    #Tick and stuff
    clock.tick(FPS)

    # Event
    if player.health < 0:
        while 1:
            clock.tick(FPS)

            label = largefont.render("Game Over", 1, (255,0,0))
            text_rect = label.get_rect(center=(width/2, height/2))
            screen.blit(label, text_rect)
            label = largefont.render("You Scored: " + str(SCORE), 1, (255,255,0))
            text_rect = label.get_rect(center=(width/2, height/2 + 50))
            screen.blit(label, text_rect)
            label = smallfont.render("Press Enter to quit!", 1, (0,255,0))
            text_rect = label.get_rect(center=(width/2, height/2 + 100))
            screen.blit(label, text_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        quit()
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sprite = FighterShip()
                if SHIP_STATE[0][1] == True:
                    if player.money < sprite.price:
                        cur_error = not_enough_money
                        error_sound.play()
                        error = True
                    else:
                        player.money -= sprite.price
                        all_sprites.add(sprite)
                        ship_sprites.add(sprite)
                        ship_place.play()
                else:
                    if player.money < sprite.unlock_price:
                        cur_error = not_enough_money
                        error_sound.play()
                        error = True
                    else:
                        SHIP_STATE[0][1] = True
                        player.money -= sprite.unlock_price
            if event.key == pygame.K_w:
                sprite = ShieldShip()
                if earth.level >= 2:
                    if SHIP_STATE[1][1] == True:
                        if player.money < sprite.price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= sprite.price
                            all_sprites.add(sprite)
                            ship_sprites.add(sprite)
                            ship_place.play()
                    else:
                        if player.money < sprite.unlock_price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            SHIP_STATE[1][1] = True
                            player.money -= sprite.unlock_price
                else:
                    cur_error = not_high_enough_level2
                    error_sound.play()

            if event.key == pygame.K_e:
                sprite = HealShip()
                if earth.level >= 3:
                    if SHIP_STATE[2][1] == True:
                        if player.money < sprite.price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= sprite.price
                            all_sprites.add(sprite)
                            ship_sprites.add(sprite)
                            ship_place.play()
                    else:
                        if player.money < sprite.unlock_price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            SHIP_STATE[2][1] = True
                            player.money -= sprite.unlock_price
                else:
                    cur_error = not_high_enough_level3
                    error_sound.play()
            if event.key == pygame.K_r:
                sprite = LaserShip()
                if earth.level >= 4:
                    if SHIP_STATE[3][1] == True:
                        if player.money < sprite.price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= sprite.price
                            all_sprites.add(sprite)
                            ship_sprites.add(sprite)
                            ship_place.play()
                    else:
                        if player.money < sprite.unlock_price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            SHIP_STATE[3][1] = True
                            player.money -= sprite.unlock_price
                else:
                    cur_error = not_high_enough_level4
                    error_sound.play()

            if event.key == pygame.K_t:
                sprite = MissileShip()
                if earth.level >= 5:
                    if SHIP_STATE[4][1] == True:
                        if player.money < sprite.price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= sprite.price
                            all_sprites.add(sprite)
                            ship_sprites.add(sprite)
                            ship_place.play()
                    else:
                        if player.money < sprite.unlock_price:
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            SHIP_STATE[4][1] = True
                            player.money -= sprite.unlock_price
                else:
                    cur_error = not_high_enough_level5
                    error_sound.play()
            if event.key == pygame.K_p:
                if STATE == False:
                    STATE = True
                elif STATE == True:
                    STATE = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            button_press.play()
            for button in buttons:
                if buttonDict[button][1].collidepoint(event.pos):
                    if button == 'Damage':
                        if player.money < (1500 + DAMAGE*2000):
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= 1500 + DAMAGE*2000
                            DAMAGE += 1
                    elif button == 'Accuracy':
                        if player.money < (1500 + ACCURACY*500):
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= 1500 + ACCURACY*500
                            ACCURACY += 1
                    elif button == 'Firing Speed':
                        if player.money < (1500 + FIRING_SPEED*3000):
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= 1500 + FIRING_SPEED*3000
                            FIRING_SPEED += 1
                    elif button == 'Health Multiplier':
                        if player.money < (500 + HEALTH_MULTIPLIER*1000):
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= 500 + HEALTH_MULTIPLIER*1000
                            HEALTH_MULTIPLIER += 1
                    elif button == 'Healing Effectiveness':
                        if player.money < (500 + EFFECTIVE_HEALING*500):
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= 500 + EFFECTIVE_HEALING*500
                            EFFECTIVE_HEALING += 1
                    elif button == 'Passive Income Multiplier':
                        if player.money < (500 + PASSIVE_MONEY_MULTIPLIER*200):
                            cur_error = not_enough_money
                            error_sound.play()
                            error = True
                        else:
                            player.money -= 500 + PASSIVE_MONEY_MULTIPLIER*200
                            PASSIVE_MONEY_MULTIPLIER += 1

    if old_level != earth.level:
        STATE = False
        old_level = earth.level
    #Update
    if STATE == True:
        all_sprites.update()
        #player.get_money()
        status = False
    else:
        cur_status = game_is_paused
        status = True
    for sprite in ship_sprites:
        if sprite not in friendly_ship_sprites:
            friendly_ship_sprites.add(sprite)

    for sprite in heal_ship_sprites:
        if sprite not in friendly_ship_sprites:
            friendly_ship_sprites.add(sprite)

    #Draw and render
    pygame.draw.rect(screen, black, (0, 0, width, height))
    screen.blit(bg, (200, 0))
    ##menu

    screen.blit(pygame.transform.rotate(pygame.image.load(fighter_img), 180), (160, 500))
    fighter = FighterShip()
    label = smallfont.render('Fighter (' + str('UNLOCKED) | Spawn with \'q\' for ' + str(fighter.price) if SHIP_STATE[0][1] == True else 'LOCKED) | Buy with \'q\' for ' + str(fighter.unlock_price)), 1, (255,255,255))
    label_rect = label.get_rect(center=(200, 470))
    screen.blit(label, label_rect)

    screen.blit(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(shield_img), 180), (48,32)), (150, 600))
    shield = ShieldShip()
    label = smallfont.render('Shield (' + str('UNLOCKED) | Spawn with \'w\' for ' + str(shield.price) if SHIP_STATE[1][1] == True else 'LOCKED) | Buy with \'w\' for ' + str(shield.unlock_price)), 1, (255,255,255))
    label_rect = label.get_rect(center=(200, 560))
    screen.blit(label, label_rect)

    screen.blit(pygame.image.load(healer_img), (150, 700))
    healer = HealShip()
    label = smallfont.render('Healer (' + str('UNLOCKED) | Spawn with \'e\' for ' + str(healer.price) if SHIP_STATE[2][1] == True else 'LOCKED) | Buy with \'e\' for ' + str(healer.unlock_price)), 1, (255,255,255))
    label_rect = label.get_rect(center=(200, 660))
    screen.blit(label, label_rect)

    screen.blit(pygame.image.load(laser_img), (150, 800))
    laser = LaserShip()
    label = smallfont.render('Laser (' + str('UNLOCKED) | Spawn with \'r\' for ' + str(laser.price) if SHIP_STATE[3][1] == True else 'LOCKED) | Buy with \'r\' for ' + str(laser.unlock_price)), 1, (255,255,255))
    label_rect = label.get_rect(center=(200, 760))
    screen.blit(label, label_rect)

    screen.blit(pygame.transform.rotate(pygame.image.load(missile_img), 180), (150, 900))
    missile = MissileShip()
    label = smallfont.render('Missile (' + str('UNLOCKED) | Spawn with \'t\' for ' + str(missile.price) if SHIP_STATE[4][1] == True else 'LOCKED) | Buy with \'t\' for ' + str(missile.unlock_price)), 1, (255,255,255))
    label_rect = label.get_rect(center=(200, 870))
    screen.blit(label, label_rect)

    pygame.draw.rect(screen, white, (400, 0, 5, height))
    all_sprites.draw(screen)

    for button in buttons:
        screen.blit(buttonDict[button][0], buttonDict[button][1])

    # Text in game
    label = smallfont.render("Money: " + str(player.money), 1, (255,255,0))
    screen.blit(label, (20, 20))

    label = smallfont.render("Score: " + str(SCORE), 1, (255,255, 255))
    screen.blit(label, (20, 40))

    label = smallfont.render("Upgrades", 1, (255,255, 255))
    screen.blit(label, (0, 155))

    label = smallfont.render("Level: " + str(earth.level), 1, (255,255,0))
    screen.blit(label, (width-100, 20))

    #Damage
    label = smallfont.render("Level " + str(DAMAGE) + " | " + str(1500 + DAMAGE*2000), 1, (255,255, 255))
    screen.blit(label, (60, 185))
    #Accuracy
    label = smallfont.render("Level " + str(ACCURACY) + " | " + str(1500 + ACCURACY*500), 1, (255,255, 255))
    screen.blit(label, (80, 205))
    #Firing Speed
    label = smallfont.render("Level " + str(FIRING_SPEED) + " | " + str(1500 + FIRING_SPEED*3000), 1, (255,255, 255))
    screen.blit(label, (116, 225))
    # Health Multiplier
    label = smallfont.render("Level " + str(HEALTH_MULTIPLIER) + " | " + str(500 + HEALTH_MULTIPLIER*1000), 1, (255,255, 255))
    screen.blit(label, (160, 245))
    # Healing Effectiveness
    label = smallfont.render("Level " + str(EFFECTIVE_HEALING) + " | " + str(500 + EFFECTIVE_HEALING*500), 1, (255,255, 255))
    screen.blit(label, (196, 265))
    #Passive Income Multiplier
    label = smallfont.render("Level " + str(PASSIVE_MONEY_MULTIPLIER) + " | " + str(500 + PASSIVE_MONEY_MULTIPLIER*200), 1, (255,255, 255))
    screen.blit(label, (232, 285))

    screen.blit(cur_error, (20, 60))
    if error == True:
        cur_time += 1
        if cur_time >= err_time:
            cur_error = no_error
            cur_time = 0
            error = False

    screen.blit(cur_status, (20, 80))
    if status == True:
        cur_status = no_error
        status = False

    # Push changes
    pygame.display.flip()

pygame.quit()
