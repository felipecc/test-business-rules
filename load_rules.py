import sqlite3
from datetime import date, datetime
from utils import text_without_breakline

# rule_dummy = """
#  {"function_name": "calculo_percentual_cargo",
#   "filter":
#    [{"name": "vertical",
#     "operator": "equal_to",
#     "value" : "Hospitalar"},
#     {"name": "contrato",
#     "operator": "equal_to",
#     "value" : "Cliente Novo"},
#     {"name": "evento",
#     "operator": "equal_to",
#     "value" : "Licença de Uso"}]
# }
# """

# cargo_carencia_dymmy = """
# {"cargos": [{"cargo":"Gerente Comercial","carencia":{"0":0.01,"30":0.05,"60":0.04,"90":0.03,"120":0.02}},
# {"cargo":"Executivo Contas","carencia":{
#     "0":0.02,"30":0.05,"60":0.04,"90":0.03,"120":0.02}},
# {"cargo":"Executivo Negocios","carencia":{
#     "0":0.002,"30":0.05,"60":0.04,"90":0.03,"120":0.02}},
# {"cargo":"Coordenador Comercial","carencia":{"0":0.007,"30":0.05,"60":0.04,"90":0.03,"120":0.02}}]}
# """



conn = sqlite3.connect("example.db")
cursor = conn.cursor()

def insert(
    nome: str,
    tipo: str,
    funcao_filtro: str,
    cargo_carencia: str,
    inicio_vigencia: str,
    fim_vigencia: str,
    dias_tolerancia: str = None
) -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS regra (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        tipo TEXT,
        data_criacao DATE,
        data_publicacao DATE,
        funcao_filtro TEXT,
        cargo_carencia TEXT,
        inicio_vigencia DATE,
        fim_vigencia DATE,
        dias_tolerancia TEXT)
    """)

    cursor.execute(
        """
    INSERT INTO regra (nome, tipo, data_criacao, data_publicacao, funcao_filtro, cargo_carencia, inicio_vigencia, fim_vigencia, dias_tolerancia)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            nome,
            tipo,
            datetime.now(),
            datetime.now(),
            funcao_filtro,
            cargo_carencia,
            inicio_vigencia,
            fim_vigencia,
            dias_tolerancia,
        ),
    )

    conn.commit()

# Hospitalar Regra

hospitalar_licenca_uso_filtro = """
 {"function_name": "calculo_percentual_cargo",
  "filter":
   [{"name": "vertical",
    "operator": "equal_to",
    "value" : "Hospitalar"},
    {"name": "evento",
    "operator": "equal_to",
    "value" : "Licença de Uso"}]
}
"""
hospitalar_licenca_uso_cargo_carencia = """
{"cargos": [
{"cargo":"Gerente Comercial","carencia":{"0":0.01}},
{"cargo":"Executivo Contas","carencia":{"0":0.02}},
{"cargo":"Executivo Negocios","carencia":{"0":0.002}},
{"cargo":"Coordenador Comercial","carencia":{"0":0.007}}]}
"""

hospitalar_outsourcing_filtro = """
 {"function_name": "calculo_percentual_cargo",
  "filter":
   [{"name": "vertical",
    "operator": "equal_to",
    "value" : "Hospitalar"},
    {"name": "evento",
    "operator": "equal_to",
    "value" : "Outsourcing"}]
}
"""

hospitalar_outsourcing_cargo_carencia = """
{"cargos": [
{"cargo":"Gerente Comercial","carencia":{"0":0}},
{"cargo":"Executivo Contas","carencia":{"0":0.12}},
{"cargo":"Executivo Negocios","carencia":{"0":0}},
{"cargo":"Coordenador Comercial","carencia":{"0":0}}]}
"""

hospitalar_servico_filtro = """
 {"function_name": "calculo_percentual_cargo",
  "filter":
   [{"name": "vertical",
    "operator": "equal_to",
    "value" : "Hospitalar"},
    {"name": "evento",
    "operator": "equal_to",
    "value" : "Serviços"}]
}
"""

hospitalar_servico_cargo_carencia = """
{"cargos": [
{"cargo":"Gerente Comercial","carencia":{"0":0.01}},
{"cargo":"Executivo Contas","carencia":{"0":0.02}},
{"cargo":"Executivo Negocios","carencia":{"0":0.002}},
{"cargo":"Coordenador Comercial","carencia":{"0":0.007}}]}
"""


hospitalar_servico_customizacao_filtro = """
 {"function_name": "calculo_percentual_cargo",
  "filter":
   [{"name": "vertical",
    "operator": "equal_to",
    "value" : "Hospitalar"},
    {"name": "evento",
    "operator": "equal_to",
    "value" : "Customização"}]
}
"""

hospitalar_servico_customizacao_cargo_carencia = """
{"cargos": [
{"cargo":"Gerente Comercial","carencia":{"0":0.01}},
{"cargo":"Executivo Contas","carencia":{"0":0.02}},
{"cargo":"Executivo Negocios","carencia":{"0":0.002}},
{"cargo":"Coordenador Comercial","carencia":{"0":0.007}}]}
"""


hospitalar_manutencao_filtro = """
 {"function_name": "calculo_percentual_cargo",
  "filter":
   [{"name": "vertical",
    "operator": "equal_to",
    "value" : "Hospitalar"},
    {"name": "evento",
    "operator": "equal_to",
    "value" : "Manutenção"}]
}
"""

hospitalar_manutencao_cargo_carencia = """
{"cargos": [
{"cargo":"Gerente Comercial","carencia":{"0":0.06,"30":0.05,"60":0.04,"90":0.03,"120":0.02,"150":0.0175,"180":0.0150,"210":0.0125,"240":0.01,"270":0.0075,"300":0.005,"330":0.0025,"360":0.0}},
{"cargo":"Executivo Contas","carencia":{"0":0.06,"30":0.05,"60":0.04,"90":0.03,"120":0.02,"150":0.0175,"180":0.0150,"210":0.0125,"240":0.01,"270":0.0075,"300":0.005,"330":0.0025,"360":0.0}},
{"cargo":"Executivo Negocios","carencia":{"0":0.0,"30":0.0,"60":0.0,"90":0.0,"120":0.0,"150":0.0,"180":0.0,"210":0.0,"240":0.0,"270":0.0,"300":0.0,"330":0.0,"360":0.0}},
{"cargo":"Coordenador Comercial","carencia":{"0":0.0,"30":0.0,"60":0.0,"90":0.0,"120":0.0,"150":0.0,"180":0.0,"210":0.0,"240":0.0,"270":0.0,"300":0.0,"330":0.0,"360":0.0}}]}
"""


hospitalar_locacao_filtro = """
 {"function_name": "calculo_percentual_cargo",
  "filter":
   [{"name": "vertical",
    "operator": "equal_to",
    "value" : "Hospitalar"},
    {"name": "evento",
    "operator": "equal_to",
    "value" : "Locacao"}]
}
"""

hospitalar_locacao_cargo_carencia = """
{"cargos": [
{"cargo":"Gerente Comercial","carencia":{"0":0.12,"30":0.10,"60":0.08,"90":0.06,"120":0.04,"150":0.0350,"180":0.03,"210":0.0250,"240":0.02,"270":0.0150,"300":0.01,"330":0.005,"360":0.0}},
{"cargo":"Executivo Contas","carencia":{"0":0.12,"30":0.10,"60":0.08,"90":0.06,"120":0.04,"150":0.0350,"180":0.03,"210":0.0250,"240":0.02,"270":0.0150,"300":0.01,"330":0.005,"360":0.0}},
{"cargo":"Executivo Negocios","carencia":{"0":0.0240,"30":0.02,"60":0.0160,"90":0.0120,"120":0.008,"150":0.007,"180":0.006,"210":0.005,"240":0.004,"270":0.003,"300":0.002,"330":0.001,"360":0.0}},
{"cargo":"Coordenador Comercial","carencia":{"0":0.0840,"30":0.07,"60":0.0560,"90":0.420,"120":0.028,"150":0.0245,"180":0.0210,"210":0.0175,"240":0.0140,"270":0.0105,"300":0.0070,"330":0.0035,"360":0.0}}]}
"""


def insert_hospitalar_licenca_uso():
    insert(
        nome="Hospitalar Licença de Uso",
        tipo="padrao",
        funcao_filtro=text_without_breakline(hospitalar_licenca_uso_filtro),
        cargo_carencia=text_without_breakline(hospitalar_licenca_uso_cargo_carencia),
        inicio_vigencia="2024-01-01",
        fim_vigencia="2024-12-31"
    )

def insert_hospitalar_outsourcing():
    insert(
        nome="Hospitalar Outsourcing",
        tipo="padrao",
        funcao_filtro=text_without_breakline(hospitalar_outsourcing_filtro),
        cargo_carencia=text_without_breakline(hospitalar_outsourcing_cargo_carencia),
        inicio_vigencia="2024-01-01",
        fim_vigencia="2024-12-31"
    )

def insert_hospitalar_servico_customizacao():
    insert(
        nome="Hospitalar Serviço de Customização",
        tipo="padrao",
        funcao_filtro=text_without_breakline(hospitalar_servico_customizacao_filtro),
        cargo_carencia=text_without_breakline(hospitalar_servico_customizacao_cargo_carencia),
        inicio_vigencia="2024-01-01",
        fim_vigencia="2024-12-31"
    )

def insert_hospitalar_manutencao():
    insert(
        nome="Hospitalar Manutenção",
        tipo="padrao",
        funcao_filtro=text_without_breakline(hospitalar_manutencao_filtro),
        cargo_carencia=text_without_breakline(hospitalar_manutencao_cargo_carencia),
        inicio_vigencia="2024-01-01",
        fim_vigencia="2024-12-31"
    )

def insert_hospitalar_locacao():
    insert(
        nome="Hospitalar Locação",
        tipo="padrao",
        funcao_filtro=text_without_breakline(hospitalar_locacao_filtro),
        cargo_carencia=text_without_breakline(hospitalar_locacao_cargo_carencia),
        inicio_vigencia="2024-01-01",
        fim_vigencia="2024-12-31"
    )
    
def insert_hospitalar_servico():
    insert(
        nome="Hospitalar Serviços",
        tipo="padrao",
        funcao_filtro=text_without_breakline(hospitalar_servico_filtro),
        cargo_carencia=text_without_breakline(hospitalar_servico_cargo_carencia),
        inicio_vigencia="2024-01-01",
        fim_vigencia="2024-12-31"
    )    

# Function to insert all hospitalar rules
def insert_all_hospitalar_rules():
    # insert_hospitalar_licenca_uso()
    # insert_hospitalar_outsourcing()
    # insert_hospitalar_servico_customizacao()
    # insert_hospitalar_manutencao()
    # insert_hospitalar_locacao()
    
    insert_hospitalar_servico()

# Call this function to insert all rules
insert_all_hospitalar_rules()