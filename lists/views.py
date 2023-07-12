from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import (
    get_list_or_404,
    redirect,
    render,
    HttpResponse,
    HttpResponseRedirect,
)
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView

from .forms import ListForm
from .mixins import OwnershipRequiredMixin
from .models import List, ListItem


class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "lists/detail.html"
    context_object_name = "list_obj"


class ListIndexView(LoginRequiredMixin, ListView):
    model = List
    template_name = "lists/index.html"
    context_object_name = "lists"

    def get_queryset(self):
        return self.request.user.lists.all()


class ListDeleteView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = List
    success_url = reverse_lazy("list_index")


class ListItemDeleteView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = ListItem
    success_url = reverse_lazy("list_index")


def list_edit(request: HttpRequest, pk: int, slug: str) -> HttpResponse:
    list_obj = List.objects.get(pk=pk)
    ListItemInlineFormset = inlineformset_factory(
        List, ListItem, fields=("text",), extra=2
    )

    if not list_obj.owner == request.user:
        return redirect("list_index")

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


def list_item_delete(request: HttpRequest, pk: int, slug: str) -> HttpResponse:
    context = {}
    list_item: ListItem = get_list_or_404(ListItem, pk=pk)

    if request.method == "POST":
        list_pk = list_item.list.pk
        list_item.delete()
        return HttpResponseRedirect(reverse("list_detail", kwargs={"pk", list_pk}))

    return render(request, "list/detail.html", context)


@login_required
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


class ListNewView(LoginRequiredMixin, CreateView):
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


class PublicListsIndexView(LoginRequiredMixin, ListView):
    model = List
    template_name = "lists/public.html"
    context_object_name = "lists"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["lists"] = List.objects.all().filter(is_public=True)
        return context


def generate_fake_data(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # do processing of data here
        from django.contrib.auth import get_user_model
        import random
        import requests

        User = get_user_model()

        # Generate 15 different usernames
        response = requests.get("https://randomuser.me/api/?results=15")
        data = response.json()
        usernames = [user["login"]["username"] for user in data["results"]]

        # create the users
        users = [
            User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="password",
            )
            for username in usernames
        ]

        # Generate 10 titles for to-do lists
        list_titles = [
            "Shopping List",
            "Home Improvement Tasks",
            "Work Projects",
            "Fitness Goals",
            "Recipe Ideas",
            "Travel Bucket List",
            "Books to Read",
            "Movies to Watch",
            "Gift Ideas",
            "Personal Goals",
        ]

        # Generate 25 list items
        response = requests.get("https://api.quotable.io/quotes/random?limit=25")
        data = response.json()

        list_items = [quote["content"] for quote in data]

        lists = [
            List.objects.create(
                title=random.choice(list_titles),
                owner=random.choice(users),
                is_public=random.choice([True, False]),
            )
            for _ in range(random.randint(5, 9))
        ]

        for list_obj in lists:
            for _ in range(random.randint(5, 9)):
                ListItem.objects.create(
                    list=list_obj,
                    text=random.choice(list_items),
                    is_complete=random.choice([True, False]),
                )

        return redirect(reverse("list_index"))

    # serve the template for get requests
    return render(request, "data.html")
