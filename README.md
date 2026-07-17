# CS2 Cross-Market Arbitrage Scout

A Python command-line tool for comparing CS2 item prices between Steam Market and Buff163.

The tool searches local item names, fetches current market prices, converts Buff163 prices from CNY to USD, applies marketplace fees, and reports whether a Steam resale spread appears profitable.

## Features

- Searches CS2 item names from `730_ItemNames.txt`
- Fetches Steam lowest listing price through Steam Market
- Fetches Buff163 lowest sell price and listing volume
- Converts CNY prices to USD
- Accounts for Steam and Buff163 marketplace fees
- Calculates estimated spread and ROI

## Getting Started

```bash
git clone https://github.com/calsalo/Cross-Market-Arbitrage-CSGO
cd Cross-Market-Arbitrage-CSGO
pip install requests python-dotenv
```

Create a `.env` file with your Buff163 session token:

```text
BUFF_SESSION=your_session_token
```

Run the scout:

```bash
python ArbEngine.py
```

## Project Structure

```text
ArbEngine.py             # CLI search and arbitrage logic
730_ItemNames.txt        # Source CS2 item-name list
Cleaned_730_Items.txt    # Cleaned item-name data
```

## Notes

This project is a market-data comparison tool, not a guaranteed arbitrage system. Real profitability depends on liquidity, fee changes, exchange rates, market delays, withdrawal limits, and platform rules.
