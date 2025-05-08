import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import blossom_exceptions
import logging
from typing import List


# Configure logging to display error messages with timestamps and severity levels
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):
    """
    Registers custom exception handlers with the FastAPI application.
    
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    @app.exception_handler(blossom_exceptions.AppError)
    async def base_custom_error_handler(request: Request, exc: blossom_exceptions.AppError):
        """
        Handles all exceptions that inherit from AppError.
        
        Args:
            request (Request): The incoming request.
            exc (AppError): The exception instance.
        
        Returns:
            JSONResponse: A JSON response with error details.
        """
        logger.error(
            f"Exception occurred while processing request: {request.url.path} | "
            f"{exc.__class__.__name__}: {exc.message}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.__dict__()
        )
    

class Boot:
    """
    Bootstraps the FastAPI application by registering exception handlers and validating environment variables.
    
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.setup()

    def setup(self):
        """
        Sets up the application by registering exception handlers and validating environment variables during startup.
        """
        @self.app.on_event("startup")
        async def startup_event():
            try:
                register_exception_handlers(self.app)
                logger.info("Bootstrapping completed successfully.")
            except blossom_exceptions.AppError as e:
                logger.critical(f"Bootstrapping failed: {e.message}")
                # Optionally, re-raise the exception to prevent the app from starting
                raise e
