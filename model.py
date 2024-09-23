from pydantic import BaseModel
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
