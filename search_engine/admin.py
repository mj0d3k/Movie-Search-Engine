from django.contrib import admin
from .models import Movie
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin


class MovieResource(resources.ModelResource):
    wikidata_id = fields.Field(attribute='wikidata_id', column_name='wikidata-id')
    review_score = fields.Field(attribute='review_score', column_name='review-score')
    rotten_tomatoes_id = fields.Field(attribute='rotten_tomatoes_id', column_name='rotten-tomatoes-id')
    freebase_id = fields.Field(attribute='freebase_id', column_name='freebase-id')
    wikipedia_link = fields.Field(attribute='wikipedia_link', column_name='wikipedia-link')

    class Meta:
        model = Movie


class MovieAdmin(ImportExportModelAdmin):
    resource_class = MovieResource


admin.site.register(Movie, MovieAdmin)