from animat import *
import random
import pygame
from constants import *
from helper_func import *
from prey import *
import numpy as np
from qlearning import qlearning
from RL import *
from sarsa import sarsa


class Predator(Animat):
	death = 0
	def __init__(self, img, scale, speed, learning):
		Animat.__init__(self, img, scale, speed)
		self.id = 1
		self.energy_level = 2000
		self.senseRange = self.scale * 2
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
			Predator.death += 1
			if self.lastState is not None:
				if self.learning == RL.QLearn:
					self.brain.learn(self.lastState, self.lastAction, reward, state)
				elif self.learning == RL.SARSA:
					self.brain.learn(self.lastState, self.lastAction, reward, state, action)
			self.reset()
			# print "One Predator died because of running out of energy"
			return
		elif self.isOnAnyPrey():
			reward += 50
			self.energy_level += 50

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
			self.image = pygame.image.load(predator_path).convert()
			self.image = pygame.transform.scale(self.image, scale)
		elif action == Action.MOVE_LEFT:
			self.image = pygame.image.load(predator_path_left).convert()
			self.image = pygame.transform.scale(self.image, scale)
		elif action == Action.MOVE_DOWN:
			self.image = pygame.image.load(predator_path_down).convert()
			self.image = pygame.transform.scale(self.image, scale)
		elif action == Action.MOVE_RIGHT:
			self.image = pygame.image.load(predator_path_right).convert()
			self.image = pygame.transform.scale(self.image, scale)

	def reset(self):
		self.lastState = None
		self.lastAction = None
		self.energy_level = 2000
		self.toRandomPosition()
		self.lastPosition = self.rect.center

	def isOnAnyPrey(self):
		for i in range(len(prey_list)):
			if doRectsOverlap(self.rect, prey_list[i].rect):
				return True
		return False

	def getPreyTuple(self):
		sensors = []
		for dir in range(0, 4):
			sensors.append(self.senseClosestPrey(dir))
		return tuple(sensors)

	def senseClosestPrey(self, dir):
		dis = self.senseRange + 1
		for i in range(0, len(prey_list)):
			if self.inSensorDirection(prey_list[i].rect, dir):
				dis = min(dis, compDistance(self.rect, prey_list[i].rect))
		if dis > self.senseRange:
			return None
		else:
			return int(dis/10)


	def sensor(self):
		cur_rect = self.rect
		sense_rect = cur_rect.inflate(self.scale * 4, self.scale * 4)
		return sense_rect

	def walk(self):
		#change y
		self.energy_level = self.energy_level - 1
		if (random.uniform(0,1) >0.1):
			self.rect.y += self.yspd
		else:
			self.yspd = self.yspd * -1
		#change x
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

	def chase_prey(self):
		for i in range (0, len(prey_list)):
			sense_rect = self.sensor()
			min_dis = np.sqrt(self.scale * 4 * self.scale * 4 * 2)
			target_x = 0
			target_y = 0
			if (doRectsOverlap(sense_rect, prey_list[i].get_rect())):
				prey_rect = prey_list[i].get_rect()
				prey_center_x, prey_center_y = prey_rect.center
				x_diff = prey_center_x - self.rect.x
				y_diff = prey_center_y - self.rect.y
				if (np.sqrt(x_diff * x_diff + y_diff * y_diff) < min_dis):
					min_dis = np.sqrt(x_diff * x_diff + y_diff * y_diff)
					target_x = prey_center_x
					target_y = prey_center_y
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
				



	def kill_prey(self):
		for i in range (0, len(prey_list)):
			if (doRectsOverlap(self.rect, prey_list[i].get_rect())):
				killed_prey = prey_list[i]
				self.energy_level = killed_prey.energy_level * 0.1 + self.energy_level
				prey_list.remove(killed_prey)
				all_sprites.remove(killed_prey)
				initial_list.remove(killed_prey)
				overlap = False
				while True:
					prey = Prey(prey_path, (20, 20), 2)
					for j in range (0, len(initial_list)):
						if (doRectsOverlap(prey.get_rect(), initial_list[j].get_rect())):
							overlap = True
							break
					if (overlap):
						overlap = False
						continue
					else:
						prey_list.append(prey)
						all_sprites.add(prey)
						initial_list.append(prey)
						break








