# raw-telegram-api
Raw Telegram API for Python 3\
#Example
```python
from raw_telegram.api import APIClient
token = "<paste your token here>"
api = APIClient(token)
api.send_method("sendMessage", {'chat_id': 5102762920, 'text': 'Hello world!'})
```
