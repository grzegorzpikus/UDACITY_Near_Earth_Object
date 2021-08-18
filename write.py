import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')
    with open(filename, 'w') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        for approach in results:
            row = [approach.time, approach.distance, approach.velocity,
                   approach.neo.designation, approach.neo.name,
                   approach.neo.diameter, approach.neo.hazardous]
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    with open(filename, 'w') as outfile:
        dict_list = []
        for approach in results:
            dictionary = {"datetime_utc": approach.time_str, \
                          "distance_au": approach.distance, \
                          "velocity_km_s": approach.velocity,
                          "neo": {"designation": approach.neo.designation, \
                                  "name": approach.neo.name, "diameter_km": approach.neo.diameter,
                                  "potentially_hazardous": approach.neo.hazardous}}
            dict_list.append(dictionary)
        json.dump(dict_list, outfile, indent=2)
