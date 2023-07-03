from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class List(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="lists"
    )
    is_public = models.BooleanField(default=False, blank=False, null=False)

    def get_absolute_url(self):
        return reverse("list_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.title} ({self.owner})"


class ListItem(models.Model):
    is_complete = models.BooleanField(default=False, null=False, blank=False)
    text = models.CharField(max_length=255, blank=False, null=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return self.text
