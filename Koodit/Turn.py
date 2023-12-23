import random


class Turn():
    def __init__(self, gui):
        self.gui = gui


    def moves_first(self, player1, player2):
        if player1.get_speed() > player2.get_speed():
            self.gui.attacker = 0
        elif player2.get_speed() > player1.get_speed():
            self.gui.attacker = 1
        elif player1.get_speed() == player2.get_speed():
            chance = random.randint(0,10)
            if chance < 6:
                self.gui.attacker = 0
            else:
                self.gui.attacker = 1














