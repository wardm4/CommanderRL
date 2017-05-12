import pygame
import libtcodpy as rogue
import constants
import random

#STRUCTS

class Tile:

	def __init__(self, block_path = None, resource = None):
		self.block_path = False
		self.resource = resource


#OBJECTS

class Actor:

	def __init__(self, x, y, sprite, hp = 10):
		self.x = x
		self.y = y
		self.sprite = sprite
		self.hp = hp

	def draw(self):
		SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

	def move(self, dx, dy):
		if (GAME_MAP[self.x + dx][self.y + dy].block_path == False) and (self.x < constants.MAP_WIDTH - 1):
			self.x += dx
			self.y += dy


class Information:

	def __init__(self, res_list = [0,0,0], money = [0,0,0], time = 0, actions = 3, workers = 0, fov = True, coin = 4, which_menu = 0, terra = 0):
		self.res_list = res_list
		self.money = money
		self.time = time
		self.actions = actions
		self.workers = workers
		self.fov = fov
		self.coin = coin
		self.which_menu = which_menu
		self.terra = terra



#COMPONONENTS

class Building:

	def __init__(self, x, y, sprite, mine, hp = 10, res = [0,0,0]):
		self.x = x
		self.y = y
		self.mine = mine
		self.hp = hp
		self.sprite = sprite

	def draw(self):
		SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))


#MAP

def map_create():
	new_map = [[ Tile() for y in range(0, constants.MAP_HEIGHT)] for x in range(0, constants.MAP_WIDTH) ]

	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):
			dumb = random.random()
			if dumb < 0.15:
				new_map[x][y].resource = "wheat"
			elif dumb > 0.25 and dumb < 0.35:
				new_map[x][y].resource = "ore"
			elif dumb > 0.4 and dumb < 0.42:
				new_map[x][y].resource = "diamond"
			elif dumb > 0.9:
				new_map[x][y].resource = "rock"
				new_map[x][y].block_path = True
			else:
				new_map[x][y].resource = "floor"

	for x in range(0, constants.MAP_WIDTH):
		new_map[x][0].resource = "rock"
		new_map[x][constants.MAP_HEIGHT - 1].resource = "rock"
		new_map[x][0].block_path = True
		new_map[x][constants.MAP_HEIGHT - 1].block_path = True

	for y in range(0, constants.MAP_HEIGHT):
		new_map[0][y].resource = "rock"
		new_map[constants.MAP_WIDTH - 1][y].resource = "rock"
		new_map[0][y].block_path = True
		new_map[constants.MAP_WIDTH - 1][y].block_path = True

	map_make_fov(new_map)
	return new_map


def map_make_fov(incoming_map):
	global FOV_MAP
	FOV_MAP = rogue.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

	for y in range(constants.MAP_HEIGHT):
		for x in range(constants.MAP_WIDTH):
			rogue.map_set_properties(FOV_MAP, x, y,
				not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
	global FOV_CALCULATE

	if INFORMATION.fov:
		INFORMATION.fov = False
		rogue.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y,
			constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)


#DRAW STUFF

def draw_game():

	global SURFACE_MAIN

	SURFACE_MAIN.fill(constants.COLOR_BLACK)
	draw_map(GAME_MAP)

	for b in building_list:
		b.draw()

	PLAYER.draw()
	draw_stats(SURFACE_MAIN)
	if INFORMATION.which_menu == 0:
		draw_purchases(SURFACE_MAIN)
	else:
		draw_actions(SURFACE_MAIN)

	if INFORMATION.terra == 1:
		draw_terra_menu(SURFACE_MAIN)

	pygame.display.flip()


def draw_map(map_to_draw):

	for x in range(0, constants.MAP_WIDTH):
		for y in range(0, constants.MAP_HEIGHT):

			is_visible = rogue.map_is_in_fov(FOV_MAP, x, y)

			if is_visible:

				if map_to_draw[x][y].resource == "wheat":
					SURFACE_MAIN.blit(constants.S_TREE, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
				elif map_to_draw[x][y].resource == "ore":
					SURFACE_MAIN.blit(constants.S_ORE, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
				elif map_to_draw[x][y].resource == "diamond":
					SURFACE_MAIN.blit(constants.S_DIAMOND, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
				elif map_to_draw[x][y].resource == "rock":
					SURFACE_MAIN.blit(constants.S_ROCK, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
				elif map_to_draw[x][y].resource == "floor":
					SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))


def draw_stats(display_surface):

	if len(building_list) >= 1:
		mining_resources()

	stats = ["Turn: " + str(INFORMATION.time) + " (" + str(INFORMATION.actions) + ")"]
	stats.append("HP: " + str(PLAYER.hp))
	stats.append("Coin: " + str(INFORMATION.coin) + " (+ " +str(INFORMATION.workers) + ")")
	stats.append("Food: " + str(INFORMATION.money[0]) + " (+ " + str(INFORMATION.res_list[0]) + ")")
	stats.append("Ore: " + str(INFORMATION.money[1]) + " (+ " + str(INFORMATION.res_list[1]) + ")")
	stats.append("Diamond: " + str(INFORMATION.money[2]) + " (+ " + str(INFORMATION.res_list[2]) + ")")

	ren = [" " for i in range(6)]

	for i in range(6):
		ren[i] = constants.STATS_FONT.render(stats[i], 0, constants.COLOR_WHITE)

	for i in range(6):
		display_surface.blit(ren[i], (constants.GAME_WIDTH + 10, 10 + i*25))


def draw_purchases(display_surface):

	mouse = pygame.mouse.get_pos()

	ren = constants.STATS_FONT.render("Buy:", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH + 10, 180))

	if mouse[0] > constants.GAME_WIDTH + 10 and mouse[0] < (constants.GAME_WIDTH + 300) and mouse[1] > 210 and mouse[1] < 235:
		pygame.draw.rect(display_surface, constants.COLOR_GREY,
			(constants.GAME_WIDTH + 10, 210, 300, 25))

	ren = constants.STATS_FONT.render("1. Worker  (2C, 1G)", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH + 10, 210))


def draw_actions(display_surface):

	mouse = pygame.mouse.get_pos()

	ren = constants.STATS_FONT.render("Actions:", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH + 10, 180))

	for i in range(3):
		if is_menu_item(mouse[0], mouse[1], i):
			pygame.draw.rect(display_surface, constants.COLOR_GREY, (constants.GAME_WIDTH + 10, 210 + i*30, 350, 25))

	ren = constants.STATS_FONT.render("b. Build (4C)", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH + 10, 210))

	ren = constants.STATS_FONT.render("m. Mine", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH + 10, 240))

	ren = constants.STATS_FONT.render("t. Terraform (8C)", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH + 10, 270))

def draw_terra_menu(display_surface):

	ren = constants.STATS_FONT.render("a. Wheat", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH/2, 210))

	ren = constants.STATS_FONT.render("b. Ore", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH/2, 240))

	ren = constants.STATS_FONT.render("c. Diamond", 0, constants.COLOR_WHITE)
	display_surface.blit(ren, (constants.GAME_WIDTH/2, 270))


#GAME LOOP

def game_main_loop():
	'''Loop the main game'''

	game_quit = False

	while not game_quit:

		if INFORMATION.terra == 1:
			handle_terraform_keys()
		else:
			what_happened = game_handle_keys()

		map_calculate_fov()

		if what_happened == "Quit":
			game_quit = True
		elif what_happened == "Action":
			INFORMATION.fov = True
			if INFORMATION.actions == 0:
				INFORMATION.time += 1
				INFORMATION.actions = 3
				update_resources()
			else:
				INFORMATION.actions -= 1

		draw_game()

	pygame.quit()
	exit()

def mining_resources():
	available_resources = [0, 0, 0]
	for i in range(len(building_list)):
		if building_list[i].mine == "wheat":
			available_resources[0] += 1
		if building_list[i].mine == "ore":
			available_resources[1] += 1
		if building_list[i].mine == "diamond":
			available_resources[2] += 1

	INFORMATION.res_list = available_resources

def update_resources():
	INFORMATION.money = [INFORMATION.money[i] + INFORMATION.res_list[i] for i in range(3)]
	INFORMATION.coin += INFORMATION.workers


def game_initialize():
	'''Initializes the main window'''

	global SURFACE_MAIN, GAME_MAP, PLAYER, INFORMATION, FOV_CALCULATE, building_list

	pygame.init()

	SURFACE_MAIN = pygame.display.set_mode( (constants.GAME_WIDTH + 400, constants.GAME_HEIGHT) )

	GAME_MAP = map_create()

	FOV_CALCULATE = True

	PLAYER = Actor(1, 1, constants.S_PLAYER)

	building_list = []

	INFORMATION = Information()


def game_handle_keys():

	events_list = pygame.event.get()
	mouse = pygame.mouse.get_pos()
	leftclick = pygame.mouse.get_pressed()[0]

	for event in events_list:
		if event.type == pygame.QUIT:
			return "Quit"

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP or event.key == pygame.K_w:
				PLAYER.move(0, -1)
				return "Action"
			elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
				PLAYER.move(0, 1)
				return "Action"
			elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
				PLAYER.move(1, 0)
				return "Action"
			elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
				PLAYER.move(-1, 0)
				return "Action"
			elif event.key == pygame.K_b:
				if INFORMATION.coin >= 4 and is_legit(PLAYER.x, PLAYER.y):
					build()
					return "Action"
			elif event.key == pygame.K_1:
				if buy_worker():
					return "Action"
			elif event.key == pygame.K_m:
				if mine():
					return "Action"
			elif event.key == pygame.K_t:
				terraform()
			elif event.key == pygame.K_TAB:
				INFORMATION.which_menu = (INFORMATION.which_menu + 1) % 2

		if is_menu_item(mouse[0], mouse[1], 0) and leftclick and INFORMATION.which_menu == 0:
			if buy_worker():
				return "Action"

		if is_menu_item(mouse[0], mouse[1], 0) and leftclick and INFORMATION.which_menu == 1:
			if INFORMATION.coin >= 4 and is_legit(PLAYER.x, PLAYER.y):
					build()
					return "Action"

		if is_menu_item(mouse[0], mouse[1], 1) and leftclick and INFORMATION.which_menu == 1:
			if mine():
				return "Action"

		if is_menu_item(mouse[0], mouse[1], 2) and leftclick and INFORMATION.which_menu == 1:
			if terraform():
				return "Pause"


def buy_worker():
	if INFORMATION.coin >= 2 and INFORMATION.money[0] >= 1:
		INFORMATION.workers += 1
		INFORMATION.coin -= 2
		INFORMATION.money[0] -= 1
		return True
	else:
		return False

def build():
	global base

	INFORMATION.coin -= 4
	INFORMATION.workers += 1
	base = Building(PLAYER.x, PLAYER.y, constants.S_BASE, GAME_MAP[PLAYER.x][PLAYER.y].resource)
	building_list.append(base)

def is_legit(x, y):
	if len(building_list) == 0:
		return True
	else:
		legit_coords = []
		for dx in [-1, 0, 1]:
			for dy in [-1, 0, 1]:
				for b in building_list:
					legit_coords.append(((b.x + dx), (b.y + dy)))
		if (x,y) in legit_coords:
			return True
		else:
			return False

def is_menu_item(x, y, i):
	if x > constants.GAME_WIDTH + 10 and x < (constants.GAME_WIDTH + 300) and y > (210 + 30*i) and y < (235 + 30*i):
		return True
	else:
		return False

def mine():
	if GAME_MAP[PLAYER.x][PLAYER.y].resource == "wheat":
		INFORMATION.money[0] += 1
		GAME_MAP[PLAYER.x][PLAYER.y].resource = "floor"
		return True
	elif GAME_MAP[PLAYER.x][PLAYER.y].resource == "ore":
		INFORMATION.money[1] += 1
		GAME_MAP[PLAYER.x][PLAYER.y].resource = "floor"
		return True
	elif GAME_MAP[PLAYER.x][PLAYER.y].resource == "diamond":
		INFORMATION.money[2] += 1
		GAME_MAP[PLAYER.x][PLAYER.y].resource = "floor"
		return True
	else:
		return False

def terraform():
	if INFORMATION.coin >= 8:
		INFORMATION.coin -= 8
		INFORMATION.terra = 1
		return True
	else:
		return False

def handle_terraform_keys():
	events_list = pygame.event.get()
	mouse = pygame.mouse.get_pos()

	for event in events_list:
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				GAME_MAP[PLAYER.x][PLAYER.y].resource = "wheat"
				INFORMATION.terra = 0
			elif event.key == pygame.K_b:
				GAME_MAP[PLAYER.x][PLAYER.y].resource = "ore"
				INFORMATION.terra = 0
			elif event.key == pygame.K_c:
				GAME_MAP[PLAYER.x][PLAYER.y].resource = "diamond"
				INFORMATION.terra = 0


if __name__ == '__main__':
	game_initialize()
	game_main_loop()