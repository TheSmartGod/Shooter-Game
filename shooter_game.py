from pygame import *
from random import randint, choice

mixer.init()
font.init()

WIDTH, HEIGHT = 800, 500
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
score = 0
state = "INTRO"

class ImageSprite(sprite.Sprite):
    def __init__(self, filename, position, size):
        super().__init__()
        self.rect = Rect(position, size)
        self.image = image.load(filename)
        self.image = transform.scale(self.image, size)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Player(ImageSprite):
    def __init__(self, filename, position, size, velocity):
        super().__init__(filename, position, size)
        self.vel = Vector2(0,0)
        self.base_vel = Vector2(velocity)
    def update(self):
        keys = key.get_pressed()
        if keys[K_RIGHT]:
            self.vel.x = self.base_vel.x
        if keys[K_LEFT]:
            self.vel.x = self.base_vel.x * -1
        if not keys[K_RIGHT] and not keys[K_LEFT]:
            self.vel.x = 0
        self.rect.topleft += self.vel
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def throw(self):
        b = Shield(filename="some.png", position=(0,0), size=(140,120), velocity=(0,-8))
        b.rect.center = self.rect.center
        throws.add(b)
        choice(soundlst).play()

class Enemy(ImageSprite):
    def __init__(self, filename, position, size, velocity):
        super().__init__(filename, position, size)
        self.velocity = Vector2(velocity)
    def update(self):
        global score
        self.rect.topleft += self.velocity
        if self.rect.top > HEIGHT:
            score-=20
            self.rect.bottom = 0
            self.rect.x = randint(self.rect.width, WIDTH-self.rect.width)

class Shield(ImageSprite):
    def __init__(self, filename, position, size, velocity):
        super().__init__(filename, position, size)
        self.velocity = Vector2(velocity)
    def update(self):
        self.rect.topleft += self.velocity
        if self.rect.bottom < 0:
            self.kill()

class TextSprite(sprite.Sprite):
    def __init__(self, text, position, font_size, color):
        super().__init__()
        self.font = font.Font("RubikBubbles-Regular.ttf",font_size)
        self.color = color
        self.update_text(text)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
    def update_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

enemies = sprite.Group()
throws = sprite.Group()

def create_enemy():
   rand_coor = randint(30,100)
   enemy = Enemy(filename="blah.png", position=(0,0), size=(rand_coor,rand_coor), velocity=(0, randint(1,5)))
   enemy.rect.x = randint(enemy.rect.width, WIDTH-enemy.rect.width)
   enemy.rect.y = -enemy.rect.height
   enemies.add(enemy)

bg_game = ImageSprite(filename="galaxy.jpg", position=(0,0), size=(WIDTH, HEIGHT))
bg_intro = ImageSprite(filename="df.jpg", position=(0,0), size=(WIDTH, HEIGHT))
Captain_America = Player(filename="Captain.png", position=(0,300), size=(100,200), velocity=(20,20))
throwing_sound = mixer.Sound("fire.ogg")
soundlst = [throwing_sound]
text = TextSprite(f"Score: 0", (30,30), 30, "white")
title = TextSprite("Captain America vs Red Skull", (100,400), 40, "beige")
instruct = TextSprite("Press S to start", (230,450), 40, "beige")
gameover = TextSprite("GAMEOVER", (160,200), 80, "red")
for i in range(3):
    create_enemy()

while not event.peek(QUIT):
    for ev in event.get():
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE and state == "GAME":
                Captain_America.throw()
            if ev.key == K_s and state == "INTRO":
                state = "GAME"
    if state == "INTRO":
        bg_intro.draw(window)
        title.draw(window)
        instruct.draw(window)
    if state == "GAME":            
        bg_game.draw(window)
        Captain_America.update()
        Captain_America.draw(window)
        enemies.update()
        enemies.draw(window)
        throws.update()
        throws.draw(window)
        text.draw(window)
        throw_hits = sprite.groupcollide(throws, enemies, True, True)
        for hit in throw_hits:
            create_enemy()
            score+=1
        player_hits = sprite.spritecollide(Captain_America, enemies,True)
        for hit in player_hits:
            score-=20
            create_enemy()
        if score < 0:
            state = "GAMEOVER"
        text.update_text(f"Score: {str(score)}")
    if state == "GAMEOVER":
        window.fill("black")
        gameover.draw(window)
    display.update()
    clock.tick(60)