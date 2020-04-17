from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import requests
import json
from django.forms import ModelForm
from appi.models import Newspiece
from datetime import datetime

# Create your views here.

class NewsForm(ModelForm):
    class Meta:
        model = Newspiece
        fields = ['Date', 'Main', 'Support']

def news_list(request, template_name='news_list.html'):
    news = Newspiece.objects.all()
    data = {}
    data['object_list'] = news
    return render(request, template_name, data)

def news_view(request, pk, template_name='news_detail.html'):
    news = get_object_or_404(Newspiece, pk=pk)    
    return render(request, template_name, {'object':news})

def news_create(request, template_name='news_form.html'):
    form = NewsForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('news_list')
    return render(request, template_name, {'form':form})

def news_update(request, pk, template_name='news_form.html'):
    news = get_object_or_404(Newspiece, pk=pk)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid():
        form.save()
        return redirect('news_list')
    return render(request, template_name, {'form':form})

def news_delete(request, pk, template_name='news_confirm_delete.html'):
    news = get_object_or_404(Newspiece, pk=pk)    
    if request.method=='POST':
        news.delete()
        return redirect('news_list')
    return render(request, template_name, {'object':news})

def corona_data(request, template_name='corona_data.html'):
    site = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/json/'
    response = requests.get(site)
    info = response.json()['records']
    i = 0
    data = []

    while i <= len(info)-1:
        info[i]['countriesAndTerritories'] = info[i]['countriesAndTerritories'].replace("_", " ")
        data.append(info[i])
        i += 1

    return render(request, template_name, {'corona_data':data})

def corona_visualization(request, template_name='corona_visualization.html'):
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


    return render(request, template_name, {
        'corona_data': data,
        'dates': dates,
        'countries': countries,
        'total_cases': total_cases,
        'total_deaths': total_deaths
        })
