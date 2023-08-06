#!/usr/bin/env python3

# Detects text in a document stored in an S3 bucket.
import boto3
import time
import json

if __name__ == "__main__":
    ACCESS_KEY = 'AKIAUJRETGIIO6QTZL7L'
    SECRET_KEY = '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'
    REGION_NAME = 'eu-west-2'

    # s3 = boto3.resource('s3',
    #                     aws_access_key_id=ACCESS_KEY,
    #                     aws_secret_access_key=SECRET_KEY)

    client = boto3.client('recognition',
                          region_name=REGION_NAME,
                          aws_access_key_id=ACCESS_KEY,
                          aws_secret_access_key=SECRET_KEY)

    response = client.start_document_analysis(
        DocumentLocation={
            'S3Object': {
                'Bucket': 'double-rooks',
                'Name': 'test_maybank.pdf'
            }
        },
        FeatureTypes=["TABLES"]
    )

    print('Starting Process...')

    for iter in range(1, 11):
        result = client.get_document_analysis(JobId=response['JobId'])

        if result['JobStatus'] == 'SUCCEEDED':
            with open("sample.json", "w") as outfile:
                json.dump(result, outfile,indent=4)
            print('Finished')
            break

        print('Still processing... ')
        time.sleep(5)

    # result = client.get_document_analysis(JobId=response['JobId'])
    #
    # print(result)

    # bucket = s3.Bucket('double-rooks')
    # pdf_file = 'test_maybank.pdf'
    #
    # response = client.analyze_document(Document={'S3Object': {'Bucket': bucket.name, 'Name': pdf_file}},
    #                                    FeatureTypes=['TABLES'])
    #
    # tables = response['Blocks']
    #
    # for table in tables:
    #     if table['BlockType'] == 'TABLE':
    #         rows = table['Relationships'][0]['Ids']
    #         cells = []
    #         for row in rows:
    #             for cell in table['Relationships'][0]['Ids']:
    #                 if cell in row:
    #                     cells.append(cell)
    #         cells = sorted(cells, key=lambda c: c['BoundingBox']['Top'])
    #         row_data = []
    #         for cell in cells:
    #             row_data.append(table['Blocks'][cell['Index']]['Text'])
    #         print(row_data)
