from location import Location

class Attack():

    def __init__(self, name, gui):
        self.gui = gui
        self.name = name
        Info = self.gui.GameInfo.get_attack_info()
        power, area, effect = Info[name]
        self.set_attributes(power, area, effect)


    def get_name(self):
        return self.name
    def get_power(self):
        return self.power


    def set_attributes(self, power, area, effect):
        self.power = int(power)
        self.area = int(area)
        self.effect = int(effect)

    def get_hit_area(self, startPoint):
        hitTiles = []
        for i in range(self.area):
            for j in range(self.area):
                hitTiles.append(Location(int(startPoint.get_x())+i*50, int(startPoint.get_y())+j*50))
        return hitTiles

    def get_effect(self):
        return self.effect