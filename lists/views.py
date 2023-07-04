from django.http import HttpRequest
from django.shortcuts import get_list_or_404, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView

from .forms import ListForm, ListItemInlineFormset
from .models import List, ListItem


class ListDetailView(DetailView):
    model = List
    template_name = "lists/detail.html"
    context_object_name = "list_obj"


class ListIndexView(ListView):
    model = List
    template_name = "lists/index.html"
    context_object_name = "lists"


class ListDeleteView(DeleteView):
    model = List
    success_url = reverse_lazy("list_index")


class ListItemDeleteView(DeleteView):
    model = ListItem
    success_url = reverse_lazy("list_index")


def list_item_edit(request: HttpRequest, pk: int) -> HttpResponse:
    list_obj = List.objects.get(pk=pk)

    if request.method == "POST":
        form = ListForm(request.POST, instance=list_obj)
        formset = ListItemInlineFormset(request.POST, instance=list_obj)
        if form.is_valid() and formset.is_valid():
            formset.save()
            return HttpResponseRedirect(list_obj.get_absolute_url())

    form = ListForm(instance=list_obj)
    formset = ListItemInlineFormset(instance=list_obj)
    context = {"form": form, "formset": formset}
    return render(request, "lists/edit.html", context)


def list_item_delete(request: HttpRequest, pk: int) -> HttpResponse:
    context = {}
    list_item: ListItem = get_list_or_404(ListItem, pk=pk)

    if request.method == "POST":
        list_pk = list_item.list.pk
        list_item.delete()
        return HttpResponseRedirect(reverse("list_detail", kwargs={"pk", list_pk}))

    return render(request, "list/detail.html", context)
