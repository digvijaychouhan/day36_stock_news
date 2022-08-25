import requests
from twilio.rest import Client

account_sid = ""
auth_token = ""

p_no = ""
v_no = ""

STOCK_NAME = "SNOW"
COMPANY_NAME = "Snowflake Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API = ""
NEWS_API = ""

STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API
}

NEWS_PARAMS = {
    "q": "snow",
    "from": "2022-08-24",
    "to": "2022-08-24",
    "sortBy": "popularity",
    "apiKey": NEWS_API
}

response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_data = float(data_list[0]["4. close"])
day_before_yesterday = float(data_list[1]["4. close"])
print(yesterday_data)
print(day_before_yesterday)
stock_diff = yesterday_data - day_before_yesterday
print(stock_diff)
up_down = None
if stock_diff > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

per_diff = round((stock_diff / yesterday_data) * 100)
print(per_diff)

news = []
if abs(per_diff) > 0.04:
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{per_diff}%\nHeadline: {article['title']}. \nBrief: " \
                          f"{article['description']}" for article in three_articles]
    print(formatted_articles)
    client = Client(account_sid, auth_token)
    print(client)
    for article in formatted_articles:
        message = client.messages \
            .create(
                body=article,
                from_=p_no,
                to=v_no
            )
        print(message.status)
