from django.shortcuts import render
from django.views import generic


class BaseIndexView(generic.TemplateView):
    template_name = 'index.html'


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })
