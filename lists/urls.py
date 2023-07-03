from django.urls import path

from .views import ListDetailView, ListIndexView


urlpatterns = [
    path("", ListIndexView.as_view(), name="list_index"),
    path("<int:pk>/", ListDetailView.as_view(), name="list_detail"),
]
