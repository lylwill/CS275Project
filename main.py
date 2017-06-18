import pygame
from constants import *
from Gameobject import *
from simulation import *

# main function, control events


def main():
	pygame.init()
	pygame.mixer.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Animat-Based Modelling')
	clock = pygame.time.Clock()
	
	predator_learn = True
	prey_learn = True
	myfont = pygame.font.SysFont("monospace", 16)
	simulation(predator_learn, prey_learn)

	running = True

	while running:
		clock.tick(FPS)
		#process event
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		#update
		all_sprites.update()
		#draw
		screen.fill(Black)
		all_sprites.draw(screen)

		preytext = myfont.render("Number of Pac-Man Dead: {0}".format(Prey.death), 1, (255, 255, 255))
		screen.blit(preytext, (5, 10))
		predatortext = myfont.render("Number of Monster Dead: {0}".format(Predator.death), 1, (255, 255, 255))
		screen.blit(predatortext, (5, 30))
		posionfoodtext = myfont.render("Number of Poisonous Food Eaten: {0}".format(Food.poison_eaten), 1, (255, 255, 255))
		screen.blit(posionfoodtext, (5, 50))
		normalfoodtext = myfont.render("Number of Normal Food Eaten: {0}".format(Food.normal_eaten), 1, (255, 255, 255))
		screen.blit(normalfoodtext, (5, 70))


		pygame.display.flip()


	pygame.quit()


if __name__ == '__main__':
	main()