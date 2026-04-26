import schedule
import time
from news_fetcher import get_ai_news
from ai_utils import summarize_news
from email_utils import send_email
from config import NEWS_TIME

def job():
    print("Fetching news...")
    articles = get_ai_news()

    print("Summarizing...")
    summary = summarize_news(articles)

    print("Sending email...")
    send_email(summary)

    print("Done!")

def run_scheduler():
    schedule.every().day.at(NEWS_TIME).do(job)

    print(f"Running... Email scheduled at {NEWS_TIME}")

    while True:
        schedule.run_pending()
        time.sleep(60)