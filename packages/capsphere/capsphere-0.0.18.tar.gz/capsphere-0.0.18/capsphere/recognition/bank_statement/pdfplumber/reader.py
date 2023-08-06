import pdfplumber

from io import BytesIO
from typing import Union
from capsphere.common.utils import read_config
from pdfplumber.page import Page


def extract_bank_name(file_path: Union[str, BytesIO]) -> str:

    with pdfplumber.open(file_path) as pdf:

        total_pages = len(pdf.pages)

        for index in range(total_pages):
            bank_name = _search_for_text(pdf.pages[index])
            if bank_name:
                return bank_name

        if not bank_name:
            raise ValueError(f'Unable to get bank name from {file_path}')


def _search_for_text(image: Page) -> str:
    bank_schemas = read_config()
    for bank in bank_schemas:
        for identifier in bank['identifiers']:
            if image.search(identifier, regex=True, case=False):
                return bank['name']
    return ""


