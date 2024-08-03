from pydantic import BaseModel
from business_rules.variables import BaseVariables
from business_rules.actions import BaseActions, rule_action
from business_rules.variables import numeric_rule_variable
from business_rules.fields import FIELD_NUMERIC
from business_rules import run_all

from datetime import date


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    expiration_day : date
    discard: int = 0
    


class ProductVariables(BaseVariables):
    
    def __init__(self, product: Product) -> None:
        self.__product = product
        
    @numeric_rule_variable(label="Days until expiration")
    def expiration_days(self):
        return (date.today() - self.__product.expiration_day).days
    
    
class ProductActions(BaseActions):
    
    def __init__(self, product: Product) -> None:
        self.__product = product
    
    @rule_action(label="Function for update product for discard", 
                 params={"should_discard": FIELD_NUMERIC })
    def product_discard(self, should_discard):
        self.__product.discard = should_discard

rules = [{
    "conditions": {
        "all": [{"name": "expiration_days", 
                 "operator": "greater_than",
                 "value" : 30}]
    },
    "actions": [
        {"name": "product_discard", "params": {
            "should_discard": 1
        }}
    ]
}]

if __name__ == "__main__":
    products = [
        Product(id=1, name="Milk", price=1.99, category="Dairy", expiration_day=date(2022, 8, 10), discard=0),
        Product(id=2, name="Bread", price=2.50, category="Bakery", expiration_day=date(2023, 8, 5), discard=0),
        Product(id=3, name="Apple", price=0.50, category="Fruits", expiration_day=date(2023, 8, 15), discard=0),
        Product(id=4, name="Cheese", price=3.75, category="Dairy", expiration_day=date(2023, 8, 12), discard=0),
        Product(id=5, name="Chicken Breast", price=7.99, category="Meat", expiration_day=date(2024, 8, 20), discard=0),
        Product(id=6, name="Lettuce", price=1.25, category="Vegetables", expiration_day=date(2024, 8, 4), discard=0),
        Product(id=7, name="Yogurt", price=0.99, category="Dairy", expiration_day=date(2024, 8, 8), discard=0),
        Product(id=8, name="Orange Juice", price=3.99, category="Beverages", expiration_day=date(2024, 8, 18), discard=0),
        Product(id=9, name="Salmon", price=12.50, category="Seafood", expiration_day=date(2024, 8, 22), discard=0),
        Product(id=10, name="Chocolate", price=2.99, category="Snacks", expiration_day=date(2024, 12, 31), discard=0),
    ]
    
    for product in products:
        run_all(rule_list=rules,
                defined_variables= ProductVariables(product),
                defined_actions=ProductActions(product),
                stop_on_first_trigger=True)
        
    for product in products:
        print(f"product_id =#{product.id} - product_discard=#{product.discard}")
        