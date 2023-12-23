from location import Location
from attack import Attack
from player_graphics_item import playerGraphicsItem

class ai():
    def __init__(self, gameGrid, gui):
        self.gameGrid = gameGrid
        self.gui = gui

    def decide_to_move(self):
        critical_range = 5
        lowest_player = None
        players = []
        for graphic in self.gui.scene.items():
            if type(graphic) is playerGraphicsItem:
                if graphic.get_player().get_game_grid() == self.gameGrid:
                    players.append(graphic)

        for player in players:
            player_hp = player.get_player().get_hitpoints()
            if player_hp < critical_range:
                critical_range = player_hp
                lowest_player = player
        if lowest_player != None:
            return lowest_player
        else:
            return 0

    def decide_best_move_point(self):
        tile_type = 0
        best_score = 0
        best_tile = self.gameGrid.get_tile(0, 0)

        for player in self.gameGrid.get_players():
            area = player.get_move_area(player.get_location())
            for location in area:
                score = 0
                tile = self.gameGrid.get_tile(int(location.get_x()/self.gui.GameInfo.get_square_size()), int(location.get_y()/self.gui.GameInfo.get_square_size()))
                if tile.get_type() > tile_type:
                    score += int(5 * (tile.get_type() - tile_type))
                    if tile.is_empty() is False:
                        score -= 1000
                    tile_type = tile.get_type()
                    best_tile = tile
                    score += int(abs(tile.get_location().get_x() - player.get_location().get_x())) + int(abs(tile.get_location().get_x() - player.get_location().get_x()))
                if score > best_score:
                    best_tile = self.gameGrid.get_tile(location.get_x(), location.get_y())
        return best_tile.get_location()


    def decide_best_attack(self):
        best_score = 0
        best_player = None
        best_attack = None
        best_tile = None
        players = []

        for graphic in self.gui.scene.items():
            if type(graphic) is playerGraphicsItem:
                if graphic.get_player().get_game_grid() == self.gameGrid:
                    players.append(graphic)


        for AttackPlayer in players:
            for attack in AttackPlayer.get_player().get_attacks():
                attack = Attack(attack, self.gui)
                for i in range(self.gui.GameInfo.get_grid_size()):
                    for j in range(self.gui.GameInfo.get_grid_size()):
                        area = attack.get_hit_area(Location(i, j))
                        score = 0
                        for player in self.gui.gameGridPlayer.get_players():
                            for location in area:
                                location2 = player.get_location()
                                if location.get_x() == location2.get_x() and location.get_y() == location2.get_y():
                                    if AttackPlayer.get_player().get_state() == 1:
                                        score += attack.get_power()*2
                                    else:
                                        score += attack.get_power()
                                    if player.get_hitpoints() <= attack.get_power():
                                        score += attack.get_power()*3
                        if score > best_score:
                            best_score = score
                            best_tile = Location(i, j)
                            best_player = AttackPlayer
                            best_attack = attack

        return best_tile, best_player, best_attack






