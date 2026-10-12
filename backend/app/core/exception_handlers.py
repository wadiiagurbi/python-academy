from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AcademyException,
    LessonNotFoundException,
    MalformedLessonException,
    PipelineNotFoundException,
    PipelineExecutionException,
    AuthenticationException,
    AuthorizationException,
    ValidationException,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AcademyException)
    async def academy_exception_handler(request: Request, exc: AcademyException):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if isinstance(exc, (LessonNotFoundException, PipelineNotFoundException)):
            status_code = status.HTTP_404_NOT_FOUND
        elif isinstance(exc, AuthenticationException):
            status_code = status.HTTP_401_UNAUTHORIZED
        elif isinstance(exc, AuthorizationException):
            status_code = status.HTTP_403_FORBIDDEN
        elif isinstance(exc, (MalformedLessonException, ValidationException)):
            status_code = status.HTTP_400_BAD_REQUEST
        elif isinstance(exc, PipelineExecutionException):
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        return JSONResponse(
            status_code=status_code,
            content={"error": {"message": exc.message, "details": exc.details}},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        if request.url.path.startswith("/api/"):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": {"message": "Internal server error", "details": {}}},
            )
        raise exc