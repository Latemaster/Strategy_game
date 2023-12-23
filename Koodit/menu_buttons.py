from PyQt6 import QtWidgets

class MenuButtons(QtWidgets.QVBoxLayout):

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.startGameButton = QtWidgets.QPushButton("Start Game")
        self.playerOrTypeButton = QtWidgets.QPushButton("Add a Player")
        self.LoadGameButton = QtWidgets.QPushButton("Load Game")

        self.tileLayout = QtWidgets.QHBoxLayout()
        self.PlayerLayout = QtWidgets.QHBoxLayout()

        self.player_options = QtWidgets.QComboBox()
        playerInfo = self.gui.GameInfo.get_player_info()
        for i in self.gui.GameInfo.get_players():
            playerInfos = playerInfo[i]
            self.player_options.addItem(playerInfos[0])



        self.tile_options = QtWidgets.QComboBox()
        tileNames = self.gui.GameInfo.get_tile_names()
        for i in range(len(tileNames)):
            self.tile_options.addItem(tileNames[i])


        self.playerLabel = QtWidgets.QLabel("Select Player")
        self.TileLabel = QtWidgets.QLabel("Select Tile Type")

        self.PlayerLayout.addWidget(self.playerLabel)
        self.PlayerLayout.addWidget(self.player_options)

        self.tileLayout.addWidget(self.TileLabel)
        self.tileLayout.addWidget(self.tile_options)

        self.addWidget(self.startGameButton)
        self.addWidget(self.playerOrTypeButton)
        self.addWidget(self.LoadGameButton)
        self.addLayout(self.PlayerLayout)
        self.addLayout(self.tileLayout)

    def set_visible(self, boolean):
            self.startGameButton.setVisible(boolean)
            self.tile_options.setVisible(boolean)
            self.player_options.setVisible(boolean)
            self.playerOrTypeButton.setVisible(boolean)
            self.playerLabel.setVisible(boolean)
            self.TileLabel.setVisible(boolean)
            self.LoadGameButton.setVisible(boolean)

