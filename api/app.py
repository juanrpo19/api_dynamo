from fastapi import FastAPI, status
from starlette_graphene3 import GraphQLApp
import sys

from api.schema import schema
from api.errors import format_located_error, server_error
from api.middleware import DisableIntrospectionMiddleware

from api.views import get_empty
from api.views import rest_get_preaprobados_consumo_combos, rest_del_preaprobados_consumo_combos, rest_set_preaprobados_consumo_combos, rest_get_preaprobados_comercial, rest_del_preaprobados_comercial, rest_set_preaprobados_comercial, rest_get_tdc_tasas_portal, rest_del_tdc_tasas_portal, rest_set_tdc_tasas_portal
from api.views import GetPreaprobadosConsumoCombosData, SetPreaprobadosConsumoCombosData, GetPreaprobadosComercialData, SetPreaprobadosComercialData, GetTdcTasasPortalData, SetTdcTasasPortalData


def create_app():
    exception_handlers = {
        500: server_error
    }

    app = FastAPI(exception_handlers=exception_handlers)
    app.add_route("/graphql", GraphQLApp(schema=schema, error_formatter=format_located_error,
                                         middleware=[DisableIntrospectionMiddleware]))

    # REST
    @app.get("/health")
    async def read_main():
        return status.HTTP_200_OK

    @app.get('/')
    async def root():
        return get_empty()

    # @app.post('/get_preaprobados_consumo_combos')
    # async def get_preaprobados_consumo_combos(request: GetPreaprobadosConsumoCombosData):
    #     return rest_get_preaprobados_consumo_combos(request)

    # @app.post('/del_preaprobados_consumo_combos')
    # async def del_preaprobados_consumo_combos(request: GetPreaprobadosConsumoCombosData):
    #     return rest_del_preaprobados_consumo_combos(request)

    # @app.post('/set_preaprobados_consumo_combos')
    # async def set_preaprobados_consumo_combos(request: SetPreaprobadosConsumoCombosData):
    #     return rest_set_preaprobados_consumo_combos(request)

    # @app.post('/get_preaprobados_comercial')
    # async def get_preaprobados_comercial(request: GetPreaprobadosComercialData):
    #     return rest_get_preaprobados_comercial(request)

    # @app.post('/del_preaprobados_comercial')
    # async def del_preaprobados_comercial(request: GetPreaprobadosComercialData):
    #     return rest_del_preaprobados_comercial(request)

    # @app.post('/set_preaprobados_comercial')
    # async def set_preaprobados_comercial(request: SetPreaprobadosComercialData):
    #     return rest_set_preaprobados_comercial(request)

    # @app.post('/get_tdc_tasas_portal')
    # async def get_tdc_tasas_portal(request: GetTdcTasasPortalData):
    #     return rest_get_tdc_tasas_portal(request)

    # @app.post('/del_tdc_tasas_portal')
    # async def del_tdc_tasas_portal(request: GetTdcTasasPortalData):
    #     return rest_del_tdc_tasas_portal(request)

    # @app.post('/set_tdc_tasas_portal')
    # async def set_tdc_tasas_portal(request: SetTdcTasasPortalData):
    #     return rest_set_tdc_tasas_portal(request)


    @app.on_event("startup")
    async def startup_event():
        import signal
        signal.signal(signal.SIGINT, receive_signal)
        # startup tasks

    return app

def receive_signal(signalNumber, frame):
    print('Received:', signalNumber)
    sys.exit()