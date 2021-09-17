


from django.urls import path

from . import views


urlpatterns = [

    path('list',views.list,name="list"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('edit/',views.edit,name="edit"),
    path('<policy_id>',views.search,name="search"),
]