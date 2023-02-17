import logging
from fastapi import Depends

from model.rent import RentReturnModel, RentModel
from services.rent import RentService

logger = logging.getLogger("api_logs")

class RentController:
    def __init__(
        self,
        rent_service : RentService = Depends(RentService),
    ):
        self.rent_service: RentService = rent_service

    async def search_rent(self, rent_data: RentModel) -> RentReturnModel:
        logger.info(rent_data)
        rent_data = rent_data.dict()
        rent_repositories =  await self.rent_service.search_rent(rent_data)
        rent = [repository for repository in rent_repositories]
        total= len(rent)
        return {"total": total, "cities": rent}
