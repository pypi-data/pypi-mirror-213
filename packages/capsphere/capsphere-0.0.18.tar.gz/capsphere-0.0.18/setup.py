from setuptools import setup, find_packages

VERSION = '0.0.18'
DESCRIPTION = 'Capsphere proprietary library'
PACKAGE_NAME = 'capsphere'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author="Andy Lee",
    author_email="andy.mt.lee@gmail.com",
    description=DESCRIPTION,
    keywords=['python', 'capsphere', 'pdf', 'credit', 'cs'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ['resources/schema.json',
                       'resources/test/ambank.pdf']
    },
    install_requires=[
        'boto3',
        'dataclass-wizard',
        'pandas',
        'pdfplumber',
        'twine',
        'wheel',
        'xlsxwriter'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
