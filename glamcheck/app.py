from fastapi import FastAPI

from glamcheck.routers import composition_router

from glamcheck.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(composition_router)
