### CREATING BASE HTML ###


def base_view(request):
    return render(request, 'base.html')


from django.shortcuts import render
from django.views import View
from .models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class MovieSearchView(View):
    template_name = 'view1.html'

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

    def correct_query(self, query, movies, k=2, threshold=0.5):
        query = query.lower()
        query_kgrams = self.kgrams(query, k)

        for movie in movies:
            if query in movie.values():
                return query

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

        if potential_corrections:
            return max(potential_corrections, key=lambda x: x[1])[0]

        return query

    def calculate_tf_idf(self, movies):
        documents = []
        for movie in movies:
            document = " ".join(
                f"{key} {' '.join(str(movie[key]).split()) * self.WEIGHTS[key]}" 
                for key in self.WEIGHTS if movie[key] and self.WEIGHTS[key] > 0
            )
            documents.append(document)

        vectorizer = TfidfVectorizer()
        tf_idf_matrix = vectorizer.fit_transform(documents)
        return tf_idf_matrix, vectorizer

    def search_movies(self, query, tf_idf_matrix, vectorizer, movies):
        query_transformed = vectorizer.transform([query])
        cosine_similarities = np.dot(tf_idf_matrix, query_transformed.T).toarray().ravel()
        top_indices = np.argsort(cosine_similarities)[::-1][:100]
        top_movies = [(movies[i], cosine_similarities[i]) for i in top_indices]
        return top_movies

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user_query = request.POST.get('user_query', '').strip()
        movies = list(Movie.objects.all().values())

        corrected_query = self.correct_query(user_query, movies)
        tf_idf_matrix, vectorizer = self.calculate_tf_idf(movies)
        top_movies = self.search_movies(corrected_query, tf_idf_matrix, vectorizer, movies)

        context = {
            'results': top_movies
        }

        return render(request, self.template_name, context)
