from django.urls import path

from core import views

app_name = "core"

urlpatterns = [
    path('', views.BaseIndexView.as_view(), name='index'),
    path('room/<slug>/', views.ChatGroupDetailView.as_view(), name='room'),
]
