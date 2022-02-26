import math
from game.casting.gem import Gem
from game.casting.rock import Rock
from game.shared.point import Point
import random

HIT_RADIUS = 50

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        gems = cast.get_actors("gems")
        rocks = cast.get_actors("rocks")
        current_position = robot.get_position()
        cur_x = current_position.get_x()
        cur_y = current_position.get_y()

        banner.set_text(f"Score: {self._score}")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        
        for gem in gems:
            gem_position = gem.get_position()
            cur_art_x = gem_position.get_x()
            cur_art_y = gem_position.get_y()
            gem.move_next(900, 600)

            if (math.sqrt(((cur_art_x-cur_x)**2) + ((cur_art_y-cur_y)**2))) < HIT_RADIUS:
                self._score += gem._point_value  
                cast.remove_actor("gems", gem)
                if int(len(cast.get_actors("gems"))) < 12:
                    gem = Gem()
                    dy = random.randint(3+ int(self._score/30), 15)
                    dx = random.randint(- 1, 1)
                    velocity = Point(dx, dy)
                    gem.set_velocity(velocity)
                    cast.add_actor("gems", gem)
                    gem = Gem()
                    dy = random.randint(3+ int(self._score/30), 15)
                    dx = random.randint(- 1, 1)
                    velocity = Point(dx, dy)
                    gem.set_velocity(velocity)
                    cast.add_actor("gems", gem)

        for rock in rocks:
            rock_position = rock.get_position()
            cur_art_x = rock_position.get_x()
            cur_art_y = rock_position.get_y()
            rock.move_next(900, 600)
            if self._score < 50:
                dy = int(rock._velocity.get_y())
                if dy < 6:
                    rock._velocity._y = int(dy * (1 + self._score / 10))
            
            if (math.sqrt(((cur_art_x-cur_x)**2) + ((cur_art_y-cur_y)**2))) < HIT_RADIUS:
                self._score += rock._point_value
                cast.remove_actor("rocks", rock)
                if int(len(cast.get_actors("rocks"))) < 10:
                    rock = Rock()
                    dy = random.randint(3+ int(self._score/30), 15)
                    dx = random.randint(- 1, 1)
                    velocity = Point(dx, dy)
                    rock.set_velocity(velocity)
                    cast.add_actor("rocks", rock)
                    rock = Rock()
                    dy = random.randint(3+ int(self._score/30), 15)
                    dx = random.randint(- 1, 1)
                    velocity = Point(dx, dy)
                    rock.set_velocity(velocity)
                    cast.add_actor("rocks", rock)

    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()