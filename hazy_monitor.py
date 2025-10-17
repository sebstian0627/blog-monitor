import requests
from bs4 import BeautifulSoup
import hashlib
import smtplib
from email.mime.text import MIMEText

URL = "https://hazyresearch.stanford.edu/blog"
HASH_FILE = "last_hash.txt"

def check_blog():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the first five post titles
    posts = []
    for article in soup.find_all('article')[:5]:
        title_tag = article.find(['h1', 'h2', 'h3'])
        if title_tag:
            posts.append(title_tag.get_text(strip=True))
    content_hash = hashlib.sha256(''.join(posts).encode()).hexdigest()

    # Load previous hash
    try:
        with open(HASH_FILE, 'r') as f:
            old_hash = f.read().strip()
    except FileNotFoundError:
        old_hash = None

    # If changed, send email and update hash
    if old_hash != content_hash:
        latest = posts[0] if posts else "New content detected"
        send_email(latest)
        with open(HASH_FILE, 'w') as f:
            f.write(content_hash)

def send_email(latest_post):
    body = f"New Hazy Research post:\n\n{latest_post}\n\n{URL}"
    msg = MIMEText(body)
    msg['Subject'] = f"New Hazy Research: {latest_post}"
    msg['From'] = f"{ { secrets.GMAIL_USER } }"
    msg['To'] = f"{ { secrets.GMAIL_USER } }"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(f"{ { secrets.GMAIL_USER } }", f"{ { secrets.GMAIL_PASS } }")
    server.send_message(msg)
    server.quit()

if __name__ == '__main__':
    check_blog()
