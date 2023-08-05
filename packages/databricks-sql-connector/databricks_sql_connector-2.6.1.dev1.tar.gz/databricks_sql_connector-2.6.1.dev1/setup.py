# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricks',
 'databricks.sql',
 'databricks.sql.auth',
 'databricks.sql.experimental',
 'databricks.sql.thrift_api',
 'databricks.sql.thrift_api.TCLIService',
 'databricks.sqlalchemy',
 'databricks.sqlalchemy.dialect']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.0.11,<2.0.0',
 'lz4>=4.0.2,<5.0.0',
 'oauthlib>=3.1.0,<4.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.2.5,<2.0.0',
 'requests>=2.18.1,<3.0.0',
 'sqlalchemy>=1.3.24,<2.0.0',
 'thrift>=0.16.0,<0.17.0']

extras_require = \
{':python_version >= "3.11"': ['pyarrow>=10.0.1', 'numpy>=1.23.4'],
 ':python_version >= "3.7" and python_version < "3.11"': ['pyarrow>=6.0.0',
                                                          'numpy>=1.16.6']}

entry_points = \
{'sqlalchemy.dialects': ['databricks = '
                         'databricks.sqlalchemy:DatabricksDialect']}

setup_kwargs = {
    'name': 'databricks-sql-connector',
    'version': '2.6.1.dev1',
    'description': 'Databricks SQL Connector for Python',
    'long_description': '# Databricks SQL Connector for Python\n\n[![PyPI](https://img.shields.io/pypi/v/databricks-sql-connector?style=flat-square)](https://pypi.org/project/databricks-sql-connector/)\n[![Downloads](https://pepy.tech/badge/databricks-sql-connector)](https://pepy.tech/project/databricks-sql-connector)\n\nThe Databricks SQL Connector for Python allows you to develop Python applications that connect to Databricks clusters and SQL warehouses. It is a Thrift-based client with no dependencies on ODBC or JDBC. It conforms to the [Python DB API 2.0 specification](https://www.python.org/dev/peps/pep-0249/) and exposes a [SQLAlchemy](https://www.sqlalchemy.org/) dialect for use with tools like `pandas` and `alembic` which use SQLAlchemy to execute DDL.\n\nThis connector uses Arrow as the data-exchange format, and supports APIs to directly fetch Arrow tables. Arrow tables are wrapped in the `ArrowQueue` class to provide a natural API to get several rows at a time.\n\nYou are welcome to file an issue here for general use cases. You can also contact Databricks Support [here](help.databricks.com).\n\n## Requirements\n\nPython 3.7 or above is required.\n\n## Documentation\n\nFor the latest documentation, see\n\n- [Databricks](https://docs.databricks.com/dev-tools/python-sql-connector.html)\n- [Azure Databricks](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/python-sql-connector)\n\n## Quickstart\n\nInstall the library with `pip install databricks-sql-connector`\n\nNote: Don\'t hard-code authentication secrets into your Python. Use environment variables\n\n```bash\nexport DATABRICKS_HOST=********.databricks.com\nexport DATABRICKS_HTTP_PATH=/sql/1.0/endpoints/****************\nexport DATABRICKS_TOKEN=dapi********************************\n```\n\nExample usage:\n```python\nimport os\nfrom databricks import sql\n\nhost = os.getenv("DATABRICKS_HOST")\nhttp_path = os.getenv("DATABRICKS_HTTP_PATH")\naccess_token = os.getenv("DATABRICKS_ACCESS_TOKEN")\n\nconnection = sql.connect(\n  server_hostname=host,\n  http_path=http_path,\n  access_token=access_token)\n\ncursor = connection.cursor()\n\ncursor.execute(\'SELECT * FROM RANGE(10)\')\nresult = cursor.fetchall()\nfor row in result:\n  print(row)\n\ncursor.close()\nconnection.close()\n```\n\nIn the above example:\n- `server-hostname` is the Databricks instance host name.\n- `http-path` is the HTTP Path either to a Databricks SQL endpoint (e.g. /sql/1.0/endpoints/1234567890abcdef),\nor to a Databricks Runtime interactive cluster (e.g. /sql/protocolv1/o/1234567890123456/1234-123456-slid123)\n- `personal-access-token` is the Databricks Personal Access Token for the account that will execute commands and queries\n\n\n## Contributing\n\nSee [CONTRIBUTING.md](CONTRIBUTING.md)\n\n## License\n\n[Apache License 2.0](LICENSE)\n',
    'author': 'Databricks',
    'author_email': 'databricks-sql-connector-maintainers@databricks.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
