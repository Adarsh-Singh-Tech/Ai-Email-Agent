import email
from email import policy
import webbrowser
import tempfile

def view_eml(file_path):
    with open(file_path, 'rb') as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    html_content = None
    text_content = None

    # Extract content
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type == "text/html":
                html_content = part.get_content()

            elif content_type == "text/plain":
                text_content = part.get_content()
    else:
        if msg.get_content_type() == "text/html":
            html_content = msg.get_content()
        else:
            text_content = msg.get_content()

    # Prefer HTML
    content = html_content or f"<pre>{text_content}</pre>"

    # Save temp HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        temp_file.write(content.encode("utf-8"))
        temp_path = temp_file.name

    # Open in browser
    webbrowser.open(f"file://{temp_path}")


if __name__ == "__main__":
    view_eml("sample_output/ai_news_sample.eml")