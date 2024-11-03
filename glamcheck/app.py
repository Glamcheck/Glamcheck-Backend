from fastapi import FastAPI
from .routers import auth_router,user_router,composition_router, recommendation_router

app = FastAPI()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(composition_router)
app.include_router(recommendation_router)
