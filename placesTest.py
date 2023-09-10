import ssl
import urllib.request
import urllib.parse
import urllib.error
import json
from typing import Tuple, List
import os


api_key = os.environ.get("MapsAPIKey")
geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?"
places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"


def print_splash():
    print("""
************************************
***        PLACES NEAR ME        ***
************************************
Enter your location or 'E' to exit.""")


def print_sub_menu():
    print("""
What are you looking for?
1. ATM
2. Bank
3. Bar
4. Cafe
5. Restaurant
6. Store
7. Supermarket   
""")


def get_location(prompt: str) -> Tuple:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    params = dict()
    params['address'] = address
    params['key'] = api_key

    url = geocode_url + urllib.parse.urlencode(params)

    uhandle = urllib.request.urlopen(url, context=ctx)
    data = uhandle.read().decode()

    # print("Retrieved", len(data), "characters.")

    try:
        js = json.loads(data)

    except:
        js = None

    if not js or "status" not in js or js["status"] != "OK":
        print("Failed to retrieve data.")

        return 0, 0, ""

    else:

        # print(json.dumps(js, indent=4))

        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        name = js["results"][0]["formatted_address"]

        return lat, lng, name


def get_places(lat: str, lng: str, radius: str = "1000", typ: str = "restaurant") -> List[str]:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    params = dict()
    params['location'] = lat + " " + lng
    params['radius'] = radius
    params['type'] = typ
    params['key'] = api_key

    url = places_url + urllib.parse.urlencode(params)

    uhandle = urllib.request.urlopen(url, context=ctx)
    data = uhandle.read().decode()

    # print("Retrieved", len(data), "characters.")
    places = []

    try:
        js = json.loads(data)

    except:
        js = None

    if not js or "status" not in js or js["status"] != "OK":
        print("Failed to retrieve data.")
        return places

    else:

        # print(json.dumps(js, indent=4))
        for i in range(len(js["results"])):
            places.append(js['results'][i]['name'][:30].ljust(30) + " - " + js['results'][i]['vicinity'])

        return places


if __name__ == '__main__':
    print_splash()

    while True:
        address = input("\nEnter location: \n> ").strip()
        if address.upper() == "E":
            exit()
        elif address.upper() == "H" or address.upper() == "HELP":
            print_splash()
        else:
            lat, lng, name = get_location(address)

            if lat == 0 and lng == 0 and name == "":
                continue

            print(f"{name}: latitude {lat}, longitude {lng}")

            print_sub_menu()

            typ = ""
            while True:
                option = input("> ")
                if option == "1":
                    typ = "atm"
                    break
                elif option == "2":
                    typ = "bank"
                    break
                elif option == "3":
                    typ = "bar"
                    break
                elif option == "4":
                    typ = "cafe"
                    break
                elif option == "5":
                    typ = "restaurant"
                    break
                elif option == "6":
                    typ = "store"
                    break
                elif option == "7":
                    typ = "supermarket"
                    break

                else:
                    print("Invalid option.")

            results = get_places(str(lat), str(lng), typ=typ)
            for r in results:
                print(r)





