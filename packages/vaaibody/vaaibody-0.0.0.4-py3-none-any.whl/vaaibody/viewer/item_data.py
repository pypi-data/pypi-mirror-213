class Point:
    def __init__(self, position=[], discription={}):
        self._position = position
        if discription:
            self._type = discription["type"]
        else:
            self._type = "point"
        self._len = 0
        if len(position) != 0:
            self._len = 1

    def __getitem__(self):
        return self._position

    def __len__(self):
        return self._len

    def get_type(self):
        return self._type

    def get_position(self):
        return self._position


class PointWithDirection:
    def __init__(self, position, direction):
        self._position = position
        self._direction = direction

    @property
    def position(self):
        return self._position

    @property
    def direction(self):
        return self._direction
