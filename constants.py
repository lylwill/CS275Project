import os
import pygame
WIDTH = 900
HEIGHT = 600
FPS = 30

Red = (255, 0, 0)
Blue = (0, 0, 255)
Black = (0, 0, 0)
White = (255, 255, 255)
Green = (0, 255, 0)
Cyan = (0, 255, 200)
Lightblue = (200, 200, 255)
Orange = (255, 102, 0)

texture_folder = os.path.dirname(__file__)
dirname = os.path.join(texture_folder, "PacmanTiles")
prey_path = os.path.join(dirname, "pmup.png")
prey_path_down = os.path.join(dirname, "pmdown.png")
prey_path_left = os.path.join(dirname, "pmleft.png")
prey_path_right = os.path.join(dirname, "pmright.png")
predator_path = os.path.join(dirname, "mup.png")
predator_path_down = os.path.join(dirname, "mdown.png")
predator_path_left = os.path.join(dirname, "mleft.png")
predator_path_right = os.path.join(dirname, "mright.png")
grass_path = os.path.join(dirname, "grass.png")
obstacle_path = os.path.join(dirname, "rock.png")
normal_food_path = os.path.join(dirname, "normalfood.png")
poison_food_path = os.path.join(dirname, "poisonfood.png")

initial_list = []
grass_list = []
obstacle_list = []
prey_list = []
predator_list = []
food_list = []
prey_death = 0
predator_death = 0
normal_food_eaten = 0
posion_food_eaten = 0


all_sprites = pygame.sprite.Group()
