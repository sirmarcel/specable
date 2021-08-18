from .beverage import Beverage


class Beer(Beverage):
    def __init__(self, volume=0.5):
        self.volume = volume
        self.abv = 5.0
