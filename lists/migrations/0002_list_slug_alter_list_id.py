# Generated by Django 4.2.2 on 2023-07-11 22:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("lists", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="list",
            name="slug",
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name="list",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]