from fastapi import FastAPI
from routers import addresses_router, clients_router
from contextlib import asynccontextmanager
from myOrm.database import sessionmanager
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(addresses_router)
app.include_router(clients_router)

# Health check endpoint for aws load balancer
@app.get("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
