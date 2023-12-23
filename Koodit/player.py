from location import Location
class Player():
    def __init__(self, playerType, location, gui, gameGrid):
        self.gui = gui
        self.playerType = playerType
        self.location = location
        attackList = self.gui.GameInfo.get_attacks()
        self.set_attributes()
        self.assign_attacks(attackList)
        self.state = 0
        self.gameGrid = gameGrid

    def set_attributes(self):
        players = self.gui.GameInfo.get_players()
        info = self.gui.GameInfo.get_player_info()
        self.name, self.hitpoints, self.speed, self.range = info[players[self.playerType]]
        self.hitpoints = int(self.hitpoints)
        self.speed = int(self.speed)
        self.range = int(self.range)
    def get_hitpoints(self):
        return self.hitpoints
    def get_range(self):
        return self.range

    def get_game_grid(self):
        return self.gameGrid

    def get_speed(self):
        return self.speed
    def get_type(self):
        return self.playerType

    def get_attacks(self):
        return self.attacks
    def get_name(self):
        return self.name
    def get_state(self):
        return self.state
    def get_location(self):
        return self.location

    def set_hp(self, hp):
        self.hitpoints = hp
    def assign_attacks(self, all_attacks):
        self.attacks = []
        self.attacks.append(all_attacks[0])
        self.attacks.append(all_attacks[self.playerType])

    def get_move_area(self, playerPos):
        startPoint = Location(int(playerPos.get_x()-1), int(playerPos.get_y()-1))
        hitTiles = []
        for i in range(self.get_range()):
            for j in range(self.get_range()):
                hitTiles.append(Location(int(startPoint.get_x())+i, int(startPoint.get_y())+j))
        return hitTiles

    def is_hit(self, attack, boost):
        if boost:
            power = attack.get_power()*2
        else:
            power = attack.get_power()
        effect = attack.get_effect()
        if self.state == 3:
            power -= 1

        if self.hitpoints > power:
            self.hitpoints -= power
            if effect > 0:
                self.state = effect
        else:
            self.hitpoints = 0
            self.player_dead()


    def updatePosition(self, location):
        self.location = location


    def poisoned(self):
        if self.state == 1:
            self.hitpoints -= 1

    def affected(self, effect):
        self.state = effect

    def remove_effect(self):
        self.state = 0
    def player_dead(self):
        tile = self.gameGrid.get_tile(self.get_location().get_x(), self.get_location().get_y())
        print("playeRDead")
        if self.gameGrid.get_id() == 0:
            self.gui.remove_player(tile, self.get_location().get_x(), self.get_location().get_y(), self.gameGrid)
        else:
            self.gui.remove_player(tile, self.get_location().get_x(), int(self.get_location().get_y()-self.gui.GameInfo.get_distance()), self.gameGrid)
        print(len(self.gameGrid.get_players()))
        if len(self.gameGrid.get_players()) == 0:
            self.gui.game_End()


