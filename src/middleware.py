from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger("uvicorn.access")


def register_middleware(app: FastAPI):

    # Security first
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"]
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Logging middleware
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"

        message = (
            f"{client_host}:{client_port} "
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"{process_time:.4f}s"
        )

        logger.info(message)

        return response