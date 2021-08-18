import csv
import json
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    list_of_neo = []
    with open(neo_csv_path, 'r') as infile:
        data_neo = csv.DictReader(infile)
        for line in data_neo:
            neo_instance = NearEarthObject(**line)
            list_of_neo.append(neo_instance)
    return list_of_neo


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    list_of_ca = []
    with open(cad_json_path) as infile:
        data_ca = json.load(infile)
        for dictionary in data_ca['data']:
            ca_instance = CloseApproach(dictionary)
            list_of_ca.append(ca_instance)
    return list_of_ca