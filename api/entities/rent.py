from dataclasses import dataclass

@dataclass
class Rent:
    id_zone: int
    insee: int
    ville: str
    dep: int
    avg_rent: float