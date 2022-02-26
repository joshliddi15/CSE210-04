import os
import random
from tkinter.tix import CELL

from game.casting.actor import Actor
from game.casting.cast import Cast
from game.casting.gem import Gem
from game.casting.rock import Rock

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point


FRAME_RATE = 60
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 15
FONT_SIZE = 30
COLS = MAX_X / CELL_SIZE
ROWS = MAX_Y / CELL_SIZE
CAPTION = "Rocks and Gems game"
DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/messages.txt"
WHITE = Color(255, 255, 255)
DEFAULT_ARTIFACTS = 10
START_ROCKS = 2
START_GEMS = 5

def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(FONT_SIZE)
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the robot
    x = int(MAX_X / 2)
    y = MAX_Y - FONT_SIZE
    position = Point(x, y)

    robot = Actor()
    robot.set_text("#")
    robot.set_font_size(FONT_SIZE)
    robot.set_color(WHITE)
    robot.set_position(position)
    cast.add_actor("robots", robot)

    for i in range(START_ROCKS):
        rock = Rock()
        cast.add_actor("rocks", rock)
    
    for i in range(START_GEMS):
        gem = Gem()
        cast.add_actor("gems", gem)

    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)

if __name__ == "__main__":
    main()