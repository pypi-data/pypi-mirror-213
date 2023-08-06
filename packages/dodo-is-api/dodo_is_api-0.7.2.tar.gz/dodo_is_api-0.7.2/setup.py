# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dodo_is_api', 'dodo_is_api.connection', 'dodo_is_api.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0',
 'pydantic>=1.10.9,<2.0.0',
 'structlog>=23.1.0,<24.0.0']

setup_kwargs = {
    'name': 'dodo-is-api',
    'version': '0.7.2',
    'description': '',
    'long_description': '<h1 align="center">\n🍕 Dodo IS API Wrapper\n</h1>\n\n<p align="center">\n<a href="https://github.com/goretsky-integration/dodo-is-api-python-wrapper/actions/workflows/unittest.yaml">\n<img src="https://github.com/goretsky-integration/dodo-is-api-python-wrapper/actions/workflows/unittest.yaml/badge.svg" alt="Test badge">\n</a>\n<a href="https://codecov.io/gh/goretsky-integration/dodo-is-api-python-wrapper">\n<img src="https://codecov.io/gh/goretsky-integration/dodo-is-api-python-wrapper/branch/main/graph/badge.svg?token=unzlMmAjsD"/>\n</a>\n<img src="https://img.shields.io/badge/python-3.11-brightgreen" alt="python">\n</p>\n\n---\n\n### Installation\n\nVia pip:\n\n```shell\npip install dodo-is-api\n```\n\nVia poetry:\n\n```shell\npoetry add dodo-is-api\n```\n\n---\n\n#### 📝 [Changelog](https://github.com/goretsky-integration/dodo-is-api-python-wrapper/blob/main/CHANGELOG.md) is here.\n\n---\n\n### 🧪 Usage:\n\n🌩️ Synchronous version:\n\n```python\nfrom datetime import datetime\nfrom uuid import UUID\n\nimport httpx\n\nfrom dodo_is_api import models\nfrom dodo_is_api.connection.synchronous import DodoISAPIConnection\n\n\ndef main():\n    access_token = \'your access token\'\n    country_code = models.CountryCode.RU\n\n    from_date = datetime(2004, 10, 7)\n    to_date = datetime(2004, 10, 7, 23)\n    units = [UUID(\'ec81831c-b8a7-4ba8-a6aa-7ae7d0c4e0bb\')]\n\n    with httpx.Client() as http_client:\n        connection = DodoISAPIConnection(\n            http_client=http_client,\n            access_token=access_token,\n            country_code=country_code,\n        )\n\n        stop_sales = connection.get_stop_sales_by_products(\n            from_date=from_date,\n            to_date=to_date,\n            units=units,\n        )\n\n    print(stop_sales)\n\n\nif __name__ == \'__main__\':\n    main()\n```\n\n⚡️ Asynchronous version:\n\n```python\nimport asyncio\nfrom datetime import datetime\nfrom uuid import UUID\n\nimport httpx\n\nfrom dodo_is_api import models\nfrom dodo_is_api.connection.asynchronous import AsyncDodoISAPIConnection\n\n\nasync def main():\n    access_token = \'your access token\'\n    country_code = models.CountryCode.RU\n\n    from_date = datetime(2004, 10, 7)\n    to_date = datetime(2004, 10, 7, 23)\n    units = [UUID(\'ec81831c-b8a7-4ba8-a6aa-7ae7d0c4e0bb\')]\n\n    with httpx.AsyncClient() as http_client:\n        connection = AsyncDodoISAPIConnection(\n            http_client=http_client,\n            access_token=access_token,\n            country_code=country_code,\n        )\n\n        stop_sales = await connection.get_stop_sales_by_products(\n            from_date=from_date,\n            to_date=to_date,\n            units=units,\n        )\n\n    print(stop_sales)\n\n\nif __name__ == \'__main__\':\n    asyncio.run(main())\n```',
    'author': 'Eldos',
    'author_email': 'eldos.baktybekov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
