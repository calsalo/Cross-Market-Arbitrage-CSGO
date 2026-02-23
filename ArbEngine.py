"""
CS2 Arbitrage Scout
A tool to compare item prices between Steam and Buff163 markets.
"""

import urllib.parse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
BUFF_SESSION = os.getenv("BUFF_SESSION")
BUFF_COOKIES = {"session": BUFF_SESSION}
STEAM_FEE = 0.1304
BUFF_FEE = 0.025
CNY_TO_USD = 1 / 7.2
REQUEST_TIMEOUT = 10


def get_buff_price(hashname):
    """Fetches the lowest sell price and volume for an item from Buff163."""
    encoded_name = urllib.parse.quote(hashname)
    url = f"https://buff.163.com/api/market/goods?game=csgo&search={encoded_name}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        res = requests.get(
            url,
            headers=headers,
            cookies=BUFF_COOKIES,
            timeout=REQUEST_TIMEOUT
        ).json()

        if res.get("code") == "OK" and res["data"]["items"]:
            item = res["data"]["items"][0]
            price_usd = float(item.get("sell_min_price")) * CNY_TO_USD
            return {"price": price_usd, "volume": item.get("sell_num")}

    except requests.exceptions.RequestException as e:
        print(f"Buff Connection Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Buff Data Parsing Error: {e}")
    return None


def get_steam_price(hashname):
    """Fetches the lowest sell price and volume for an item from Steam."""
    encoded_name = urllib.parse.quote(hashname)
    url = (
        "https://steamcommunity.com/market/priceoverview/"
        f"?appid=730&currency=1&market_hash_name={encoded_name}"
    )

    try:
        res = requests.get(url, timeout=REQUEST_TIMEOUT).json()
        if res.get("success"):
            price_str = res.get("lowest_price", "0").replace("$", "").replace(",", "")
            return {"price": float(price_str), "volume": res.get("volume", "0")}

    except requests.exceptions.RequestException as e:
        print(f"Steam Connection Error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Steam Data Parsing Error: {e}")
    return None


def analyze_arbitrage():
    """Main engine to search items and calculate price spreads."""
    query = input("\nSearch Item (e.g., 'awp | redline'): ").strip().lower()
    if not query:
        return

    matches = []
    try:
        with open('730_ItemNames.txt', 'r', encoding='utf-8') as f:
            matches = [line.strip() for line in f if query in line.lower()]
    except FileNotFoundError:
        print("Error: '730_ItemNames.txt' not found.")
        return

    if not matches:
        print("No items found.")
        return

    for i, name in enumerate(matches[:10], 1):
        print(f"{i}. {name}")

    choice = input("\nSelect item number (or 'q'): ")
    if choice.isdigit() and 0 <= (idx := int(choice) - 1) < len(matches):
        selected_item = matches[idx]
        steam = get_steam_price(selected_item)
        buff = get_buff_price(selected_item)

        if steam and buff:
            # Net Proceeds Calculation
            steam_net = steam['price'] * (1 - STEAM_FEE)
            diff = steam_net - buff['price']
            roi = (diff / buff['price']) * 100 if buff['price'] > 0 else 0

            print(f"\nResults for {selected_item}:")
            print(f"Steam Net: ${steam_net:.2f} | Buff Net: ${buff['price'] * (1-BUFF_FEE):.2f}")

            if diff > 0:
                print(f"✅ Profit: ${diff:.2f} ({roi:.1f}% ROI)")
            else:
                print(f"❌ No Profit (Loss: ${abs(diff):.2f})")
    else:
        print("Search cancelled or invalid input.")


if __name__ == "__main__":
    analyze_arbitrage()
