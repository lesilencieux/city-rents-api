from dataclasses import dataclass

@dataclass
class City:
    avg_rent: float
    rate: float
    city: str
    postal_code: str
    population: int