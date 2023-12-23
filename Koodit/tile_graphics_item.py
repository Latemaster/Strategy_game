from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6 import QtGui
from attack import Attack


class tileGraphicsItem(QGraphicsRectItem):
    def __init__(self, location, size, gui):
        super().__init__(location.get_x(), location.get_y(), size, size)
        self.location = location
        self.size = size
        self.setBrush(QtGui.QColor(255, 255, 255))
        self.gui = gui

    def mousePressEvent(self, event):
            if self.location.get_y() >= 0:
                self.gui.tile_clicked(int(self.location.get_x()/self.size), int(self.location.get_y()/self.size), 8)
                if self.gui.gameStarted:
                    self.setPen(QtGui.QPen(QtGui.QColor("Red")))
            else:
                if type(self.gui.selected_attack) is Attack:
                    self.gui.current_attack_area = self.gui.select_attack_area(self.gui.selected_attack, self.get_location())
                else:
                    print("Select Attack")
                    print(self.gui.selected_attack)


    def get_location(self):
        return self.location

