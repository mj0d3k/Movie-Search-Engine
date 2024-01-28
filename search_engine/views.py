from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Movie
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import math
import string
import re


### CREATING BASE HTML ###


def base_view(request):
    return render(request, 'base.html')


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
        top_indices = np.argsort(cosine_similarities)[::-1][:50]
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


# class MovieSearchView(View):
#     template_name = 'view1.html'

#     WEIGHTS = {
#         "title": 5,
#         "cast": 3,
#         "director": 3,
#         "description": 2,
#         "release_date": 2,
#         "country": 2,
#         "music": 1,
#         "duration": 1,
#         "wikidata_id": 0,
#         "wikipedia_link": 0,
#         "review_score": 0,
#         "rotten_tomatoes_id": 0,
#         "freebase_id": 0,
#     }

#     def jaccard_similarity(self, set1, set2):
#         intersection = len(set1.intersection(set2))
#         union = len(set1) + len(set2) - intersection
#         return intersection / union if union != 0 else 0

#     def kgrams(self, term, k):
#         return set(term[i:i+k] for i in range(len(term) - k + 1))

#     def correct_query(self, query, movies, k=2, threshold=0.5):
#         query = query.lower()
#         query_kgrams = self.kgrams(query, k)

#         for movie in movies:
#             if query in movie.values():
#                 return query

#         potential_corrections = []
#         for movie in movies:
#             for key, value in movie.items():
#                 if isinstance(value, str):
#                     values = [value]
#                 elif isinstance(value, list):
#                     values = value
#                 else:
#                     continue

#                 for item in values:
#                     item_kgrams = self.kgrams(item.lower(), k)
#                     similarity = self.jaccard_similarity(query_kgrams, item_kgrams)
#                     if similarity >= threshold:
#                         potential_corrections.append((item, similarity))

#         if potential_corrections:
#             return max(potential_corrections, key=lambda x: x[1])[0]

#         return query

#     def preprocess_document(self, doc):
#         punctuation_pattern = f"[{re.escape(string.punctuation)}]"
#         processed_doc = re.sub(punctuation_pattern, "", doc)
#         return processed_doc

#     def calculate_tf(self, words_list):
#         tf = {}
#         words_list_unique = set(words_list)

#         for u in words_list_unique:
#             how_many = words_list.count(u)
#             tf[u] = how_many

#         tf_values = tf.values()
#         max_in_tf = max(tf_values)

#         for word in words_list_unique:
#             tf[word] = tf[word] / max_in_tf

#         return tf

#     def calculate_idf(self, n, words):
#         idf = {}
#         all_unique_words = set(words)

#         for u in all_unique_words:
#             idf[u] = math.log10(n / words.count(u))

#         return idf

#     def calculate_tf_idf(self, docs):
#         doc_tf = []
#         words = []

#         for doc in docs:
#             words_list = doc.lower().split()
#             words.extend(set(words_list))
#             tf = self.calculate_tf(words_list)
#             doc_tf.append(tf)

#         idf = self.calculate_idf(len(docs), words)

#         array = []

#         for tf in doc_tf:
#             array_2 = {w: tf[w] * idf[w] for w in tf}
#             array.append(array_2)

#         return array

#     def calculate_document_tf_idf(self, movies):
#         documents = []
#         for movie in movies:
#             document = " ".join(
#                 f"{key} {' '.join(str(movie[key]).split()) * self.WEIGHTS[key]}" 
#                 for key in self.WEIGHTS if movie[key] and self.WEIGHTS[key] > 0
#             )
#             documents.append(self.preprocess_document(document))

#         return self.calculate_tf_idf(documents)

#     def search_movies(self, query, tf_idf_array, movies):
#         query_processed = self.preprocess_document(query).split()
#         query_tf = self.calculate_tf(query_processed)
#         query_tf_idf = {w: query_tf[w] * (math.log10(len(movies) / query_processed.count(w)) if query_processed.count(w) > 0 else 0) for w in query_tf}

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         user_query = request.POST.get('user_query', '').strip()
#         movies = list(Movie.objects.all().values())

#         corrected_query = self.correct_query(user_query, movies)
#         tf_idf_array = self.calculate_document_tf_idf(movies)
#         top_movies = self.search_movies(corrected_query, tf_idf_array, movies)

#         context = {
#             'results': top_movies
#         }

#         return render(request, self.template_name, context)


from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Movie
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.common.by import By

class MovieInfoView(View):
    def get(self, request, wikidata_id):
        movie = get_object_or_404(Movie, wikidata_id=wikidata_id)
        clickstream_data = self.fetch_clickstream_data(movie.title)

        clickstream_json = json.dumps(clickstream_data, ensure_ascii=False)

        return render(request, 'view2.html', {
            'movie': movie, 
            'clickstream_data': clickstream_data,
            'clickstream_json': clickstream_json
        })

    def fetch_clickstream_data(self, movie_title):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')

        with webdriver.Chrome(options=chrome_options) as driver:
            data = self.fetch_data_for_movie(movie_title, driver)
        return data

    def fetch_data_for_movie(self, movie_title, driver):
        url = self.create_url(movie_title)
        driver.get(url)
        time.sleep(10)

        markers = driver.find_elements("xpath", "//div[contains(@class, 'sc-hHEiqL kvHQHO')]")
        if len(markers) < 2:
            return []

        split_index = markers[1].location['y']

        data_elements = driver.find_elements("xpath", "//div[@data-tag='allowRowEvents']")

        extracted_data = []
        for i in range(0, len(data_elements), 6):
            element_location = data_elements[i].location['y']
            pageview_type = 'outgoing' if element_location > split_index else 'incoming'

            source = data_elements[i].text
            views = data_elements[i + 2].text
            percentage = data_elements[i + 4].text

            if source and source not in ["other-search", "empty-search", "other-empty", "other-external", "other-internal", movie_title]:
                link = self.create_wikipedia_link(source)
                extracted_data.append({
                    "label": source,
                    "views": views,
                    "percentage": percentage,
                    "link": link,
                    "type": pageview_type
                })

        return extracted_data

    def create_url(self, movie_title):
        formatted_title = movie_title.replace(' ', '_')
        return f"https://wikinav.toolforge.org/?language=en&title={formatted_title}"

    def create_wikipedia_link(self, text):
        formatted_text = text.replace(' ', '_')
        return f"https://en.wikipedia.org/wiki/{formatted_text}"

    def fetch_movie_poster_url(self, wikipedia_url):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--ignore-ssl-errors=yes')
        chrome_options.add_argument('--ignore-certificate-errors')

        with webdriver.Chrome(options=chrome_options) as driver:
            driver.get(wikipedia_url)
            time.sleep(2)

            try:
                image_element = driver.find_element(By.XPATH, "//table[contains(@class, 'infobox')]//img")
                poster_url = image_element.get_attribute('src')

                if poster_url and poster_url.startswith("//"):
                    poster_url = "https:" + poster_url

                return poster_url
            except Exception as e:
                print("Nie znaleziono plakatu filmu.", e)
                return None


    def get(self, request, wikidata_id):
        movie = get_object_or_404(Movie, wikidata_id=wikidata_id)
        wikipedia_url = self.create_wikipedia_link(movie.title)
        poster_url = self.fetch_movie_poster_url(wikipedia_url)
        clickstream_data = self.fetch_clickstream_data(movie.title)
        clickstream_json = json.dumps(clickstream_data, ensure_ascii=False)

        return render(request, 'view2.html', {
            'movie': movie, 
            'clickstream_data': clickstream_data,
            'clickstream_json': clickstream_json,
            'poster_url': poster_url
        })
