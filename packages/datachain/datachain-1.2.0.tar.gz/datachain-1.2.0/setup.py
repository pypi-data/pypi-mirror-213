# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datachain',
 'datachain.config',
 'datachain.core',
 'datachain.sources',
 'datachain.sources.bytes',
 'datachain.sources.files',
 'datachain.sources.query',
 'datachain.sources.utils',
 'datachain.utils']

package_data = \
{'': ['*']}

extras_require = \
{'ftp': ['python-dotenv>=1.0.0,<2.0.0'],
 'http': ['requests>=2.31.0,<3.0.0'],
 'kaggle': ['python-dotenv>=1.0.0,<2.0.0'],
 'mysql': ['python-dotenv>=1.0.0,<2.0.0',
           'sqlalchemy==1.4.46',
           'mysqlclient>=2.1.1,<3.0.0'],
 'pgsql': ['python-dotenv>=1.0.0,<2.0.0',
           'sqlalchemy==1.4.46',
           'psycopg2-binary>=2.9.5,<3.0.0'],
 'salesforce': ['python-dotenv>=1.0.0,<2.0.0',
                'simple-salesforce>=1.12.2,<2.0.0'],
 'sftp': ['python-dotenv>=1.0.0,<2.0.0', 'paramiko>=3.2.0,<4.0.0'],
 'sharepoint': ['python-dotenv>=1.0.0,<2.0.0',
                'azure-common>=1.1.28,<2.0.0',
                'azure-storage-blob>=12.14.1,<13.0.0',
                'azure-storage-common>=2.1.0,<3.0.0',
                'shareplum>=0.5.1,<0.6.0'],
 'snowflake': ['sqlalchemy==1.4.46',
               'snowflake-connector-python>=2.9.0,<3.0.0',
               'snowflake-sqlalchemy>=1.4.4,<2.0.0',
               'cryptography==38.0.4'],
 'tabular': ['pandas>=2.0.2,<3.0.0']}

setup_kwargs = {
    'name': 'datachain',
    'version': '1.2.0',
    'description': 'Tools to build data pipelines.',
    'long_description': '',
    'author': 'Rayane AMROUCHE',
    'author_email': 'rayaneamrouche@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
