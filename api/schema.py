import logging
import graphene
from datetime import datetime
from pytz import timezone
from pygraphene.types import PynamoObjectType

from db.models import PreaprobadosConsumoCombos , get_preaprobados_consumo_combos, LastEvaluatedKeyPreaprobadosConsumoCombos

from db.models import PreaprobadosComercial , get_preaprobados_comercial ,  LastEvaluatedKeyPreaprobadosComercial

from db.models import TdcTasasPortal , get_tdc_tasas_portal, LastEvaluatedKeyTdcTasasPortal



def getCrud():
    tzx = timezone("America/Bogota")
    modificacioncrudint = int(datetime.now(tzx).strftime("%Y%m%d%H%M%S"))
    return modificacioncrudint


class PreaprobadosConsumoCombosType(PynamoObjectType):
    class Meta:
        model = PreaprobadosConsumoCombos
     
class PreaprobadosConsumoCombos(graphene.ObjectType):
    total_count = graphene.Int(required=True)
    preaprobadosconsumocombos = graphene.List(PreaprobadosConsumoCombosType)



class PreaprobadosComercialType(PynamoObjectType):
    class Meta:
        model = PreaprobadosComercial

class PreaprobadosComercial(graphene.ObjectType):
    total_count = graphene.Int(required=True)
    preaprobadoscomercial = graphene.List(PreaprobadosComercialType)



class TdcTasasPortalType(PynamoObjectType):
    class Meta:
        model = TdcTasasPortal

class TdcTasasPortal(graphene.ObjectType):
    total_count = graphene.Int(required=True)
    tdctasasportal = graphene.List(TdcTasasPortalType)




class Query(graphene.ObjectType):
    preaprobados_consumo_combos = graphene.Field(PreaprobadosConsumoCombos, clave=graphene.String() , clave_ordenamiento=graphene.String(), limit=graphene.Int(), ascendente=graphene.Boolean(), last_evaluated_key= LastEvaluatedKeyPreaprobadosConsumoCombos())
    preaprobados_comercial = graphene.Field(PreaprobadosComercial, clave=graphene.String() , clave_ordenamiento=graphene.String(), limit=graphene.Int(), ascendente=graphene.Boolean(), last_evaluated_key= LastEvaluatedKeyPreaprobadosComercial())
    tdc_tasas_portal = graphene.Field(TdcTasasPortal, clave=graphene.String() , clave_ordenamiento=graphene.String(), limit=graphene.Int(), ascendente=graphene.Boolean(), last_evaluated_key= LastEvaluatedKeyTdcTasasPortal())
    status = graphene.String()


### Resolvers
    def resolve_status(self, info, **kwargs):
        return "Ok"


    def resolve_preaprobados_consumo_combos(self, info , clave , clave_ordenamiento = None ,limit = 100, ascendente = True, last_evaluated_key = None, **kwargs):
        complete = PreaprobadosConsumoCombos()

        if clave is not None:
            result = get_preaprobados_consumo_combos( clave , clave_ordenamiento, limit, ascendente, last_evaluated_key )
        else:
            result = None

        complete.total_count = len(result)
        complete.preaprobadosconsumocombos = result
        return complete



    def resolve_preaprobados_comercial(self, info , clave , clave_ordenamiento = None ,limit = 100, ascendente = True, last_evaluated_key = None, **kwargs):
        complete = PreaprobadosComercial()
        if clave is not None:
            result = get_preaprobados_comercial( clave , clave_ordenamiento, limit, ascendente, last_evaluated_key )
        else:
            result = None

        complete.total_count = len(result)
        complete.preaprobadoscomercial = result
        return complete



    def resolve_tdc_tasas_portal(self, info , clave , clave_ordenamiento = None ,limit = 100, ascendente = True, last_evaluated_key = None, **kwargs):
        complete = TdcTasasPortal()
        
        if clave is not None:
            result = get_tdc_tasas_portal( clave , clave_ordenamiento, limit, ascendente, last_evaluated_key )
        else:
            result = None

        complete.total_count = len(result)
        complete.tdctasasportal = result
        return complete





schema = graphene.Schema(query=Query, types=[   PreaprobadosConsumoCombosType, 
                                                PreaprobadosComercialType, 
                                                TdcTasasPortalType
                                            ])
