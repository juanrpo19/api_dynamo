from fastapi.responses import PlainTextResponse
from pytz import timezone
from datetime import datetime
from utils import Utils
import logging
from pydantic import BaseModel, conlist
from typing import Optional

from db.models import get_preaprobados_consumo_combos , PreaprobadosConsumoCombos , get_preaprobados_comercial , PreaprobadosComercial , get_tdc_tasas_portal , TdcTasasPortal

timeZone = timezone("America/Bogota")

class config:
    conf = Utils.load_config("config.json")

def get_time():
    return datetime.now(timeZone).strftime("%Y-%m-%d %H:%M:%S")

def get_empty():
    msg = "vrgo-api-alternativas-portal-cobranza " + get_time()
    logging.info("Endpoint request: " + msg)
    return PlainTextResponse(msg)

def availableMethods(request):
    return PlainTextResponse( "Métodos Disponibles: " + "get_preaprobados_consumo_combos , set_preaprobados_consumo_combos , del_preaprobados_consumo_combos , get_preaprobados_comercial , set_preaprobados_comercial , del_preaprobados_comercial , get_tdc_tasas_portal , set_tdc_tasas_portal , del_tdc_tasas_portal")

def getCrud():
    modificacioncrudint = int(datetime.now(timeZone).strftime("%Y%m%d%H%M%S"))
    return modificacioncrudint

def getTimeStamp():
    return datetime.now(timeZone).isoformat()

def getMeta(request, size):
    meta = {
        "_requestDateTime": getTimeStamp()
        , "_responseSize": size
    }
    return {k: v for k, v in meta.items() if v is not None}

def getError(e , status):
    cod = "SP" if status == 400 else "SA"
    ret = [
        {
            "code" : cod + str(status) + "vrgo-api-alternativas-portal-cobranza",
            "detail": str(e)

        }
    ]
    return ret

def getErrorResponse(status , e , request):
    ret = {
            "meta" : getMeta(request , None) ,
            "status" : status ,
            "title" : "BAD REQUEST" if status == 400 else "INTERNAL SERVER ERROR" ,            
            "errors" : getError(e , status)             
        }

    return ret

def jsonify(pynamObjectList):
    result = []
    for obj in pynamObjectList:
        try:
            current = {}
            for name , attr in obj.attribute_values.items():
                current[name] = attr
                
            result.append(current)
        except Exception as e:
            msg = "Error en la generación del objeto json de respuesta: " + str(e) + ", Objeto: " + str(obj)
            logging.error(msg)
            raise Exception(msg)

    return result

def get_limit_ascendente_lastEvaluatedKey(obj):
    limit = obj.get("limit", 100)
    ascendente =  obj.get("ascendente", True)
    last_evaluated_key =  obj.get("last_evaluated_key", None)
    return limit, ascendente, last_evaluated_key


class GetPreaprobadosConsumoCombos(BaseModel):
    clave: str
    clave_ordenamiento: Optional[str]
    limit: Optional[int]
    ascendente: Optional[bool]
    last_evaluated_key: Optional[str]


class GetPreaprobadosConsumoCombosData(BaseModel):
    data: conlist(GetPreaprobadosConsumoCombos, min_items=1)


def rest_get_preaprobados_consumo_combos(request: GetPreaprobadosConsumoCombosData):
    try:

        payload = request.dict(exclude_none=True)
        data = payload.get("data" , [])
        res = []
        ret = {}
        for obj in data:
            clave , clave_ordenamiento = get_keys_preaprobados_consumo_combos(obj)
            limit, ascendente, last_evaluated_key = get_limit_ascendente_lastEvaluatedKey( obj )
            result = get_preaprobados_consumo_combos( clave , clave_ordenamiento, limit, ascendente, last_evaluated_key)
            res = res + jsonify(result)

        ret["meta"] = getMeta(request, len(res))
        ret["data"] = res
        logging.info("Response Size: {0}".format(ret["meta"].get("_responseSize", 0)))
        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status, e, request)
        return ret



def rest_del_preaprobados_consumo_combos(request: GetPreaprobadosConsumoCombosData):
    try:

        payload = request.dict(exclude_none=True)
        data = payload.get("data" , [])
        res = []
        ret = {}
        modcrud = getCrud()
        for obj in data:

            clave , clave_ordenamiento = get_keys_preaprobados_consumo_combos(obj)
            limit, ascendente, last_evaluated_key = get_limit_ascendente_lastEvaluatedKey( obj )
            result = get_preaprobados_consumo_combos( clave , clave_ordenamiento , limit, ascendente, last_evaluated_key )

            for item in result:
                item.activo = 0
                item.modificacion_crud = modcrud
                item.save()
                res.append("{}".format( (item.clave , item.clave_ordenamiento) ))

        ret["meta"] = getMeta(request, len(res))
        ret["data"] = res
        logging.info("Response: {0}".format(ret))
        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status, e, request)
        return ret


class SetPreaprobadosConsumoCombos(BaseModel):
    clave: str
    clave_ordenamiento: str
    tipoid: Optional[str]
    id: Optional[str]
    nombre_cliente: Optional[str]
    segmento: Optional[str]
    ejecutivo: Optional[str]
    tel1: Optional[int]
    tel2: Optional[int]
    tel3: Optional[int]
    tel4: Optional[int]
    tel5: Optional[int]
    tel6: Optional[int]
    tel7: Optional[int]
    tel8: Optional[int]
    tel9: Optional[int]
    tel10: Optional[int]
    ciudad_contacto: Optional[str]
    cupo_asigando_crediagil: Optional[str]
    num_prestamo: Optional[float]
    valor_desembolso: Optional[float]
    tipo_plan: Optional[str]
    producto: Optional[str]
    plazo_actual: Optional[float]
    frecuencia_pago: Optional[str]
    tasa_namv: Optional[float]
    tipo_de_tasa: Optional[str]
    fecha_desembolso: Optional[str]
    fecha_vencimiento: Optional[str]
    nueva_fecha_vencimiento: Optional[str]
    saldo_neto: Optional[float]
    cuota_regular: Optional[float]
    cuota_incluye_seguro: Optional[str]
    cuota_fija_k: Optional[float]
    tipo_de_cuota: Optional[str]
    intereses_pendientes: Optional[float]
    saldo_sg_vida: Optional[float]
    fecha_prox_pago: Optional[str]
    nueva_fecha_prox_pago: Optional[str]
    fecha_ultimo_pago: Optional[str]
    num_cuotas_faltantes: Optional[int]
    plazo_min: Optional[int]
    plazo_max: Optional[int]
    ampliacion_plazo_meses: Optional[int]
    max_periodo_de_gracia_o_prorroga: Optional[int]
    meses_prorroga_elegidos: Optional[int]
    nuevo_plazo_total_en_meses: Optional[str]
    mes_pago_fng: Optional[str]
    monto_fng: Optional[str]
    mes_pago_comision_mipyme: Optional[str]
    monto_comision_mipyme: Optional[float]
    frec_mipyme: Optional[str]
    comision_mipyme_fng: Optional[str]
    cuota_anterior: Optional[float]
    vlr_cuota_actual: Optional[float]
    nueva_cuota_sin_otros_conceptos: Optional[str]
    nueva_cuota_a_capital: Optional[str]
    nueva_cuota_total: Optional[str]
    disminucion_de_cuota: Optional[str]
    nueva_cuota_sistema: Optional[str]
    marca_riesgos: Optional[str]
    genero: Optional[str]
    fecha_nacimiento: Optional[float]
    email_1: Optional[str]
    email_2: Optional[str]
    nueva_g: Optional[str]
    region: Optional[str]
    codigo_seg_vida: Optional[int]
    extraprima_seguro: Optional[float]
    factor_seguro: Optional[float]
    seguro_desempleo: Optional[float]
    prob: Optional[str]
    televentas_habeas_data: Optional[str]
    mail_habeas_data: Optional[str]
    sms_habeas_data: Optional[str]
    departamento: Optional[str]
    aliado: Optional[str]
    base: Optional[str]
    opcion_1: Optional[str]
    opcion_2: Optional[str]
    prioridad_creditos: Optional[int]
    fecha_proyprox_pago: Optional[float]
    redescuento: Optional[int]
    concepto_distribucion1: Optional[float]
    conector_distribucion1: Optional[str]
    concepto_distribucion2: Optional[float]
    conector_distribucion2: Optional[str]
    concepto_distribucion3: Optional[float]
    conector_distribucion3: Optional[str]
    concepto_distribucion4: Optional[float]
    conector_distribucion4: Optional[str]
    concepto_distribucion5: Optional[float]
    conector_distribucion5: Optional[str]
    concepto_distribucion6: Optional[float]
    conector_distribucion6: Optional[str]
    concepto_distribucion7: Optional[float]
    conector_distribucion7: Optional[str]
    concepto_distribucion8: Optional[float]
    conector_distribucion8: Optional[str]
    concepto_distribucion9: Optional[float]
    estado: Optional[str]
    base_aliados: Optional[str]
    nombre: Optional[str]
    grupo: Optional[str]
    perfil: Optional[str]
    cod_abogado: Optional[str]
    cod_abogado_para: Optional[str]
    dias_mora: Optional[int]
    nombre_para: Optional[str]
    grupo_para: Optional[str]
    perfil_para: Optional[str]
    cobro_juridico: Optional[str]
    fuente: Optional[str]
    cnt_dias_mora: Optional[float]
    consdocdeu: Optional[int]
    nueva_marca: Optional[str]
    venezolanos: Optional[str]
    canal_rpc_semana: Optional[str]
    exclusion_rpc: Optional[str]
    exclusion_lc: Optional[str]
    novedad: Optional[str]
    alternativa_aplicada_agr: Optional[str]
    marca_agrupada_rgo: Optional[str]
    producto_agrupado_origen: Optional[str]
    f_aplicacion: Optional[int]
    bpo: Optional[str]
    exclusion_alt: Optional[str]
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    activo: Optional[int]


class SetPreaprobadosConsumoCombosData(BaseModel):
    data: conlist(SetPreaprobadosConsumoCombos, min_items=1)


def rest_set_preaprobados_consumo_combos(request: SetPreaprobadosConsumoCombosData):
    try:

        payload = request.dict(exclude_none=True)
        lista = payload.get("data",[])
        ret = {}
        reslist = []
        modcrud = getCrud()
        for body in lista:
            try:
                newSet = PreaprobadosConsumoCombos()
        
                newSet.clave = body['clave']
                newSet.clave_ordenamiento = body['clave_ordenamiento']
                newSet.tipoid = body.get('tipoid',None)
                newSet.id = body.get('id',None)
                newSet.nombre_cliente = body.get('nombre_cliente',None)
                newSet.segmento = body.get('segmento',None)
                newSet.ejecutivo = body.get('ejecutivo',None)
                newSet.tel1 = body.get('tel1',None)
                newSet.tel2 = body.get('tel2',None)
                newSet.tel3 = body.get('tel3',None)
                newSet.tel4 = body.get('tel4',None)
                newSet.tel5 = body.get('tel5',None)
                newSet.tel6 = body.get('tel6',None)
                newSet.tel7 = body.get('tel7',None)
                newSet.tel8 = body.get('tel8',None)
                newSet.tel9 = body.get('tel9',None)
                newSet.tel10 = body.get('tel10',None)
                newSet.ciudad_contacto = body.get('ciudad_contacto',None)
                newSet.cupo_asigando_crediagil = body.get('cupo_asigando_crediagil',None)
                newSet.num_prestamo = body.get('num_prestamo',None)
                newSet.valor_desembolso = body.get('valor_desembolso',None)
                newSet.tipo_plan = body.get('tipo_plan',None)
                newSet.producto = body.get('producto',None)
                newSet.plazo_actual = body.get('plazo_actual',None)
                newSet.frecuencia_pago = body.get('frecuencia_pago',None)
                newSet.tasa_namv = body.get('tasa_namv',None)
                newSet.tipo_de_tasa = body.get('tipo_de_tasa',None)
                newSet.fecha_desembolso = body.get('fecha_desembolso',None)
                newSet.fecha_vencimiento = body.get('fecha_vencimiento',None)
                newSet.nueva_fecha_vencimiento = body.get('nueva_fecha_vencimiento',None)
                newSet.saldo_neto = body.get('saldo_neto',None)
                newSet.cuota_regular = body.get('cuota_regular',None)
                newSet.cuota_incluye_seguro = body.get('cuota_incluye_seguro',None)
                newSet.cuota_fija_k = body.get('cuota_fija_k',None)
                newSet.tipo_de_cuota = body.get('tipo_de_cuota',None)
                newSet.intereses_pendientes = body.get('intereses_pendientes',None)
                newSet.saldo_sg_vida = body.get('saldo_sg_vida',None)
                newSet.fecha_prox_pago = body.get('fecha_prox_pago',None)
                newSet.nueva_fecha_prox_pago = body.get('nueva_fecha_prox_pago',None)
                newSet.fecha_ultimo_pago = body.get('fecha_ultimo_pago',None)
                newSet.num_cuotas_faltantes = body.get('num_cuotas_faltantes',None)
                newSet.plazo_min = body.get('plazo_min',None)
                newSet.plazo_max = body.get('plazo_max',None)
                newSet.ampliacion_plazo_meses = body.get('ampliacion_plazo_meses',None)
                newSet.max_periodo_de_gracia_o_prorroga = body.get('max_periodo_de_gracia_o_prorroga',None)
                newSet.meses_prorroga_elegidos = body.get('meses_prorroga_elegidos',None)
                newSet.nuevo_plazo_total_en_meses = body.get('nuevo_plazo_total_en_meses',None)
                newSet.mes_pago_fng = body.get('mes_pago_fng',None)
                newSet.monto_fng = body.get('monto_fng',None)
                newSet.mes_pago_comision_mipyme = body.get('mes_pago_comision_mipyme',None)
                newSet.monto_comision_mipyme = body.get('monto_comision_mipyme',None)
                newSet.frec_mipyme = body.get('frec_mipyme',None)
                newSet.comision_mipyme_fng = body.get('comision_mipyme_fng',None)
                newSet.cuota_anterior = body.get('cuota_anterior',None)
                newSet.vlr_cuota_actual = body.get('vlr_cuota_actual',None)
                newSet.nueva_cuota_sin_otros_conceptos = body.get('nueva_cuota_sin_otros_conceptos',None)
                newSet.nueva_cuota_a_capital = body.get('nueva_cuota_a_capital',None)
                newSet.nueva_cuota_total = body.get('nueva_cuota_total',None)
                newSet.disminucion_de_cuota = body.get('disminucion_de_cuota',None)
                newSet.nueva_cuota_sistema = body.get('nueva_cuota_sistema',None)
                newSet.marca_riesgos = body.get('marca_riesgos',None)
                newSet.genero = body.get('genero',None)
                newSet.fecha_nacimiento = body.get('fecha_nacimiento',None)
                newSet.email_1 = body.get('email_1',None)
                newSet.email_2 = body.get('email_2',None)
                newSet.nueva_g = body.get('nueva_g',None)
                newSet.region = body.get('region',None)
                newSet.codigo_seg_vida = body.get('codigo_seg_vida',None)
                newSet.extraprima_seguro = body.get('extraprima_seguro',None)
                newSet.factor_seguro = body.get('factor_seguro',None)
                newSet.seguro_desempleo = body.get('seguro_desempleo',None)
                newSet.prob = body.get('prob',None)
                newSet.televentas_habeas_data = body.get('televentas_habeas_data',None)
                newSet.mail_habeas_data = body.get('mail_habeas_data',None)
                newSet.sms_habeas_data = body.get('sms_habeas_data',None)
                newSet.departamento = body.get('departamento',None)
                newSet.aliado = body.get('aliado',None)
                newSet.base = body.get('base',None)
                newSet.opcion_1 = body.get('opcion_1',None)
                newSet.opcion_2 = body.get('opcion_2',None)
                newSet.prioridad_creditos = body.get('prioridad_creditos',None)
                newSet.fecha_proyprox_pago = body.get('fecha_proyprox_pago',None)
                newSet.redescuento = body.get('redescuento',None)
                newSet.concepto_distribucion1 = body.get('concepto_distribucion1',None)
                newSet.conector_distribucion1 = body.get('conector_distribucion1',None)
                newSet.concepto_distribucion2 = body.get('concepto_distribucion2',None)
                newSet.conector_distribucion2 = body.get('conector_distribucion2',None)
                newSet.concepto_distribucion3 = body.get('concepto_distribucion3',None)
                newSet.conector_distribucion3 = body.get('conector_distribucion3',None)
                newSet.concepto_distribucion4 = body.get('concepto_distribucion4',None)
                newSet.conector_distribucion4 = body.get('conector_distribucion4',None)
                newSet.concepto_distribucion5 = body.get('concepto_distribucion5',None)
                newSet.conector_distribucion5 = body.get('conector_distribucion5',None)
                newSet.concepto_distribucion6 = body.get('concepto_distribucion6',None)
                newSet.conector_distribucion6 = body.get('conector_distribucion6',None)
                newSet.concepto_distribucion7 = body.get('concepto_distribucion7',None)
                newSet.conector_distribucion7 = body.get('conector_distribucion7',None)
                newSet.concepto_distribucion8 = body.get('concepto_distribucion8',None)
                newSet.conector_distribucion8 = body.get('conector_distribucion8',None)
                newSet.concepto_distribucion9 = body.get('concepto_distribucion9',None)
                newSet.estado = body.get('estado',None)
                newSet.base_aliados = body.get('base_aliados',None)
                newSet.nombre = body.get('nombre',None)
                newSet.grupo = body.get('grupo',None)
                newSet.perfil = body.get('perfil',None)
                newSet.cod_abogado = body.get('cod_abogado',None)
                newSet.cod_abogado_para = body.get('cod_abogado_para',None)
                newSet.dias_mora = body.get('dias_mora',None)
                newSet.nombre_para = body.get('nombre_para',None)
                newSet.grupo_para = body.get('grupo_para',None)
                newSet.perfil_para = body.get('perfil_para',None)
                newSet.cobro_juridico = body.get('cobro_juridico',None)
                newSet.fuente = body.get('fuente',None)
                newSet.cnt_dias_mora = body.get('cnt_dias_mora',None)
                newSet.consdocdeu = body.get('consdocdeu',None)
                newSet.nueva_marca = body.get('nueva_marca',None)
                newSet.venezolanos = body.get('venezolanos',None)
                newSet.canal_rpc_semana = body.get('canal_rpc_semana',None)
                newSet.exclusion_rpc = body.get('exclusion_rpc',None)
                newSet.exclusion_lc = body.get('exclusion_lc',None)
                newSet.novedad = body.get('novedad',None)
                newSet.alternativa_aplicada_agr = body.get('alternativa_aplicada_agr',None)
                newSet.marca_agrupada_rgo = body.get('marca_agrupada_rgo',None)
                newSet.producto_agrupado_origen = body.get('producto_agrupado_origen',None)
                newSet.f_aplicacion = body.get('f_aplicacion',None)
                newSet.bpo = body.get('bpo',None)
                newSet.exclusion_alt = body.get('exclusion_alt',None)
                newSet.activo = body.get('activo',1)
                newSet.year = body.get('year',None)
                newSet.month = body.get('month',None)
                newSet.day = body.get('day',None)
                newSet.modificacion_crud = modcrud
        
                newSet.save()
                reslist.append("OK")
            except Exception as e:
                reslist.append("Error: " + str(e))

        ret["meta"] = getMeta(request , len(reslist))
        ret["data"] = reslist
        logging.info("Response: {0}".format(ret))

        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return ret




def get_keys_preaprobados_consumo_combos( obj ):
    try:
        return obj['clave'] , obj.get('clave_ordenamiento', None)
    except Exception as e:
        msg = "Error en el envío de las llaves (HashKey Faltante): " + str(e) + ", Enviado:" + str(obj)
        logging.error(msg)
        raise Exception(msg)
    


class GetPreaprobadosComercial(BaseModel):
    clave: str
    clave_ordenamiento: Optional[str]
    limit: Optional[int]
    ascendente: Optional[bool]
    last_evaluated_key: Optional[str]


class GetPreaprobadosComercialData(BaseModel):
    data: conlist(GetPreaprobadosComercial, min_items=1)


def rest_get_preaprobados_comercial(request: GetPreaprobadosComercialData):
    try:

        payload = request.dict(exclude_none=True)
        data = payload.get("data" , [])
        res = []
        ret = {}
        for obj in data:
            clave , clave_ordenamiento = get_keys_preaprobados_comercial(obj)
            limit, ascendente, last_evaluated_key = get_limit_ascendente_lastEvaluatedKey( obj )
            result = get_preaprobados_comercial( clave , clave_ordenamiento, limit, ascendente, last_evaluated_key)
            res = res + jsonify(result)

        ret["meta"] = getMeta(request, len(res))
        ret["data"] = res
        logging.info("Response Size: {0}".format(ret["meta"].get("_responseSize", 0)))
        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status, e, request)
        return ret



def rest_del_preaprobados_comercial(request: GetPreaprobadosComercialData):
    try:

        payload = request.dict(exclude_none=True)
        data = payload.get("data" , [])
        res = []
        ret = {}
        modcrud = getCrud()
        for obj in data:

            clave , clave_ordenamiento = get_keys_preaprobados_comercial(obj)
            limit, ascendente, last_evaluated_key = get_limit_ascendente_lastEvaluatedKey( obj )
            result = get_preaprobados_comercial( clave , clave_ordenamiento , limit, ascendente, last_evaluated_key )

            for item in result:
                item.activo = 0
                item.modificacion_crud = modcrud
                item.save()
                res.append("{}".format( (item.clave , item.clave_ordenamiento) ))

        ret["meta"] = getMeta(request, len(res))
        ret["data"] = res
        logging.info("Response: {0}".format(ret))
        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status, e, request)
        return ret


class SetPreaprobadosComercial(BaseModel):
    clave: str
    clave_ordenamiento: str
    corte: Optional[int]
    tipo_id: Optional[int]
    nit_cliente: Optional[str]
    razon_social: Optional[str]
    segmento: Optional[str]
    nro_operacion: Optional[str]
    prorroga: Optional[str]
    plazomax_prorroga: Optional[int]
    ampl_cons: Optional[str]
    plazomin_ampl_cons: Optional[int]
    plazomax_ampl_cons: Optional[int]
    ampl_pg_cons: Optional[str]
    plazomin_ampl_pg_cons: Optional[int]
    plazomax_ampl_pg_cons: Optional[int]
    ampl_mod: Optional[str]
    plazomin_ampl_mod: Optional[int]
    plazomax_ampl_mod: Optional[int]
    ampl_pg_mod: Optional[str]
    plazomin_ampl_pg_mod: Optional[int]
    plazomax_ampl_pg_mod: Optional[int]
    ampl_reest: Optional[str]
    plazomin_ampl_reest: Optional[int]
    plazomax_ampl_reest: Optional[int]
    ampl_pg_reest: Optional[str]
    plazomin_ampl_pg_reest: Optional[int]
    plazomax_ampl_pg_reest: Optional[int]
    bin: Optional[int]
    descripcion_bin: Optional[str]
    cupo_minimo: Optional[float]
    id_preaprobado: Optional[str]
    mpio_exp_cc_cliente: Optional[str]
    dpto_exp_cc_cliente: Optional[str]
    subsegmento: Optional[str]
    saldo_obligacion: Optional[float]
    plan: Optional[str]
    avales: Optional[str]
    desc_tipo_gtia: Optional[str]
    clave_larga: Optional[str]
    clave_corta: Optional[str]
    asignacion: Optional[str]
    control_pr: Optional[int]
    tipo_preaprobado: Optional[str]
    nivel_alerta: Optional[str]
    afectacion: Optional[str]
    linea_redescuento: Optional[str]
    of_gte: Optional[int]
    calife_actual: Optional[str]
    ciiucenie: Optional[int]
    saldo_cliente: Optional[float]
    calife: Optional[str]
    califintmodred: Optional[str]
    califi_real: Optional[str]
    max_mora_cli: Optional[int]
    endeudamiento: Optional[float]
    marca_026: Optional[str]
    altmora: Optional[float]
    apl: Optional[str]
    fdesem: Optional[str]
    vdesem: Optional[float]
    seg_cuota_fut: Optional[float]
    fecha_venc_def: Optional[str]
    f_prox_pago: Optional[str]
    plazo: Optional[int]
    gerenciado: Optional[str]
    pcons: Optional[str]
    regcons: Optional[str]
    sector: Optional[str]
    subsector: Optional[str]
    producto: Optional[str]
    fondo: Optional[str]
    obl341: Optional[str]
    tipo_de_tasa: Optional[str]
    tasa: Optional[float]
    tasa_anterior: Optional[float]
    id_rep_legal: Optional[int]
    mpio_exp_cc_rep_legal: Optional[str]
    dpto_exp_cc_rep_legal: Optional[str]
    nombre_cli_rep: Optional[str]
    marca_preaprobado: Optional[str]
    marca_garantia: Optional[str]
    tipo_de_amortizacion: Optional[str]
    tipo_cuota: Optional[str]
    tipo_tasa: Optional[str]
    tamano_empresa: Optional[str]
    nombre_garantia: Optional[str]
    tipo_moneda: Optional[int]
    bajo_monto: Optional[str]
    desc_tipo_fondo: Optional[str]
    proximo_pago: Optional[float]
    plan_desembolso: Optional[str]
    paquete_consolidacion: Optional[str]
    proceso_agil_consolidacion_pasivos: Optional[str]
    cuenta: Optional[str]
    saldo_capital: Optional[float]
    cuotas_faltantes: Optional[int]
    periodo_de_gracia_restante: Optional[str]
    spread: Optional[float]
    periodicidad_pago: Optional[str]
    modalidad: Optional[str]
    intereses_acumulados: Optional[float]
    otros_conceptos_acumulados: Optional[float]
    tasa_seguro_anual: Optional[float]
    cod_base_seg_vida: Optional[str]
    valor_desembolso_para_seg_vida: Optional[float]
    mes_pago_fng: Optional[str]
    porcent_comision_fng: Optional[float]
    mes_pago_fag: Optional[str]
    porcent_comision_fag: Optional[float]
    saldo_total_vencido: Optional[float]
    saldo_capital_vencido: Optional[float]
    saldo_interes_cte_vencido: Optional[float]
    saldo_interes_mora_causados: Optional[float]
    saldo_int_mora_en_susp_causac: Optional[float]
    saldo_seguros_vencidos: Optional[float]
    saldo_otros_seguros: Optional[float]
    comision_exp: Optional[float]
    iva_exp: Optional[float]
    vlr_obligacion: Optional[float]
    pago_min_cons: Optional[float]
    consdocdeu: Optional[int]
    nombre_usuario_dueno_tarea: Optional[str]
    cod_abogado: Optional[str]
    nombre_abogado: Optional[str]
    grupo_abogado: Optional[str]
    perfil_abogado: Optional[str]
    organizacion: Optional[float]
    pagares_a_consolidar: Optional[str]
    fecha1_pror: Optional[str]
    fecha2_pror: Optional[str]
    fecha3_pror: Optional[str]
    dtf_ta: Optional[float]
    ibr_namv: Optional[float]
    ibr_natv: Optional[float]
    ibr_nasv: Optional[float]
    ipc_vm: Optional[float]
    ipc_vac: Optional[float]
    ipc_va: Optional[float]
    id_embargo: Optional[str]
    descripcion_gestion: Optional[str]
    codigo_aprobador: Optional[str]
    f_gestion_cobdigit: Optional[str]
    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    activo: Optional[int]


class SetPreaprobadosComercialData(BaseModel):
    data: conlist(SetPreaprobadosComercial, min_items=1)


def rest_set_preaprobados_comercial(request: SetPreaprobadosComercialData):
    try:

        payload = request.dict(exclude_none=True)
        lista = payload.get("data",[])
        ret = {}
        reslist = []
        modcrud = getCrud()
        for body in lista:
            try:
                newSet = PreaprobadosComercial()
        
                newSet.clave = body['clave']
                newSet.clave_ordenamiento = body['clave_ordenamiento']
                newSet.corte = body.get('corte',None)
                newSet.tipo_id = body.get('tipo_id',None)
                newSet.nit_cliente = body.get('nit_cliente',None)
                newSet.razon_social = body.get('razon_social',None)
                newSet.segmento = body.get('segmento',None)
                newSet.nro_operacion = body.get('nro_operacion',None)
                newSet.prorroga = body.get('prorroga',None)
                newSet.plazomax_prorroga = body.get('plazomax_prorroga',None)
                newSet.ampl_cons = body.get('ampl_cons',None)
                newSet.plazomin_ampl_cons = body.get('plazomin_ampl_cons',None)
                newSet.plazomax_ampl_cons = body.get('plazomax_ampl_cons',None)
                newSet.ampl_pg_cons = body.get('ampl_pg_cons',None)
                newSet.plazomin_ampl_pg_cons = body.get('plazomin_ampl_pg_cons',None)
                newSet.plazomax_ampl_pg_cons = body.get('plazomax_ampl_pg_cons',None)
                newSet.ampl_mod = body.get('ampl_mod',None)
                newSet.plazomin_ampl_mod = body.get('plazomin_ampl_mod',None)
                newSet.plazomax_ampl_mod = body.get('plazomax_ampl_mod',None)
                newSet.ampl_pg_mod = body.get('ampl_pg_mod',None)
                newSet.plazomin_ampl_pg_mod = body.get('plazomin_ampl_pg_mod',None)
                newSet.plazomax_ampl_pg_mod = body.get('plazomax_ampl_pg_mod',None)
                newSet.ampl_reest = body.get('ampl_reest',None)
                newSet.plazomin_ampl_reest = body.get('plazomin_ampl_reest',None)
                newSet.plazomax_ampl_reest = body.get('plazomax_ampl_reest',None)
                newSet.ampl_pg_reest = body.get('ampl_pg_reest',None)
                newSet.plazomin_ampl_pg_reest = body.get('plazomin_ampl_pg_reest',None)
                newSet.plazomax_ampl_pg_reest = body.get('plazomax_ampl_pg_reest',None)
                newSet.bin = body.get('bin',None)
                newSet.descripcion_bin = body.get('descripcion_bin',None)
                newSet.cupo_minimo = body.get('cupo_minimo',None)
                newSet.id_preaprobado = body.get('id_preaprobado',None)
                newSet.mpio_exp_cc_cliente = body.get('mpio_exp_cc_cliente',None)
                newSet.dpto_exp_cc_cliente = body.get('dpto_exp_cc_cliente',None)
                newSet.subsegmento = body.get('subsegmento',None)
                newSet.saldo_obligacion = body.get('saldo_obligacion',None)
                newSet.plan = body.get('plan',None)
                newSet.avales = body.get('avales',None)
                newSet.desc_tipo_gtia = body.get('desc_tipo_gtia',None)
                newSet.clave_larga = body.get('clave_larga',None)
                newSet.clave_corta = body.get('clave_corta',None)
                newSet.asignacion = body.get('asignacion',None)
                newSet.control_pr = body.get('control_pr',None)
                newSet.tipo_preaprobado = body.get('tipo_preaprobado',None)
                newSet.nivel_alerta = body.get('nivel_alerta',None)
                newSet.afectacion = body.get('afectacion',None)
                newSet.linea_redescuento = body.get('linea_redescuento',None)
                newSet.of_gte = body.get('of_gte',None)
                newSet.calife_actual = body.get('calife_actual',None)
                newSet.ciiucenie = body.get('ciiucenie',None)
                newSet.saldo_cliente = body.get('saldo_cliente',None)
                newSet.calife = body.get('calife',None)
                newSet.califintmodred = body.get('califintmodred',None)
                newSet.califi_real = body.get('califi_real',None)
                newSet.max_mora_cli = body.get('max_mora_cli',None)
                newSet.endeudamiento = body.get('endeudamiento',None)
                newSet.marca_026 = body.get('marca_026',None)
                newSet.altmora = body.get('altmora',None)
                newSet.apl = body.get('apl',None)
                newSet.fdesem = body.get('fdesem',None)
                newSet.vdesem = body.get('vdesem',None)
                newSet.seg_cuota_fut = body.get('seg_cuota_fut',None)
                newSet.fecha_venc_def = body.get('fecha_venc_def',None)
                newSet.f_prox_pago = body.get('f_prox_pago',None)
                newSet.plazo = body.get('plazo',None)
                newSet.gerenciado = body.get('gerenciado',None)
                newSet.pcons = body.get('pcons',None)
                newSet.regcons = body.get('regcons',None)
                newSet.sector = body.get('sector',None)
                newSet.subsector = body.get('subsector',None)
                newSet.producto = body.get('producto',None)
                newSet.fondo = body.get('fondo',None)
                newSet.obl341 = body.get('obl341',None)
                newSet.tipo_de_tasa = body.get('tipo_de_tasa',None)
                newSet.tasa = body.get('tasa',None)
                newSet.tasa_anterior = body.get('tasa_anterior',None)
                newSet.id_rep_legal = body.get('id_rep_legal',None)
                newSet.mpio_exp_cc_rep_legal = body.get('mpio_exp_cc_rep_legal',None)
                newSet.dpto_exp_cc_rep_legal = body.get('dpto_exp_cc_rep_legal',None)
                newSet.nombre_cli_rep = body.get('nombre_cli_rep',None)
                newSet.marca_preaprobado = body.get('marca_preaprobado',None)
                newSet.marca_garantia = body.get('marca_garantia',None)
                newSet.tipo_de_amortizacion = body.get('tipo_de_amortizacion',None)
                newSet.tipo_cuota = body.get('tipo_cuota',None)
                newSet.tipo_tasa = body.get('tipo_tasa',None)
                newSet.tamano_empresa = body.get('tamano_empresa',None)
                newSet.nombre_garantia = body.get('nombre_garantia',None)
                newSet.tipo_moneda = body.get('tipo_moneda',None)
                newSet.bajo_monto = body.get('bajo_monto',None)
                newSet.desc_tipo_fondo = body.get('desc_tipo_fondo',None)
                newSet.proximo_pago = body.get('proximo_pago',None)
                newSet.plan_desembolso = body.get('plan_desembolso',None)
                newSet.paquete_consolidacion = body.get('paquete_consolidacion',None)
                newSet.proceso_agil_consolidacion_pasivos = body.get('proceso_agil_consolidacion_pasivos',None)
                newSet.cuenta = body.get('cuenta',None)
                newSet.saldo_capital = body.get('saldo_capital',None)
                newSet.cuotas_faltantes = body.get('cuotas_faltantes',None)
                newSet.periodo_de_gracia_restante = body.get('periodo_de_gracia_restante',None)
                newSet.spread = body.get('spread',None)
                newSet.periodicidad_pago = body.get('periodicidad_pago',None)
                newSet.modalidad = body.get('modalidad',None)
                newSet.intereses_acumulados = body.get('intereses_acumulados',None)
                newSet.otros_conceptos_acumulados = body.get('otros_conceptos_acumulados',None)
                newSet.tasa_seguro_anual = body.get('tasa_seguro_anual',None)
                newSet.cod_base_seg_vida = body.get('cod_base_seg_vida',None)
                newSet.valor_desembolso_para_seg_vida = body.get('valor_desembolso_para_seg_vida',None)
                newSet.mes_pago_fng = body.get('mes_pago_fng',None)
                newSet.porcent_comision_fng = body.get('porcent_comision_fng',None)
                newSet.mes_pago_fag = body.get('mes_pago_fag',None)
                newSet.porcent_comision_fag = body.get('porcent_comision_fag',None)
                newSet.saldo_total_vencido = body.get('saldo_total_vencido',None)
                newSet.saldo_capital_vencido = body.get('saldo_capital_vencido',None)
                newSet.saldo_interes_cte_vencido = body.get('saldo_interes_cte_vencido',None)
                newSet.saldo_interes_mora_causados = body.get('saldo_interes_mora_causados',None)
                newSet.saldo_int_mora_en_susp_causac = body.get('saldo_int_mora_en_susp_causac',None)
                newSet.saldo_seguros_vencidos = body.get('saldo_seguros_vencidos',None)
                newSet.saldo_otros_seguros = body.get('saldo_otros_seguros',None)
                newSet.comision_exp = body.get('comision_exp',None)
                newSet.iva_exp = body.get('iva_exp',None)
                newSet.vlr_obligacion = body.get('vlr_obligacion',None)
                newSet.pago_min_cons = body.get('pago_min_cons',None)
                newSet.consdocdeu = body.get('consdocdeu',None)
                newSet.nombre_usuario_dueno_tarea = body.get('nombre_usuario_dueno_tarea',None)
                newSet.cod_abogado = body.get('cod_abogado',None)
                newSet.nombre_abogado = body.get('nombre_abogado',None)
                newSet.grupo_abogado = body.get('grupo_abogado',None)
                newSet.perfil_abogado = body.get('perfil_abogado',None)
                newSet.organizacion = body.get('organizacion',None)
                newSet.pagares_a_consolidar = body.get('pagares_a_consolidar',None)
                newSet.fecha1_pror = body.get('fecha1_pror',None)
                newSet.fecha2_pror = body.get('fecha2_pror',None)
                newSet.fecha3_pror = body.get('fecha3_pror',None)
                newSet.dtf_ta = body.get('dtf_ta',None)
                newSet.ibr_namv = body.get('ibr_namv',None)
                newSet.ibr_natv = body.get('ibr_natv',None)
                newSet.ibr_nasv = body.get('ibr_nasv',None)
                newSet.ipc_vm = body.get('ipc_vm',None)
                newSet.ipc_vac = body.get('ipc_vac',None)
                newSet.ipc_va = body.get('ipc_va',None)
                newSet.id_embargo = body.get('id_embargo',None)
                newSet.descripcion_gestion = body.get('descripcion_gestion',None)
                newSet.codigo_aprobador = body.get('codigo_aprobador',None)
                newSet.f_gestion_cobdigit = body.get('f_gestion_cobdigit',None)
                newSet.activo = body.get('activo',1)
                newSet.year = body.get('year',None)
                newSet.month = body.get('month',None)
                newSet.day = body.get('day',None)
                newSet.modificacion_crud = modcrud
        
                newSet.save()
                reslist.append("OK")
            except Exception as e:
                reslist.append("Error: " + str(e))

        ret["meta"] = getMeta(request , len(reslist))
        ret["data"] = reslist
        logging.info("Response: {0}".format(ret))

        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return ret




def get_keys_preaprobados_comercial( obj ):
    try:
        return obj['clave'] , obj.get('clave_ordenamiento', None)
    except Exception as e:
        msg = "Error en el envío de las llaves (HashKey Faltante): " + str(e) + ", Enviado:" + str(obj)
        logging.error(msg)
        raise Exception(msg)
    


class GetTdcTasasPortal(BaseModel):
    clave: str
    clave_ordenamiento: Optional[str]
    limit: Optional[int]
    ascendente: Optional[bool]
    last_evaluated_key: Optional[str]


class GetTdcTasasPortalData(BaseModel):
    data: conlist(GetTdcTasasPortal, min_items=1)


def rest_get_tdc_tasas_portal(request: GetTdcTasasPortalData):
    try:

        payload = request.dict(exclude_none=True)
        data = payload.get("data" , [])
        res = []
        ret = {}
        for obj in data:
            clave , clave_ordenamiento = get_keys_tdc_tasas_portal(obj)
            limit, ascendente, last_evaluated_key = get_limit_ascendente_lastEvaluatedKey( obj )
            result = get_tdc_tasas_portal( clave , clave_ordenamiento, limit, ascendente, last_evaluated_key)
            res = res + jsonify(result)

        ret["meta"] = getMeta(request, len(res))
        ret["data"] = res
        logging.info("Response Size: {0}".format(ret["meta"].get("_responseSize", 0)))
        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status, e, request)
        return ret



def rest_del_tdc_tasas_portal(request: GetTdcTasasPortalData):
    try:

        payload = request.dict(exclude_none=True)
        data = payload.get("data" , [])
        res = []
        ret = {}
        modcrud = getCrud()
        for obj in data:

            clave , clave_ordenamiento = get_keys_tdc_tasas_portal(obj)
            limit, ascendente, last_evaluated_key = get_limit_ascendente_lastEvaluatedKey( obj )
            result = get_tdc_tasas_portal( clave , clave_ordenamiento , limit, ascendente, last_evaluated_key )

            for item in result:
                item.activo = 0
                item.modificacion_crud = modcrud
                item.save()
                res.append("{}".format( (item.clave , item.clave_ordenamiento) ))

        ret["meta"] = getMeta(request, len(res))
        ret["data"] = res
        logging.info("Response: {0}".format(ret))
        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status, e, request)
        return ret


class SetTdcTasasPortal(BaseModel):
    clave: str
    clave_ordenamiento: str
    ingestion_year: Optional[int]
    ingestion_month: Optional[int]
    ingestion_day: Optional[int]
    costumer_number: Optional[str]
    tipo_id_cliente: Optional[str]
    id_cliente: Optional[str]
    nombre_cliente: Optional[str]
    tipo_id_amparador: Optional[str]
    id_amparador: Optional[str]
    nombre_amparador: Optional[str]
    organizacion: Optional[float]
    cuenta: Optional[str]
    estado_cuenta: Optional[str]
    block_code_1: Optional[str]
    block_code_2: Optional[str]
    dias_mora: Optional[float]
    tarjeta: Optional[str]
    bin: Optional[str]
    ultimos_4_numeros: Optional[str]
    franquicia: Optional[str]
    estado_tarjeta: Optional[str]
    block_code_tarjeta: Optional[str]
    ciclo: Optional[float]
    fecha_ultimo_corte: Optional[str]
    fecha_limite_de_pago: Optional[str]
    fecha_proximo_corte: Optional[str]
    dias_proximo_corte: Optional[float]
    transaciones_suspendidas: Optional[float]
    monto_transaciones_suspendidas: Optional[float]
    deuda_total: Optional[float]
    comisiones_deuda_total: Optional[float]
    intereses_deuda_total: Optional[float]
    suma_comisiones_intereses_deuda_total: Optional[float]
    capital_deuda_total: Optional[float]
    tasa_ponderada_deuda_total: Optional[float]
    tasa_pareto_deuda_total: Optional[float]
    codigo_transaccion_deuda_total: Optional[str]
    pago_minimo_pendiente: Optional[float]
    comisiones_pago_minimo_pendiente: Optional[float]
    intereses_pago_minimo_pendiente: Optional[float]
    suma_comisiones_intereses_pago_minimo_pendiente: Optional[float]
    capital_pago_minimo_pendiente: Optional[float]
    tasa_ponderada_pago_minimo: Optional[float]
    tasa_pareto_pago_minimo: Optional[float]
    codigo_transaccion_pago_minimo: Optional[str]
    plazo_maximo: Optional[str]
    plazo_rango: Optional[str]
    fecha_registro: Optional[str]
    hora_registro: Optional[str]
    fecha_saldos: Optional[str]
    fecha_reg: Optional[float]
    tasa_politica: Optional[float]
    year: Optional[int]
    month: Optional[int]
    activo: Optional[int]


class SetTdcTasasPortalData(BaseModel):
    data: conlist(SetTdcTasasPortal, min_items=1)


def rest_set_tdc_tasas_portal(request: SetTdcTasasPortalData):
    try:

        payload = request.dict(exclude_none=True)
        lista = payload.get("data",[])
        ret = {}
        reslist = []
        modcrud = getCrud()
        for body in lista:
            try:
                newSet = TdcTasasPortal()
        
                newSet.clave = body['clave']
                newSet.clave_ordenamiento = body['clave_ordenamiento']
                newSet.ingestion_year = body.get('ingestion_year',None)
                newSet.ingestion_month = body.get('ingestion_month',None)
                newSet.ingestion_day = body.get('ingestion_day',None)
                newSet.costumer_number = body.get('costumer_number',None)
                newSet.tipo_id_cliente = body.get('tipo_id_cliente',None)
                newSet.id_cliente = body.get('id_cliente',None)
                newSet.nombre_cliente = body.get('nombre_cliente',None)
                newSet.tipo_id_amparador = body.get('tipo_id_amparador',None)
                newSet.id_amparador = body.get('id_amparador',None)
                newSet.nombre_amparador = body.get('nombre_amparador',None)
                newSet.organizacion = body.get('organizacion',None)
                newSet.cuenta = body.get('cuenta',None)
                newSet.estado_cuenta = body.get('estado_cuenta',None)
                newSet.block_code_1 = body.get('block_code_1',None)
                newSet.block_code_2 = body.get('block_code_2',None)
                newSet.dias_mora = body.get('dias_mora',None)
                newSet.tarjeta = body.get('tarjeta',None)
                newSet.bin = body.get('bin',None)
                newSet.ultimos_4_numeros = body.get('ultimos_4_numeros',None)
                newSet.franquicia = body.get('franquicia',None)
                newSet.estado_tarjeta = body.get('estado_tarjeta',None)
                newSet.block_code_tarjeta = body.get('block_code_tarjeta',None)
                newSet.ciclo = body.get('ciclo',None)
                newSet.fecha_ultimo_corte = body.get('fecha_ultimo_corte',None)
                newSet.fecha_limite_de_pago = body.get('fecha_limite_de_pago',None)
                newSet.fecha_proximo_corte = body.get('fecha_proximo_corte',None)
                newSet.dias_proximo_corte = body.get('dias_proximo_corte',None)
                newSet.transaciones_suspendidas = body.get('transaciones_suspendidas',None)
                newSet.monto_transaciones_suspendidas = body.get('monto_transaciones_suspendidas',None)
                newSet.deuda_total = body.get('deuda_total',None)
                newSet.comisiones_deuda_total = body.get('comisiones_deuda_total',None)
                newSet.intereses_deuda_total = body.get('intereses_deuda_total',None)
                newSet.suma_comisiones_intereses_deuda_total = body.get('suma_comisiones_intereses_deuda_total',None)
                newSet.capital_deuda_total = body.get('capital_deuda_total',None)
                newSet.tasa_ponderada_deuda_total = body.get('tasa_ponderada_deuda_total',None)
                newSet.tasa_pareto_deuda_total = body.get('tasa_pareto_deuda_total',None)
                newSet.codigo_transaccion_deuda_total = body.get('codigo_transaccion_deuda_total',None)
                newSet.pago_minimo_pendiente = body.get('pago_minimo_pendiente',None)
                newSet.comisiones_pago_minimo_pendiente = body.get('comisiones_pago_minimo_pendiente',None)
                newSet.intereses_pago_minimo_pendiente = body.get('intereses_pago_minimo_pendiente',None)
                newSet.suma_comisiones_intereses_pago_minimo_pendiente = body.get('suma_comisiones_intereses_pago_minimo_pendiente',None)
                newSet.capital_pago_minimo_pendiente = body.get('capital_pago_minimo_pendiente',None)
                newSet.tasa_ponderada_pago_minimo = body.get('tasa_ponderada_pago_minimo',None)
                newSet.tasa_pareto_pago_minimo = body.get('tasa_pareto_pago_minimo',None)
                newSet.codigo_transaccion_pago_minimo = body.get('codigo_transaccion_pago_minimo',None)
                newSet.plazo_maximo = body.get('plazo_maximo',None)
                newSet.plazo_rango = body.get('plazo_rango',None)
                newSet.fecha_registro = body.get('fecha_registro',None)
                newSet.hora_registro = body.get('hora_registro',None)
                newSet.fecha_saldos = body.get('fecha_saldos',None)
                newSet.fecha_reg = body.get('fecha_reg',None)
                newSet.tasa_politica = body.get('tasa_politica',None)
                newSet.year = body.get('year',None)
                newSet.month = body.get('month',None)
                newSet.activo = body.get('activo',1)
                newSet.modificacion_crud = modcrud
        
                newSet.save()
                reslist.append("OK")
            except Exception as e:
                reslist.append("Error: " + str(e))

        ret["meta"] = getMeta(request , len(reslist))
        ret["data"] = reslist
        logging.info("Response: {0}".format(ret))

        return ret

    except Exception as e:
        status = 400
        ret = getErrorResponse(status , e , request)
        return ret




def get_keys_tdc_tasas_portal( obj ):
    try:
        return obj['clave'] , obj.get('clave_ordenamiento', None)
    except Exception as e:
        msg = "Error en el envío de las llaves (HashKey Faltante): " + str(e) + ", Enviado:" + str(obj)
        logging.error(msg)
        raise Exception(msg)
    


