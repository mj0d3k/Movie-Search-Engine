# from django.shortcuts import render
# from django.views import View
# from .models import Test
# import numpy as np


# class TestView(View):
#     template_name = 'test_view.html'

#     def levenshtein(self, term, term1):
#         w, h = len(term) + 1, len(term1) + 1
#         matrix = np.zeros((h, w), dtype=int)

#         for i in range(h):
#             matrix[i][0] = i

#         for j in range(w):
#             matrix[0][j] = j

#         for i in range(1, h):
#             for j in range(1, w):
#                 jedn = 0 if term[j - 1] == term1[i - 1] else 1
#                 matrix[i][j] = min(
#                     matrix[i - 1][j] + 1,
#                     matrix[i][j - 1] + 1,
#                     matrix[i - 1][j - 1] + jedn
#                 )

#         return matrix[h - 1][w - 1]

#     def correct_query(self, query, movies):
#         min_distance = float('inf')
#         corrected_query = query
#         for movie in movies:
#             for key in movie:
#                 if isinstance(movie[key], str):
#                     distance = self.levenshtein(query.lower(), movie[key].lower())
#                     if distance < min_distance and distance <= 3:
#                         min_distance = distance
#                         corrected_query = movie[key]
#                 elif isinstance(movie[key], list):
#                     for item in movie[key]:
#                         distance = self.levenshtein(query.lower(), item.lower())
#                         if distance < min_distance and distance <= 3:
#                             min_distance = distance
#                             corrected_query = item
#         return corrected_query

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         user_query = request.POST.get('user_query', '').strip()

#         movies = Test.objects.all().values()

#         corrected_query = self.correct_query(user_query, movies)

#         if corrected_query != user_query:
#             context = {'corrected_query': corrected_query}
#         else:
#             context = {'user_query': user_query}

#         return render(request, self.template_name, context)


from django.shortcuts import render
from django.views import View
from .models import Movie
import numpy as np

class TestView(View):
    template_name = 'test_view.html'

    def jaccard_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1) + len(set2) - intersection
        return intersection / union if union != 0 else 0

    def kgrams(self, term, k):
        return set(term[i:i+k] for i in range(len(term) - k + 1))

    def correct_query(self, query, movies, k=2, threshold=0.5):
        query = query.lower()
        query_kgrams = self.kgrams(query, k)

        # Sprawdź, czy dokładne dopasowanie istnieje
        for movie in movies:
            if query in movie.values():
                return query

        # Zbieranie potencjalnych korekt
        potential_corrections = []
        for movie in movies:
            for key, value in movie.items():
                if isinstance(value, str):
                    values = [value]
                elif isinstance(value, list):
                    values = value
                else:
                    continue

                for item in values:
                    item_kgrams = self.kgrams(item.lower(), k)
                    similarity = self.jaccard_similarity(query_kgrams, item_kgrams)
                    if similarity >= threshold:
                        potential_corrections.append((item, similarity))

        # Wybór najlepszej korekty
        if potential_corrections:
            return max(potential_corrections, key=lambda x: x[1])[0]

        return query


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



from django.shortcuts import render
from django.views import View
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Movie
import numpy as np

class MovieSearchView(View):
    template_name = 'movie_search.html'

    WEIGHTS = {
        "title": 5,
        "cast": 3,
        "director": 3,
        "description": 2,
        "release_date": 2,
        "country": 2,
        "music": 1,
        "duration": 1,
        "wikidata_id": 0,
        "wikipedia_link": 0,
        "review_score": 0,
        "rotten_tomatoes_id": 0,
        "freebase_id": 0,
    }

    def jaccard_similarity(self, set1, set2):
        intersection = len(set1.intersection(set2))
        union = len(set1) + len(set2) - intersection
        return intersection / union if union != 0 else 0

    def kgrams(self, term, k):
        return set(term[i:i+k] for i in range(len(term) - k + 1))

    def calculate_tfidf_weights(self, movies):
        docs = []
        for movie in movies:
            doc = ""
            for key, weight in self.WEIGHTS.items():
                value = getattr(movie, key, None)
                if value:
                    doc += (" " + str(value)) * weight
            docs.append(doc.lower())

        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(docs)

        return vectorizer, tfidf_matrix

    def post(self, request, *args, **kwargs):
        user_query = request.POST.get('user_query', '').strip()

        movies = list(Test.objects.all())  # Konwertuj QuerySet na listę

        vectorizer, tfidf_matrix = self.calculate_tfidf_weights(movies)

        corrected_query = self.correct_query(user_query, movies)

        query_vector = vectorizer.transform([corrected_query.lower()])
        cosine_similarities = (tfidf_matrix * query_vector.T).toarray()

        sorted_movies_indices = np.argsort(cosine_similarities.flatten())[::-1]

        results = []
        for index in sorted_movies_indices[:100]:
            results.append({
                'title': movies[index].title,
                'score': cosine_similarities.flatten()[index]
            })

        return render(request, self.template_name, {'user_query': user_query, 'results': results})


    def correct_query(self, query, movies, k=2, threshold=0.5):
        query = query.lower()
        query_kgrams = self.kgrams(query, k)

        for movie in movies:
            if query in movie.title.lower():
                return movie.title

        potential_corrections = []
        for movie in movies:
            for key, weight in self.WEIGHTS.items():
                value = getattr(movie, key, None)
                if value:
                    item_kgrams = self.kgrams(str(value).lower(), k)
                    similarity = self.jaccard_similarity(query_kgrams, item_kgrams)
                    if similarity >= threshold:
                        potential_corrections.append((value, similarity * weight))

        if potential_corrections:
            return max(potential_corrections, key=lambda x: x[1])[0]

        return query

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_query = request.POST.get('user_query', '').strip()

        movies = Test.objects.all()

        vectorizer, tfidf_matrix = self.calculate_tfidf_weights(movies)

        corrected_query = self.correct_query(user_query, movies)

        query_vector = vectorizer.transform([corrected_query.lower()])
        cosine_similarities = (tfidf_matrix * query_vector.T).toarray()

        sorted_movies_indices = np.argsort(cosine_similarities.flatten())[::-1]

        results = []
        for index in sorted_movies_indices[:100]:
            results.append({
                'title': movies[index].title,
                'score': cosine_similarities.flatten()[index]
            })

        return render(request, self.template_name, {'user_query': user_query, 'results': results})
