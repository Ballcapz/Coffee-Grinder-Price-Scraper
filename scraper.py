import requests
from bs4 import BeautifulSoup
import smtplib

URL = 'https://www.seattlecoffeegear.com/baratza-sette-30-grinder'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

email_sender = 'zach.dev.full.send@gmail.com'
receivers = ['zlg23johnson@gmail.com']

def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(id="product-price-12655").find("span").get_text()
    converted_price = float(price[1:5])

    if (converted_price <= 226.0):
        send_mail()
    else:
        print(converted_price)

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email_sender, 'pborkseiidokifdq')

    subject = 'Baratza Grinder Price Down'
    body = 'Check the link ' + URL

    message = f"Subject: {subject}\n\n{body}"

    try:
        server.sendmail(email_sender, receivers, message)
        print("Email sent successfully")
    except Exception:
        print("Error: unable to send email")

    server.quit()


check_price()