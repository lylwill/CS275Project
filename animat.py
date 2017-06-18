from Gameobject import *
from constants import *
import random
from helper_func import *

class Action:
	actions = [0, 1, 2, 3]
	count = 4
	MOVE_UP = 0
	MOVE_LEFT = 1
	MOVE_DOWN = 2
	MOVE_RIGHT = 3

class Animat(GameObject):
	def __init__(self, img, scale, speed):
		GameObject.__init__(self, img, scale)
		self.xspd = speed
		self.yspd = speed
		self.brain = None
		self.energy = 0
		self.lastState = None
		self.lastAction = None
		self.lastPosition = self.rect.center

	def random_walk(self):
		r = random.randint(0, Action.count-1)
		self.perform_action(r)

	def calculateState(self):
		states = []
		for i in range(-2, 3):
			for j in range(-2, 3):
				x = self.rect.x + i * 10
				y = self.rect.y + j * 10
				collide = False
				for k in range(len(initial_list)):
					if isPointInsideRect(x, y, initial_list[k].rect):
						collide = True
						# print initial_list[k].id
						if initial_list[k].id == GameObject.PREDATOR_ID:
							states.append(1)
						elif initial_list[k].id == GameObject.PREY_ID:
							states.append(2)
						elif initial_list[k].id == GameObject.FOOD_ID:
							if initial_list[k].poison:
								states.append(3)
							else:
								states.append(4)
						elif initial_list[k].id == GameObject.OBSTACLE_ID:
							states.append(5)
						elif initial_list[k].id == GameObject.GRASS_ID:
							# print "find"
							states.append(6)
						else:
							# print initial_list[k].id
							states.append(7)
						break
				if not collide:
					states.append(0)
		# print tuple(states)
		return tuple(states)


	def perform_action(self, action):
		self.lastPosition = self.rect.center
		if action == Action.MOVE_UP:
			self.move_up()
		elif action == Action.MOVE_LEFT:
			self.move_left()
		elif action == Action.MOVE_DOWN:
			self.move_down()
		elif action == Action.MOVE_RIGHT:
			self.move_right()
		self.make_wrap_around()
		if self.isOnAnyObstacle():
			self.rect.center = self.lastPosition
			self.random_walk()


	def getObstacleTuple(self):
		sensors = []
		for dir in range(0, 4):
			sensors.append(self.senseClosestObstacle(dir))
		return tuple(sensors)

	def senseClosestObstacle(self, dir):
		dis = self.senseRange + 1
		for i in range(0, len(obstacle_list)):
			if self.inSensorDirection(obstacle_list[i].rect, dir):
				dis = min(dis, compDistance(self.rect, obstacle_list[i].rect))
		if dis > self.senseRange:
			return None
		else:
			return int(dis/10)

	def inSensorDirection(self, rect, dir):
		x_diff = 1 if rect.x >= self.rect.x else -1
		y_diff = 1 if rect.y > self.rect.y else -1
		new_dir = 0
		if x_diff == 1:
			if y_diff == 1:
				new_dir = 0
			else:
				new_dir = 1
		else:
			if y_diff == 1:
				new_dir = 2
			else:
				new_dir = 3
		return new_dir == dir

	def isOnAnyObstacle(self):
		for i in range(len(obstacle_list)):
			if doRectsOverlap(self.rect, obstacle_list[i].rect):
				return True
		return False

	def move_up(self):
		self.rect.y -= self.yspd

	def move_down(self):
		self.rect.y += self.yspd

	def move_left(self):
		self.rect.x -= self.xspd

	def move_right(self):
		self.rect.x += self.xspd

	def make_wrap_around(self):
		if (self.rect.left > WIDTH):
			self.rect.right = 0
		if (self.rect.right < 0):
			self.rect.left = WIDTH
		if (self.rect.bottom < 0):
			self.rect.top = HEIGHT
		if (self.rect.top > HEIGHT):
			self.rect.bottom = 0

	def avoid_obstacle(self):
		for i in range (0, len(obstacle_list)):
			if (doRectsOverlap(self.rect, obstacle_list[i].get_rect())):
				obs_rect = obstacle_list[i].get_rect()
				obs_center_x, obs_center_y = obs_rect.center
				avoid_dir = random.randint(1, 3)
				x_diff = obs_center_x - self.rect.x
				y_diff = obs_center_y - self.rect.y
				speed = abs(self.xspd)
				if (avoid_dir == 1):
					if (x_diff > 0):
						self.xspd = -1 * speed
					else:
						self.xspd = speed
				elif (avoid_dir == 2):
					if (y_diff > 0):
						self.yspd = -1 * speed
					else:
						self.yspd = speed
				else:
					if (x_diff > 0):
						self.xspd = -1 * speed
					else:
						self.xspd = speed
					if (y_diff > 0):
						self.yspd = -1 * speed
					else:
						self.yspd = speed
