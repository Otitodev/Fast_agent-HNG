from fastapi import HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional, List
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None

class AppException(Exception):
    """Base exception class for application-specific exceptions"""
    def __init__(self, message: str, status_code: int, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)

class LLMServiceError(AppException):
    """Raised when there's an error with the LLM service"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )

class ValidationError(AppException):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )

class NotFoundError(AppException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )

async def http_exception_handler(request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            details={"type": exc.__class__.__name__}
        ).dict()
    )

async def app_exception_handler(request, exc: AppException):
    """Handle custom application exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.message,
            details=exc.details
        ).dict()
    )

async def validation_exception_handler(request, exc: RequestValidationError):
    """Handle request validation errors"""
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"]) or "request"
        errors.append(f"{field}: {error['msg']}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation error",
            details={"errors": errors}
        ).dict()
    )

async def generic_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="An unexpected error occurred",
            details={
                "type": exc.__class__.__name__,
                "message": str(exc)
            }
        ).dict()
    )
