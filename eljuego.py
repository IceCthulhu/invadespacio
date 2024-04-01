import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ejemplo de sprites")

# Definir color de fondo
BG_COLOR = (0, 0, 0)

# Clase para representar un sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, design, color, scale):
        super().__init__()
        self.image = self.create_sprite(design, color, scale)
        self.original_image = self.image.copy()  # Guardar la imagen original para rotaciones
        self.rect = self.image.get_rect()
        self.speed = 5  # Velocidad de movimiento
        self.angle = 0  # Ángulo de rotación

    def create_sprite(self, design, color, scale):
        sprite_width = len(design[0])
        sprite_height = len(design)
        sprite_surface = pygame.Surface((sprite_width * scale, sprite_height * scale), pygame.SRCALPHA)  # Usar SRCALPHA para transparencia
        sprite_surface.fill((0, 0, 0, 0))  # Rellenar con color transparente

        for y, row in enumerate(design):
            for x, char in enumerate(row):
                if char == '*':
                    pygame.draw.rect(sprite_surface, color, (x * scale, y * scale, scale, scale))

        return sprite_surface

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def rotate(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

# Clase para representar un enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self, color, scale, x, y):
        super().__init__()
        self.image = self.create_sprite(color, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def create_sprite(self, color, scale):
        sprite_design = [
            " *** ",
            "* * *",
            " *** ",
            "*   *",
            "** **"
        ]
        sprite_width = len(sprite_design[0])
        sprite_height = len(sprite_design)
        sprite_surface = pygame.Surface((sprite_width * scale, sprite_height * scale), pygame.SRCALPHA)  # Usar SRCALPHA para transparencia
        sprite_surface.fill((0, 0, 0, 0))  # Rellenar con color transparente

        for y, row in enumerate(sprite_design):
            for x, char in enumerate(row):
                if char == '*':
                    pygame.draw.rect(sprite_surface, color, (x * scale, y * scale, scale, scale))

        return sprite_surface

# Clase para representar un proyectil
class Projectile(pygame.sprite.Sprite):
    def __init__(self, color, scale, start_x, start_y):
        super().__init__()
        self.image = pygame.Surface((scale, scale))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = 10  # Velocidad de movimiento

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:  # Eliminar el proyectil cuando sale de la pantalla
            self.kill()

# Crear un grupo de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()  # Grupo para los enemigos

# Crear enemigos y agregarlos al grupo
EN_total = 8  # Número total de enemigos
for i in range(EN_total):
    COL_ran = (random.randint(1, 256), random.randint(1, 256), random.randint(1, 256))
    x = SCREEN_WIDTH / (EN_total / 1.5) + (i * 70)
    enemy = Enemy(COL_ran, 10, x, 85)  # Color aleatorio y escala de 10
    all_sprites.add(enemy)
    enemies.add(enemy)

# Crear un sprite del jugador y agregarlo al grupo
sprite_design = [
    "  *  ",
    " *** ",
    "*****",
    "*****",
    "*   *"
]
sprite1 = Sprite(sprite_design, (0, 200, 75), 10)  # Color verde azulado y escala de 10
sprite1.rect.x = (SCREEN_WIDTH - sprite1.rect.width) // 2  # Centrar horizontalmente
sprite1.rect.y = SCREEN_HEIGHT - (sprite1.rect.height + 10)  # Ubicar en la parte inferior
all_sprites.add(sprite1)

# Crear un grupo para los proyectiles
projectiles = pygame.sprite.Group()

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Disparar proyectil al presionar espacio
                projectile = Projectile((255, 255, 255), 5, sprite1.rect.centerx, sprite1.rect.top)
                projectiles.add(projectile)
                all_sprites.add(projectile)

    # Actualizar lógica del juego
    all_sprites.update()

    # Detectar colisiones entre proyectiles y enemigos
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)

    # Limpiar la pantalla
    screen.fill(BG_COLOR)  # Cambiar color de fondo

    # Dibujar todos los sprites en pantalla
    all_sprites.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
