class AcademyException(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)


class LessonNotFoundException(AcademyException):
    def __init__(self, slug: str):
        super().__init__(f"Lesson '{slug}' not found", {"slug": slug})


class MalformedLessonException(AcademyException):
    def __init__(self, path: str, reason: str):
        super().__init__(f"Malformed lesson at {path}: {reason}", {"path": path, "reason": reason})


class PipelineNotFoundException(AcademyException):
    def __init__(self, pipeline_id: int):
        super().__init__(f"Pipeline {pipeline_id} not found", {"pipeline_id": pipeline_id})


class PipelineExecutionException(AcademyException):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, details)


class AuthenticationException(AcademyException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)


class AuthorizationException(AcademyException):
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message)


class ValidationException(AcademyException):
    def __init__(self, message: str, errors: list | None = None):
        super().__init__(message, {"errors": errors or []})