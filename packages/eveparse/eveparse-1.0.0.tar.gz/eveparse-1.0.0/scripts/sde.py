import csv
import io
import json
import os
import pathlib
import requests
import sys

MD5_HASH_FILE_PATH: str = str(pathlib.Path(__file__).parent.parent / "hash.md5")
INV_TYPES_JSON_FILE_PATH: str = str(pathlib.Path(__file__).parent.parent / "eveparse/data/invTypes.json")

MD5_HASH_URL: str = "https://www.fuzzwork.co.uk/dump/sqlite-latest.sqlite.bz2.md5"
INV_TYPES_CSV_URL: str = "https://www.fuzzwork.co.uk/dump/latest/invTypes-nodescription.csv"


def convert_csv_to_dict(csv_file_content: str) -> dict:
    inv_types = {}
    with io.StringIO(csv_file_content) as csv_file:
        csv_content = csv.reader(csv_file)
        for row in csv_content:
            # CSV column names are:
            # type_id, group_id, name, mass, volume, capacity, portion_size, race_id,
            # base_price, published, market_group_id, icon_id, sound_id, graphic_id

            type_id = row[0]
            name = row[2]
            published = row[9]
            if published == "0":
                continue

            type_id = int(type_id)
            inv_types[name.casefold()] = {
                "type_id": type_id,
                "name": name,
            }
    return inv_types


def delete_file(file_path: str) -> None:
    if os.path.exists(file_path):
        os.remove(file_path)


def request_url_text(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def read_file_text(file_path: str) -> str:
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def write_file_text(file_path: str, text: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)


def write_file_json(file_path: str, data: dict) -> None:
    with open(file_path, "w") as file:
        json.dump(data, file)


def main():
    # Check for SDE update
    latest_md5_hash_string = request_url_text(MD5_HASH_URL)
    current_md5_hash_string = read_file_text(MD5_HASH_FILE_PATH)
    if latest_md5_hash_string == current_md5_hash_string:
        sys.exit(0)

    # Download updated SDE
    csv_file = request_url_text(INV_TYPES_CSV_URL)

    # Convert CSV SDE to JSON and write to file
    inv_types = convert_csv_to_dict(csv_file)
    write_file_json(INV_TYPES_JSON_FILE_PATH, inv_types)

    # Update hash
    write_file_text(MD5_HASH_FILE_PATH, latest_md5_hash_string)


if __name__ == '__main__':
    main()
