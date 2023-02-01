import requests
from bs4 import BeautifulSoup

page = "&page=1"

brand = "PEUGEOT"
year_max = 2020
year_min = 2010
km_max = 100000
km_min = 1000
energy = "ess"
price_min = 1400
price_max = 28300


def scrap_listing(brand, year_max, year_min, km_min, km_max, energy, price_min, price_max):
    url = "https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}".format(
        energy=energy, brand=brand, km_max=km_max, km_min=km_min, price_max=price_max, price_min=price_min, year_max=year_max, year_min=year_min)

    response = requests.get(url)

    return response.text


if __name__ == "__main__":
    html_page = scrap_listing(
        brand, year_max, year_min, km_min, km_max, energy, price_min, price_max)
    soup = BeautifulSoup(html_page, 'html.parser')
    searchCard = soup.find_all(class_='searchCard')
    for searchCard in searchCard:
        print(searchCard.text)
