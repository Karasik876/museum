# Generated by Django 5.0.3 on 2024-04-09 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.collection')),
            ],
        ),
        migrations.CreateModel(
            name='UserCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='collection.collection')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.useraccount')),
            ],
            options={
                'unique_together': {('user_id', 'collection_id')},
            },
        ),
    ]