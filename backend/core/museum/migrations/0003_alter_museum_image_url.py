# Generated by Django 5.0.3 on 2024-05-19 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("museum", "0002_remove_museumuser_access_level_museum_image_url_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="museum",
            name="image_url",
            field=models.CharField(
                default="https://digital-portfolio.hb.ru-msk.vkcs.cloud/defaultMuseumAvatar.png",
                max_length=255,
            ),
        ),
    ]
