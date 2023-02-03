import requests
from bs4 import BeautifulSoup

brand = "PEUGEOT"
year_max = 2020
year_min = 2010
km_max = 100000
km_min = 0
energy = "ess"
price_min = 0
price_max = 28300


def scrap_listing(brand, year_max, year_min, km_min, km_max, energy, price_min, price_max, page_num):
    url = "https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}&options=&page={page_num}".format(
        energy=energy, brand=brand, km_max=km_max, km_min=km_min, price_max=price_max, price_min=price_min, year_max=year_max, year_min=year_min, page_num=page_num)

    response = requests.get(url)

    return response.text


if __name__ == "__main__":
    for page_num in range(1, 11):
        html_page = scrap_listing(brand, year_max, year_min, km_min, km_max, energy, price_min, price_max, page_num)
        soup = BeautifulSoup(html_page, 'html.parser')
        searchCards = soup.find_all(class_="searchCard")
        for searchCard in searchCards:
            characteristics = searchCard.find_all(class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')
            price = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2')
            brand_= searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2')
            motor = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2')

            characteristics_year = characteristics[0]
            characteristics_km = characteristics[1]
            characteristics_fuel = characteristics[3]
            print(brand_.text, motor.text, "année:", characteristics_year.text, characteristics_km.text, "carburant:", characteristics_fuel.text, "prix:", price.text)


