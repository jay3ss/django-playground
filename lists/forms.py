from django.forms import ModelForm, inlineformset_factory

from .models import List, ListItem


class ListForm(ModelForm):
    class Meta:
        model = List
        exclude = ("owner",)


ListItemInlineFormset = inlineformset_factory(List, ListItem, fields=("text",), extra=2)
