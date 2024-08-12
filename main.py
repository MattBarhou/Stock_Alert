import requests
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = os.environ['STOCK_API_KEY']
API_KEY = os.environ['API_KEY']
STOCK_ENDPOINT = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={STOCK_API_KEY}"
NEWS_ENDPOINT = f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&apiKey={API_KEY}"
URL = f"https://newsapi.org/v2/everything?q=from=2024-08-11&to=2024-08-12&sortBy=publishedAt&pageSize=3&apiKey={API_KEY}"
three_articles = None


#Fetch the article description
def get_articles():
    global three_articles
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        three_articles = articles[:3]  # Assign the first three articles to the global variable


stock_response = requests.get(STOCK_ENDPOINT)
if stock_response.status_code == 200:
    info = stock_response.json()

    yesterday_closing = float(info['Time Series (Daily)']['2024-08-02']['4. close'])
    day_before_closing = float(info['Time Series (Daily)']['2024-08-01']['4. close'])

    #calculate percentage increase
    increase = ((yesterday_closing - day_before_closing) / day_before_closing * 100)

    #Check if the price of the stock has increased or decreased by 5%
    if abs(increase) >= 5:
        get_articles()
    else:
        print("No significant price movements")
else:
    print(f'Error occurred: {stock_response.status_code}')



# Send a separate message with each article's title and description to phone number.

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

formatted_articles = [f'Latest story: {article["title"]}\n {article["description"]}' for article in three_articles]

for article in formatted_articles:

    message = client.messages.create(
        body=article,
        from_="+14692083653",
        to="+16479685744",
    )

    print(message.body)

