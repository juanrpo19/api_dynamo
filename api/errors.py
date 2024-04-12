from pynamodb.exceptions import QueryError
from graphql.error.syntax_error import GraphQLSyntaxError
from graphql.error import GraphQLError, graphql_error
from starlette.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from utils import Utils
import logging


class config:
    conf = Utils.load_config("config.json")


class CustomFatalError(Exception):
    def __init__(self, message, cause, code=None, params=None):
        """
            Instantiate the custom error class using your
            custom field(s)
        """
        super().__init__(message)
        self.message = str(message)
        self.cause = cause
        self.code = code
        self.params = params


def format_located_error(error):
    """
        Helper method to help error based on type comparison
    """
    if isinstance(error, HTTPException):
        logging.error('\nmessage: ' + error.detail + '\ncode: ' + str(error.status_code))
        return {
            'error': 'Error de conexión HTTP o no ha enviado una consulta válida',
            'message: ': error.detail,
            'code: ': error.status_code
        }

    if isinstance(error, QueryError):
        logging.error('\nmessage: ' + error.msg + '\ncode: ' + "1002")
        return {
            'error': 'Error interno en la consulta',
            'message': error.msg,
            'code': 1002
        }

    if isinstance(error, GraphQLSyntaxError):
        logging.error('\nmessage: ' + graphql_error.print_error(error) + '\ncode: ' + "1003")

        return {
            'error': 'La consulta falla por un error interno de validación (sintaxis, lógica , etc.)',
            'message': error.message,
            'code': 1003
        }

    if isinstance(error, GraphQLError):
        logging.error('\nmessage: ' + graphql_error.print_error(error) + '\ncode: ' + "1000")
        return {
            'error:': 'La consulta está mal formada',
            'message': error.message,
            'code': 1000
        }

    if isinstance(error, CustomFatalError):
        logging.error('\nmessage: ' + error.message + '\ncode: ' + "1004")
        return {
            'error': 'Las variables o el contexto proporcionados por el usuario son incorrectos y la función de resolución / suscripción intencionalmente genera un error (por ejemplo, no se le permite ver al usuario solicitado)',
            'message': error.message,
            'code': 1004
        }


# HTTP Error 400
async def server_error(request: Request, exc: HTTPException):
    logging.error('\nmessage: ' + str(exc) + '\ncode: ' + "400")
    return JSONResponse({
        'error': 'Error de conexión HTTP o no ha enviado una consulta válida',
        'message: ': str(exc),
        'code: ': 400
    }, status_code=400)
