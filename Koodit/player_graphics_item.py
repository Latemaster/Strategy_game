from PyQt6 import QtWidgets, QtGui
from location import Location
from attack import Attack


class playerGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, player, size, gui, side):
        super().__init__(0, 0, size, size)
        self.player = player
        self.size = size
        self.location = Location(0, 0)
        self.gui = gui
        self.colors = self.gui.GameInfo.get_player_colors()
        self.setBrush(QtGui.QColor(255, 255, 255))
        self.setPlayerType()
        self.updatePosition(side)


    def get_location(self):
        return self.location

    def get_player(self):
        return self.player
    def setPlayerType(self):
        self.setBrush(QtGui.QColor(self.colors[self.get_player().get_type()]))

    def updatePosition(self, side):
        self.location = Location(self.player.get_location().get_x()*self.size, (self.player.get_location().get_y()-side)*self.size)
        self.setPos(self.location.get_x(), self.location.get_y())

        return self

    def mousePressEvent(self, event):
        if self.gui.gameStarted is True:
            self.gui.playerSelected = self
            self.gui.show_selected_player()
            attacks = self.gui.GameInfo.get_attacks()
            name = attacks[self.player.get_type()]
            self.gui.reset_attack_area(self.gui.GameInfo.get_distance())
            attack = Attack(name, self.gui)
            self.gui.selected_attack = attack
            self.gui.gameButtons.update_attack_info(Attack(attacks[0], self.gui), attack)
            self.gui.change_attacks()
            self.gui.current_move_area = self.gui.select_move_area(self.get_location().get_x(), self.get_location().get_y(), self.get_player())
        else:
            if self.gui.tile_or_player_index == 0:
                tile = self.gui.gameGridPlayer.get_tile(int(self.location.get_x()/self.size), int(self.location.get_y()/self.size))
                self.gui.remove_player(tile, int(self.location.get_x()/self.size), int(self.location.get_y()/self.size), self.gui.gameGridPlayer)
            else:
                print(self.player.location.get_x(), self.player.location.get_y(), "+")
                self.gui.tile_clicked(int(self.location.get_x()/self.size), int(self.location.get_y()/self.size), 8)
        self.gui.gameButtons.update_player_info(self.gui.gameButtons.playerInfo, self.player.get_name(), self.player.get_hitpoints(), self.player.get_state())



