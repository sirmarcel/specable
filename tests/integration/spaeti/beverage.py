from specable import Specable


class Beverage(Specable):
    def get_dict(self):
        return {"volume": self.volume}

    def drink(self):
        """Return ml of pure ethanol consumed."""

        return self.volume * (self.abv / 100.0) * 1000
