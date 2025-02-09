from fastapi import FastAPI

from glamcheck.routers import composition_router

app = FastAPI()

app.include_router(composition_router)
