from django.contrib.auth import get_user_model
from django.db import models


class List(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="lists"
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.owner})"


class ListItem(models.Model):
    completed = models.BooleanField(default=False, null=False, blank=False)
    text = models.TextField(blank=False, null=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return self.text[:50]
