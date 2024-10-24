from fastapi import FastAPI
from routers.router_data import router_data
from routers.router_metadata import router_metadata
from routers.router_analytics import router

app = FastAPI()
app.include_router(router_metadata)
app.include_router(router_data)
app.include_router(router)