from tile import Tile
from location import Location
class Gamegrid():
    def __init__(self, width, height, gridID):
        self.gridID = gridID
        self.players = []
        self.tiles = [[Tile(Location(x, y)) for x in range(height)] for y in range(width)]

    def get_height(self):
        return len(self.tiles[0])

    def get_id(self):
        return self.gridID


    def get_tiles(self):
        tiles = []
        for i in range(4):
            for j in range(4):
                tiles.append(self.get_tile(i, j))
        return tiles
    def get_width(self):
        return len(self.tiles)

    def get_tile(self, x, y):
        return self.tiles[x][y]

    def get_players(self):
        temp = []
        for i in self.players:
            temp.append(i)
        return temp


    def add_player(self, player, x, y):
        self.players.append(player)
        tile = self.get_tile(x, y)
        tile.set_player(player)


    def get_player(self, num):
        if len(self.players) > num:
            return self.players[num]
    def remove_player(self, x, y):
        for player in self.players:
            if player.get_location().get_x() == x and player.get_location().get_y() == y:
                self.players.remove(player)






