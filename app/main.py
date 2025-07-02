from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.authorization.routes import router as auth_router
from app.database import create_db
from app.routes import router as test_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(test_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
