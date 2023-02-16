import requests
from bs4 import BeautifulSoup
import csv
import random
from fake_useragent import UserAgent


brand = input("Entrez une marque MERCEDES, AUDI, PEUGEOT : ")
year_min = int(input("Entrez l'année minimale : "))
year_max = int(input("Entrez l'année maximale : "))
km_min = int(input("Entrez le kilométrage minimal : "))
km_max = int(input("Entrez le kilométrage maximal : "))
energy = input(
    "Entrez le type de carburant  essence:ess, diesiel: dies, electrique: elec : ")
price_min = int(input("Entrez le prix minimal : "))
price_max = int(input("Entrez le prix maximal : "))

# Variables utilisées pour stocker les filtres à appliquer lors de la recherche des annonces de voitures.


def scrap_listing(brand, year_max, year_min, km_min, km_max, energy, price_min, price_max, page_num):
    # Créer un dictionnaire pour stocker les en-têtes
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"}

    url = f"https://www.lacentrale.fr/listing?energies={energy}&makesModelsCommercialNames={brand}&mileageMax={km_max}&mileageMin={km_min}&priceMax={price_max}&priceMin={price_min}&yearMax={year_max}&yearMin={year_min}&options=&page={page_num}"

    response = requests.get(url, headers=headers)
    print("je récupère les informations sur la page : " + url)
    return response.text

# Fonction qui récupère une page de résultats de recherche à partir du site La Centrale,
# en utilisant les paramètres fournis.
# enoie une requête GET à l'aide du module requests puis retourne le contenu HTML de la page.


if __name__ == "__main__":
    with open('cars.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(['Marque'.ljust(20), 'modèle'.ljust(30), 'Moteur'.ljust(
            40), 'Année'.ljust(10), 'Kilométrage'.ljust(15), 'Carburant'.ljust(10), 'Prix'])

#  ouverture d'un fichier 'cars.csv' en mode écriture et utilise la méthode csv.writer
#  pour écrire les en-têtes de colonne dans le fichier.

        for page_num in range(1, 11):
            html_page = scrap_listing(
                brand, year_max, year_min, km_min, km_max, energy, price_min, price_max, page_num)
            soup = BeautifulSoup(html_page, 'html.parser')
            searchCards = soup.find_all(class_="searchCard")
            for searchCard in searchCards:
                characteristics = searchCard.find_all(
                    class_='Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2')
                price = searchCard.find(
                    class_='Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2')
                brand_ = searchCard.find(
                    class_='Text_Text_text Vehiculecard_Vehiculecard_title Text_Text_subtitle2')
                motor = searchCard.find(
                    class_='Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2')

                price_ = int(price.text.replace("€", "").replace(" ", ""))
                characteristics_year = int(characteristics[0].text)
                characteristics_km = int(characteristics[1].text.replace(
                    "km", "").replace(" ", "").replace("\xa0", ""))
                characteristics_fuel = characteristics[3]
                model = brand_.text.split(brand)[1].strip()

# Boucle for pour parcourir les pages ddu site La Centrale
# La fonction scrap_listing est appelée pour chaque page.

                print(f"marque: {brand} modèle: {model} moteur: {motor.text} année: {characteristics_year}, kilométrage: {characteristics_km} carburant: {characteristics_fuel.text} prix: {price_}")
                writer.writerow([brand.ljust(20), model.ljust(30), motor.text.ljust(
                    40), str(characteristics_year).ljust(10), str(characteristics_km).ljust(15), characteristics_fuel.text.ljust(10), price_])
# Ecriture des données dans le fichier csv.
