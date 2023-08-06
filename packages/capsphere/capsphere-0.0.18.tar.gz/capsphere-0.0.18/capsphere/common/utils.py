import json
import pandas as pd
import pkg_resources
import re
import os
import itertools
import calendar

from decimal import Decimal

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), '../resources')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def get_file_format(filename: str) -> str:
    parts = filename.split(".")
    if len(parts) == 2:
        return parts[1]
    else:
        raise ValueError(f"Unrecognised filename format '{filename}': Unable to split strings")


def read_config() -> dict:
    with pkg_resources.resource_stream('capsphere', 'resources/schema.json') as f:
        # print(json.load(f))
        return json.load(f)


def get_test_resource_path(filename: str) -> str:
    return pkg_resources.resource_filename('capsphere', 'resources/test/' + filename)


def process_text(text_list: list[str]):
    """
    This is where we standardise headers or text. Leading and trailing spaces in strings should be eliminated,
    periods at the start and end of strings should be eliminated too. Any periods or spaces in between strings
    must be converted to underscores.
    """
    processed_text = []
    for text in text_list:
        # remove leading and trailing spaces, periods, slashes and parenthesis
        text = text.strip(". /()")

        # replace spaces, periods, slashes and brackets in between text with underscores
        text = re.sub(r'[\s./]+', '_', text)

        # replace strings within brackets with underscores followed by the strings
        text = re.sub(r'\[([^]]+)\]', r'_\1', text)

        # remove any remaining underscores at the beginning or end
        text = text.strip('_')
        processed_text.append(text)
    return processed_text


def flatten_list(data: list[list]):
    return list(itertools
                .chain
                .from_iterable(data))


def __format_column(df_column: pd.Series) -> pd.Series:
    return df_column.str.replace(',', '').replace('', '0.00')


def sort_rows_by_month(df: pd.DataFrame) -> pd.DataFrame:
    df.index = pd.to_datetime(df.index, format='%b %Y')
    df = df.sort_index(ascending=True)
    df.index = df.index.strftime('%b %Y')
    return df
