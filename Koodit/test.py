import unittest
from GUI import GUI
from PyQt6 import QtWidgets
import sys
from player_graphics_item import playerGraphicsItem
from location import Location

class Test(unittest.TestCase):


    def test_move_player(self):
        app = QtWidgets.QApplication(sys.argv)
        game = GUI()
        game.read_file("tempfile")
        game.add_player_graphics(0, 0, game.gameGridPlayer, 0, 0)
        game.gameButtons.turnIndex = 1
        game.playerSelected = game.get_Graphics(0, 0, 50, playerGraphicsItem)
        move_area = game.playerSelected.get_player().get_move_area(Location(game.playerSelected.get_player().get_location().get_x(),game.playerSelected.get_player().get_location().get_x()))
        game.move_player(1, 1, move_area)
        tile = game.gameGridPlayer.get_tile(1, 1)
        player = tile.get_player()
        self.assertEqual(1, player.get_location().get_x()/game.squareSize, "Player x is 1)")
        self.assertEqual(1, player.get_location().get_x()/game.squareSize, "Player y is 1")



