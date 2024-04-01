import pygame
import sys

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
        self.rect = self.image.get_rect()
        self.speed = 5  # Velocidad de movimiento

    def create_sprite(self, design, color, scale):
        sprite_width = len(design[0])
        sprite_height = len(design)
        sprite_surface = pygame.Surface((sprite_width * scale, sprite_height * scale))
        sprite_surface.fill(BG_COLOR)  # Cambiar color de fondo

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
            "*****",
            "*   *",
            "*   *",
            "*   *",
            "*****"
        ]
        sprite_width = len(sprite_design[0])
        sprite_height = len(sprite_design)
        sprite_surface = pygame.Surface((sprite_width * scale, sprite_height * scale))
        sprite_surface.fill(BG_COLOR)  # Cambiar color de fondo

        for y, row in enumerate(sprite_design):
            for x, char in enumerate(row):
                if char == '*':
                    pygame.draw.rect(sprite_surface, color, (x * scale, y * scale, scale, scale))

        return sprite_surface

# Crear un grupo de sprites
all_sprites = pygame.sprite.Group()

# Crear enemigos y agregarlos al grupo
EN_total = 8  # Número total de enemigos
for i in range(EN_total):
    x = SCREEN_WIDTH / (EN_total / 1.5) + (i * 70)
    enemy = Enemy((220, 0, 30), 10, x, 50)  # Color rojo y escala de 10
    all_sprites.add(enemy)

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

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar lógica del juego
    all_sprites.update()

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
