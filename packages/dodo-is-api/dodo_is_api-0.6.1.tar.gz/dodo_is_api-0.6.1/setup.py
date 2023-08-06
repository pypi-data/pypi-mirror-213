# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dodo_is_api', 'dodo_is_api.connection', 'dodo_is_api.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'structlog>=23.1.0,<24.0.0']

setup_kwargs = {
    'name': 'dodo-is-api',
    'version': '0.6.1',
    'description': '',
    'long_description': '<div align="center">\n<a href="https://dodo-brands.stoplight.io">\n<img width="350px" src="https://api.huntflow.io/logo/866df3c58ea44c158c6e36010631fd9f.jpg">\n</a>\n</div>\n    \n<h1 align="center">\n🍕 Dodo IS API Wrapper\n</h1>\n\n<p align="center">\n<a href="https://github.com/goretsky-integration/dodo-is-api-python-wrapper/actions/workflows/unittest.yaml">\n<img src="https://github.com/goretsky-integration/dodo-is-api-python-wrapper/actions/workflows/unittest.yaml/badge.svg" alt="Test badge">\n</a>\n<a href="https://codecov.io/gh/goretsky-integration/dodo-is-api-python-wrapper">\n<img src="https://codecov.io/gh/goretsky-integration/dodo-is-api-python-wrapper/branch/main/graph/badge.svg?token=unzlMmAjsD"/>\n</a>\n<img src="https://img.shields.io/badge/python-3.11-brightgreen" alt="python">\n</p>\n\n---\n\n### Installation\n\nVia pip:\n```shell\npip install dodo-is-api\n```\n\nVia poetry:\n```shell\npoetry add dodo-is-api\n```\n\n---\n\n#### 📝 [Changelog](https://github.com/goretsky-integration/dodo-is-api-python-wrapper/blob/main/CHANGELOG.md) is here.\n\n---\n\n### 🧪 Usage:\n\n- Delivery:\n    - [Late delivery vouchers](#get-late-delivery-vouchers-)\n- Production:\n    - [Stop sales](#get-stop-sales-)\n\n---\n\n#### 🛵 Get late delivery vouchers:\n\n```python\nimport datetime\nfrom uuid import UUID\n\nfrom dodo_is_api.connection import DodoISAPIConnection\nfrom dodo_is_api.connection.http_clients import closing_http_client\nfrom dodo_is_api.mappers import map_late_delivery_voucher_dto\n\naccess_token = \'my-token\'\ncountry_code = \'kg\'\n\nunits = [UUID(\'e0ce0423-3064-4e04-ad3e-39906643ef14\'), UUID(\'bd09b0a8-147d-46f7-8908-874f5f59c9a2\')]\nfrom_date = datetime.datetime(year=2023, month=3, day=16)\nto_date = datetime.datetime(year=2023, month=3, day=17)\n\nwith closing_http_client(access_token=access_token, country_code=country_code) as http_client:\n    dodo_is_api_connection = DodoISAPIConnection(http_client=http_client)\n\n    # it will handle pagination for you\n    for late_delivery_vouchers in dodo_is_api_connection.iter_late_delivery_vouchers(\n            from_date=from_date,\n            to_date=to_date,\n            units=units\n    ):\n        # map to dataclass DTO if you need\n        late_delivery_voucher_dtos = [\n            map_late_delivery_voucher_dto(late_delivery_voucher)\n            for late_delivery_voucher in late_delivery_vouchers\n        ]\n        ...\n```\n\n---\n\n#### 📦 Get stop sales:\n\n```python\nimport datetime\nfrom uuid import UUID\n\nfrom dodo_is_api.connection import DodoISAPIConnection\nfrom dodo_is_api.connection.http_clients import closing_http_client\nfrom dodo_is_api.mappers import map_stop_sale_by_ingredient_dto\n\naccess_token = \'my-token\'\ncountry_code = \'kg\'\n\nunits = [UUID(\'e0ce0423-3064-4e04-ad3e-39906643ef14\'), UUID(\'bd09b0a8-147d-46f7-8908-874f5f59c9a2\')]\nfrom_date = datetime.datetime(year=2023, month=3, day=16)\nto_date = datetime.datetime(year=2023, month=3, day=17)\n\nwith closing_http_client(access_token=access_token, country_code=country_code) as http_client:\n    dodo_is_api_connection = DodoISAPIConnection(http_client=http_client)\n\n    # for products - dodo_is_api_connection.get_stop_sales_by_products\n    # for sales channels - dodo_is_api_connection.get_stop_sales_by_sales_channels\n    stop_sales = dodo_is_api_connection.get_stop_sales_by_ingredients(\n        from_date=from_date,\n        to_date=to_date,\n        units=units\n    )\n\n    # map to dataclass DTO if you need\n    # use suitable mapper\n    # in this case, ingredient stop sale mapper is used\n    late_delivery_voucher_dtos = [\n        map_stop_sale_by_ingredient_dto(stop_sale)\n        for stop_sale in stop_sales\n    ]\n    ...\n```\n',
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
