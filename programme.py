import csv
import os


class InvalidInput(Exception):
    "Raised when the input do not match valid value"
    pass



def accueil():
    while True:
        try:
            print("1. Afficher les tous les immeubles")
            print("2. Faire une recherche")
            choice = input("Choisissez une commande: ").strip()

            match choice:
                case "1":
                    buildings = get_all_building()
                    buildings_sort_by_id = sorted(
                        buildings, key=lambda d: d["building_id"])
                    buildings_sort_by_lastname = sorted(
                        buildings, key=lambda d: d["lastname"])
                    print_result(buildings_sort_by_id)
                    print()
                    print_result(buildings_sort_by_lastname)

                case "2":
                    search()
                    # affiche la recherche

                case _:
                    print("Valeur invalide")
                    raise InvalidInput
                    # this.input
        except InvalidInput:
            continue
        else:
            break


############# Recherche ##############
def search():
    while True:
        try:
            input_header = input("Veuillez choisir la catégorie de la recherche: ").strip()
            input_search = input("Saisissez votre recherche: ").strip()
            buildings = get_search_all_file(input_header, input_search)
            if(len(buildings) == 0):
                print("Aucun résultat")
            else:
                buildings_sort_by_id = sorted(buildings, key=lambda d: d["building_id"])
                buildings_sort_by_lastname = sorted(buildings, key=lambda d: d["lastname"])
                print_result(buildings_sort_by_id)
                print()
                print_result(buildings_sort_by_lastname)
                accueil()

        except InvalidInput:
            print("Catégorie invalide")
            continue
        else:
            break

def get_search_all_file(input_header: str, input_search: str) -> list[dict]:
    buildings: list[dict] = []
    paths = get_all_file_path()
    for path in paths:
        buildings.extend(get_search_csv(input_header, input_search, path))
    return buildings

def get_search_csv(input_header: str, input_search: str, path: str) -> list[dict]:
    retour: list[dict] = []
    with open(path, "r") as file:
        csv_dict_reader = csv.DictReader(file)
        if input_header in csv_dict_reader.fieldnames:
            for row in csv_dict_reader:
                if(row[input_header].lower() == input_search.lower()):
                    retour.append(row)
        else:
            raise InvalidInput
    return retour


############### Tout ###########################

def get_all_file_path() -> list[str]:
    directory = 'data'
    files_path: list[str] = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        files_path.append(file_path)
    return files_path


def get_building_csv(path: str) -> list[dict]:
    retour = []
    with open(path, "r") as file:
        csv_dict_reader = csv.DictReader(file)
        for row in csv_dict_reader:
            retour.append(row)
    return retour


def get_all_building() -> list[dict]:
    buildings: list[dict] = []
    paths = get_all_file_path()
    for path in paths:
        buildings.extend(get_building_csv(path))
    return buildings

###############

def print_result(results: list[dict]):
    keys = results[0].keys()
    format_row = "{:<26}" * (len(keys))
    print(format_row.format(*keys))
    for row in results:
        print(format_row.format(*row.values()))

######################



accueil()