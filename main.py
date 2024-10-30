from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers import (auth_router, contribution_router, department_router,
                         member_router, user_router)
from core import set_default_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    set_default_data()
    yield


app = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc', openapi_url='/api/openapi.json', lifespan=lifespan)

app.include_router(auth_router)
app.include_router(member_router)
app.include_router(user_router)
app.include_router(contribution_router)
app.include_router(department_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"APP": "Church Management System Backend Services"}
