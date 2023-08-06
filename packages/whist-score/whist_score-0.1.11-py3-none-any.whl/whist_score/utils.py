import json


def read_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return json.load(file)


def write_json(file_path: str, payload: dict) -> None:
    with open(file_path, "w") as file:
        json.dump(payload, file)
