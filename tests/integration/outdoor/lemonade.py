from spaeti import Beverage


class Lemonade(Beverage):
    def __init__(self, volume=0.4):
        self.volume = volume
        self.abv = 0.0
