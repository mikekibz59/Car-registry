"""Error handling Module for ViewSet """

from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework.response import Response
from django.db.models import ObjectDoesNotExist


def _build_json_response(err) -> dict:
    json_response = dict()
    json_response['status'] = err.status_code
    json_response['message'] = str(err.detail[0]) if isinstance(
        err.detail, list) else str(err.detail)
    return json_response


def handle_error(function) -> Response:
    """Helper decorator for handling viewset errors """

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)

        except ParseError as err:
            data = _build_json_response(err)
            return Response(data, status=err.status_code)

        except NotFound as err:
            data = _build_json_response(err)
            return Response(data, status=err.status_code)

        except ValidationError as err:
            data = _build_json_response(err)
            return Response(data, status=err.status_code)

        except ObjectDoesNotExist as err:
            data = {'message': str(err), 'status': 404}
            return Response(data, status=404)

        except Exception:
            data = {'message': 'Something went wrong!',
                    'status': 500}
            return Response(data, status=500)

    return wrapper