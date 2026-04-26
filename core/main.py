from news_fetcher import get_ai_news
from ai_utils import summarize_news
from email_utils import send_email

def run():
    print("Fetching news...")
    articles = get_ai_news()

    print("Summarizing...")
    summary = summarize_news(articles)

    print("Sending email...")
    send_email(summary)

    print("✅ Email sent successfully!")

if __name__ == "__main__":
    run()