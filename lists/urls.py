from django.urls import path

from .views import (
    ListDetailView,
    ListDeleteView,
    # ListEditView,
    ListIndexView,
    PublicListsIndexView,
    list_edit,
    list_new,
)


urlpatterns = [
    path("", ListIndexView.as_view(), name="list_index"),
    path("<slug:slug>/<uuid:pk>/", ListDetailView.as_view(), name="list_detail"),
    path("edit/<slug:slug>/<uuid:pk>/", list_edit, name="list_edit"),
    path("delete/<slug:slug>/<uuid:pk>/", ListDeleteView.as_view(), name="list_delete"),
    path("new/", list_new, name="list_new"),
    path("public/", PublicListsIndexView.as_view(), name="list_public"),
    # path("<slug:slug>/<uuid:pk>/delete", ListDeleteView.as_view(), name="list_item_delete"),
]
