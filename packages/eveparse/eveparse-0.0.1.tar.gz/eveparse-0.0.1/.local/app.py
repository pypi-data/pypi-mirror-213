from eveparse import parse
from eveparse.errors import ParserError

FILE_PATH = "evepraisal.txt"  # 217
# FILE_PATH = "pastes/cargo_scanner.txt"  # 0
# FILE_PATH = "pastes/drone.txt"  # 0
# FILE_PATH = "pastes/dscan.txt"  # 126
# FILE_PATH = "pastes/fitting.txt"  # 0
# FILE_PATH = "pastes/market_orders.txt"  # 7
# FILE_PATH = "pastes/multibuy.txt"  # 1
# FILE_PATH = "pastes/orders_history.txt"  # 4
# FILE_PATH = "pastes/quickbar.txt"  # 0
# FILE_PATH = "pastes/sell_orders.txt"  # 3
# FILE_PATH = "pastes/survey_scan.txt"  # 0
# FILE_PATH = "pastes/view_contents.txt"  # 26

with open(FILE_PATH, "r", encoding="utf-8") as f:
    lines = []
    for _line in f.readlines():
        _line = _line.strip()
        if _line:
            lines.append(_line)

count = 0

for line in lines:
    try:
        type_id, name, quantity = parse(line)
    except ParserError:
        count += 1
        print(line)

print(count)
