# music.py
import pygame

class Music:
    def __init__(self):
        self.background_music = pygame.mixer.Sound('space.wav')

    def play_background_music(self):
        self.background_music.play(-1)  # Repetir la música indefinidamente

    def stop_background_music(self):
        self.background_music.stop()

