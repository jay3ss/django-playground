import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class List(models.Model):
    title = models.CharField(max_length=150, blank=False, null=False)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="lists"
    )
    slug = models.SlugField(null=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    is_public = models.BooleanField(default=False, blank=False, null=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("list_detail", kwargs={"pk": self.id, "slug": self.slug})

    def __str__(self) -> str:
        return f"{self.title} ({self.owner})"


class ListItem(models.Model):
    is_complete = models.BooleanField(default=False, null=False, blank=False)
    text = models.CharField(max_length=255, blank=False, null=False)
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="items")

    def __str__(self) -> str:
        return self.text
