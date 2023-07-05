from django.forms import ModelForm

from .models import List


class ListForm(ModelForm):
    class Meta:
        model = List
        exclude = ("owner",)
