import pygame
import random
from constants import *
from helper_func import *
from initialization import *

class simulation():
	def __init__(self, predator_learn, prey_learn):
		Pac_spd_flag = True
		Mon_spd_flag = True
		Pac_amt_flag = True
		Mon_amt_flag = True
		while (Pac_spd_flag):
			Pac_spd_input = raw_input("Please specify the Pac-Men' speed (h/m/l) :")
			#print(str(Pac_spd_input))
			if (str(Pac_spd_input) == "h"):
				Pac_spd = 50
				Pac_spd_flag = False
			elif(str(Pac_spd_input) == "m"):
				Pac_spd = 25
				Pac_spd_flag = False
			elif(str(Pac_spd_input) == "l"):
				Pac_spd = 10
				Pac_spd_flag = False
			else:
				print("Please choose either h or m or l")
		while (Mon_spd_flag):
			Pac_spd_input = raw_input("Please specify the Monsters' speed (h/m/l) :")
			if (str(Pac_spd_input) == "h"):
				Mon_spd = 50
				Mon_spd_flag = False
			elif(str(Pac_spd_input) == "m"):
				Mon_spd = 25
				Mon_spd_flag = False
			elif(str(Pac_spd_input) == "l"):
				Mon_spd = 10
				Mon_spd_flag = False
			else:
				print("Please choose either h or m or l")
		while (Pac_amt_flag):
			Pac_amt_input = raw_input("Please specify the Pac-Men' population (h/m/l) :")
			if (str(Pac_amt_input) == "h"):
				Pac_amt = 15
				Pac_amt_flag = False
			elif(str(Pac_amt_input) == "m"):
				Pac_amt = 10
				Pac_amt_flag = False
			elif(str(Pac_amt_input) == "l"):
				Pac_amt = 5
				Pac_amt_flag = False
			else:
				print("Please choose either h or m or l")
		while (Mon_amt_flag):
			Mon_amt_input = raw_input("Please specify the Monsters' population (h/m/l) :")
			if (str(Mon_amt_input) == "h"):
				Mon_amt = 15
				Mon_amt_flag = False
			elif(str(Mon_amt_input) == "m"):
				Mon_amt = 10
				Mon_amt_flag = False
			elif(str(Mon_amt_input) == "l"):
				Mon_amt = 5
				Mon_amt_flag = False
			else:
				print("Please choose either h or m or l")
		# initialize obstacles
		initialize_object(initial_list, obstacle_list, (20, 20), 20, 'obstacle')
		#initialize prey
		initialize_animats(initial_list, prey_list, (20, 20), Pac_amt, Pac_spd, 'prey')
		#initialize predator
		initialize_animats(initial_list, predator_list, (20, 20), Mon_amt, Mon_spd, 'predator')
		# initialize grass
		initialize_object(initial_list, grass_list, (20, 20), 20, 'grass')
		#intialize normal food
		initialize_object(initial_list, food_list, (20, 20), 50, 'normalfood')
		#initialize posion food
		initialize_object(initial_list, food_list, (20, 20), 50, 'poisonfood')
