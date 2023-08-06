import pandas as pd
from decimal import Decimal
from capsphere.common.utils import __format_column

TWO_PLACES = Decimal(10) ** -2


def from_ambank(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[0] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def from_maybank(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter out if contains string
    filtered_df = df[~df[1].str.contains('[a-zA-Z]')]
    # another filter is filter out first & last row
    filtered_df = filtered_df.iloc[1:-1]

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['value_date'] = transformed_df[2]
    transformed_df['transaction'] = transformed_df[3]
    transformed_df['debit'] = __format_column(
        transformed_df[transformed_df[4].str.contains('\-')][4].str.replace('-', ''))
    transformed_df['credit'] = __format_column(
        transformed_df[transformed_df[4].str.contains('\+')][4].str.replace('+', ''))
    transformed_df['balance'] = __format_column(transformed_df[5])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains('\-')])
    total_cred_transactions = len(transformed_df[transformed_df[4].str.contains('\+')])

    # opening balance
    if '-' in transformed_df.iloc[0][4]:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def from_maybank_islamic(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter out if contains string
    filtered_df = df[~df[1].str.contains('[a-zA-Z]')]

    # filter if contains number
    filtered_df = filtered_df[filtered_df[1].str.contains(r'\d', na=False)]

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first'}).fillna('')
    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['debit'] = __format_column(
        transformed_df[transformed_df[3].str.contains('\-')][3].str.replace('-', ''))
    transformed_df['credit'] = __format_column(
        transformed_df[transformed_df[3].str.contains('\+')][3].str.replace('+', ''))
    transformed_df['balance'] = __format_column(transformed_df[4])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[3].str.contains('\-')])
    total_cred_transactions = len(transformed_df[transformed_df[3].str.contains('\+')])

    # opening balance
    if '-' in transformed_df.iloc[0][3]:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def from_cimb(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[-1] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[-1]) + pd.to_numeric(
            transformed_df['debit'].iloc[-1])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[-1]) - pd.to_numeric(
            transformed_df['credit'].iloc[-1])

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[0]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def from_rhb(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    return Decimal(transformed_df['balance'].iloc[0]).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def from_hong_leong(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    # if two rows get combined, separate into two new rows
    for index, value in enumerate(filtered_df[1]):
        new_list = [
            ['', '', '', '', ''],
            ['', '', '', '', '']
        ]
        if len(value.split(' ')[1]) > 1:
            new_list[0][0] = value.split(' ')[0]
            new_list[1][0] = value.split(' ')[1]
            if len(filtered_df.iloc[index][3]) != 0:
                new_list[0][2] = filtered_df.iloc[index][3].split(' ')[0]
                new_list[1][2] = filtered_df.iloc[index][3].split(' ')[1]
            if len(filtered_df.iloc[index][4]) != 0:
                new_list[0][3] = filtered_df.iloc[index][4].split(' ')[0]
                new_list[1][3] = filtered_df.iloc[index][4].split(' ')[1]

            new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4, 5])
            # drop the current row
            filtered_df = filtered_df.drop(index)
            # combine new row with the DataFrame
            filtered_df = pd.concat([filtered_df, new_df], ignore_index=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['credit'] = __format_column(transformed_df[3])
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['balance'] = __format_column(transformed_df[5])

    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_cred_transactions = len(transformed_df[transformed_df[3].str.contains(r'\d', na=False)])
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])

    # opening balance
    opening_balance = df.iloc[1][5].replace(',', '')
    # closing balance
    other_filtered_df = df[df[1].str.contains(r'\d', na=False)]
    last_row_with_number = other_filtered_df[other_filtered_df[5].str.contains('\d', na=False)].tail(1)
    closing_balance = __format_column(last_row_with_number[5])
    closing_balance = pd.to_numeric(closing_balance).sum()

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(closing_balance).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        other_filtered_df[1].iloc[-1]


def from_public_bank(transactions: list) -> tuple:
    # Custom function PUBLIC BANK - with only credit transactions, it will get as 4 columns instead of 5
    for index, transaction in enumerate(transactions):
        if len(transaction) == 4:
            new_dict = {}
            new_dict[1] = transaction[1]
            new_dict[2] = transaction[2]
            new_dict[3] = ''
            # if comma(,) detected as (.)
            if transaction[3].count(".") > 1:
                transaction[3] = transaction[3].replace(".", "", transaction[3].count(".") - 1)
            new_dict[4] = transaction[3]
            new_dict[5] = transaction[4]
            transactions[index] = new_dict

    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[5].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    # if two columns (transaction and debit) get combined, need to break that string apart for debit column
    for index, value in enumerate(filtered_df[3]):
        if any(char.isalpha() for char in value):
            filtered_df.iloc[index][3] = value.split(' ')[0]

    # if two rows get combined, separate into two rows
    for index, value in enumerate(filtered_df[4]):
        if value != '':
            if len(value.split(' ')[1]) > 1:
                new_list = [
                    ['', '', '', '', ''],
                    ['', '', '', '', '']
                ]
                new_list[0][3] = filtered_df.iloc[index][4].split(' ')[0]
                new_list[0][1] = filtered_df.iloc[index][2]
                new_list[1][3] = filtered_df.iloc[index][4].split(' ')[1]
                new_list[1][1] = filtered_df.iloc[index][2]

                new_df = pd.DataFrame(new_list, columns=[1, 2, 3, 4, 5])
                # drop the current row
                filtered_df = filtered_df.drop(index)
                # combine new row with the DataFrame
                filtered_df = pd.concat([filtered_df, new_df], ignore_index=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['debit'] = __format_column(transformed_df[3])
    transformed_df['credit'] = __format_column(transformed_df[4])
    transformed_df['balance'] = __format_column(transformed_df[5])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[3].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])

    # last date
    last_row_with_date = filtered_df[filtered_df[1].str.contains('\d', na=False)].tail(1)
    last_date = last_row_with_date[1].to_string(index=False)

    # closing balance
    last_row_with_number = filtered_df[filtered_df[5].str.contains('\d', na=False)].tail(1)
    closing_balance = __format_column(last_row_with_number[5])
    closing_balance = pd.to_numeric(closing_balance).sum()

    return Decimal(transformed_df['balance'].iloc[0]).quantize(TWO_PLACES), \
        Decimal(closing_balance).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        last_date


def from_alliance(transactions: list) -> tuple:
    # Tested for scanned docs, if period (.) detected as comma (,)
    for index, transaction in enumerate(transactions):
        if transaction[4].count(".") == 0 and transaction[4].count(",") == 1:
            transaction[4] = transaction[4].replace(",", ".")

    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6].str.replace('CR', '').str.replace('DR', '-'))

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[0] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]


def from_bank_islam(transactions: list) -> tuple:
    df = pd.DataFrame(transactions)

    # filter if contains number
    filtered_df = df[df[1].str.contains(r'\d', na=False)]
    filtered_df = filtered_df.reset_index(drop=True)

    # if debit column has strings from transaction column
    for index, value in enumerate(filtered_df[4]):
        if any(char.isdigit() for char in value.split(' ')[0]):
            filtered_df.iloc[index][4] = value.split(' ')[0]
        else:
            filtered_df.iloc[index][4] = ''

    # if debit column has strings from transaction column
    for index, value in enumerate(filtered_df[5]):
        if any(char.isdigit() for char in value.split(' ')[0]):
            filtered_df.iloc[index][5] = value.split(' ')[0]
        else:
            filtered_df.iloc[index][5] = ''

    transformed_df = filtered_df.groupby((~df[1].isnull()).cumsum()).agg({1: 'first',
                                                                          2: lambda x: '\n'.join(x),
                                                                          3: 'first',
                                                                          4: 'first',
                                                                          5: 'first',
                                                                          6: 'first'}).fillna('')

    transformed_df['date'] = transformed_df[1]
    transformed_df['transaction'] = transformed_df[2]
    transformed_df['cheque'] = transformed_df[3]
    transformed_df['debit'] = __format_column(transformed_df[4])
    transformed_df['credit'] = __format_column(transformed_df[5])
    transformed_df['balance'] = __format_column(transformed_df[6])

    total_debit = pd.to_numeric(transformed_df['debit']).sum()
    total_credit = pd.to_numeric(transformed_df['credit']).sum()
    # this is important to get count on debit & credit transactions only if rows have values
    total_deb_transactions = len(transformed_df[transformed_df[4].str.contains(r'\d', na=False)])
    total_cred_transactions = len(transformed_df[transformed_df[5].str.contains(r'\d', na=False)])

    # opening balance
    if transformed_df['debit'].iloc[0] != '0.00':
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) + pd.to_numeric(
            transformed_df['debit'].iloc[0])
    else:
        opening_balance = pd.to_numeric(transformed_df['balance'].iloc[0]) - pd.to_numeric(
            transformed_df['credit'].iloc[0])

    return Decimal(opening_balance).quantize(TWO_PLACES), \
        Decimal(transformed_df['balance'].iloc[-1]).quantize(TWO_PLACES), \
        Decimal(total_debit).quantize(TWO_PLACES), \
        Decimal(total_credit).quantize(TWO_PLACES), \
        Decimal(total_debit / total_deb_transactions).quantize(TWO_PLACES), \
        Decimal(total_credit / total_cred_transactions).quantize(TWO_PLACES), \
        transformed_df['date'].iloc[-1]
