from specable import Interface

from .beverage import Beverage
from .beer import Beer

drinks = [Beer]

clerk = Interface("spaeti", "drinks")
from_dict = clerk.from_dict
from_yaml = clerk.from_yaml
to_yaml = clerk.to_yaml
