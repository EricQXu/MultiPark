"""
https://www.youtube.com/watch?v=-8n91btt5d8
https://www.youtube.com/watch?v=NjvIooRpuH4
https://www.pygame.org/docs/
"""
import pygame #imports pygame module into project (1)
import random

Alpha = 1
Beta = 1
Gamma = 10

class Car:
	def __init__(self, x, y, sprite_path):
		self.x = x
		self.y = y
		raw_sprite = pygame.image.load(sprite_path)
		self.width = 50
		self.height = 100
		self.sprite = pygame.transform.scale(raw_sprite, (self.width, self.height))
		self.max_speed = 5
		self.acceleration = 1
		self.velocity = 0

	def accelerate(self):
		self.velocity = min(self.velocity+self.acceleration, self.max_speed)

	def decelerate(self):
		self.velocity = max(0, self.velocity-self.acceleration)

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_width(self):
		return self.width

	def get_hieght(self):
		return self.height

	def get_velocity(self):
		return self.velocity

	def draw(self, display):
		display.blit(self.sprite, (int(self.x), int(self.y)))

class Spot:
	def __init__(self, x, y, sprite_path):
		self.x = x
		self.y = y
		raw_sprite = pygame.image.load(sprite_path)
		self.width = 50
		self.height = 100
		self.sprite = pygame.transform.scale(raw_sprite, (self.width, self.height))

	def set_x(self, x):
		self.x = x

	def set_y(self, y):
		self.y = y

	def get_x(self):
		return self.x

	def get_y(self):
		return self.y

	def get_width(self):
		return self.width

	def get_hieght(self):
		return self.height

	def draw(self, display):
		display.blit(self.sprite, (int(self.x), int(self.y)))


def create_level(level_paths, playerPath1, playerPath2, spotPath, parkedPaths):
	'''
	:param level_path: path to level file
	:return: parked_cars: list of "Car" objects, parking_spot: list of "Spot" objects
	'''
	# create game state
	level_paths = ['level1.txt', 'level2.txt', 'level3.txt', 'level4.txt', 'level5.txt']
	level_path = level_paths[int(random.random()*len(level_paths))]
	level_file = open(level_path, 'r+') #opens level1 using file handler
	car_list = []
	spot_list = []
	lines = level_file.readlines()
	level_file.close()
	row_num = 0
	for line in lines:
		col_num = 0
		for symbol in line:
			# turn row_num and col_num into x and y
			x = (800.0/18)*col_num
			y = (600.0/6)*row_num

			parkedPath = parkedPaths[int(random.random()*len(parkedPaths))]
			if symbol == 'w':
				spot_list.append(Spot(x, y, spotPath))
			if symbol == 'x':
				car_list.append(Car(x, y, parkedPath))

			col_num += 1
		row_num += 1

	car1 = Car(550, 300, playerPath1)
	car2 = Car(200, 300, playerPath2)

	return car1, car2, car_list, spot_list

def update_game_state(car1, car2, parked_cars, keys):
	'''
	:param car1: player 1's car
	:param car2: player 2's car
	:param parked_cars: list of "Car" objects
	:param parking_spots: list of "Spot" objects
	:return: nothing
	'''
	# Update car1's and car 2's locations
	#PLAYER1_MOVEMENT
	x1 = car1.get_x()
	y1 = car1.get_y()
	x2 = car2.get_x()
	y2 = car2.get_y()

	#PLAYER1_MOVEMENT
	if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN] or keys[pygame.K_UP]:
		car1.accelerate()
		velocity = car1.get_velocity()
		if keys[pygame.K_LEFT]:
			x1 -= velocity #Move left
		if keys[pygame.K_RIGHT]:
			x1 += velocity #Move right
		if keys[pygame.K_DOWN]:
			y1 += velocity #Move down
		if keys[pygame.K_UP]:
			y1 -= velocity #Move up
	else:
		car1.decelerate()

	if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s] or keys[pygame.K_w]:
		car2.accelerate()
		velocity = car2.get_velocity()
		if keys[pygame.K_a]:
			x2 -= velocity #Move left
		if keys[pygame.K_d]:
			x2 += velocity #Move right
		if keys[pygame.K_s]:
			y2 += velocity #Move down
		if keys[pygame.K_w]:
			y2 -= velocity #Move up
	else:
		car2.decelerate()


	# if event.key == pygame.K_LEFT:
	# 	x1 -= 2 #Move left
	# elif event.key == pygame.K_RIGHT:
	# 	x1 += 2 #Move right
	#
	# if event.key == pygame.K_DOWN:
	# 	y1 += 2 #Move down
	# elif event.key == pygame.K_UP:
	# 	y1 -= 2 #Move up
	# #PLAYER2_MOVEMENT
	# if event.key == pygame.K_a:
	# 	x2 -= 2 #Move left
	# elif event.key == pygame.K_d:
	# 	x2 += 2 #Move right
	#
	# if event.key == pygame.K_s:
	# 	y2 += 2 #Move down
	# elif event.key == pygame.K_w:
	# 	y2 -= 2 #Move up

	# collision detection
	#x1 is player x and parked_car.get_x is the x-coor of parked car
	update_car1 = True
	update_car2 = True
	for parked_car in parked_cars:
		error = 5
		pcwh = parked_car.get_width()/2 - error
		pchh = parked_car.get_hieght()/2 - error
		c1wh = car1.get_width()/2 - error
		c1hh = car1.get_hieght()/2 - error
		c2wh = car2.get_width()/2 - error
		c2hh = car2.get_hieght()/2 - error
		global Beta

		# car 1
		if (x1+c1wh >= parked_car.get_x()-pcwh and x1+c1wh <= parked_car.get_x()+pcwh) or \
				(x1-c1wh >= parked_car.get_x()-pcwh and x1-c1wh <= parked_car.get_x()+pcwh):
			x_ovl = True
		else:
			x_ovl = False

		if (y1 + c1hh >= parked_car.get_y() - pchh and y1 + c1hh <= parked_car.get_y() + pchh) or \
				(y1 - c1hh >= parked_car.get_y() - pchh and y1 - c1hh <= parked_car.get_y() + pchh):
			y_ovl = True
		else:
			y_ovl = False

		if x_ovl and y_ovl:
			update_car1 = False

		# car 2
		if (x2 + c2wh >= parked_car.get_x() - pcwh and x2 + c2wh <= parked_car.get_x() + pcwh) or \
				(x2 - c2wh >= parked_car.get_x() - pcwh and x2 - c2wh <= parked_car.get_x() + pcwh):
			x_ovl = True
		else:
			x_ovl = False

		if (y2 + c2hh >= parked_car.get_y() - pchh and y2 + c2hh <= parked_car.get_y() + pchh) or \
				(y2 - c2hh >= parked_car.get_y() - pchh and y2 - c2hh <= parked_car.get_y() + pchh):
			y_ovl = True
		else:
			y_ovl = False

		if x_ovl and y_ovl:
			update_car2 = False

		if (x1 + c1wh >= x2 - c2wh and x1 + c1wh <= x2 + c2wh) or \
				(x1 - c1wh >= x2 - c2wh and x1 - c1wh <= x2 + c2wh):
			x_ovl = True
		else:
			x_ovl = False

		if (y2 + c2hh >= y1 - c1hh and y2 + c2hh <= y1 + c1hh) or \
				(y2 - c2hh >= y1 - c1hh and y2 - c2hh <= y1 + c1hh):
			y_ovl = True
		else:
			y_ovl = False

		if x_ovl and y_ovl:
			update_car1 = False
			update_car2 = False

	# check borders
	if (x1 >= 800 or x1 <= 0) or (y1 >= 600 or y1 <= 0):
		update_car1 = False
	if (x2 >= 800 or x2 <= 0) or (y2 >= 600 or y2 <= 0):
		update_car2 = False

	if update_car1:
		car1.set_x(x1)
		car1.set_y(y1)
	if update_car2:
		car2.set_x(x2)
		car2.set_y(y2)

def draw_game_state(display, car1, car2, parked_cars, parking_spots):
	'''
	:param display: display of pygame
	:param car1: player 1's car
	:param car2: player 2's car
	:param parked_cars: list of "Car" objects
	:param parking_spots: list of "Spot" objects
	:return: nothing
	'''
	# draw cars and co. on the pygame display
	display.fill((100,255,100))
	for parking_spot in parking_spots:
		parking_spot.draw(display)
	for parked_car in parked_cars:
		parked_car.draw(display)
	car1.draw(display)
	car2.draw(display)

	"""
		display.fill(bgcolor) # See vid (11)
		pygame.draw.rect(display, color1, (player_pos1[0], player_pos1[1], player_size1, player_size1)) #Draws Rectangle1 (8)
		pygame.draw.rect(display, color2, (player_pos2[0], player_pos2[1], player_size2, player_size2)) #Draws Rectangle2 (8)
	"""

def check_win_condition(car1, car2, parking_spots):
	'''
	:param car1: player 1's car
	:param car2: player 2's car
	:param parking_spots: list of "Spot" objects
	:return: player_win: integer variable that stores the state of win_condition
				player_win = -1 -> no one has won yet
				player_win = 1 -> player 1 won
				player_win = 2 -> player 2 won
	'''
	# TODO: Eric fill this in

	# player_win = variable that stores the state of win_condition
	#   player_win = -1 -> no one has won yet
	#   player_win = 1 -> player 1 won
	#   player_win = 2 -> player 2 won
	x1 = car1.get_x()
	y1 = car1.get_y()
	x2 = car2.get_x()
	y2 = car2.get_y()

	win_car1 = False
	win_car2 = False

	for parking_spot in parking_spots:
		global Gamma
		if (x1 >= parking_spot.get_x() - Gamma and x1<= parking_spot.get_x() + Gamma) and (y1>=parking_spot.get_y() - Gamma and y1<=parking_spot.get_y() + Gamma):
			win_car1 = True
		if (x2 >= parking_spot.get_x() - Gamma and x2<= parking_spot.get_x() + Gamma) and (y2>=parking_spot.get_y() - Gamma and y2<=parking_spot.get_y() + Gamma):
			win_car2 = True

	if win_car1:
		player_win = 1
	elif win_car2:
		player_win = 2
	else:
		player_win = -1

	if player_win == -1:
		print("No one wins :(")

	if player_win == 1:
		print("Player 1 won!")

	if player_win == 2:
		print("Player 2 won!")

	# check if x,y locations of EITHER car1 OR car2 satisfy win condition.
	return player_win

def draw_victory_screen(player_win, display):
	'''
	:param player_win: integer variable that stores the state of win_condition
				player_win = -1 -> no one has won yet
				player_win = 1 -> player 1 won
				player_win = 2 -> player 2 won
	:return: nothing
	'''
	# TODO: Eric fill this in LAST (THIS DOES NOT MATTER AS MUCH AS THE OTHER FUNCTIONS)

	noonewin = pygame.image.load(r'noonewin.png')
	player1win = pygame.image.load(r'player1win.png')
	player2win = pygame.image.load(r'player2win.png')
	if player_win == -1:
		display.blit(noonewin, (int(0), int(0)))
	elif player_win == 1:
		display.blit(player1win, (int(0), int(0)))
	elif player_win == 2:
		display.blit(player2win, (int(0), int(0)))
	# displays victory screen for player who won (or if no one wins)


def main():
	pygame.init()  # intilialize pygame (2)

	bgcolor = (0, 0, 0)
	W = 800  # Window Width
	H = 600  # Window Height

	pygame.display.set_caption('MultiPark v.1.0')
	icon = pygame.image.load('icon.png')
	pygame.display.set_icon(icon)
	clock = pygame.time.Clock()

	display = pygame.display.set_mode((W, H))  # Makes a window (3)

	game_over = False  # initializes game is not over (4)

	playerPath1 = 'player.png'
	playerPath2 = 'player.png'
	spotPath = 'spot.png'
	parkedPaths = ['Accord.png', 'Cybertruck.png', 'Mustang.png', 'Toyota_Corolla.png']
	level_paths = ['level1.txt']

	# Keep running until game is over (5)
	while not game_over:
		player_win = -1
		level_over = False
		victory_over = False
		car1, car2, parked_cars, parking_spots = create_level(level_paths, playerPath1, playerPath2, spotPath, parkedPaths)
		while not level_over:
			for event in pygame.event.get():  # Collects the user mouse and keybrd movemnt (6)
				if event.type == pygame.QUIT:  # Use X button to quit (7)
					# sys.exit()
					victory_over = True
					level_over = True
					game_over = True

			keys = pygame.key.get_pressed()
			update_game_state(car1, car2, parked_cars, keys)

			# draw the change in position
			draw_game_state(display, car1, car2, parked_cars, parking_spots)

			# Did any car successfully park?
			# player_win = variable that stores the state of win_condition
			#   player_win = -1 -> no one has won yet
			#   player_win = 1 -> player 1 won
			#   player_win = 2 -> player 2 won
			player_win = check_win_condition(car1, car2, parking_spots)
			if player_win != -1:
				level_over = True

			pygame.display.update()  # update screen evry iteration (9)
			clock.tick(60)  # 60 FPS

		while not victory_over:
			for event in pygame.event.get():  # Collects the user mouse and keybrd movemnt (6)
				if event.type == pygame.QUIT:  # Use X button to quit (7)
					# sys.exit()
					victory_over = True
					game_over = True
				if event.type == pygame.KEYDOWN:
					victory_over = True

			# player_win = variable that stores the state of win_condition
			#   player_win = -1 -> no one has won yet
			#   player_win = 1 -> player 1 won
			#   player_win = 2 -> player 2 won
			draw_victory_screen(player_win, display)

			pygame.display.update()  # update screen evry iteration (9)
			clock.tick(60)  # 60 FPS

		# clock.tick(1000)  # 60 FPS

	pygame.quit()
	quit()

if __name__ == '__main__':
	main()

