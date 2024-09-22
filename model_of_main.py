from pydantic import BaseModel
from business_rules.variables import BaseVariables
from business_rules.actions import BaseActions, rule_action
from business_rules.variables import numeric_rule_variable
from business_rules.fields import FIELD_NUMERIC, FIELD_TEXT
from business_rules import run_all

from datetime import date


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    expiration_day: date
    discard: int = 0


class ProductVariables(BaseVariables):  # type: ignore

    def __init__(self, product: Product) -> None:
        self.__product = product

    @numeric_rule_variable(label="Days until expiration")
    def expiration_days(self):  # type: ignore
        return (date.today() - self.__product.expiration_day).days


class ProductActions(BaseActions):  # type: ignore

    def __init__(self, product: Product) -> None:
        self.__product = product

    @rule_action(label="Function for update product for discard",
                 params={"should_discard": FIELD_NUMERIC, "rule_name": FIELD_TEXT})
    def product_discard(self, should_discard, rule_name):  # type: ignore
        print(f'rule name = {rule_name}')
        self.__product.discard = should_discard


name_identify = 'Device for young heart'

rules = [{
    "conditions": {
        "all": [{"name": "expiration_days",
                 "operator": "greater_than",
                 "value": 30}]
    },
    "actions": [
        {"name": "product_discard", "params": {
            "should_discard": 1,
            "rule_name": f'expirations_days_product {name_identify}'
        }}
    ]
}]


def faixa_proxima(valor, faixas):  # type: ignore
    menor_diferenca = float('inf')
    faixa_proxima = None

    for faixa in faixas:
        diferenca = abs(valor - faixa)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            faixa_proxima = faixa

    return faixa_proxima


def calcula_comissao(nr_maximo_parcelas, nr_dias_maximo_atraso, ):  # type: ignore
    pass


if __name__ == "__main__":

    # resultado = faixa_proxima(1,[30,60])
    # print(resultado)

    # eventos = {30: 1.5, 60: 2, 90: 4}
    # eventos_meses = [k for k in eventos.keys()]
    # print(eventos.get(20,None))

    # print(eventos_meses)

    # faixas = [evento.key for evento in eventos]
    # print(faixas)

    products = [
        Product(id=1, name="Milk", price=1.99, category="Dairy",
                expiration_day=date(2022, 8, 10), discard=0),
        # Product(id=2, name="Bread", price=2.50, category="Bakery", expiration_day=date(2023, 8, 5), discard=0),
        # Product(id=3, name="Apple", price=0.50, category="Fruits", expiration_day=date(2023, 8, 15), discard=0),
        # Product(id=4, name="Cheese", price=3.75, category="Dairy", expiration_day=date(2023, 8, 12), discard=0),
        # Product(id=5, name="Chicken Breast", price=7.99, category="Meat", expiration_day=date(2024, 8, 20), discard=0),
        # Product(id=6, name="Lettuce", price=1.25, category="Vegetables", expiration_day=date(2024, 8, 4), discard=0),
        # Product(id=7, name="Yogurt", price=0.99, category="Dairy", expiration_day=date(2024, 8, 8), discard=0),
        # Product(id=8, name="Orange Juice", price=3.99, category="Beverages", expiration_day=date(2024, 8, 18), discard=0),
        # Product(id=9, name="Salmon", price=12.50, category="Seafood", expiration_day=date(2024, 8, 22), discard=0),
        # Product(id=10, name="Chocolate", price=2.99, category="Snacks", expiration_day=date(2024, 12, 31), discard=0),
    ]

    for product in products:
        run_all(rule_list=rules,
                defined_variables=ProductVariables(product),
                defined_actions=ProductActions(product),
                stop_on_first_trigger=True)

    # for product in products:
    #     print(f"product_id ={product.id} - product_discard={product.discard}")
