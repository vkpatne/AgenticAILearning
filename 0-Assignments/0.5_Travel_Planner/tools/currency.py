import requests

def get_exchange_rate(base: str, target: str):
    url = f"https://api.exchangerate.host/latest?base={base}&symbols={target}"
    res = requests.get(url).json()
    rate = res.get("rates", {}).get(target.upper())
    if rate:
        return f"1 {base.upper()} = {rate:.2f} {target.upper()}"
    return f"Could not fetch exchange rate for {base} to {target}"

def convert_currency(amount: float, base: str, target: str):
    url = f"https://api.exchangerate.host/convert?from={base}&to={target}&amount={amount}"
    res = requests.get(url).json()
    result = res.get("result")
    if result is not None:
        return f"{amount} {base.upper()} = {result:.2f} {target.upper()}"
    return f"Conversion failed for {amount} {base} to {target}"
