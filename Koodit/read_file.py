
class ReadFile():

    def __init__(self):
        self.players = {}
        self.attacks = {}
        self.effects = {}
        self.colors = []
        self.tileNames = []
        self.gridNums = [0,0,0,0,0,0]


    def read_info_file(self, info):
        playerNames = []
        playerTypes = []
        playerHitpoints = []
        playerSpeed = []
        attackNames = []
        attackPowers = []
        playerRanges= []
        attackAreas = []
        attackEffect = []
        effectNames = []
        effectPowers = []
        effectTypes = []

        file = open(info)
        read = True
        while read:
            line = str.rstrip(file.readline())
            if line == "GUI":
                while line != "NEWBLOCK":
                    line = str.rstrip(file.readline())
                    if line == "GEOMETRY:":
                        geometry = str.rstrip(file.readline())
                        geometry = geometry.split(",")
                        self.gridNums[0] = int(geometry[0])
                        self.gridNums[1] = int(geometry[1])
                    if line == "SQUARESIZE:":
                        self.gridNums[2] = int(str.rstrip(file.readline()))
                    elif line == "GRIDSIZE:":
                        self.gridNums[3] = int(str.rstrip(file.readline()))
                    elif line == "DISTANCE:":
                        self.gridNums[4] = int(str.rstrip(file.readline()))
                    elif line == "PLAYERAMOUNT:":
                        self.gridNums[5] = int(str.rstrip(file.readline()))
            elif line == "PLAYERS":
                while line != "NEWBLOCK":
                    line = str.rstrip(file.readline())
                    if line == "NAMES:":
                        playerNames = str.rstrip(file.readline())
                        playerNames = playerNames.split(",")
                    elif line == "TYPE:":
                        playerTypes = str.rstrip(file.readline())
                        playerTypes = playerTypes.split(",")
                    elif line == "HITPOINTS:":
                        playerHitpoints = str.rstrip(file.readline())
                        playerHitpoints = playerHitpoints.split(",")
                    elif line == "SPEED:":
                        playerSpeed = str.rstrip(file.readline())
                        playerSpeed = playerSpeed.split(",")
                    elif line == "RANGE:":
                        playerRanges = str.rstrip(file.readline())
                        playerRanges = playerRanges.split(",")

            elif line == "ATTACKS":
                while line != "NEWBLOCK":
                    line = str.rstrip(file.readline())
                    if line == "NAMES:":
                        attackNames = str.rstrip(file.readline())
                        attackNames= attackNames.split(",")
                    elif line == "POWER:":
                        attackPowers = str.rstrip(file.readline())
                        attackPowers = attackPowers.split(",")
                    elif line == "AREA:":
                        attackAreas = str.rstrip(file.readline())
                        attackAreas = attackAreas.split(",")
                    elif line == "EFFECT:":
                        attackEffect = str.rstrip(file.readline())
                        attackEffect = attackEffect.split(",")
            elif line == "EFFECTS":
                while line != "NEWBLOCK":
                    line = str.rstrip(file.readline())
                    if line == "NAMES:":
                        effectNames = str.rstrip(file.readline())
                        effectNames = effectNames.split(",")
                    if line == "TYPE:":
                        effectTypes = str.rstrip(file.readline())
                        effectTypes = effectTypes.split(",")
                    if line == "POWER:":
                        effectPowers = str.rstrip(file.readline())
                        effectPowers = effectPowers.split(",")
            elif line == "TILENAMES":
                line = str.rstrip(file.readline())
                self.tileNames = line.split(",")
            elif line == "COLORS":
                colors = str.rstrip(file.readline())
                self.colors = colors.split(",")
            elif line == "STOP":
                read = False


            for i in range(len(playerTypes)):
                self.players.update({playerTypes[i]: (playerNames[i], playerHitpoints[i], playerSpeed[i], playerRanges[i])})

            for j in range(len(attackNames)):
                self.attacks.update({attackNames[j]: (attackPowers[j], attackAreas[j], attackEffect[j])})

            for k in range(len(effectNames)):
                self.effects.update({effectNames[k]: (effectPowers[k], effectTypes[k])})



    def get_players(self):
        return list(self.players.keys())

    def get_tile_names(self):
        return self.tileNames
    def get_player_info(self):
        return self.players

    def get_square_size(self):
       return self.gridNums[2]

    def get_gui_geometry(self):
        return self.gridNums[:2]

    def get_distance(self):
        return self.gridNums[4]

    def get_grid_size(self):
        return self.gridNums[3]

    def get_player_amount(self):
        return self.gridNums[5]
    def get_attacks(self):
        return list(self.attacks.keys())

    def get_effects(self):
        return list(self.effects.keys())

    def get_attack_info(self):
        return self.attacks

    def get_effect_info(self):
        return self.effects
    def get_player_colors(self):
        temp = []
        temp.append(self.colors[0])
        temp.append(self.colors[1])
        temp.append(self.colors[2])
        temp.append(self.colors[3])
        temp.append(self.colors[6])
        return temp

    def get_tile_colors(self):
        temp = []
        temp.append(self.colors[2])
        temp.append(self.colors[4])
        temp.append(self.colors[0])
        temp.append(self.colors[8])
        temp.append(self.colors[3])
        return temp

    def get_grid_colors(self):
        temp = []
        temp.append(self.colors[7])
        temp.append(self.colors[3])
        temp.append(self.colors[1])
        temp.append(self.colors[5])



