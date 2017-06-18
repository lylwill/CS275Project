from animat import *
from predator import *
import random
import pygame
from constants import *
from simulation import *
from helper_func import *
from Gameobject import *
import numpy as np
from qlearning import qlearning
from sarsa import sarsa
from RL import *


class Prey(Animat):
	death = 0
	def __init__(self, img, scale, speed, learning):
		Animat.__init__(self, img, scale, speed)
		self.id = 2
		self.energy_level = 1000
		self.senseRange = self.scale * 10
		self.learning = learning
		if learning == RL.QLearn:
			self.brain = qlearning(actions=Action.actions, epsilon=0)
		elif learning == RL.SARSA:
			self.brain = sarsa(actions=Action.actions, epsilon=0)
		else:
			self.brain = None

	def update(self):
		state = self.calculateState()
		action = None
		if self.learning == RL.SARSA:
			action = self.brain.choose_action(state)
		reward = -1
		self.energy_level -= 1
		if self.energy_level == 0:
			Prey.death += 1
			if self.lastState is not None:
				if self.learning == RL.QLearn:
					self.brain.learn(self.lastState, self.lastAction, reward, state)
				elif self.learning == RL.SARSA:
					self.brain.learn(self.lastState, self.lastAction, reward, state, action)
			self.reset()
			# print "One Prey died because of running out of energy"
			return
		elif self.isOnAnyPredator():
			Prey.death += 1
			reward -= 50
			if self.lastState is not None:
				if self.learning == RL.QLearn:
					self.brain.learn(self.lastState, self.lastAction, reward, state)
				elif self.learning == RL.SARSA:
					self.brain.learn(self.lastState, self.lastAction, reward, state, action)
			self.reset()
			# print "One Prey died because of eaten by a predator"
		
		if self.isOnAnyFood():
			for i in range(len(food_list)):
				if doRectsOverlap(self.rect, food_list[i].rect):
					if food_list[i].poison:
						Food.poison_eaten += 1
						reward -= 30
						self.energy_level -= 10
					else:
						Food.normal_eaten += 1
						reward += 20
						self.energy_level += 10
					food_list[i].toRandomPosition()
		elif self.isOnAnyGrass():
			reward += 20
			self.energy_level += 5

		if self.learning == RL.QLearn:
			if self.lastState is not None:
				self.brain.learn(self.lastState, self.lastAction, reward, state)

			state = self.calculateState()
			action = self.brain.choose_action(state)
		elif self.learning == RL.SARSA:
			if self.lastState is not None:
				self.brain.learn(self.lastState, self.lastAction, reward, state, action)
		else:
			self.random_walk()
			return

		self.lastState = state
		self.lastAction = action
		self.changesprite(action, (20, 20))
		self.perform_action(action)

	def changesprite(self, action, scale):
		if action == Action.MOVE_UP:
			self.image = pygame.image.load(prey_path).convert()
			self.image = pygame.transform.scale(self.image, scale)
		elif action == Action.MOVE_LEFT:
			self.image = pygame.image.load(prey_path_left).convert()
			self.image = pygame.transform.scale(self.image, scale)
		elif action == Action.MOVE_DOWN:
			self.image = pygame.image.load(prey_path_down).convert()
			self.image = pygame.transform.scale(self.image, scale)
		elif action == Action.MOVE_RIGHT:
			self.image = pygame.image.load(prey_path_right).convert()
			self.image = pygame.transform.scale(self.image, scale)

	def reset(self):
		self.lastState = None
		self.lastAction = None
		self.energy_level = 1000
		self.toRandomPosition()
		self.lastPosition = self.rect.center

	def isOnAnyPredator(self):
		for i in range(len(predator_list)):
			if doRectsOverlap(self.rect, predator_list[i].rect):
				return True
		return False

	def isOnAnyFood(self):
		for i in range(len(food_list)):
			if doRectsOverlap(self.rect, food_list[i].rect):
				return True
		return False

	def isOnAnyGrass(self):
		for i in range(len(grass_list)):
			if doRectsOverlap(self.rect, grass_list[i].get_rect()):
				return True
		return False

	def hasPredatorNearby(self):
		dis = 50
		for i in range(len(predator_list)):
			if compDistance(self.rect, predator_list[i].rect) <= 40:
				return True
		return False

	def hasPoisonFoodNearby(self):
		for i in range(len(food_list)):
			if food_list[i].poison and compDistance(self.rect, food_list[i].rect) <= 40:
				return True
		return False

	def hasNormalFoodNearby(self):
		for i in range(len(food_list)):
			if not food_list[i].poison and compDistance(self.rect, food_list[i].rect) <= 40:
				return True
		return False

	def hasGrassNearby(self):
		for i in range(len(grass_list)):
			if compDistance(self.rect, grass_list[i].rect) <=40:
				return True
		return False


	def getNormalFoodTuple(self):
		sensors = []
		for dir in range(0, 4):
			sensors.append(self.senseClosestNormalFood(dir))
		return tuple(sensors)

	def getPoisonFoodTuple(self):
		sensors = []
		for dir in range(0, 4):
			sensors.append(self.senseClosestPoisonFood(dir))
		return tuple(sensors)

	def getGrassTuple(self):
		sensors = []
		for dir in range(0, 4):
			sensors.append(self.senseClosestGrass(dir))
		return tuple(sensors)

	def getPredatorTuple(self):
		sensors = []
		for dir in range(0, 4):
			sensors.append(self.senseClosestPredator(dir))
		return tuple(sensors)


	def senseClosestNormalFood(self, dir):
		dis = self.senseRange + 1
		for i in range(0, len(food_list)):
			if not food_list[i].poison and self.inSensorDirection(food_list[i].rect, dir):
				dis = min(dis, compDistance(self.rect, food_list[i].rect))
		if dis > self.senseRange:
			return None
		else:
			return int(dis/10)


	def senseClosestPoisonFood(self, dir):
		dis = self.senseRange + 1
		for i in range(0, len(food_list)):
			if food_list[i].poison and self.inSensorDirection(food_list[i].rect, dir):
				dis = min(dis, compDistance(self.rect, food_list[i].rect))
		if dis > self.senseRange:
			return None
		else:
			return int(dis/10)

	def senseClosestGrass(self, dir):
		dis = self.senseRange + 1
		for i in range(0, len(grass_list)):
			if self.inSensorDirection(grass_list[i].rect, dir):
				dis = min(dis, compDistance(self.rect, grass_list[i].rect))

		if dis > self.senseRange:
			return None
		else:
			return int(dis/10)

	def senseClosestPredator(self, dir):
		dis = self.senseRange + 1
		predator = None
		for i in range(0, len(predator_list)):
			if self.inSensorDirection(predator_list[i].rect, dir):
				dis = min(dis, compDistance(self.rect, predator_list[i].rect))
		if dis > self.senseRange:
			return None
		else:
			return int(dis/10)

	def sensor(self):
		cur_rect = self.rect
		sense_rect = cur_rect.inflate(self.scale * 2, self.scale * 2)
		return sense_rect

	def walk(self):
		self.energy_level = self.energy_level - 1
		if (random.uniform(0,1) >0.1):
			self.rect.y += self.yspd
		else:
			self.yspd = self.yspd * -1
		if (random.uniform(0,1) > 0.1):
			self.rect.x += self.xspd
		else:
			self.xspd = self.xspd * -1

	def make_wrap_around(self):
		if (self.rect.left > WIDTH):
			self.rect.right = 0
		if (self.rect.right < 0):
			self.rect.left = WIDTH
		if (self.rect.bottom < 0):
			self.rect.top = HEIGHT
		if (self.rect.top > HEIGHT):
			self.rect.bottom = 0

	def search_food(self):
		for i in range (0, len(food_list)):
			sense_rect = self.sensor()
			min_dis = np.sqrt(self.scale * 2 * self.scale * 2 * 2)
			target_x = 0
			target_y = 0
			if (doRectsOverlap(sense_rect, food_list[i].get_rect())):
				food_rect = food_list[i].get_rect()
				food_center_x, food_center_y = food_rect.center
				x_diff = food_center_x - self.rect.x
				y_diff = food_center_y - self.rect.y
				if (np.sqrt(x_diff * x_diff + y_diff * y_diff) < min_dis):
					min_dis = np.sqrt(x_diff * x_diff + y_diff * y_diff)
					target_x = food_center_x
					target_y = food_center_y
					new_x_diff = target_x - self.rect.x
					new_y_diff = target_y - self.rect.y
					speed = abs(self.xspd)
					if (new_x_diff > 0):
						self.xspd = speed
					else:
						self.xspd = -1 * speed
					if (new_y_diff > 0):
						self.yspd = speed
					else:
						self.yspd = -1 * speed

	def eat_food(self):
		for i in range (0, len(food_list)):
			if (doRectsOverlap(self.rect, food_list[i].get_rect())):
				eaten_food = food_list[i]
				if (eaten_food.poison):
					self.energy_level = self.energy_level - 100
					self.xspd = self.xspd / 2
					self.yspd = self.yspd / 2
					food_list.remove(eaten_food)
					all_sprites.remove(eaten_food)
					initial_list.remove(eaten_food)
					overlap = False
					while True:
						food = Food(poison_food_path, (20, 20), True)
						for j in range (0, len(initial_list)):
							if (doRectsOverlap(food.get_rect(), initial_list[j].get_rect())):
								overlap = True
								break
						if (overlap):
							overlap = False
							continue
						else:
							food_list.append(food)
							all_sprites.add(food)
							initial_list.append(food)
							break
				else:
					self.energy_level = self.energy_level + 100
					food_list.remove(eaten_food)
					all_sprites.remove(eaten_food)
					initial_list.remove(eaten_food)
					overlap = False
					while True:
						food = Food(normal_food_path, (20, 20), False)
						for j in range (0, len(initial_list)):
							if (doRectsOverlap(food.get_rect(), initial_list[j].get_rect())):
								overlap = True
								break
						if (overlap):
							overlap = False
							continue
						else:
							food_list.append(food)
							all_sprites.add(food)
							initial_list.append(food)
							break





