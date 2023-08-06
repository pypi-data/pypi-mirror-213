# Poetry has issues with editable installs. This shim is required for that purpose
from setuptools import setup

setup(
    name='airflow_data_validation',
    version='0.1.0',
    description='test tables data',
    url='https://github.com/guestyorg/airflow_data_validation',
)
