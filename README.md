
# elprisenligenu-python-client

A simple Python client for fetching electricity prices from [elprisenligenu.dk](https://www.elprisenligenu.dk/).


## Usage
```python
import datetime

from elprisenligenu import Client

c = Client()

start = datetime.date.today() - datetime.timedelta(days=1)
end = datetime.date.today()

prices = c.get_prices(start=start, end=end)

```