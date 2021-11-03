from .beverage import Beverage


class Beer(Beverage):

    kind = "nicebeer"

    def __init__(self, volume=0.5):
        self.volume = volume
        self.abv = 5.0
