# -*- coding: UTF-8 -*-
"""FI MUNI Brno - IB111: Basics of Programming, Advanced Group
-Project 2: Handling data from Adaptive Learning - slepemapy.cz."""

import csv
import requests
import pycountry_convert

"""
@article{
  author={Papou{\v{s}}ek, Jan and Pel{\'a}nek, Radek and Stanislav, V{\'\i}t},
  title={Adaptive Geography Practice Data Set},
  journal={Journal of Learning Analytics},
  year={2015},
  issn={1929-7750}
}
"""


def load_answer(limit: int = 1000000) -> dict:
    """Loads the csv file with answers from the dataset.
    Limit = amount of rows loaded."""
    with open("answer.csv") as csv_file:
        keys = ["id", "user", "place_asked", "place_answered",
                "type", "inserted", "response_time", "place_map",
                "language", "options", "ip_country", "ip_id"]
        csv_data = csv.reader(csv_file, delimiter=';')
        answers = {}
        for key in keys:
            answers[key] = []

        for row_id, row in enumerate(csv_data):
            if row_id > 0:
                # int -> id, user, place_asked, place_answered, type,
                # response_time, place_map, language, ip_country, ip_id
                # array of int -> options
                for key_id, key in enumerate(keys):
                    if key in ["id", "user", "place_asked", "place_answered",
                               "type", "response_time", "place_map",
                               "language", "ip_id"]:
                        if row[key_id]:
                            answers[key].append(int(row[key_id]))
                        else:
                            answers[key].append(0)
                    elif key in ('inserted', 'ip_country'):
                        answers[key].append(row[key_id])
                    elif key == "options":
                        answers[key].append(row[key_id])

                if row_id > limit:  # max=5000000
                    break
        return answers


def load_place() -> dict:
    """Loads the csv file with places from the dataset."""
    with open("place_laos_optimized.csv", encoding='utf-8') as csv_file:
        keys = ["id", "code", "name", "type", "maps"]
        csv_data = csv.reader(csv_file, delimiter=';')
        places = {}
        for key in keys:
            places[key] = []
        for row_id, row in enumerate(csv_data):
            if row_id > 0:
                # int -> id, type
                # str -> code, name, maps
                for key_id, key in enumerate(keys):
                    if key in ["id", "type"]:
                        if row[key_id]:
                            places[key].append(int(row[key_id]))
                        else:
                            places[key].append(0)
                    else:
                        places[key].append(row[key_id])
        return places


def load_place_type() -> list:
    """Loads the csv file with place types from the dataset."""
    with open("place_type.csv") as csv_file:
        place_types = []
        csv_data = csv.reader(csv_file, delimiter=';')
        for row_id, row in enumerate(csv_data):
            if row_id > 0:
                place_types.append(row[1])
        return place_types


def avg(array: list, dec_round=None) -> float:
    """Returns the average value of the given array."""
    if dec_round:
        return round(sum(array) / len(array), dec_round)
    else:
        return round(sum(array) / len(array))
    # return round(sum(array) / len(array), dec_round) if dec_round else round(
    #     sum(array) / len(array))


def average_response_time(answers: dict) -> None:
    """Prints the average response time from the list of given answers"""
    print("Average response time", avg(answers["response_time"]) / 1000,
          "seconds")


def compare_question_types(answers: dict) -> None:
    """Is it easier to name the place or locate the place,
    which takes longer?"""
    locate_times = []
    name_times = []

    # 1 = correct answer, 0 = incorrect
    locate_success = []
    name_success = []

    for i in range(len(answers["id"])):
        # 1 = find on map, 2 = name the place

        if answers["type"][i] == 1:
            locate_times.append(answers["response_time"][i] / 1000)
            locate_success.append(
                int(answers["place_asked"][i] == answers["place_answered"][i]))

        elif answers["type"][i] == 2:
            name_times.append(answers["response_time"][i] / 1000)
            name_success.append(
                int(answers["place_asked"][i] == answers["place_answered"][i]))

    print("Avg for locate on map:", avg(locate_times), "seconds")
    print("Avg for name the location:", avg(name_times), "seconds")
    print("Success rate for locating on map:", avg(locate_success, 2) * 100,
          "%")
    print("Success rate for naming the location:", avg(name_success, 2) * 100,
          "%")


def compare_language_stats(answers: dict) -> None:
    """Statistics according to the language used
    Language version of the system: 0) Czech, 1) English, 2) Spanish."""
    langs = ["Czech", "English", "Spanish"]
    lang_success = {}
    lang_time = {}

    for i in range(len(answers["language"])):
        if answers["language"][i] in lang_success.keys():
            lang_time[answers["language"][i]].append(
                answers["response_time"][i] / 1000)
            lang_success[answers["language"][i]].append(
                int(answers["place_asked"][i] == answers["place_answered"][i]))
        else:
            lang_time[answers["language"][i]] = \
                [answers["response_time"][i] / 1000]
            lang_success[answers["language"][i]] = \
                [int(answers["place_asked"][i] == answers["place_answered"][i])]

    for lang in lang_time:
        print("Avg time for {}:".format(langs[lang]), avg(lang_time[lang]),
              "seconds")
        print("Success rate for {}:".format(langs[lang]),
              avg(lang_success[lang], 2) * 100, "%")


def add_time_data(time_of_day: int, answers: dict, tod_success: dict,
                  tod_time: dict, i: int) -> tuple:
    """Add data to success and time dictionaries according
     to the time of the day."""
    times = ["Morning", "Midday", "Afternoon", "Evening", "Night"]

    if times[time_of_day] in tod_success.keys():
        tod_time[times[time_of_day]].append(answers["response_time"][i] / 1000)
        tod_success[times[time_of_day]].append(
            int(answers["place_asked"][i] == answers["place_answered"][i]))
    else:
        tod_time[times[time_of_day]] = [answers["response_time"][i] / 1000]
        tod_success[times[time_of_day]] = \
            [int(answers["place_asked"][i] == answers["place_answered"][i])]

    return tod_success, tod_time


def compare_times_of_day(answers: dict) -> None:
    """ Statistics according to tge time of the day
    Morning: 6AM - 10AM, Midday: 11AM - 3PM, Afternoon: 4PM - 7PM,
    Evening: 8PM - 11PM, Night: 12AM - 5AM.
    tod = time of day
    (yyyy-mm-dd hh:mm:ss)"""
    tod_success = {}
    tod_time = {}

    time_ranges = [(6, 10), (11, 15), (16, 19), (20, 23), (0, 5)]
    for i in range(len(answers["inserted"])):
        for j in range(len(time_ranges)):
            if time_ranges[j][0] <= int(answers["inserted"][i][11:13]) <= \
                    time_ranges[j][1]:
                tod_success, tod_time = add_time_data(j, answers, tod_success,
                                                      tod_time, i)
        # if 6 <= int(answers["inserted"][i][11:13]) <= 10:
        #     tod_success, tod_time = add_time_data(0, answers, tod_success,
        #                                           tod_time, i)
        # elif 11 <= int(answers["inserted"][i][11:13]) <= 15:
        #     tod_success, tod_time = add_time_data(1, answers, tod_success,
        #                                           tod_time, i)
        # elif 16 <= int(answers["inserted"][i][11:13]) <= 19:
        #     tod_success, tod_time = add_time_data(2, answers, tod_success,
        #                                           tod_time, i)
        # elif 20 <= int(answers["inserted"][i][11:13]) <= 23:
        #     tod_success, tod_time = add_time_data(3, answers, tod_success,
        #                                           tod_time, i)
        # elif 0 <= int(answers["inserted"][i][11:13]) <= 5:
        #     tod_success, tod_time = add_time_data(4, answers, tod_success,
        #                                           tod_time, i)

    print_tod_stats(tod_success, tod_time)


def print_tod_stats(tod_success: dict, tod_time: dict) -> None:
    """Prints the statistics according to the time of the day."""
    for tod in tod_success.keys():
        print("Avg time for {}:".format(tod),
              avg(tod_time[tod]), "seconds")
        print("Success rate for {}:".format(tod),
              avg(tod_success[tod], 2) * 100, "%")


def geo_object_type_stats(answers: dict, places: dict, place_types: list) \
        -> None:
    """What is is easiest type of geographical object to answer?"""
    types_succ = {}
    for i in range(len(answers["type"])):
        curr_place_type = place_types[places["type"]
                                      [answers["place_asked"][i]] - 1]
        if curr_place_type in types_succ.keys():
            types_succ[curr_place_type].append(
                int(answers["place_asked"][i] == answers["place_answered"][i]))
        else:
            types_succ[curr_place_type] = \
                [int(answers["place_asked"][i] == answers["place_answered"][i])]

    for obj_type in types_succ:
        print("Success rate for {}:".format(obj_type),
              avg(types_succ[obj_type], 2) * 100, "%")


def get_continent(place: str) -> str or None:
    """Uses the HERE Maps API to determine on which continent
    the given place is located."""
    url = "https://geocoder.api.here.com/6.2/geocode.json"
    parameters = {'app_id': "yx6gGIhrAsuHt2xAsWYl",
                  'app_code': "9tLzXvWE-vMGT7DangdpPA",
                  'addressattributes': "country",
                  'searchtext': place}
    result = requests.get(url, params=parameters)
    data = result.json()
    if data["Response"]["View"]:
        try:
            country_code_alpha3 = \
                data["Response"]["View"][0]["Result"][-1]["Location"] \
                    ["Address"]["Country"]
            country_code = pycountry_convert. \
                country_alpha3_to_country_alpha2(country_code_alpha3)
            fetched_continent = pycountry_convert. \
                country_alpha2_to_continent_code(country_code)
            continents = {'AF': "Africa",
                          'NA': "North America",
                          'OC': "Oceania",
                          'AN': "Antarctica",
                          'AS': "Asia",
                          'EU': "Europe",
                          'SA': "South America"}
            return continents[fetched_continent]
        except KeyError:
            return None
    else:
        return None


def cz_sk_continent_analysis(answers: dict, places: dict,
                             query_limit: int = 1000) -> None:
    """Which continent do Czechs and Slovaks know best/worst?"""
    query_count = 0
    czsk_answers = {}
    print("len answ", len(answers["language"]))
    for a_id in range(len(answers["language"])):
        # print(a_id, query_count)
        if a_id > 0 and query_count < query_limit:
            if answers["language"][a_id] == 0:
                plc_id = answers["place_asked"][a_id]
                place_name = places["name"][plc_id + 1]
                continent = get_continent(place_name)
                query_count += 1
                print(query_count)
                if continent:
                    if continent in czsk_answers.keys():
                        czsk_answers[continent].append(
                            int(answers["place_asked"][a_id] ==
                                answers["place_answered"][a_id]))
                    else:
                        czsk_answers[continent] = \
                            [int(answers["place_asked"][a_id] ==
                                 answers["place_answered"][a_id])]

    for cont in list(czsk_answers.keys()):
        print("Success rate for {}:".format(cont),
              avg(czsk_answers[cont], 2) * 100, "%")


# ------------------------------ MAIN PROGRAMME ------------------------------

MY_ANSWERS = load_answer()
MY_PLACES = load_place()
MY_PLACE_TYPES = load_place_type()
average_response_time(MY_ANSWERS)
compare_question_types(MY_ANSWERS)
compare_language_stats(MY_ANSWERS)
compare_times_of_day(MY_ANSWERS)
geo_object_type_stats(MY_ANSWERS, MY_PLACES, MY_PLACE_TYPES)
cz_sk_continent_analysis(MY_ANSWERS, MY_PLACES)

# print(get_continent("Bratislava"))
# print(czsk_answers)
# print(answers["language"])
# print(query_count)
