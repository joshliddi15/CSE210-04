from game.casting.object import Object


class Gem(Object):
    """
    This is a basic Gem
    """
    def __init__(self):
        super().__init__()
        self._point_value = 1
        self._text = "*"