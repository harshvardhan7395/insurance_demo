
from django.urls import path

from . import views


urlpatterns = [

    path('login/',views.app_login,name="app_login"),

    path('list',views.list,name="list"),
    path('logout/', views.logot,name="logout")
]