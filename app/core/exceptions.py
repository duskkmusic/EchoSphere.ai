from fastapi import HTTPException, status


class DebateException(Exception):
    """Base exception for debate-related errors"""
    pass


class DocumentNotProcessedException(DebateException):
    """Raised when trying to use a document that hasn't been processed"""
    pass


class AgentNotFoundException(DebateException):
    """Raised when agent is not found"""
    pass


class DebateAlreadyStartedException(DebateException):
    """Raised when trying to start an already started debate"""
    pass


class InsufficientPermissionsException(HTTPException):
    """Raised when user doesn't have required permissions"""
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class ResourceNotFoundException(HTTPException):
    """Raised when a resource is not found"""
    def __init__(self, resource: str, resource_id: int | str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id {resource_id} not found"
        )


class ValidationException(HTTPException):
    """Raised when validation fails"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class RateLimitException(HTTPException):
    """Raised when rate limit is exceeded"""
    def __init__(self, limit: int):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {limit} requests per minute."
        )


class LLMException(Exception):
    """Raised when LLM API fails"""
    pass


class DocumentProcessingException(Exception):
    """Raised when document processing fails"""
    pass
