# Generated by Django 5.0.1 on 2024-01-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='director',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='duration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='freebase_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='music',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='review_score',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='rotten_tomatoes_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='wikidata_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='wikipedia_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]