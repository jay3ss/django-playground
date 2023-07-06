from typing import Any, Dict
from django.forms import inlineformset_factory
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_list_or_404, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView

from .forms import ListForm
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


def list_edit(request: HttpRequest, pk: int) -> HttpResponse:
    list_obj = List.objects.get(pk=pk)
    ListItemInlineFormset = inlineformset_factory(
        List, ListItem, fields=("text",), extra=2
    )

    if request.method == "POST":
        form = ListForm(request.POST, instance=list_obj)
        formset = ListItemInlineFormset(request.POST, instance=list_obj)
        if form.is_valid() and formset.is_valid():
            formset.save()
            form.save()
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


def list_new(request: HttpRequest) -> HttpResponse:
    ListItemInlineFormset = inlineformset_factory(
        List, ListItem, fields=("text",), extra=5
    )

    if request.method == "POST":
        list_obj = List.objects.create(title=request.POST["title"], owner=request.user)
        form = ListForm(request.POST, instance=list_obj)
        formset = ListItemInlineFormset(request.POST, instance=list_obj)
        if form.is_valid() and formset.is_valid():
            formset.save()
            form.save()
            return HttpResponseRedirect(list_obj.get_absolute_url())

    form = ListForm()
    formset = ListItemInlineFormset()
    context = {"form": form, "formset": formset}
    return render(request, "lists/new.html", context)


class ListNewView(CreateView):
    model = List
    template_name = "lists/new.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            ListItemInlineFormset = inlineformset_factory(
                List, ListItem, fields=("text",), extra=5
            )
            context["formset"] = ListItemInlineFormset(self.request.POST)
            context["form"] = ListForm(self.request.POST)
        else:
            ListItemInlineFormset = inlineformset_factory(
                List, ListItem, fields=("text",), extra=5
            )
            context["formset"] = ListItemInlineFormset()
            context["form"] = ListForm()

        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        context = super().get_context_data()
        form = context["form"]
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class PublicListsIndexView(ListView):
    model = List
    template_name = "lists/index.html"
    context_object_name = "lists"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["lists"] = List.objects.all().filter(is_public=True)
        return context
