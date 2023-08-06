<h1 align="center">
🍕 Dodo IS API Wrapper
</h1>

<p align="center">
<a href="https://github.com/goretsky-integration/dodo-is-api-python-wrapper/actions/workflows/unittest.yaml">
<img src="https://github.com/goretsky-integration/dodo-is-api-python-wrapper/actions/workflows/unittest.yaml/badge.svg" alt="Test badge">
</a>
<a href="https://codecov.io/gh/goretsky-integration/dodo-is-api-python-wrapper">
<img src="https://codecov.io/gh/goretsky-integration/dodo-is-api-python-wrapper/branch/main/graph/badge.svg?token=unzlMmAjsD"/>
</a>
<img src="https://img.shields.io/badge/python-3.11-brightgreen" alt="python">
</p>

---

### Installation

Via pip:

```shell
pip install dodo-is-api
```

Via poetry:

```shell
poetry add dodo-is-api
```

---

#### 📝 [Changelog](https://github.com/goretsky-integration/dodo-is-api-python-wrapper/blob/main/CHANGELOG.md) is here.

---

### 🧪 Usage:

🌩️ Synchronous version:

```python
from datetime import datetime
from uuid import UUID

import httpx

from dodo_is_api import models
from dodo_is_api.connection.synchronous import DodoISAPIConnection


def main():
    access_token = 'your access token'
    country_code = models.CountryCode.RU

    from_date = datetime(2004, 10, 7)
    to_date = datetime(2004, 10, 7, 23)
    units = [UUID('ec81831c-b8a7-4ba8-a6aa-7ae7d0c4e0bb')]

    with httpx.Client() as http_client:
        connection = DodoISAPIConnection(
            http_client=http_client,
            access_token=access_token,
            country_code=country_code,
        )

        stop_sales = connection.get_stop_sales_by_products(
            from_date=from_date,
            to_date=to_date,
            units=units,
        )

    print(stop_sales)


if __name__ == '__main__':
    main()
```

⚡️ Asynchronous version:

```python
import asyncio
from datetime import datetime
from uuid import UUID

import httpx

from dodo_is_api import models
from dodo_is_api.connection.asynchronous import AsyncDodoISAPIConnection


async def main():
    access_token = 'your access token'
    country_code = models.CountryCode.RU

    from_date = datetime(2004, 10, 7)
    to_date = datetime(2004, 10, 7, 23)
    units = [UUID('ec81831c-b8a7-4ba8-a6aa-7ae7d0c4e0bb')]

    with httpx.AsyncClient() as http_client:
        connection = AsyncDodoISAPIConnection(
            http_client=http_client,
            access_token=access_token,
            country_code=country_code,
        )

        stop_sales = await connection.get_stop_sales_by_products(
            from_date=from_date,
            to_date=to_date,
            units=units,
        )

    print(stop_sales)


if __name__ == '__main__':
    asyncio.run(main())
```