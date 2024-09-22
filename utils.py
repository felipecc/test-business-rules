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
