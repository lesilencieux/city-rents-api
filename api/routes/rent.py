import logging
from fastapi import APIRouter, Body, Depends, status

from controllers.rent import RentController
from model.rent import (
    RentReturnModel,
    RentModel,
)

logger = logging.getLogger("api_logs")

rent_router = APIRouter(prefix="/api/v1")


@rent_router.post(
    "/search", status_code=status.HTTP_200_OK, response_model=RentReturnModel
)
async def search_location(
    rent_data: RentModel,
    rent_controller=Depends(RentController),
):
    return await rent_controller.search_rent(rent_data)
