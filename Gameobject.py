
"""
class Animat
class Food
class Grass
class Obstacle
"""

import pygame
import random
from constants import *
from helper_func import *

class GameObject(pygame.sprite.Sprite):
	PREDATOR_ID = 1
	PREY_ID = 2
	GRASS_ID = 3
	OBSTACLE_ID = 4
	FOOD_ID = 5
	def __init__(self, img, scale):
		pygame.sprite.Sprite.__init__(self)
		self.id = 0
		self.image = pygame.image.load(img).convert()
		self.image = pygame.transform.scale(self.image, scale)
		self.scale = scale[0]
		self.image.set_colorkey(Black)
		self.rect = self.image.get_rect()
		self.toRandomPosition()

	def get_rect(self):
		return self.rect

	def toRandomPosition(self):
		self.rect.center = randomPosition()
		overlap = False
		for i in range(0, len(initial_list)):
			if initial_list[i] != self and doRectsOverlap(self.rect, initial_list[i].rect):
				overlap = True
				break
		if overlap:
			self.toRandomPosition()

class Grass(GameObject):
	def __init__(self, img, scale):
		GameObject.__init__(self, img, scale)
		self.id = 3

class Obstacles(GameObject):
	def __init__(self, img, scale):
		GameObject.__init__(self, img, scale)
		self.id = 4
		self.image.set_colorkey(White)
		self.image.set_colorkey(Black)


class Food(GameObject):
	poison_eaten = 0
	normal_eaten = 0
	def __init__(self, img, scale, poison):
		GameObject.__init__(self, img, scale)
		self.id = 5
		self.image.set_colorkey(White)
		self.poison = poison


