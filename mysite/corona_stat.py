import requests
import json
import datetime as dt

site = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
response = requests.get(site)
info = response.json()['records']


today = dt.datetime.now()
today_formatted = today.strftime("%d/%m/%Y")

print("Please, insert date OR country. Leave other empty.")
date = input('Fetch data from certain date (format dd/mm/yyyy): ')
country = input('Fetch data from certain country (format eg. United Kingdom): ')
country = country.replace(" ", "_")

if date == "" and country == "":
    print("Please, check your inputs.")

i = 0
try:
    total_cases = 0
    total_deaths = 0
    if date != "":
        if len(date) != 10 or "/" not in (date[2] or "/" not in date[5]):
            raise ValueError
        while i <= len(info)-1:
            if date in info[i].values():
                print('Date:', date, 'Country:', info[i]['countriesAndTerritories'].replace("_", " "), " | ",'New cases:', info[i]['cases'], 'New deaths:', info[i]['deaths'])
                total_cases += int(info[i]['cases'])
                total_deaths += int(info[i]['deaths'])
            i += 1
        print("Summary:", "\n", "Date:", date, "Total cases:", total_cases, "Total deaths:", total_deaths)
    
    if country != "":
        while i <= len(info)-1:
            if country in info[i].values():
                print('Date:', info[i]['dateRep'], 'Country:', info[i]['countriesAndTerritories'].replace("_", " "), 'New cases:', info[i]['cases'], 'New deaths:', info[i]['deaths'])
                total_cases += int(info[i]['cases'])
                total_deaths += int(info[i]['deaths'])
            i += 1
        print("Summary:", "\n", "Country:", country.replace("_", " "), "Date:", today_formatted, "Total cases:", total_cases, "Total deaths:", total_deaths)

except ValueError:
    print('Incorrect format, try again.')
