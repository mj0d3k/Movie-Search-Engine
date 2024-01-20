from django.shortcuts import render
from django.views import View
from .models import Test
import numpy as np


class TestView(View):
    template_name = 'test_view.html'

    def levenshtein(self, term, term1):
        w, h = len(term) + 1, len(term1) + 1
        matrix = np.zeros((h, w), dtype=int)

        for i in range(h):
            matrix[i][0] = i

        for j in range(w):
            matrix[0][j] = j

        for i in range(1, h):
            for j in range(1, w):
                jedn = 0 if term[j - 1] == term1[i - 1] else 1
                matrix[i][j] = min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + jedn
                )

        return matrix[h - 1][w - 1]

    def correct_query(self, query, movies):
        min_distance = float('inf')
        corrected_query = query
        for movie in movies:
            for key in movie:
                if isinstance(movie[key], str):
                    distance = self.levenshtein(query.lower(), movie[key].lower())
                    if distance < min_distance and distance <= 3:
                        min_distance = distance
                        corrected_query = movie[key]
                elif isinstance(movie[key], list):
                    for item in movie[key]:
                        distance = self.levenshtein(query.lower(), item.lower())
                        if distance < min_distance and distance <= 3:
                            min_distance = distance
                            corrected_query = item
        return corrected_query

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_query = request.POST.get('user_query', '').strip()

        movies = Test.objects.all().values()

        corrected_query = self.correct_query(user_query, movies)

        if corrected_query != user_query:
            context = {'corrected_query': corrected_query}
        else:
            context = {'user_query': user_query}

        return render(request, self.template_name, context)
