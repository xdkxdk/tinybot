""" Contains functions to fetch info from different simple online APIs."""
from utilities import web


def urbandictionary_search(search):
    """
    Searches urbandictionary's API for a given search term.
    :param search: The search term str to search for.
    :return: defenition str or None on no match or error.
    """
    if str(search).strip():
        urban_api_url = 'http://api.urbandictionary.com/v0/define?term=%s' % search
        response = web.http_get(urban_api_url, json=True)
        if response['json'] is not None:
            try:
                definition = response['json']['list'][0]['definition']
                return definition.encode('ascii', 'ignore')
            except (KeyError, IndexError):
                return None
    else:
        return None


def weather_search(city):
    """
    Searches worldweatheronline's API for weather data for a given city.
    You must have a working API key to be able to use this function.
    :param city: The city str to search for.
    :return: weather data str or None on no match or error.
    """
    if str(city).strip():
        api_key = '1a7c7025fa5dec52e070bbc5a7714'
        if not api_key:
            return 'Missing api key.'
        else:
            weather_api_url = 'http://api.worldweatheronline.com/free/v2/weather.ashx?' \
                              'q=%s&format=json&key=%s' % (city, api_key)

            response = web.http_get(weather_api_url, json=True)
            if response['json'] is not None:
                try:
                    pressure = response['json']['data']['current_condition'][0]['pressure']
                    temp_c = response['json']['data']['current_condition'][0]['temp_C']
                    temp_f = response['json']['data']['current_condition'][0]['temp_F']
                    query = response['json']['data']['request'][0]['query'].encode('ascii', 'ignore')
                    result = '%s. Temperature: %sC (%sF) Pressure: %s millibars' % (query, temp_c, temp_f, pressure)
                    return result
                except (IndexError, KeyError):
                    return None
    else:
        return None


def whois(ip):
    """
    Searches ip-api for information about a given IP.
    :param ip: The ip str to search for.
    :return: information str or None on error.
    """
    if str(ip).strip():
        url = 'http://ip-api.com/json/%s' % ip
        response = web.http_get(url, json=True)
        if response['json'] is not None:
            try:
                city = response['json']['city']
                country = response['json']['country']
                isp = response['json']['isp']
                org = response['json']['org']
                region = response['json']['regionName']
                zipcode = response['json']['zip']
                info = country + ', ' + city + ', ' + region + ', Zipcode: ' + zipcode + '  Isp: ' + isp + '/' + org
                return info
            except KeyError:
                return None
    else:
        return None


def chuck_norris():
    """
    Finds a random Chuck Norris joke/quote.
    :return: joke str or None on failure.
    """
    url = 'http://api.icndb.com/jokes/random/?escape=javascript'
    response = web.http_get(url, json=True)
    if response['json'] is not None:
        if response['json']['type'] == 'success':
            joke = response['json']['value']['joke'].decode('string_escape')
            return joke
        return None


def hash_cracker(hash_str):
    """
    Using md5cracker.org to crack md5 hashes with.
    :param hash_str: str the md5 hash to crack.
    :return: dict{'status', 'result', 'message'} or None on error.
    """
    url = 'http://md5cracker.org/api/api.cracker.php?r=9327&database=md5cracker.org&hash=%s' % hash_str
    response = web.http_get(url, json=True)
    if response['json'] is not None:
        return {
            'status': response['json']['status'],
            'result': response['json']['result'],
            'message': response['json']['message']
        }
    return None
