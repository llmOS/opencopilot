from starlette import status


class APIErrorResponse(Exception):
    """Base class for other exceptions"""

    def __init__(self):
        pass

    def to_status_code(self) -> status:
        raise NotImplementedError

    def to_code(self) -> str:
        raise NotImplementedError

    def to_message(self) -> str:
        raise NotImplementedError


InternalServerErrorCode = "internal_server_error"
InternalServerErrorMessage = (
    "The request could not be completed due to an " "internal server error."
)


class InternalServerAPIError(APIErrorResponse):
    """Raised when an internal server error occurs"""

    def __init__(self):
        pass

    def to_status_code(self) -> status:
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    def to_code(self) -> str:
        return InternalServerErrorCode

    def to_message(self) -> str:
        return InternalServerErrorMessage


class ValidationAPIError(APIErrorResponse):
    def __init__(self, param: str):
        self.param = param

    def to_status_code(self) -> status:
        return status.HTTP_422_UNPROCESSABLE_ENTITY

    def to_code(self) -> str:
        return "validation_error"

    def to_message(self) -> str:
        return f"Invalid parameter: {self.param}"


class NotFoundAPIError(APIErrorResponse):
    def __init__(self, resource: str):
        self.resource = resource

    def to_status_code(self) -> status:
        return status.HTTP_404_NOT_FOUND

    def to_code(self) -> str:
        return "not_found"

    def to_message(self) -> str:
        return f"{self.resource} not found."


class BadGatewayAPIError(APIErrorResponse):
    """Raised when an error occurs on the upstream server"""

    def __init__(self):
        pass

    def to_status_code(self) -> status:
        return status.HTTP_502_BAD_GATEWAY

    def to_code(self) -> str:
        return "bad_gateway"

    def to_message(self) -> str:
        return (
            "The request could not be completed due to the server "
            "receiving an invalid response from an inbound server it "
            "accessed while attempting to fulfill the request. "
            "Check if LLM is running."
        )


class OpenAIError(APIErrorResponse):
    def __init__(self, message):
        self.message = message

    def to_status_code(self) -> status:
        return status.HTTP_502_BAD_GATEWAY

    def to_code(self) -> str:
        return "openai_error"

    def to_message(self) -> str:
        return self.message


class WeaviateConnectionError(APIErrorResponse):
    def __init__(self, message):
        self.message = message

    def to_status_code(self) -> status:
        return status.HTTP_502_BAD_GATEWAY

    def to_code(self) -> str:
        return "weaviate_error"

    def to_message(self) -> str:
        return self.message


class LocalLLMConnectionError(APIErrorResponse):
    def __init__(self, message):
        self.message = message

    def to_status_code(self) -> status:
        return status.HTTP_502_BAD_GATEWAY

    def to_code(self) -> str:
        return "local_llm_error"

    def to_message(self) -> str:
        return self.message


class GenericCopilotRuntimeError(APIErrorResponse):
    def __init__(self, message):
        self.message = message

    def to_status_code(self) -> status:
        return status.HTTP_502_BAD_GATEWAY

    def to_code(self) -> str:
        return "copilot_error"

    def to_message(self) -> str:
        return self.message


class AuthorizationMissingAPIError(APIErrorResponse):
    def __init__(self):
        pass

    def to_status_code(self) -> status:
        return status.HTTP_401_UNAUTHORIZED

    def to_code(self) -> str:
        return "authorization_missing"

    def to_message(self) -> str:
        return f"Request is missing or has invalid 'Authorization' header."


class InvalidCredentialsAPIError(APIErrorResponse):
    def __init__(self):
        pass

    def to_status_code(self) -> status:
        return status.HTTP_401_UNAUTHORIZED

    def to_code(self) -> str:
        return "invalid_credentials"

    def to_message(self) -> str:
        return "Invalid credentials"


class ForbiddenAPIError(APIErrorResponse):
    def __init__(self):
        pass

    def to_status_code(self) -> status:
        return status.HTTP_403_FORBIDDEN

    def to_code(self) -> str:
        return "forbidden"

    def to_message(self) -> str:
        return "User does not have access rights to the content"
