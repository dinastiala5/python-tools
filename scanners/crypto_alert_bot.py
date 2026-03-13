import requests
import time
from datetime import datetime

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "usd"
}

# set alert price
bitcoin_alert = 75000
ethereum_alert = 3000
solana_alert = 150

print("\n=== CRYPTO ALERT BOT STARTED ===\n")

while True:
    try:
        response = requests.get(url, params=params)
        data = response.json()

        btc = data["bitcoin"]["usd"]
        eth = data["ethereum"]["usd"]
        sol = data["solana"]["usd"]

        print("\nUpdated:", datetime.now().strftime("%H:%M:%S"))
        print("BTC:", btc)
        print("ETH:", eth)
        print("SOL:", sol)

        if btc >= bitcoin_alert:
            print("🚨 ALERT: Bitcoin reached", btc)

        if eth >= ethereum_alert:
            print("🚨 ALERT: Ethereum reached", eth)

        if sol >= solana_alert:
            print("🚨 ALERT: Solana reached", sol)

        time.sleep(15)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
