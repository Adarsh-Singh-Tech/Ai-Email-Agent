import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL, APP_PASSWORD


def make_links_clickable(text):
    return re.sub(
        r'(https?://\S+)',
        r'<a href="\1" target="_blank" style="color:#2563eb;">Read more</a>',
        text
    )


def format_html(content):
    content = make_links_clickable(content)

    # Convert markdown-like headings to styled HTML
    content = content.replace("## 🧠 Top Insight", "<h2 style='margin-top:20px;'>🧠 Top Insight</h2>")
    content = content.replace("## 🔥 AI News", "<h2 style='margin-top:20px;'>🔥 AI News</h2>")
    content = content.replace("## 📊 Trend Summary", "<h2 style='margin-top:20px;'>📊 Trend Summary</h2>")

    content = content.replace("### 🔹", "<div style='margin-top:20px; padding:15px; background:#f9fafb; border-radius:10px;'><h3>🔹")
    content = content.replace("**What happened:**", "</h3><p><b>What happened:</b>")
    content = content.replace("**Why it matters:**", "</p><p><b>Why it matters:</b>")
    content = content.replace("**Impact:**", "</p><p><b>Impact:</b>")
    content = content.replace("**Source:**", "</p><p><b>Source:</b>")

    content = content.replace("\n", "<br>") + "</p></div>"

    return f"""
    <html>
    <body style="font-family: Arial; background:#eef2f7; padding:20px;">
        
        <div style="max-width:720px; margin:auto; background:white; padding:30px; border-radius:12px;">

            <h1 style="margin-bottom:10px;">🚀 AI Intelligence Brief</h1>
            <p style="color:#555;">Hi Adarsh, here’s your curated AI update:</p>

            <div style="margin-top:20px;">
                {content}
            </div>

            <hr style="margin-top:30px;">
            <p style="font-size:12px; color:#999;">
                Clean. Filtered. Insightful.
            </p>

        </div>

    </body>
    </html>
    """


def send_email(content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🚀 AI Intelligence Brief"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    html_content = format_html(content)

    msg.attach(MIMEText(html_content, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()