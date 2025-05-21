from fastapi import FastAPI
from routers import client_router, address_router, product_router
from contextlib import asynccontextmanager
from orm import sessionmanager
from config import Config
import uvicorn
import logging
import sys


# Configure logging to output to stdout
# Set log level based on Config.DEBUG_LOGS:
# - If DEBUG_LOGS is True, set level to DEBUG for detailed logs
# - If DEBUG_LOGS is False, set level to INFO for standard logs
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if Config.DEBUG_LOGS else logging.INFO)


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
app.include_router(client_router)
app.include_router(address_router)
app.include_router(product_router)

# Health check endpoint for aws load balancer
@app.get("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
