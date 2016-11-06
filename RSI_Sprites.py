all_sprites = pygame.sprite.Group()
ship_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()


# Folder inits
# game_folder = os.path.dirname(__file__)
# img_folder = os.path.join(game_folder, "assets")\
# self.rect.center = (random.randint(0,width), random.randint(0,height))

#Sprites

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center
        self.speedy = 25
        # Attributes
        self.bulletaccuracy = 10
        self.speedx = random.randint(-self.bulletaccuracy,self.bulletaccuracy)
        self.damage = 15

    def update(self):
        hits = pygame.sprite.spritecollide(self, enemy_sprites, False)
        if hits:
            self.kill()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top == height - 200:
            self.kill()

class Enemy_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center
        self.speedy = -25
        # Attributes
        self.bulletaccuracy = 10
        self.speedx = random.randint(-self.bulletaccuracy,self.bulletaccuracy)
        self.damage = 15

    def update(self):
        hits = pygame.sprite.spritecollide(self, ship_sprites, False)
        if hits:
            self.kill()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top == height - 200:
            self.kill()

class Ship1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("assets/ball.bmp")
        self.image = pygame.Surface((50, 40))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        mouse = pygame.mouse.get_pos()
        self.rect.center = (mouse[0], 200)
        # Attributes
        self.speedy = 2
        self.firingspeed = 20
        self.health = 20

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top == height - 200:
            self.kill()

        if (random.randint(1, self.firingspeed) == self.firingspeed / 2):
            new_bullet = Bullet()
            new_bullet.rect.center = (self.rect.midbottom)
            all_sprites.add(new_bullet)
            bullet_sprites.add(new_bullet)

        hits = pygame.sprite.spritecollide(self, enemy_bullet_sprites, False)
        if hits:
            self.health -= 15
        if (self.health <= 0):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100, 40))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height - 100)
        # Attributes
        self.firingspeed = 10
        self.health = 200

    def update(self):
        hits = pygame.sprite.spritecollide(self, bullet_sprites, False)
        if hits:
            self.health -= 15
        if (self.health <= 0):
            self.kill()

        if (random.randint(1, self.firingspeed) == self.firingspeed / 2):
            new_bullet = Enemy_Bullet()
            new_bullet.rect.center = (self.rect.midtop)
            all_sprites.add(new_bullet)
            enemy_bullet_sprites.add(new_bullet)
