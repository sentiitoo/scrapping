import requests
from bs4 import BeautifulSoup
import csv
import random
import useragent

brand = "MERCEDES"
year_max = 2023
year_min = 2021
km_min = 0
km_max = 100000
energy = "ess"
price_min = 0
price_max = 200300


def scrap_listing(brand, year_max, year_min, km_min, km_max, energy, price_min, price_max, page_num):
    # Créer un dictionnaire pour stocker les en-têtes
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

    url = f"https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}&options=&page={page_num}"

    response = requests.get(url, headers=headers)
    print("je récupère les informations sur la page : " + url)
    return response.text


if __name__ == "__main__":
     with open('cars.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter='|')
        writer.writerow(['Marque'.ljust(20), 'modèle'.ljust(30), 'Moteur'.ljust(40), 'Année'.ljust(10), 'Kilométrage'.ljust(15), 'Carburant'.ljust(10), 'Prix'])
        
        for page_num in range(1, 2):
            html_page = scrap_listing(brand, year_max, year_min, km_min, km_max, energy, price_min, price_max, page_num)
            soup = BeautifulSoup(html_page, 'html.parser')
            searchCards = soup.find_all(class_="searchCard")
            for searchCard in searchCards:
                characteristics = searchCard.find_all(class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')
                price = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2')
                brand_= searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2')
                motor = searchCard.find(class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2')

                
                price_int = int(price.text.replace("€", "").replace(" ", ""))
                characteristics_year = characteristics[0]
                characteristics_km = int(characteristics[1].text.replace("km", "").replace(" ", "").replace("\xa0", ""))
                characteristics_fuel = characteristics[3]
                model = brand_.text.split(brand)[1].strip()

                
                print(brand_.text, motor.text, "année:", characteristics_year.text, characteristics_km, "carburant:", characteristics_fuel.text, "prix:",price_int)
                writer.writerow([brand.ljust(20), model.ljust(30), motor.text.ljust(40), characteristics_year.text.ljust(10), str(characteristics_km).ljust(15), characteristics_fuel.text.ljust(10), str(price_int)])
