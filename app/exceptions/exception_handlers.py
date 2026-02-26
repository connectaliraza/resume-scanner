from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import ResumeProcessingError


async def resume_processing_exception_handler(
    request: Request, exc: ResumeProcessingError
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "error_code": exc.status_code},
    )
