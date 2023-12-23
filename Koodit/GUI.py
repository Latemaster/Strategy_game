from PyQt6 import QtWidgets, QtGui
from gamegrid import Gamegrid
from tile_graphics_item import tileGraphicsItem
from player import Player
from player_graphics_item import playerGraphicsItem
from Koodit.menu_buttons import MenuButtons
from Koodit.game_buttons import GameButtons
from location import Location
import sys
from read_file import ReadFile
from Turn import Turn
from opponent_ai import ai
class GUI(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Strategia Peli")

        button = QtWidgets.QPushButton("Valitse Tiedosto", self)
        button.clicked.connect(self.open_file)

        self.setCentralWidget(button)


    def open_file(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setWindowTitle("Valitse Tiedosto")
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if fileDialog.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            selected_files = fileDialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.read_file(file_path)
    def load_file(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setWindowTitle("Valitse Tiedosto")
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if fileDialog.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            selected_files = fileDialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.load_game(file_path)
    def save_into_file(self):
        fileDialog = QtWidgets.QFileDialog()
        fileDialog.setWindowTitle("Valitse Tiedosto")
        fileDialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        if fileDialog.exec() == QtWidgets.QFileDialog.DialogCode.Accepted:
            selected_files = fileDialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.save_game(file_path)
    def read_file(self, filepath):
        self.GameInfo = ReadFile()
        self.GameInfo.read_info_file(filepath)
        self.GameBegin(self.GameInfo.get_square_size())
    def GameBegin(self, square_size):
        self.winner = True
        #self.GameInfo = ReadFile()
        #self.GameInfo.read_info_file(filepath)
        geometry = self.GameInfo.get_gui_geometry()
        self.setGeometry(geometry[0], geometry[0], geometry[1], geometry[1])

        self.setCentralWidget(QtWidgets.QWidget())
        self.horizontal = QtWidgets.QHBoxLayout()
        self.vertical1 = QtWidgets.QVBoxLayout()
        self.vertical2 = QtWidgets.QVBoxLayout()
        self.centralWidget().setLayout(self.horizontal)
        self.horizontal.addLayout(self.vertical1)
        self.horizontal.addLayout(self.vertical2)
        self.scene = QtWidgets.QGraphicsScene()
        self.squareSize = square_size
        self.gameStarted = False
        self.selected_attack = None
        self.opponent_selected_attack = None
        self.attacker = 0
        self.turn = Turn(self)
        self.turnActive = True
        self.tile_or_player_index = 0
        self.add_gamegrid(0, self.GameInfo.get_grid_size(), self.GameInfo.get_grid_size())
        self.add_gamegrid(self.GameInfo.get_distance(), self.GameInfo.get_grid_size(), self.GameInfo.get_grid_size())
        self.gameGridPlayer = Gamegrid(self.GameInfo.get_grid_size(), self.GameInfo.get_grid_size(), 0)
        self.gameGridOpponent = Gamegrid(self.GameInfo.get_grid_size(), self.GameInfo.get_grid_size(), 1)

        self.playerSelected = None
        self.opponent_playerSelected = None
        self.opponent_action = 0
        self.player_action = 0
        self.current_player_move_location = Location(0, 0)
        self.current_opponent_move_location = Location(0, 0)
        self.init_window()
        self.menuButtons = MenuButtons(self)
        self.gameButtons = GameButtons(self)
        self.vertical2.addLayout(self.menuButtons)
        self.vertical2.addLayout(self.gameButtons)
        self.gameButtons.set_visible(False)
        self.current_attack_area = None
        self.current_opponent_attack_area = None
        self.current_move_area = None
        self.current_opponent_move_area = None
        self.menuButtons.playerOrTypeButton.clicked.connect(self.player_or_tile)
        self.menuButtons.startGameButton.clicked.connect(self.startGame)
        self.opponentAI = ai(self.gameGridOpponent, self)
        self.menuButtons.LoadGameButton.clicked.connect(self.load_file)
        self.moved_last_turn = False
    def startGame(self):
        if len(self.gameGridPlayer.players) == self.GameInfo.get_player_amount():
            self.gameStarted = True
            player = self.gameGridPlayer.get_player(0)
            self.playerSelected = self.get_Graphics(player.get_location().get_x(), player.get_location().get_y(), self.squareSize, playerGraphicsItem)
            self.menuButtons.set_visible(False)
            self.gameButtons.set_visible(True)
            self.set_opponent_players(self.GameInfo.get_distance())
            player = self.gameGridOpponent.get_player(0)
            self.opponent_playerSelected = self.get_Graphics(player.get_location().get_x(), player.get_location().get_y(), self.squareSize, playerGraphicsItem)
            print(self.opponent_playerSelected)
            self.gameButtons.attackButton.clicked.connect(self.use_turn_to_attack)
            self.gameButtons.MoveButton.clicked.connect(self.use_turn_to_move)
            self.gameButtons.turnButton.clicked.connect(self.next_turn)
            self.gameButtons.attackOptionsButton.clicked.connect(self.change_attacks)
            self.gameButtons.SaveButton.clicked.connect(self.save_into_file)
            self.gameButtons.update_player_info(self.gameButtons.opponent1Layout, self.gameGridOpponent.get_player(0).get_name(),self.gameGridOpponent.get_player(0).get_hitpoints(),self.gameGridOpponent.get_player(0).get_state())
            self.gameButtons.update_player_info(self.gameButtons.opponent2Layout,self.gameGridOpponent.get_player(1).get_name(),self.gameGridOpponent.get_player(1).get_hitpoints(),self.gameGridOpponent.get_player(1).get_state())
            self.gameButtons.update_player_info(self.gameButtons.opponent3Layout, self.gameGridOpponent.get_player(2).get_name(),self.gameGridOpponent.get_player(2).get_hitpoints(),self.gameGridOpponent.get_player(2).get_state())

        else:
            print("Not enough players")


    #creates a scene and adds a grid of colxrow to the scene, then returns the scene
    def add_gamegrid(self, pos, col, row):
        for i in range(col):
            for j in range(row):
                location = Location(i*self.squareSize, (j*self.squareSize - pos*self.squareSize))
                item = tileGraphicsItem(location, self.squareSize, self)
                self.scene.addItem(item)


    #creates a view and adds them to the vertical Layout.
    def init_window(self):
        self.view1 = QtWidgets.QGraphicsView(self.scene, self)
        self.vertical1.addWidget(self.view1)



    def change_attacks(self):
        if self.playerSelected is not None:
            player = self.playerSelected.get_player()
            attacks = player.get_attacks()
            if self.gameButtons.attackOptionsButton.text() == str(attacks[1]):
                self.gameButtons.attackOptionsButton.setText(str(attacks[0]))
            else:
                self.gameButtons.attackOptionsButton.setText(str(attacks[1]))


    def set_opponent_players(self, pos):
        playerIndex = 0
        while len(self.gameGridOpponent.players) < self.GameInfo.get_player_amount():
            bestTile = self.gameGridOpponent.get_tile(0, 0)
            for a in range(self.GameInfo.get_grid_size()):
                if bestTile.is_empty() is not True:
                    bestTile = self.gameGridOpponent.get_tile(a, 0)
            for i in range(self.GameInfo.get_grid_size()):
                for j in range(self.GameInfo.get_grid_size()):
                    tile = self.gameGridOpponent.get_tile(i, j)
                    if tile.get_type() > bestTile.get_type() and tile.is_empty() is True:
                        bestTile = tile
            player = self.gameGridPlayer.get_player(playerIndex)
            type = player.get_type()
            self.add_player_graphics(bestTile.get_location().get_y(), bestTile.get_location().get_x(), self.gameGridOpponent, pos, type)
            playerIndex += 1


    def player_or_tile(self):
        if self.menuButtons.playerOrTypeButton.text() == "Add a Player":
            self.tile_or_player_index = 1
            self.menuButtons.playerOrTypeButton.setText("Add a Tile")
        else:
            self.tile_or_player_index = 0
            self.menuButtons.playerOrTypeButton.setText("Add a Player")


    def tile_clicked(self, x, y, pos):
        if self.gameStarted is False:
            if self.tile_or_player_index == 1:
                self.select_tile_type(x, y, pos, self.menuButtons.tile_options.currentIndex())
            else:
                playerIndex = self.menuButtons.player_options.currentIndex()
                self.add_player_graphics(x, y, self.gameGridPlayer, 0, playerIndex)
        else:
            self.current_player_move_location = Location(x, y)
            self.reset_move_area()




    def select_attack_area(self, attack, location):
        self.reset_attack_area(self.GameInfo.get_distance())
        hit_area = attack.get_hit_area(location)
        for area in hit_area:
            if 0 <= area.get_x() <= 150 and -400 <= area.get_y() <= -250:
                graphic = self.get_Graphics(area.get_x()/self.squareSize, area.get_y()/self.squareSize, self.squareSize, tileGraphicsItem)
                graphic.setPen(QtGui.QPen(QtGui.QColor("Red")))
        return hit_area

    def reset_attack_area(self, pos):
        for tile in self.gameGridOpponent.get_tiles():
            graphic = self.get_Graphics(tile.get_location().get_x(), tile.get_location().get_y() - pos, self.squareSize, tileGraphicsItem)
            graphic.setPen(QtGui.QPen(QtGui.QColor("Black")))
            self.current_attack_area = None

    def reset_move_area(self):
        for tile in self.gameGridPlayer.get_tiles():
            graphic = self.get_Graphics(tile.get_location().get_x(), tile.get_location().get_y() , self.squareSize, tileGraphicsItem)
            graphic.setPen(QtGui.QPen(QtGui.QColor("Black")))


    def select_move_area(self, x, y, player):
        self.reset_move_area()
        move_area = player.get_move_area(Location(x/self.squareSize, y/self.squareSize))
        for area in move_area:
            if 0 <= area.get_x() <= 3 and 0 <= area.get_y() <= 3:
                graphic = self.get_Graphics(area.get_x(), area.get_y(), self.squareSize, tileGraphicsItem)
                graphic.setPen(QtGui.QPen(QtGui.QColor("Green")))
        return move_area
    def move_player(self, x, y, move_area):

        move = False
        for area in move_area:
            if area.get_x() == x and area.get_y() == y:
                move = True
        if move:
            if self.gameButtons.turnIndex == 1:
                self.set_player(x, y, self.gameGridPlayer, self.playerSelected, 0)
                self.playerSelected = None
            elif self.gameButtons.turnIndex == 0:
                print("You are attacking")
        else:
            print("out of moving range")

    def set_player(self, x, y, gameGrid, player, pos):
        if gameGrid.get_tile(x, y).is_empty() and player != None:
            if gameGrid.gridID == 0:
                previous_Tile = gameGrid.get_tile(int(player.get_location().get_x()/self.squareSize), int(player.get_location().get_y()/self.squareSize))
            else:
                previous_Tile = gameGrid.get_tile(int(player.get_location().get_x()/self.squareSize), int((player.get_location().get_y()/self.squareSize+pos)))


            previous_Tile.remove_player()
            tile = gameGrid.get_tile(x, y)
            tile.set_player(player)
            player.get_player().updatePosition(Location(x, y))
            player.updatePosition(pos)



    def get_Graphics(self, x, y, size, Graphicitem):
        for graphic in self.scene.items():
            if type(graphic) is Graphicitem:
                if int(graphic.get_location().get_x()) == int(x*size) and int(graphic.get_location().get_y()) == int(y*size):
                    return graphic

    def select_tile_type(self, x, y, pos, tileIndex):
        tileGraphics1 = self.get_Graphics(x, y, self.squareSize, tileGraphicsItem)
        tileGraphics2 = self.get_Graphics(x, y - pos, self.squareSize, tileGraphicsItem)
        tile1 = self.gameGridPlayer.get_tile(x, y)
        tile2 = self.gameGridOpponent.get_tile(x, y)
        tile1.set_type(tileIndex)
        tile2.set_type(tileIndex)
        color = self.GameInfo.get_tile_colors()
        tileGraphics1.setBrush(QtGui.QColor(color[tileIndex]))
        tileGraphics2.setBrush(QtGui.QColor(color[tileIndex]))


    def add_player_graphics(self, x, y, gameGrid, pos, playerIndex):
        tile = gameGrid.get_tile(x, y)
        if len(gameGrid.players) < self.GameInfo.get_player_amount() and tile.is_empty():
            player = Player(playerIndex, Location(x, y), self, gameGrid)
            playerGraphics = playerGraphicsItem(player, self.squareSize, self, pos)
            self.scene.addItem(playerGraphics)
            gameGrid.add_player(player, x, y)
        elif tile.is_empty() is not True:
            self.remove_player(tile, x, y, gameGrid)
            print("Tile is not empty")
        else:
            print("field is full")



    def use_attack(self, attacker, attack_area, boost):
        if attack_area is not None:
            if attacker == 1:
                gameGrid = self.gameGridOpponent
                pos = self.GameInfo.get_distance()
                selected_attack = self.selected_attack
            else:
                gameGrid = self.gameGridPlayer
                pos = 0
                selected_attack = self.opponent_selected_attack
            players = gameGrid.get_players()
            for player in players:
                for i in range(len(attack_area)):
                    if (player.get_location().get_y() - pos)*self.squareSize == attack_area[i].get_y() and player.get_location().get_x()*self.squareSize == attack_area[i].get_x():
                        player.is_hit(selected_attack, boost)
                if attacker != 0:
                    self.gameButtons.update_all_player_info(players)


    def use_turn_to_move(self):
        if self.gameButtons.turnIndex == 1:
            self.execute_turn()
        else:
            print("Select Move Player to Move")

    def use_turn_to_attack(self):
        if self.gameButtons.turnIndex == 0:
            self.execute_turn()
        else:
            print("Select Attack to Attack")

    def execute_turn(self):


        player_to_move = self.opponentAI.decide_to_move()
        tile_to_move = self.opponentAI.decide_best_move_point()

        if player_to_move != 0 and self.moved_last_turn == False:
            self.opponent_action = 1
            self.opponent_playerSelected = player_to_move
            self.current_opponent_move_location = tile_to_move
            self.moved_last_turn = True
        else:
            self.moved_last_turn = False
            opponent_startpoint, self.opponent_playerSelected, self.opponent_selected_attack = self.opponentAI.decide_best_attack()
            startPoint_x = opponent_startpoint.get_x()*self.squareSize
            startPoint_y = opponent_startpoint.get_y()*self.squareSize
            self.opponent_action = 0
            self.current_opponent_attack_area = self.opponent_selected_attack.get_hit_area(Location(startPoint_x, startPoint_y))
            for tile in self.current_opponent_attack_area:
                graphic = self.get_Graphics(tile.get_x()/self.squareSize, tile.get_y()/self.squareSize, self.squareSize, tileGraphicsItem)
                if graphic is not None:
                    graphic.setPen(QtGui.QPen(QtGui.QColor("Yellow")))


        self.player_action = self.gameButtons.turnIndex
        if self.turnActive:
            if self.player_action == 1 and self.opponent_action == 1:
                if self.playerSelected.get_player().get_state() != 2:
                    self.move_player(self.current_player_move_location.get_x(), self.current_player_move_location.get_y(), self.current_move_area)
                else:
                    print("player paralyzed")
                if self.opponent_playerSelected.get_player().get_state != 2:
                    self.set_player(self.current_opponent_move_location.get_x(), self.current_opponent_move_location.get_y(), self.gameGridOpponent, self.opponent_playerSelected, self.GameInfo.get_distance())
                else:
                    print("Opponent player paralyzed")

            elif self.player_action == 0 and self.opponent_action == 1:
                if self.opponent_playerSelected.get_player().get_state != 2:
                    self.set_player(self.current_opponent_move_location.get_x(),self.current_opponent_move_location.get_y(), self.gameGridOpponent,self.opponent_playerSelected, self.GameInfo.get_distance())
                else:
                    print("Opponent player paralyzed")
                if self.playerSelected.get_player().get_state() == 1:
                    boost = True
                else:
                    boost = False
                self.use_attack(1, self.current_attack_area, boost)

            elif self.player_action == 1 and self.opponent_action == 0:
                if self.playerSelected.get_player().get_state() != 2:
                    self.move_player(self.current_player_move_location.get_x(),
                                     self.current_player_move_location.get_y(), self.current_move_area)
                else:
                    print("player paralyzed")
                if self.opponent_playerSelected.get_player().get_state() == 1:
                    boost = True
                else:
                    boost = False
                self.use_attack(0, self.current_opponent_attack_area, boost)
            else:
                self.turn.moves_first(self.playerSelected.get_player(), self.opponent_playerSelected.get_player())
                if self.playerSelected.get_player().get_state() == 1:
                    playerboost = True
                else:
                    playerboost = False
                if self.opponent_playerSelected.get_player().get_state() == 1:
                    opBoost = True
                else:
                    opBoost = False
                if self.attacker == 0:
                    self.use_attack(self.attacker, self.current_opponent_attack_area, opBoost)
                    self.attacker = 1
                    if self.opponent_playerSelected is not None:
                        self.use_attack(self.attacker, self.current_attack_area, playerboost)
                elif self.attacker == 1:
                    self.use_attack(self.attacker, self.current_attack_area, playerboost)
                    self.attacker = 0
                    if self.opponent_playerSelected is not None:
                        self.use_attack(self.attacker, self.current_opponent_attack_area, opBoost)
            print(self.opponent_playerSelected.get_player().get_location().get_x(), self.opponent_playerSelected.get_player().get_location().get_y())
            self.opponent_playerSelected = None
            self.turnActive = False
            self.gameButtons.update_turn_info()
            self.set_tile_effects(self.gameGridPlayer)
            self.set_tile_effects(self.gameGridOpponent)
        else:
            print("continue to next turn")


    def next_turn(self):
        self.turnActive = True
        self.gameButtons.turnButton.setText("Turn Active")
        self.reset_move_area()
        self.gameButtons.update_all_player_info(self.gameGridOpponent.get_players())

    def show_selected_player(self):
        for graphic in self.scene.items():
            graphic.setPen(QtGui.QPen(QtGui.QColor("Black")))
        self.playerSelected.setPen(QtGui.QPen(QtGui.QColor("Red")))


    def remove_player(self, tile, x, y, gameGrid):
        tile.remove_player()
        if gameGrid.gridID == 0:
            gameGrid.remove_player(x, y)
        else:
            gameGrid.remove_player(x, int(y +self.GameInfo.get_distance()))
        playerGraphics = self.get_Graphics(x, y, self.squareSize, playerGraphicsItem)
        self.scene.removeItem(playerGraphics)



    def select_attack(self, attack):
        self.selected_attack = attack


    def save_game(self, file):
        with open(file, "w"):
            pass
        file = open(file, "w")
        Player_players = self.gameGridPlayer.get_players()
        Opponent_players = self.gameGridOpponent.get_players()
        for player in Player_players:
            file.write("PLAYER," + str(player.playerType) + "," + str(player.get_location().get_x()) + "," + str(player.get_location().get_y()) + "," + str(player.get_hitpoints()) + "," + str(player.get_state()) + ";")

        for player in Opponent_players:
            file.write("PLAYER," + str(player.playerType) + "," + str(player.get_location().get_x()) + "," + str(player.get_location().get_y()) + "," + str(player.get_hitpoints()) + "," + str(player.get_state()) + ";")
        file.write("\n")
        for y in range(self.GameInfo.get_grid_size()):
            for x in range(self.GameInfo.get_grid_size()):
                tile = self.gameGridPlayer.get_tile(x, y)
                type = tile.get_type()
                file.write(str(type) + "," + str(x) + "," + str(y) + ";")
        file.write(":")
        for y in range(self.GameInfo.get_grid_size()):
            for x in range(self.GameInfo.get_grid_size()):
                tile = self.gameGridOpponent.get_tile(x, y)
                type = tile.get_type()
                file.write(str(type) + "," + str(x) + "," + str(y) + ";")

    def load_game(self, filepath):
        if len(self.gameGridPlayer.get_players()) == 0:
            self.load_game_info(filepath)
            self.startGame()
    def load_game_info(self, file):
        fileinfo = open(file, "r")
        line = fileinfo.readline().rstrip()
        line = line.split(";")
        i = 0
        pos = self.GameInfo.get_distance()

        for player in line:
            if len(player) > 1:
                player = player.split(",")
                playerType = int(player[1])
                playerX = int(player[2])
                playerY = int(player[3])
                playerHp = int(player[4])
                playerState = int(player[5])
                if i < 3:
                    self.add_player_graphics(playerX, playerY, self.gameGridPlayer, 0, playerType)
                    player = self.gameGridPlayer.get_player(i)
                    player.set_hp(playerHp)
                    player.affected(playerState)
                else:
                    self.add_player_graphics(playerX, playerY, self.gameGridOpponent, pos, playerType)
                    player = self.gameGridOpponent.get_player(i-3)
                    player.set_hp(playerHp)
                    player.affected(playerState)

                i += 1
        line = fileinfo.readline().rstrip()
        line = line.split(":")
        playerTiles = line[0].split(";")
        opponentTiles = line[1].split(";")
        for tile in playerTiles:
            tile = tile.split(",")
            if len(tile) > 1:
                tileType = int(tile[0])
                tileX = int(tile[1])
                tileY = int(tile[2])
                self.select_tile_type(tileX, tileY, 0, tileType)
        for tile in opponentTiles:
            tile = tile.split(",")
            if len(tile) > 1:
                tileType = int(tile[0])
                tileX = int(tile[1])
                tileY = int(tile[2])
                self.select_tile_type(tileX, tileY, self.GameInfo.get_distance(), tileType)

    def set_tile_effects(self, gameGrid):
        for player in gameGrid.get_players():
            tile = self.gameGridPlayer.get_tile(player.get_location().get_x(), player.get_location().get_y())
            if tile.get_type() == 0:
                player.affected(1)
            elif tile.get_type() == 4:
                player.affected(2)

    def game_End(self):
        if len(self.gameGridPlayer.get_players()) == 0:
            self.winner = False
        else:
            self.winner = True

        if self.winner:
            self.gameButtons.GameEndButton.setText("YOU WIN!!!!")
        else:
            self.gameButtons.GameEndButton.setText("YOU LOSE:(")

        self.gameButtons.GameEndButton.setVisible(True)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    game = GUI()
    game.show()
    sys.exit(app.exec())
