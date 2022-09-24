from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="index"),
    path('add/', views.add_trans, name="add"),
    path('del/', views.del_trans, name="del"),
    path('<str:user>/add/', views.add_trans, name="add"),
    path('<str:user>/del/', views.del_trans, name="del"),
    path('<str:user>/', views.userFound, name="found"),
]