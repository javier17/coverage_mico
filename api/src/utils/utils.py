
from enum import Enum
from http import HTTPStatus


class ResponseTools:
    def map_response_code_to_type(response_code):
        response_ranges = {
            range(100, 400): ResponseType.SUCCESS,
            range(400, 600): ResponseType.ERROR,
        }

        for code_range, response_type in response_ranges.items():
            if response_code in code_range:
                return response_type

        return None

    def build_response(code=200, message=None, response=None, error_message=None):
        response_type = ResponseTools.map_response_code_to_type(code)

        if response_type is None:
            raise ValueError("Invalid response code")

        result = {
            "status": {
                "type": response_type.value,
                "code": code,
                "message": message or HTTPStatus(code).description,
                "errorMessage": error_message
            },
            "response": response
        }

        return result


class ResponseType(Enum):
    SUCCESS = "success"
    ERROR = "error"


