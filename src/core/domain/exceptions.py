"""Domain-specific exceptions."""


class DomainException(Exception):
    """Base class for domain exceptions."""

    def __init__(self, code: str, message: str, details: str = ""):
        """Initialize the exception.

        Args:
            code: Error code.
            message: Error message.
            details: Additional details.
        """
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class InvalidCoordinatesError(DomainException):
    """Exception for invalid coordinates."""

    def __init__(self, details: str = ""):
        super().__init__(
            code="INVALID_COORDINATES",
            message="Latitude must be between -90 and 90, longitude between -180 and 180.",
            details=details
        )


class InvalidDateError(DomainException):
    """Exception for invalid date."""

    def __init__(self, details: str = ""):
        super().__init__(
            code="INVALID_DATE",
            message="Invalid date format. Use YYYY-MM-DD.",
            details=details
        )


class CalculationError(DomainException):
    """Exception for calculation errors."""

    def __init__(self, details: str = ""):
        super().__init__(
            code="CALCULATION_ERROR",
            message="Error calculating astrological data.",
            details=details
        )