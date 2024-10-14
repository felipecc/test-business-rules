from datetime import datetime
import re
import json
from typing import Tuple

SEPARATOR = "#"


def create_name_rule(id: int, name: str) -> str:
    return f"{id}{SEPARATOR}{name}"


def extract_name_rule(name_rule: str) -> Tuple[int, str]:
    id, name = name_rule.split(SEPARATOR)

    return int(id), name


def parse_datetime(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')


def is_valid_json(jzon: str) -> bool:
    try:
        json.loads(jzon)
        return True
    except json.JSONDecodeError as err:
        print(f'JSONDecodeError: {err}')
        return False


def is_valid_date(data_test: str) -> bool:
    try:
        return bool(datetime.strptime(data_test, "%Y-%m-%d"))
    except ValueError:
        return False


def extract_numbers_from_text(number: str) -> int | None:
    match = re.match(r'\d+', number)
    if match:
        return int(match.group())
    return None

def text_without_breakline(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def read_oportunidades_from_csv(file_path: str) -> [any]:  # type: ignore
    oportunidades = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file, delimiter=";")
        for row in csv_reader:
            oportunidade = Oportunidade(
                oportunidade_id=row["OPORTUNIDADE_ID"],
                codigo_oportunidade=row["CODIGO_OPORTUNIDADE"],
                ds_contrato_benner=row["DS_CONTRATO_BENNER"],
                tp_status=row["TP_STATUS"],
                nm_vertical=row["NM_VERTICAL"],
                nm_regional=row["NM_REGIONAL"],
                dt_criacao=parse_datetime(row["DT_CRIACAO"]),
                dt_fechamento=parse_datetime(row["DT_FECHAMENTO"]),
                dt_estim_fechamento=parse_datetime(row["DT_ESTIM_FECHAMENTO"]),
                ds_porte=row["DS_PORTE"],
                ds_tipo=row["DS_TIPO"],
                nm_razao_social=row["NM_RAZAO_SOCIAL"],
                nr_cnpj=row["NR_CNPJ"],
                nm_dono=row["NM_DONO"],
                nm_sponsor=row["NM_SPONSOR"],
                nm_parceiro=row.get("NM_PARCEIRO"),  # Campo opcional
                ds_classificacao=row["DS_CLASSIFICACAO"],
                cd_item_oportunidade=row["CD_ITEM_OPORTUNIDADE"],
                ds_item=row["DS_ITEM"],
                nm_vertical_item=row["NM_VERTICAL_ITEM"],
                nr_quantidade=int(row["NR_QUANTIDADE"]),
                nr_preco_unitario=float(row["NR_PRECO_UNITARIO"]),
                nr_preco_total=float(row["NR_PRECO_TOTAL"]),
                nr_desconto=float(row["NR_DESCONTO"]),
                nr_preco_total_desconto=float(row["NR_PRECO_TOTAL_DESCONTO"]),
                dt_modificacao_item=parse_datetime(row["DT_MODIFICACAO_ITEM"]),
                dt_insert=parse_datetime(row["DT_INSERT"]),
                tp_venda=row["TP_VENDA"],
                tp_servico=row["TP_SERVICO"],
                ds_primeira_parcela=row["DS_PRIMEIRA_PARCELA"],
            )
            oportunidades.append(oportunidade)
    return oportunidades

