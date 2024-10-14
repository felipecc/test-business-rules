from pydantic import BaseModel, root_validator, model_validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime



class Condition(BaseModel):
    name: str
    operator: str
    value: Union[str | float]


class Action(BaseModel):
    name: str
    params: Dict[str, Any]  # Permite qualquer estrutura no dicionário 'params'


class AllConditions(BaseModel):
    all: List[Condition]


class Rule(BaseModel):
    conditions: AllConditions
    actions: List[Action]


class Carencia(BaseModel):
    dias: int
    vl_percentual: float


class CargoCarencia(BaseModel):
    cargo: str
    carencia: Dict[str, float]


class DiasTolerancia(BaseModel):
    dias: Dict[int, int]


class ListaCargoCarencia(BaseModel):
    cargos: List[CargoCarencia]


class Regra(BaseModel):
    id: int
    descricao: str
    regra: str
    cargo_carencia: List[CargoCarencia]
    dias_tolerancia: Union[Dict[int, int] | None]


class Oportunidade(BaseModel):
    oportunidade_id: str
    codigo_oportunidade: str
    ds_contrato_benner: str
    tp_status: str
    nm_vertical: str
    nm_regional: str
    dt_criacao: datetime
    dt_fechamento: datetime
    dt_estim_fechamento: datetime
    ds_porte: Optional[str] = None
    ds_tipo: str
    nm_razao_social: str
    nr_cnpj: Optional[str] = None
    nm_dono: Optional[str] = None
    nm_sponsor: Optional[str] = None
    nm_parceiro: Optional[str] = None
    ds_classificacao: str
    cd_item_oportunidade: str
    ds_item: str
    nm_vertical_item: str
    nr_quantidade: int
    nr_preco_unitario: float
    nr_preco_total: float
    nr_desconto: float
    nr_preco_total_desconto: float
    dt_modificacao_item: datetime
    dt_insert: datetime
    tp_venda: str
    tp_servico: str
    ds_primeira_parcela: Optional[str] = None


class OportunidadeNaoProcessada(BaseModel):
    oportunidade: Oportunidade
    motivo: str
    regra: str
    
class Recebimento(BaseModel):
    receita_master: str
    estrutura: str
    nf: int
    documentodigitado: int
    dataemissao: datetime
    contrato: str
    objeto_contrato: str
    documento: int
    documentocontabil: str
    item: str
    handle: int
    handle_item: int
    valortotal: float
    valor_liquido: float
    iss: Optional[int]
    base_valor_provisao: float
    data_atualizacao: str    

class Provisionamento(BaseModel):
    id: str
    estado: str
    empresa: str
    filiais: Optional[str]
    divisao_dre: Optional[str]
    codigo_cc: Optional[str]
    codigo: Optional[int]
    codigo_monitor: Optional[int]
    cliente: Optional[str]
    centro_custo: Optional[str]
    receita_master: Optional[str]
    estrutura: Optional[str]
    contrato: Optional[str]
    objetocontrato: Optional[str]
    documento: Optional[int]
    documento_contabil: Optional[str]
    item: Optional[str]
    handle: Optional[int]
    handle_item: int
    valor_total: Optional[float]
    valorliquido: Optional[float]
    iss: Optional[float]
    base_valor_provisao: Optional[float]
    apelido: Optional[str]
    dataatualizacao: Optional[str]
    tipo: Optional[str]
    nome_codigo: Optional[str]
    handle_contrato: Optional[int]
    
    
class RecebimentoDetalhado(BaseModel):
    id: int
    documento_id: Optional[int]
    doc_origem_id: Optional[int]
    documentonf: Optional[str]
    doc_numero_pedido: Optional[str]
    oportunidade: Optional[str]
    empresa: Optional[str]
    filial_id: Optional[int]
    filial: Optional[str]
    numero_nota: Optional[int]
    item_id: Optional[int]
    item: Optional[str]
    emissao: Optional[str]
    datacancelamento: Optional[datetime]
    datavencimento: Optional[datetime]
    datainclusao: Optional[datetime]
    dataliquidacao: Optional[datetime]
    data_da_baixa: Optional[datetime]
    codigo_cliente_portal_fin: Optional[int]
    codigo_cliente: Optional[int]
    nome_cliente: Optional[str]
    parcela_id: Optional[int]
    valor_faturado_bruto: Optional[str]
    valor_faturado_liquido: Optional[str]
    fator_do_item: Optional[str]
    valor_faturado_liquido_s_iss: Optional[str]
    valor_do_item: Optional[str]
    valor_parcela: Optional[str]
    valor_a_rec_por_item: Optional[str]
    aliquota_iss: Optional[str]
    valor_iss_da_parcela: Optional[str]
    valor_a_rec_por_item_s_iss: Optional[str]
    vl_recebido_bruto: Optional[str]
    vl_recebido_liquido: Optional[str]
    valor_recebido_por_item: Optional[str]
    valor_recebido_por_item_bruto: Optional[str]
    vl_juros_recebido: Optional[str]
    valor_rec_por_item_bruto_c_j: Optional[str]
    valor_base_comissao: Optional[str] 
    handle_item: int
    
    @model_validator(mode='before')
    @classmethod
    def validate_all_dates(cls, values):
        date_format = '%d/%m/%y'
        date_fields = ['datacancelamento', 'datavencimento', 'datainclusao', 'dataliquidacao','data_da_baixa']
        for field in date_fields:
            if field in values and isinstance(values[field], str):
                try:
                    values[field] = datetime.strptime(values[field], date_format)
                except ValueError:
                    raise ValueError(f"Invalid date format in '{field}': {values[field]}. Use 'dd/mm/yy' format.")
        
        return values
