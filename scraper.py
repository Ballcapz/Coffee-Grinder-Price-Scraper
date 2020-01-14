import os
import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
load_dotenv()

EMAIL_PWD = os.getenv("EMAIL_APP_CREDS")

SCG_URL = 'https://www.seattlecoffeegear.com/baratza-sette-30-grinder'
AMZN_URL = 'https://www.amazon.com/Baratza-Sette-30-Conical-Grinder/dp/B075G11F9N/ref=sr_1_2?crid=2Z502RIPRQ7E9&keywords=baratza+sette+30&qid=1572464591&sprefix=baratza+se%2Caps%2C188&sr=8-2'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}

email_sender = 'zach.dev.full.send@gmail.com'
receivers = ['zlg23johnson@gmail.com']

def check_scg_coffee_price():
    page = requests.get(SCG_URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    price = soup.find(id="product-price-12655").find("span").get_text()
    converted_price = float(price[1:5])

    if (converted_price <= 226.0):
        bara_subject = 'Baratza Grinder Price Drop!'
        bara_body = f'Check it out here {SCG_URL}'
        send_mail(bara_subject, bara_body)
    else:
        print(f'SCG Price is currently {converted_price}')

def check_amzn_coffee_price():
    page = requests.get(AMZN_URL, headers=headers)

    amzn_soup = BeautifulSoup(page.content, 'html.parser')
    real_amzn_soup = BeautifulSoup(amzn_soup.prettify(), 'html.parser')

    amzn_price = real_amzn_soup.find(id="priceblock_ourprice").get_text()
    amzn_converted_price = float(amzn_price[1:5])

    if (amzn_converted_price <= 226.0):
        amzn_subject = 'Baratza Grinder Price Drop!'
        amzn_body = f'Check it out here {AMZN_URL}'
        send_mail(amzn_subject, amzn_body)
    else:
        print(f'Amazon price is currently {amzn_converted_price}')

def send_mail(subject, body):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(email_sender, EMAIL_PWD)

    message = f"Subject: {subject}\n\n{body}"

    try:
        server.sendmail(email_sender, receivers, message)
        print("Email sent successfully")
    except Exception:
        print("Error: unable to send email")

    server.quit()


check_scg_coffee_price()
check_amzn_coffee_price()
