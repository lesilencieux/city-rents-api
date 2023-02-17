import pydantic



class RentModel(pydantic.BaseModel):
    dep: int
    area: int
    price: float


class RentReturnModel(pydantic.BaseModel):
    total: int
    cities: list
    