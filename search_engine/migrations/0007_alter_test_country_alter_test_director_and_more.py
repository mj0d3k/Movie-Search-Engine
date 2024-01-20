# Generated by Django 5.0.1 on 2024-01-20 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0006_alter_test_cast'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='country',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='director',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='duration',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='freebase_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='music',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='review_score',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='rotten_tomatoes_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='title',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='wikidata_id',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]