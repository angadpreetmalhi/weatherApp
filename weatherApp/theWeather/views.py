from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d24b3e18207ef37cb66d0a13ae428204'
    errorMessage= ''
    message=''
    messageClass=''
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            newCity=(form.cleaned_data['name'])
            print(newCity)
            countExistingCity=City.objects.filter(name=newCity).count()
            print(countExistingCity)
            if countExistingCity==0:
                requestData = requests.get(url.format(newCity)).json()
                if requestData['cod']==200:
                    form.save()
                else:
                    errorMessage='Requested city does not exist in the World'
            else:
                errorMessage='City is already exist in database'
        if errorMessage:
            message =errorMessage
            messageClass='is-danger'
        else:
            message='City is added successfully'
            messageClass='is-success'
    form= CityForm()
    cities = City.objects.all()
    citiesData = []
    for city in cities:
        requestData = requests.get(url.format(city)).json()

        cityData = {
            'city': city.name,
            'temperature': requestData['main']['temp'],
            'description': requestData['weather'][0]['description'],
            'humidity': requestData['main']['humidity'],
            'icon': requestData['weather'][0]['icon'],
        }
        citiesData.append(cityData)

    params = {'citiesData': citiesData,'form': form,'message': message,
              'messageClass':messageClass}
    return render(request, 'theWeather/weatherHTML.html', params)

def deleteOneCity(request,cityName):
    City.objects.get(name=cityName).delete()
    return redirect('home')
def deleteAllCities(request):
    cities=City.objects.all()
    for city in cities:
        City.objects.get(name=city).delete()
    return  redirect('home')