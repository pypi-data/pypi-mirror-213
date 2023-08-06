from csv import DictReader

import xmltodict


def load_xml(path: str) -> dict:
    with open(path) as fh:
        return xmltodict.parse(fh.read())


def load_csv(path: str) -> list[dict]:
    with open(path) as fh:
        return list(DictReader(fh, delimiter=","))
