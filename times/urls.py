from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index' ),
    path('city/',views.city,name='city' ),
    path('index2/',views.index2,name='index2' ),
]
