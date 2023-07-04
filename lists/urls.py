from django.urls import path

from .views import (
    ListDetailView,
    ListDeleteView,
    # ListEditView,
    ListIndexView,
    list_item_edit,
)


urlpatterns = [
    path("", ListIndexView.as_view(), name="list_index"),
    path("<int:pk>/", ListDetailView.as_view(), name="list_detail"),
    path("<int:pk>/edit", list_item_edit, name="list_edit"),
    path("<int:pk>/delete", ListDeleteView.as_view(), name="list_delete"),
    # path("<int:pk>/delete", ListDeleteView.as_view(), name="list_item_delete"),
]
