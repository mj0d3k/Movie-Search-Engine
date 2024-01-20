# Generated by Django 5.0.1 on 2024-01-20 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('search_engine', '0009_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('wikidata_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('wikipedia_link', models.URLField(blank=True, null=True)),
                ('review_score', models.CharField(blank=True, max_length=1000, null=True)),
                ('rotten_tomatoes_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('freebase_id', models.CharField(blank=True, max_length=1000, null=True)),
                ('director', models.CharField(blank=True, max_length=1000, null=True)),
                ('music', models.CharField(blank=True, max_length=1000, null=True)),
                ('cast', models.CharField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=1000, null=True)),
                ('duration', models.CharField(blank=True, max_length=1000, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('release_date', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
