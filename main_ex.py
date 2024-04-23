import os
import requests
from dotenv import load_dotenv

def get_data(currency):
    url = f"https://v6.exchangerate-api.com/v6/d620169727488f74311cfb51/latest/{currency}"
    response = requests.get(url)
    return response.json()

def get_exchange_rate(from_currency, to_currency):
    data = get_data(from_currency)
    return data["conversion_rates"][to_currency]

def get_exchange_rate_from_to(from_currency, to_currency, amount):
    rate = get_exchange_rate(from_currency, to_currency)
    return amount * rate

def main():
    from_currency = input("Введите код валюты, которую хотите обменять: ").upper()
    to_currency = input("Введите код валюты, которую хотите получить: ").upper()
    amount = float(input("Введите сумму для обмена: "))
    
    converted_amount = get_exchange_rate_from_to(from_currency, to_currency, amount)
    print(f"{amount} {from_currency} = {converted_amount} {to_currency}")

if __name__ == "__main__":
    main()