import random
from constants import *
import pygame

def doRectsOverlap(rect1, rect2):
	return rect1.colliderect(rect2) or rect2.colliderect(rect1)
	# for a, b in [(rect1, rect2), (rect2, rect1)]:
	# 	if ((isPointInsideRect(a.left, a.top, b)) or\
	# 		(isPointInsideRect(a.left, a.bottom, b)) or\
	# 		(isPointInsideRect(a.right, a.top, b)) or\
	# 		(isPointInsideRect(a.right, a.bottom, b))):
	# 		return True
	# return False

def isPointInsideRect(x, y, rect):
	if (x > rect.left) and (x < rect.right) and (y > rect.top) and (y < rect.bottom):
		return True
	else:
		return False


def compDistance(rect1,  rect2):
	x_diff = abs(rect1.x - rect2.x)
	x_diff = min(x_diff, WIDTH - x_diff)
	y_diff = abs(rect1.y - rect2.y)
	y_diff = min(y_diff, HEIGHT - y_diff)
	return (x_diff ** 2 + y_diff ** 2) ** 0.5

def randomPosition():
	randX = random.randint(0, WIDTH)
	randY = random.randint(0, HEIGHT)
	return (randX, randY)