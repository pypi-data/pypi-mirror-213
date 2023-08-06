import pandas as pd
from io import BytesIO


def create_worksheet(bank_data: list[dict]) -> BytesIO:
    df = pd.DataFrame(bank_data)

    # Group by bank
    grouped_df = df.groupby(df['bank'])

    excel_file = BytesIO()

    # Write excel
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet('Sheet1')

        sheet_start_row = 1

        worksheet.write(sheet_start_row, 0, 'Reconstructed Cash Flows')
        sheet_start_row += 1
        worksheet.write(sheet_start_row, 0, '*Average of 6 months bank statements')
        sheet_start_row += 2

        # Write in Excel for each bank
        for bank_name, value_df in grouped_df:
            # Remove bank name from columns
            columns_to_exclude = ['bank']
            filtered_df = value_df.drop(columns_to_exclude, axis=1)

            # Rename month header to the specific bank name
            new_column_name = {'month': bank_name}
            filtered_df = filtered_df.rename(columns=new_column_name)
            filtered_df = filtered_df.set_index(bank_name)

            filtered_df_agg = filtered_df.agg(['sum', 'mean']).round(2)
            filtered_df_agg.index = ['Total', 'Average']

            table = pd.concat([filtered_df, filtered_df_agg])
            table = table.rename_axis(bank_name)
            table.to_excel(writer, sheet_name='Sheet1', startrow=sheet_start_row, startcol=0)
            sheet_start_row += len(table) + 3

        worksheet.write(sheet_start_row, 0, 'Reconstructed Cash Flow based on 6 months Bank Statements.')
        sheet_start_row += 2

        columns_to_exclude = ['bank']
        df = df.drop(columns_to_exclude, axis=1)

        df = df.set_index('month')

        df_agg = df.agg(['sum', 'mean']).round(2)
        df_agg.index = ['Total', 'Average']

        table = pd.concat([df, df_agg])
        table.to_excel(writer, sheet_name='Sheet1', startrow=sheet_start_row, startcol=0)
        sheet_start_row += len(table) + 3

    excel_file.seek(0)

    return excel_file
