import logging
from logging.config import dictConfig
from fastapi import FastAPI
from conf.log_config import LogConfig

from routes.rent import rent_router


dictConfig(LogConfig().dict())
logger = logging.getLogger("api_logs")

# FastApi app
app = FastAPI(
        debug=True,
        title="Rent search API docs",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redocs",
        version="1.0.0",
        description="",
)


app.include_router(rent_router)