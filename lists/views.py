from django.views.generic import DetailView, ListView

from .models import List, ListItem


class ListDetailView(DetailView):
    model = List
    template_name = "lists/detail.html"


class ListIndexView(ListView):
    model = List
    template_name = "lists/index.html"
