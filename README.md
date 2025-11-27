
# elprisenligenu-python-client

A simple Python client for fetching electricity prices from [elprisenligenu.dk](https://www.elprisenligenu.dk/).


## Usage
```python
import datetime

from elprisenligenu import Client

c = Client()

s = datetime.date.today() - datetime.timedelta(days=1)
e = datetime.date.today()

p = c.get_prices(start=s, end=e)

```
