import pygame
import libtcodpy as rogue

pygame.init()

#sizes
GAME_WIDTH = 960
GAME_HEIGHT = 768
MAP_WIDTH = 30
MAP_HEIGHT = 24
CELL_WIDTH = 32
CELL_HEIGHT = 32

#Colors
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)
COLOR_GREY = (150,150,150)

#Game colors
COLOR_DEFAULT_BG = COLOR_GREY

#Sprites
S_PLAYER = pygame.image.load("data/at.png")
S_ROCK = pygame.image.load("data/rock.png")
S_FLOOR = pygame.image.load("data/floor1.png")
S_BASE = pygame.image.load("data/base.png")
S_TREE = pygame.image.load("data/tree.png")
S_ORE = pygame.image.load("data/ore.png")
S_DIAMOND = pygame.image.load("data/diamond.png")
S_CREATURE = pygame.image.load("data/creature.png")
S_SHADE = pygame.image.load("data/yellowshade.png")

#FONTS

STATS_FONT = pygame.font.Font("data/flux.ttf", 20)

#FOV
FOV_ALGO = rogue.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10