from django.urls import path

from .views import (
    ListDetailView,
    ListDeleteView,
    # ListEditView,
    ListIndexView,
    list_edit,
    list_new,
)


urlpatterns = [
    path("", ListIndexView.as_view(), name="list_index"),
    path("<int:pk>/", ListDetailView.as_view(), name="list_detail"),
    path("<int:pk>/edit", list_edit, name="list_edit"),
    path("<int:pk>/delete", ListDeleteView.as_view(), name="list_delete"),
    path("new/", list_new, name="list_new"),
    # path("<int:pk>/delete", ListDeleteView.as_view(), name="list_item_delete"),
]
