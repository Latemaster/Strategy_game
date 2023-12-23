class Tile():
    def __init__(self, location):
        self.player = None
        self.type = 3
        self.location = location


    def is_empty(self):
        if self.player is None:
            return True

    def get_location(self):
        return self.location
    def set_type(self, tileType):
        self.type = tileType

    def get_type(self):
        return self.type

    def set_player(self, player):
        if self.is_empty():
            self.player = player

    def get_player(self):
        return self.player

    def remove_player(self):
        #removed = self.get_player()
        self.player = None
        #return removed


    def set_effect(self, type):
        pass
        #Sets effect for player on tile
        #self.player.effect = Effect[type]
