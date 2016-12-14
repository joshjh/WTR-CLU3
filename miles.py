__author__ = 'josh'
import re
from datetime import datetime
import CLU_FIXED_VALUES
import googlemaps
from CLU_FIXED_VALUES import bcolors


def get_mileage(ps1='PL22BG', ps2=''):
    """
    :param ps1: The home post code
    :param ps2: Our current post code
    :return: The mileage between the two from google api
    """
    try:

        if check_ps_valid(ps1) and check_ps_valid(ps2):

            gmaps = googlemaps.Client(key='AIzaSyBOznCk1vrnWD_Gk6y5lZuX8BGBJM_8j4Y')
            now = datetime.now()

            directions_result = gmaps.directions(ps1, ps2, mode="driving", departure_time=now, units='imperial', region='uk',
                             alternatives=False)
            # this is terrible, there must be a better way of getting and int mileage.
            # google api returns a mess of nested dictionaries and lists
            # the below offensive next drills though the dictionary nest, extracts the value of 'distance and txt, strips 'mi'
            # out, then drops a integer, which is returned

            distance = float(str(dict(dict(dict(directions_result[0].get('legs')[0])).get('distance')).get('text')).strip(' mi'))
            return distance
    except googlemaps.exceptions.ApiError:
        print(bcolors.FAIL + ' GOOGLE API EXCEPTION - CANNOT CHECK POSTCODE' + bcolors.ENDC)


def check_ps_valid(ps):

    for x in range(len(CLU_FIXED_VALUES.POSTCODE_FORMATS)):
        match = re.search(CLU_FIXED_VALUES.POSTCODE_FORMATS[x], ps.replace(' ', ''))

    if match is None:
        print(bcolors.FAIL + 'cannot match {} to re expression for postcodes' + bcolors.ENDC)
        return False

    else:
        return True

