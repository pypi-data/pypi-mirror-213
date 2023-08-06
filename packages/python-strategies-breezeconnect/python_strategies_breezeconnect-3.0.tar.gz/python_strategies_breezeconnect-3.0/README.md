# UAT  python_strategies

## Steps to install Strategy Library for UAT


```python

pip install python_strategies_breezeconnect==3.0

```


## code usage

```python

from python_strategies import Strategies

async def main():
    obj = Strategies(app_key = "your app key",secret_key = "your secret key",api_session = "your api session",max_profit = "your max profit",max_loss = "your max loss")
    await obj.long_straddle(stock_code = "NIFTY",strike_price = "18700",qty = "50",expiry_date = "2023-06-15T06:00:00.000Z",exchange_code = "NFO")

await main()

```

