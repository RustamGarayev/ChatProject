from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.BaseIndexView.as_view(), name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
