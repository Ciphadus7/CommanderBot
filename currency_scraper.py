from bs4 import BeautifulSoup
import requests


def get_currency(in_currency, out_currency, amt):
    url = f"https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount={amt}"
    content = requests.get(url).text
    soup = BeautifulSoup(content, 'html.parser')
    rate = soup.find("span", class_='ccOutputRslt').get_text()
    rateSimp = rate[0:-8]                     
    return rateSimp                     

