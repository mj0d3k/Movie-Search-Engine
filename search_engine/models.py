from django.db import models


class Test(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    wikidata_id = models.CharField(max_length=255, null=True, blank=True)
    wikipedia_link = models.URLField(null=True, blank=True)
    review_score = models.CharField(max_length=255, null=True, blank=True)
    rotten_tomatoes_id = models.CharField(max_length=255, null=True, blank=True)
    freebase_id = models.CharField(max_length=255, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    music = models.CharField(max_length=255, null=True, blank=True)
    cast = models.CharField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

