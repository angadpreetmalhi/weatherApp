from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='home'),
    path('delete/<cityName>/',views.deleteOneCity,name='deleteOneCity'),
    path('_',views.deleteAllCities,name='deleteAllCities')
]
