from prey import Prey
from predator import Predator
from Gameobject import *
from constants import *
from helper_func import *
from RL import *

def initialize_animats(initial_list, object_list, scale, number, speed, kind):
	for i in range(0, number):
		if (kind == 'prey'):
			animat = Prey(prey_path, scale, speed, RL.QLearn)
			overlap = False
			for j in range (0, len(initial_list)):
				if (doRectsOverlap(animat.get_rect(), initial_list[j].get_rect())):
					overlap = True
					break
			if (overlap):
				i = i - 1
			else:
				object_list.append(animat)
				all_sprites.add(animat)
				initial_list.append(animat)
		else:
			animat = Predator(predator_path, scale, speed, RL.QLearn)
			overlap = False
			for j in range (0, len(initial_list)):
				if (doRectsOverlap(animat.get_rect(), initial_list[j].get_rect())):
					overlap = True
					break
			if (overlap):
				i = i - 1
			else:
				object_list.append(animat)
				all_sprites.add(animat)
				initial_list.append(animat)

def initialize_object(initial_list, object_list, scale, number, kind):
	for i in range(0, number):
		if (kind == 'grass'):
			objects = Grass(grass_path, scale)
			overlap = False
			for j in range (0, len(initial_list)):
				if (doRectsOverlap(objects.get_rect(), initial_list[j].get_rect())):
					overlap = True
					break
			if (overlap):
				i = i - 1
			else:
				object_list.append(objects)
				all_sprites.add(objects)
				initial_list.append(objects)
		elif(kind == 'obstacle'):
			objects = Obstacles(obstacle_path, scale)
			overlap = False
			for j in range (0, len(initial_list)):
				if (doRectsOverlap(objects.get_rect(), initial_list[j].get_rect())):
					overlap = True
					break
			if (overlap):
				i = i - 1
			else:
				object_list.append(objects)
				all_sprites.add(objects)
				initial_list.append(objects)
		elif(kind == 'normalfood'):
			objects = Food(normal_food_path, scale, False)
			overlap = False
			for j in range (0, len(initial_list)):
				if (doRectsOverlap(objects.get_rect(), initial_list[j].get_rect())):
					overlap = True
					break
			if (overlap):
				i = i - 1
			else:
				object_list.append(objects)
				all_sprites.add(objects)
				initial_list.append(objects)
		elif(kind == 'poisonfood'):
			objects = Food(poison_food_path, scale, True)
			overlap = False
			for j in range (0, len(initial_list)):
				if (doRectsOverlap(objects.get_rect(), initial_list[j].get_rect())):
					overlap = True
					break
			if (overlap):
				i = i - 1
			else:
				object_list.append(objects)
				all_sprites.add(objects)
				initial_list.append(objects)