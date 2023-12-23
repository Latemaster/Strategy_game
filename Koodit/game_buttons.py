from PyQt6 import QtWidgets

class GameButtons(QtWidgets.QVBoxLayout):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.turnIndex = 0
        self.OpponentPlayerLayout = QtWidgets.QHBoxLayout()
        self.attackLayout = QtWidgets.QHBoxLayout()
        self.actionLayout = QtWidgets.QHBoxLayout()
        self.attacks = self.gui.GameInfo.get_attacks
        self.attackButton = QtWidgets.QPushButton("ATTACK")
        self.MoveButton = QtWidgets.QPushButton("MAKE MOVE")
        self.attackOptionsButton = QtWidgets.QPushButton("BASIC")
        self.SaveButton = QtWidgets.QPushButton("SAVE")

        self.GameEndButton = QtWidgets.QPushButton("-")
        self.GameEndButton.setVisible(False)

        self.turnButton = QtWidgets.QPushButton("Turn Active")

        self.opponent1Layout = self.set_opponent_info()
        self.opponent2Layout = self.set_opponent_info()
        self.opponent3Layout = self.set_opponent_info()

        self.OpponentPlayerLayout.addLayout(self.opponent1Layout)
        self.OpponentPlayerLayout.addLayout(self.opponent2Layout)
        self.OpponentPlayerLayout.addLayout(self.opponent3Layout)

        self.Info = QtWidgets.QHBoxLayout()
        self.playerInfo = QtWidgets.QVBoxLayout()
        self.attackInfo1 = QtWidgets.QVBoxLayout()
        self.attackInfo2 = QtWidgets.QVBoxLayout()

        self.playerLabel = QtWidgets.QLabel("PlayerInfo")
        self.playerName = QtWidgets.QLabel("Name")
        self.playerHealth = QtWidgets.QLabel("Health")
        self.playerStatus = QtWidgets.QLabel("Status")

        self.playerLabel.setFixedSize(self.playerLabel.sizeHint())
        self.playerName.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))
        self.playerHealth.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))
        self.playerStatus.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))

        self.playerInfo.addWidget(self.playerLabel)
        self.playerInfo.addWidget(self.playerName)
        self.playerInfo.addWidget(self.playerHealth)
        self.playerInfo.addWidget(self.playerStatus)
        self.playerInfo.addWidget(self.turnButton)

        self.playerInfo.setSpacing(3)

        self.attackLabel1 = QtWidgets.QLabel("1. AttackInfo")
        self.attackPower1 = QtWidgets.QLabel("5")
        self.effect1 = QtWidgets.QLabel("poison")

        self.attackLabel2 = QtWidgets.QLabel("2. AttackInfo")
        self.attackPower2 = QtWidgets.QLabel("5")
        self.effect2 = QtWidgets.QLabel("poison")

        self.attackLabel1.setFixedSize(self.attackLabel1.sizeHint())
        self.attackPower1.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))
        self.effect1.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))

        self.attackLabel2.setFixedSize(self.attackLabel1.sizeHint())
        self.attackPower2.setFixedSize(self.gui.squareSize, int(self.gui.squareSize / 2))
        self.effect2.setFixedSize(self.gui.squareSize, int(self.gui.squareSize / 2))

        self.attackInfo1.addWidget(self.attackLabel1)
        self.attackInfo1.addWidget(self.attackPower1)
        self.attackInfo1.addWidget(self.effect1)

        self.attackInfo2.addWidget(self.attackLabel2)
        self.attackInfo2.addWidget(self.attackPower2)
        self.attackInfo2.addWidget(self.effect2)



        self.attackInfo1.setSpacing(3)


        self.Info.addLayout(self.attackInfo1)
        self.Info.addLayout(self.attackInfo2)

        self.actionLabel = QtWidgets.QLabel("Selecting Player for Attack")
        self.moveOrAttackButton = QtWidgets.QPushButton("Move Player")




        self.attacksLabel = QtWidgets.QLabel("Click to Attack")

        self.attackLayout.addWidget(self.attacksLabel)
        self.attackLayout.addWidget(self.attackButton)
        self.attackLayout.addWidget(self.attackOptionsButton)
        self.actionLayout.addWidget(self.actionLabel)
        self.actionLayout.addWidget(self.moveOrAttackButton)
        self.actionLayout.addWidget(self.MoveButton)

        self.addLayout(self.OpponentPlayerLayout)
        self.addLayout(self.attackLayout)
        self.addLayout(self.Info)
        self.addLayout(self.actionLayout)

        self.addLayout(self.playerInfo)
        self.addWidget(self.SaveButton)
        self.moveOrAttackButton.clicked.connect(self.attack_or_move)

    def set_visible(self, boolean):
        self.attackOptionsButton.setVisible(boolean)
        self.moveOrAttackButton.setVisible(boolean)
        self.attackButton.setVisible(boolean)
        self.attacksLabel.setVisible(boolean)
        self.actionLabel.setVisible(boolean)
        self.playerName.setVisible(boolean)
        self.playerHealth.setVisible(boolean)
        self.playerStatus.setVisible(boolean)
        self.attackPower1.setVisible(boolean)
        self.effect1.setVisible(boolean)
        self.playerLabel.setVisible(boolean)
        self.attackLabel1.setVisible(boolean)
        self.attackPower2.setVisible(boolean)
        self.effect2.setVisible(boolean)
        self.attackLabel2.setVisible(boolean)
        self.turnButton.setVisible(boolean)
        self.MoveButton.setVisible(boolean)
        self.SaveButton.setVisible(boolean)

        for i in range(self.opponent1Layout.count()):
            item1 = self.opponent1Layout.itemAt(i)
            item2 = self.opponent2Layout.itemAt(i)
            item3 = self.opponent3Layout.itemAt(i)
            widget1 = item1.widget()
            widget2 = item2.widget()
            widget3 = item3.widget()
            if widget1 is not None:
                widget1.setVisible(boolean)
            if widget2 is not None:
                widget2.setVisible(boolean)
            if widget3 is not None:
                widget3.setVisible(boolean)


    def attack_or_move(self):
        if self.moveOrAttackButton.text() == "Move Player":
            self.turnIndex = 1
            self.gui.player_action = self.turnIndex
            self.moveOrAttackButton.setText("Select Player for Attack")
            self.actionLabel.setText("Moving Player")
        else:
            self.turnIndex = 0
            self.gui.player_action = self.turnIndex
            self.moveOrAttackButton.setText("Move Player")
            self.actionLabel.setText("Selecting Player for Attack")

    def set_opponent_info(self):

        OpponentLayout = QtWidgets.QVBoxLayout()

        playerLabel = QtWidgets.QLabel("PlayerInfo")
        playerName = QtWidgets.QLabel("Name")
        playerHealth = QtWidgets.QLabel("Health")
        playerStatus = QtWidgets.QLabel("Status")

        playerLabel.setFixedSize(playerLabel.sizeHint())
        playerName.setFixedSize(int(self.gui.squareSize*1.2), int(self.gui.squareSize/2))
        playerHealth.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))
        playerStatus.setFixedSize(self.gui.squareSize, int(self.gui.squareSize/2))


        OpponentLayout.addWidget(playerLabel)
        OpponentLayout.addWidget(playerName)
        OpponentLayout.addWidget(playerHealth)
        OpponentLayout.addWidget(playerStatus)

        return OpponentLayout

    def update_attack_info(self, attack1, attack2):
        self.attackLabel1.setText(attack1.get_name())
        self.attackPower1.setText("Power: " + str(attack1.get_power()))
        self.effect1.setText("Effect: "+ str(attack1.get_effect()))
        self.attackLabel2.setText(attack2.get_name())
        self.attackPower2.setText("Power: " + str(attack2.get_power()))
        self.effect2.setText("Effect: " + str(attack2.get_effect()))

    def update_attack_options(self, player):
        attacks = player.get_attacks()
        self.attackOptionsButton.setText(attacks[1])

    def update_turn_info(self):
        if self.turnButton.text == "Next Turn":
            self.turnButton.setText("")
        else:
            self.turnButton.setText("Next Turn")


    def update_player_info(self, layout, name, hp, state):
        item1 = layout.itemAt(1)
        item2 = layout.itemAt(2)
        item3 = layout.itemAt(3)
        item1 = item1.widget()
        item2 = item2.widget()
        item3 = item3.widget()
        item1.setText(str(name))
        item2.setText("HP: " + str(hp))
        item3.setText("Status: " + str(state))

    def update_all_player_info(self, players):
        if len(players) == 3:
            self.update_player_info(self.opponent1Layout, players[0].get_name(), players[0].get_hitpoints(), players[0].get_state())
            self.update_player_info(self.opponent2Layout, players[1].get_name(), players[1].get_hitpoints(), players[1].get_state())
            self.update_player_info(self.opponent3Layout, players[2].get_name(), players[2].get_hitpoints(), players[2].get_state())
        elif len(players) == 2:
            self.update_player_info(self.opponent1Layout, players[0].get_name(), players[0].get_hitpoints(),players[0].get_state())
            self.update_player_info(self.opponent2Layout, players[1].get_name(), players[1].get_hitpoints(), players[1].get_state())
            self.update_player_info(self.opponent3Layout, "-", "_","_")


        elif len(players) == 1:
            self.update_player_info(self.opponent1Layout, players[0].get_name(), players[0].get_hitpoints(),players[0].get_state())
            self.update_player_info(self.opponent2Layout, "-", "_", "_")
            self.update_player_info(self.opponent3Layout, "-", "_","_")


