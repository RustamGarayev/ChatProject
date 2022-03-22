from django.views import generic
from django.contrib.auth import get_user_model
from core.models import ChatGroup
from django.http import Http404

User = get_user_model()


class BaseIndexView(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(BaseIndexView, self).get_context_data(**kwargs)

        context["available_rooms"] = ChatGroup.objects.filter(users=user)

        return context


class ChatGroupDetailView(generic.DetailView):
    model = ChatGroup
    template_name = "room.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_object(self, queryset=None):
        obj = super(ChatGroupDetailView, self).get_object(queryset=queryset)
        if self.request.user not in obj.users.all():
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ChatGroupDetailView, self).get_context_data(**kwargs)

        user = self.request.user

        context['room_name'] = self.kwargs['slug']
        context["available_rooms"] = ChatGroup.objects.filter(users=user)

        return context
