"""
author : Nathan ROI
"""

from serpapi import GoogleSearch
import csv
import os  # Gestion des dossiers
from datetime import date

API_KEY = "" # Get your API KEY at https://serpapi.com/

# =========================== requête serpAPI sur google trends =========================== #

def req(input_value):
    """
    Envoie une requête à SerpAPI pour obtenir les données de Google Trends
    pour une recherche donnée (input_value).

    :param input_value : String : valeur de recherche
    :return res : Dict : dictionnaire avec les résultats de la recherche
    """
    params = {
        "api_key": API_KEY,         # Clé API SerpAPI
        "engine": "google_trends",  # Spécifie l'utilisation de l'engine Google Trends
        "q": input_value,           # Le terme recherché
        "hl": "fr",                 # Langue
        "data_type": "GEO_MAP_0",   # Type de données demandées (répartition géographique ici)
        "region": "REGION",         # Région cible
        "geo": "FR",                # Code géographique
        "date": "all",              # Période de temps (à partir de 2004 jusqu'à aujourd'hui)
        "tz": "-60"                 # Fuseau horaire
    }

    res_search = GoogleSearch(params)
    res = res_search.get_dict()
    return res


# =========================== formattage des données de serpAPI =========================== #

def format_data(res_search):
    """
    Formate les données obtenues via SerpAPI pour n'extraire que les régions
    et leurs valeurs d'intérêt.

    :param res_search: Array of dict
    :return region_format: Array of dict
    """

    regions = res_search['interest_by_region']
    region_format = []

    for elem in regions:
        print({'location' : elem['location'], 'value' : elem['value']})
        region_format.append({'location' : elem['location'], 'value' : elem['value']})

    return region_format


# =========================== création d'un fichier csv =========================== #
def jouJ():
    """
    :return: String : renvoie la date d'aujourd'hui selon le format : DD-MM-YYYY
    """
    return  date.today().strftime("%d-%m-%Y")

def create_directory_with_date():
    """
    Créer un dossier avec la date d'aujourd'hui
    :return:
    """
    # Obtenir la date du jour
    foldername = jouJ()

    # Créer un dossier avec le nom de la date s'il n'existe pas
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    return foldername

def create_filename(text, folder_name):
    """
    Crée un nom de fichier basé sur le texte de la recherche et la date actuelle.
    Format : terme_recherche_DD-MM-YYYY.csv.

    :param folder_name: String : nom du dossier dans lequel le fichier doit être enregistré
    :param text: String : terme(s) de la recherche
    :return: String : nom du fichier à enregistrer
    """
    today_date = jouJ()
    filename  = text.replace(" ", "_") + "_" + today_date + ".csv"

    full_path = os.path.join(folder_name, filename)

    return full_path

def create_csv(res_format, file_name):
    """
    Écrit les données formatées dans un fichier CSV avec le nom spécifié.

    :param res_format: Array of dict : tableau de dictionnaire contenant les données à enregistrer
    :param file_name: String : nom du fichier
    :return: None
    """
    #Création et écriture dans le fichier CSV
    with open(file_name, mode="w", newline="", encoding="utf-8") as file:
        # Définir les noms des colonnes
        fieldnames = ["location", "value"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Écrire les en-têtes
        writer.writeheader()

        # Écrire les données
        writer.writerows(res_format)

    print("Fichier CSV créé avec succès !")


# =========================== proposition de nouvelle recherche =========================== #

def new_search():
    """
    Propose à l'utilisateur de lancer une nouvelle recherche ou de quitter.

    :return: None
    """
    choix = input("Voulez-vous faire une nouvelle recherche ? y/n ")
    match choix.upper():
        case 'Y':
            return search()
        case 'N':
            print("\nciao !")
            return exit(0)


# =========================== effectue une recherche et enregistre le résultat dans un CSV =========================== #

def search():
    """
    Fonction principale : permet de chercher un terme, formater les résultats,
    les écrire dans un fichier CSV, puis proposer une nouvelle recherche.

    :return: None
    """
    input_value = input("Chercher : ")
    res = req(input_value)
    if 'error' in res:
        print(res['error'])
        new_search()
    else :
        data = format_data(res)
        create_csv(data, create_filename(input_value, create_directory_with_date()))
        new_search()

#### Lancement du programme ####
search()