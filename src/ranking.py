from src.scraper.storage import getMovies
import math, sys, re

def movie_in_list(movie, movie_list):
    for mov in movie_list:
        if mov['_id'] == movie['_id']:
            return True

def score(query, time_available):
    movie_results = []
    query_list = re.split('[,\ !?|]', query)
    query_it = filter(None, query_list) # Create iterator of words removing any empty strings

    ES_SCORE_WEIGHT = 0.9
    RATING_SCORE_WEIGHT = 0.1

    movies = []
    max_es_score = 0.0
    for word in query_it:
        results = getMovies(word)
        for movie_result in results['hits']['hits']:
            if not movie_in_list(movie_result, movies):
                movies.append(movie_result)
        max_score = results['hits']['max_score']
        if max_score and max_score > max_es_score:
            max_es_score = results['hits']['max_score']

    # results = getMovies(query)

    # max_es_score = results['hits']['max_score']
    # movies = results['hits']['hits']

    # Custom scoring modify each movie score based on "movie_rating"
    for movie in movies:
        movie_rating = 0.0
        try:
            movie_rating = float(movie['_source']['movie_rating'])
        except:
            movie_rating = 0.0
        movie['_score'] = math.log(ES_SCORE_WEIGHT) + math.log(movie['_score']) - math.log(max_es_score)
        if movie_rating != 0.0:
            movie['_score'] = math.log(RATING_SCORE_WEIGHT) + math.log(movie_rating) - math.log(10)


    # Sort the movies by _score
    movies.sort(key=lambda x: x['_score'], reverse=True)

    # Greedily take the top movies that fit in the time_available
    for movie in movies:
        movie_runtime = 0
        try:
            movie_runtime = int(movie['_source']['movie_runtime'])
        except:
            movie_runtime = sys.maxsize
            
        if movie_runtime < time_available:
            movie_results.append(movie['_source'])
            time_available -= movie_runtime

    return movie_results