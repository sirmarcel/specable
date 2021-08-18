from unittest import TestCase

from pathlib import Path
import sys

sys.path.append(Path() / "spaeti")

import spaeti


class TestIntegration(TestCase):
    def setUp(self):
        self.beer_dict = {"spaeti/beer": {"volume": 0.5}}
        self.lemonade_dict = {"outdoor/lemonade": {"volume": 0.3}}
        self.champagne_dict = {"spaeti.backroom/champagne": {"volume": 0.25}}

    def test_works(self):
        beer = spaeti.from_dict(self.beer_dict)
        beer2 = spaeti.Beer(volume=0.5)

        self.assertEqual(beer.drink(), beer2.drink())

    def test_default_namespace(self):
        beer = spaeti.from_dict({"beer": {"volume": 0.5}})

        self.assertEqual(beer.to_dict(), self.beer_dict)

    def test_roundtrip(self):
        self.assertEqual(self.beer_dict, spaeti.from_dict(self.beer_dict).to_dict())
        self.assertEqual(
            self.lemonade_dict, spaeti.from_dict(self.lemonade_dict).to_dict()
        )
        self.assertEqual(
            self.champagne_dict, spaeti.from_dict(self.champagne_dict).to_dict()
        )

    def test_from_yaml(self):
        beer = spaeti.from_yaml("beer.yaml")
        self.assertEqual(beer.to_dict(), spaeti.from_dict(self.beer_dict).to_dict())

    def test_yaml_roundtrip(self):
        champagne = spaeti.from_dict(self.champagne_dict)

        spaeti.to_yaml("champagne.yaml", champagne)
        champagne2 = spaeti.from_yaml("champagne.yaml")

        self.assertEqual(champagne2.to_dict(), champagne.to_dict())
