import requests
from datetime import datetime

def get_currency_rates():
    api_key = "SUA_CHAVE_EXCHANGERATE_API"  # Obtenha em https://www.exchangerate-api.com
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "USD_BRL": data["conversion_rates"]["BRL"],
            "USD_EUR": data["conversion_rates"]["EUR"],
            "USD_JPY": data["conversion_rates"]["JPY"]
        }
    except:
        return {"USD_BRL": 5.50, "USD_EUR": 0.85, "USD_JPY": 150.0}  # Fallback

def get_stock_quotes():
    api_key = "SUA_CHAVE_ALPHA_VANTAGE"  # Obtenha em https://www.alphavantage.co
    symbols = ["^BVSP", "^GSPC", "^IXIC"]  # IBOVESPA, S&P 500, NASDAQ
    quotes = {}
    for symbol in symbols:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            quotes[symbol] = float(data["Global Quote"]["05. price"])
        except:
            quotes[symbol] = 0.0  # Fallback
    return quotes

def get_esports_games():
    # LoL (MSI, LCK)
    try:
        response = requests.get("http://na.lolesports.com/api/programming.json?parameters[method]=all¶meters[week]=1¶meters[tournament]=102¶meters[expand_matches]=1")
        lol_games = [{"jogo": f"{match['contestants']['blue']['name']} vs {match['contestants']['red']['name']}", "data": match.get("dateTime", ""), "torneio": "MSI"} for match in response.json()[0]["matches"].values()]
    except:
        lol_games = [
            {"jogo": "T1 vs Gen.G", "data": "2025-07-15", "torneio": "LCK"},
            {"jogo": "Fnatic vs G2", "data": "2025-07-16", "torneio": "MSI"}
        ]

    # Valorant (VCT, Masters)
    vct_games = [
        {"jogo": "G2 Esports vs Fnatic", "data": "2025-07-20", "torneio": "VCT Masters Toronto"},
        {"jogo": "Paper Rex vs DRX", "data": "2025-07-21", "torneio": "VCT Pacific"}
    ]  # Dados fictícios, substituir por API real se disponível

    # Counter-Strike
    cs_games = [
        {"jogo": "NaVi vs FaZe", "data": "2025-07-18", "torneio": "ESL Pro League"},
        {"jogo": "Vitality vs G2", "data": "2025-07-19", "torneio": "IEM Cologne"}
    ]  # Dados fictícios, substituir por API HLTV se disponível

    # LTA (Tennis)
    lta_games = [
        {"jogo": "Nadal vs Djokovic", "data": "2025-07-22", "torneio": "LTA Championship"},
        {"jogo": "Alcaraz vs Sinner", "data": "2025-07-23", "torneio": "LTA Open"}
    ]  # Dados fictícios

    return lol_games + vct_games + cs_games + lta_games