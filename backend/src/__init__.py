from fastapi import FastAPI
from src.auth.routes import auth_router
from src.rds.routes import rds_router
from src.dbops.routes import dbops_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import register_all_errors
from .middleware import register_middleware
#from src.config import Config

@asynccontextmanager
async def lifespan(api:FastAPI):
    print(f"Server is starting ...")
    await init_db()
    yield
    print(f"Server has been stopped..")

version = "v1"

api = FastAPI(
    title = "DbDash - Dashboard",
    description = "Dashborad for Managing RDS instances.",
    version = version,
    lifespan = lifespan
)

register_all_errors(api)
register_middleware(api)

# Serve uploaded files
#api.mount(Config.FILE_DIRECTORY_DP_EXPOSE, StaticFiles(directory=Config.FILE_DIRECTORY_DP), name="profile")


api.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
api.include_router(rds_router, prefix=f"/api/{version}/aws", tags=["aws"])
api.include_router(dbops_router, prefix=f"/api/{version}/dbops", tags=["dbops"])
