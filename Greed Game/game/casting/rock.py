from game.casting.object import Object


class Rock(Object):
    """
    This is a basic rock
    """
    def __init__(self):
        super().__init__()
        self._point_value = -1
        self._text = "O"
