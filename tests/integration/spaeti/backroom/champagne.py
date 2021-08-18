from spaeti import Beverage


class Champagne(Beverage):
    namespace = "spaeti.backroom"

    def __init__(self, volume=0.2):
        self.volume = volume
        self.abv = 12.0
