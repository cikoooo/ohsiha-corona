import requests
from datetime import datetime

site = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
response = requests.get(site)
info = response.json()['records']
i = 0
data = []
dates = []
countries = []
total_cases = []
total_deaths = []

while i <= len(info)-1:
    info[i]['countriesAndTerritories'] = info[i]['countriesAndTerritories'].replace("_", " ")
    data.append(info[i])
    i += 1

n = 0
while n <= len(info)-1:
    if data[n]['dateRep'] not in dates:
        dates.append(data[n]['dateRep'])
        n += 1
    else:
        n += 1

dates.sort(key=lambda date: datetime.strptime(date, "%d/%m/%Y"))
print(dates)

y = 0
while y <= len(info)-1:
    if data[y]['countriesAndTerritories'] not in countries:
        countries.append(data[y]['countriesAndTerritories'])
        y += 1
    else:
        y += 1

a = 0
cases = 0
deaths = 0
for a in range(len(data)):
    if a == len(data)-1:
        cases += int(data[a]['cases'])
        deaths += int(data[a]['deaths'])
        total_cases.append(cases)
        total_deaths.append(deaths)
    elif a == 0:
        continue
    elif data[a]['countriesAndTerritories'] == data[a-1]['countriesAndTerritories']:
        cases += int(data[a-1]['cases'])
        deaths += int(data[a-1]['deaths'])
    else:
        cases += int(data[a-1]['cases'])
        deaths += int(data[a-1]['deaths'])
        total_cases.append(cases)
        total_deaths.append(deaths)
        cases = 0
        deaths = 0



'''
<div id="container"></div>
    <script src="https://code.highcharts.com/highcharts.src.js"></script>
    <script>
    Highcharts.chart('container', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'testi'
        },
        xAxis: {
            categories: {{ countries|safe }}
        },
        series: [{
            name: 'Cases per country',
            data: {{ total_cases|safe }},
            color: 'green'
        }, {
            name: 'Deaths per country',
            data: {{ total_deaths|safe }},
            color: 'red'
        }]
    });

    </script>
'''