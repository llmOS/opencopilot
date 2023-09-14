import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from opencopilot.domain.errors import CopilotRuntimeError
from opencopilot.domain.errors import LocalLLMRuntimeError
from opencopilot.domain.errors import OpenAIRuntimeError
from opencopilot.domain.errors import WeaviateRuntimeError
from opencopilot.logger import api_logger
from opencopilot.service.error_responses import APIErrorResponse
from opencopilot.service.error_responses import GenericCopilotRuntimeError
from opencopilot.service.error_responses import LocalLLMConnectionError
from opencopilot.service.error_responses import OpenAIError
from opencopilot.service.error_responses import WeaviateConnectionError
from opencopilot.service.middleware import util
from opencopilot.service.middleware.entities import RequestStateKey
from opencopilot.utils.http_headers import add_response_headers

logger = api_logger.get()


class MainMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        request_id = util.get_state(request, RequestStateKey.REQUEST_ID)
        ip_address = util.get_state(request, RequestStateKey.IP_ADDRESS)
        country = util.get_state(request, RequestStateKey.COUNTRY)
        try:
            logger.info(
                f"REQUEST STARTED "
                f"request_id={request_id} "
                f"request_path={request.url.path} "
                f"ip={ip_address} "
                f"country={country} "
            )
            before = time.time()
            response: Response = await call_next(request)

            duration = time.time() - before
            process_time = (time.time() - before) * 1000
            formatted_process_time = "{0:.2f}".format(process_time)
            if response.status_code != 404:
                logger.info(
                    f"REQUEST COMPLETED "
                    f"request_id={request_id} "
                    f"request_path={request.url.path} "
                    f"completed_in={formatted_process_time}ms "
                    f"status_code={response.status_code}"
                )
            return await _get_response_with_headers(response, duration)
        except OpenAIRuntimeError as exc:
            raise OpenAIError(exc.message) from exc
        except WeaviateRuntimeError as exc:
            raise WeaviateConnectionError(exc.message) from exc
        except LocalLLMRuntimeError as exc:
            raise LocalLLMConnectionError(exc.message) from exc
        except CopilotRuntimeError as exc:
            raise GenericCopilotRuntimeError(exc.message) from exc
        except Exception as error:
            if isinstance(error, APIErrorResponse):
                is_exc_info = error.to_status_code() == 500
                logger.error(
                    f"Error while handling request. request_id={request_id} "
                    f"request_path={request.url.path}"
                    f"status code={error.to_status_code()}"
                    f"code={error.to_code()}"
                    f"message={error.to_message()}",
                    exc_info=is_exc_info,
                )
            else:
                logger.error(
                    f"Error while handling request. request_id={request_id} "
                    f"request_path={request.url.path}",
                    exc_info=True,
                )
            raise error


async def _get_response_with_headers(response, duration):
    response = await add_response_headers(response, duration)
    return response
