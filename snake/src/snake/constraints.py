from dataclasses import dataclass


@dataclass
class Constraints:
    mapWidth: int
    mapHeight: int
    portalBorder: bool
