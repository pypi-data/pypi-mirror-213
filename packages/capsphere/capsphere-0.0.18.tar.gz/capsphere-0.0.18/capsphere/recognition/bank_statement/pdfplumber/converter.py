import pdfplumber
import pandas as pd
import numpy as np

from io import BytesIO
from typing import Union
from decimal import Decimal

from capsphere.common.date import convert_date
from capsphere.common.utils import flatten_list, process_text, read_config
from dateutil import parser
from pdfplumber.page import Page

TWO_PLACES = Decimal(10) ** -2
SCHEMA = read_config()


def func_ambank(content: Union[BytesIO, str]) -> tuple:
    headers = flatten_list([bank['headers'] for bank in SCHEMA
                            if bank['name'] == 'AmBank'])

    converted_headers = process_text(headers)

    total_transactions = []

    statement_date = ""

    with pdfplumber.open(content) as pdf:

        total_pages = len(pdf.pages)
        for index in range(total_pages):
            if not statement_date:
                statement_date = "" if extract_date(pdf.pages[index]) is None \
                    else extract_date(pdf.pages[index])
            if __check_if_tables_found(pdf.pages[index]):
                page_table = pdf.pages[index].extract_table(table_settings={"vertical_strategy": "lines_strict"})
                for transaction in page_table:
                    if __check_all_entries_empty(transaction):
                        break
                    total_transactions.append(transaction)

        if not statement_date:
            raise ValueError(f'Cannot process statement_date for {pdf}')

        df = pd.DataFrame(total_transactions, columns=converted_headers)

        df = df.replace('', np.nan)
        transformed_df = df.groupby((~df['date'].isnull()).cumsum()).agg({'date': 'first',
                                                                          'transaction': lambda x: '\n'.join(x),
                                                                          'cheque_no': 'first',
                                                                          'debit': 'first',
                                                                          'credit': 'first',
                                                                          'balance': 'first'}).fillna('')
        transformed_df.index.name = None
        transformed_df['debit'] = __format_column(transformed_df['debit'])
        transformed_df['credit'] = __format_column(transformed_df['credit'])
        transformed_df['balance'] = __format_column(transformed_df['balance'])

        total_debit = pd.to_numeric(
            transformed_df['debit']).sum()
        total_credit = pd.to_numeric(
            transformed_df['credit']).sum()
        total_deb_transactions = df[df['debit'].notnull()].debit.size
        total_cred_transactions = df[df['credit'].notnull()].credit.size

        return Decimal(transformed_df['balance'].iloc[0]).quantize(TWO_PLACES), \
            Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
            Decimal(total_debit).quantize(TWO_PLACES), \
            Decimal(total_credit).quantize(TWO_PLACES), \
            Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
            Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
            convert_date(statement_date)


def func_cimb(content: Union[BytesIO, str]) -> tuple:
    headers = flatten_list([bank['headers'] for bank in SCHEMA
                            if bank['name'] == 'CIMB'])

    converted_headers = process_text(headers)

    total_transactions = []

    statement_date = ""

    with pdfplumber.open(content) as pdf:
        total_pages = len(pdf.pages)
        for index in range(total_pages):
            if not statement_date:
                statement_date = "" if extract_date(pdf.pages[index]) is None \
                    else extract_date(pdf.pages[index])
            if __check_if_tables_found(pdf.pages[index]):
                page_table = pdf.pages[index].extract_table(table_settings={"vertical_strategy": "lines_strict"})
                for transaction in page_table:
                    # CIMB does not need this function as it will returns an error for end page with no transaction.
                    # if __check_all_entries_empty(transaction):
                    #     break

                    # CIMB additional function - append only transaction row
                    if __check_if_balances_column_not_null(transaction):
                        total_transactions.append(transaction)

        # CIMB additional function - reordering of the transaction list which is in descending order
        __check_if_transactions_need_ordering(total_transactions)
        df = pd.DataFrame(total_transactions, columns=converted_headers)

        df = df.replace('', np.nan)
        transformed_df = df.groupby((~df['date'].isnull()).cumsum()).agg({'date': 'first',
                                                                          'description': lambda x: '\n'.join(x),
                                                                          'cheque_ref_no': 'first',
                                                                          'withdrawal': 'first',
                                                                          'deposits': 'first',
                                                                          'balance': 'first'}).fillna('')
        transformed_df.index.name = None
        transformed_df['debit'] = __format_column(transformed_df['withdrawal'])
        transformed_df['credit'] = __format_column(transformed_df['deposits'])
        transformed_df['balance'] = __format_column(transformed_df['balance'])

        # CIMB additional function - opening balance needs to check if the amount already being debited or credited

        if pd.to_numeric(transformed_df['debit'].iloc[0]) > 0:
            opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
                transformed_df['debit'].iloc[0])
        elif pd.to_numeric(transformed_df['credit'].iloc[0]) > 0:
            opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
                transformed_df['credit'].iloc[0])
        else:
            opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0])

        total_debit = pd.to_numeric(
            transformed_df['debit']).sum()
        total_credit = pd.to_numeric(
            transformed_df['credit']).sum()
        total_deb_transactions = df[df['withdrawal'].notnull()].withdrawal.size
        total_cred_transactions = df[df['deposits'].notnull()].deposits.size

        return Decimal(opening_balance).quantize(TWO_PLACES), \
            Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
            Decimal(total_debit).quantize(TWO_PLACES), \
            Decimal(total_credit).quantize(TWO_PLACES), \
            Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
            Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
            convert_date(transformed_df['date'].iloc[-1])


def __check_all_entries_empty(transaction: Union[list[list[str | None]], None]) -> bool:
    return True if all(entry == '' or entry.isspace() for entry in transaction) else False


def __format_column(df_column: pd.Series) -> pd.Series:
    return df_column.str.replace(',', '').replace('', '0.00')


def __check_if_tables_found(content: Page) -> bool:
    check = content.find_tables(table_settings={"vertical_strategy": "lines_strict"})
    return True if len(check) > 0 else False


def __check_if_transactions_need_ordering(transaction: Union[list[list[str | None]], None]) -> list:
    first_transaction_date = parser.parse(transaction[0][0])
    last_transaction_date = parser.parse(transaction[-1][0])
    if first_transaction_date > last_transaction_date:
        transaction.reverse()

    return transaction


def __check_if_balances_column_not_null(transaction: Union[list[list[str | None]], None]) -> bool:
    if len(transaction) == 6:
        if transaction[5] is not None:
            return any(char.isdigit() for char in transaction[5])
        else:
            return False


def extract_date(content: Page) -> str:
    for line in content.extract_text().splitlines():
        if 'STATEMENT DATE / TARIKH PENYATA' in line:
            return line[-10:]
        elif 'Statement Date / Tarikh Penyata' in line:
            return line[-10:]
