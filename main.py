from fastapi import FastAPI
from app.routes.route import router

app = FastAPI(title='service BI')
app.include_router(router)