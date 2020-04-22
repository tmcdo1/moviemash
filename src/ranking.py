from src.scraper.storage import getMovies, getMoviesWithGenres
import math, sys, re

def movie_in_list(movie, movie_list):
    for mov in movie_list:
        if mov['_id'] == movie['_id']:
            return True

def score(query, time_available, preferred_new=False, genres=[]):
    movie_results = []
    query_list = re.split('[,\ !?|]\+\-\~', query)
    query_it = list(filter(None, query_list)) # Create list of words removing any empty strings
    query = ' '.join(query_it)

    ES_SCORE_WEIGHT = 0.6
    RATING_SCORE_WEIGHT = 2
    NEW_SCORE_WEIGHT = 20

    # movies = []
    # max_es_score = 0.0
    # for word in query_it:
    #     results = getMovies(word)
    #     for movie_result in results['hits']['hits']:
    #         if not movie_in_list(movie_result, movies):
    #             movies.append(movie_result)
    #     max_score = results['hits']['max_score']
    #     if max_score and max_score > max_es_score:
    #         max_es_score = results['hits']['max_score']

    results = {}
    if len(genres) == 0:
        results = getMovies(query)
    else:
        results = getMoviesWithGenres(query, genres)

    max_es_score = results['hits']['max_score']
    movies = results['hits']['hits']

    # Custom scoring modify each movie score based on "movie_rating"
    for movie in movies:
        movie_rating = 0.0
        try:
            movie_rating = float(movie['_source']['movie_rating'])
        except:
            movie_rating = 0.0
        movie['_score'] = ES_SCORE_WEIGHT * (math.log(movie['_score']) - math.log(max_es_score))
        if movie_rating != 0.0:
            movie['_score'] += RATING_SCORE_WEIGHT * (math.log(movie_rating) - math.log(10))

        # If newer movies are preferred, add to score
        if preferred_new:
            MOVIE_YEAR_BASE = 1930
            movie_year = MOVIE_YEAR_BASE
            try:
                movie_year = int(movie['_source']['movie_year'])
            except:
                movie_year = MOVIE_YEAR_BASE
            
            movie['_score'] += NEW_SCORE_WEIGHT * (math.log(movie_year) - math.log(MOVIE_YEAR_BASE))
        


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
            # print(movie['_source']['movie_name'], movie['_score'])
            movie_results.append(movie['_source'])
            time_available -= movie_runtime

    return movie_results

def score_with_gt(query, time_available, preferred_new=False, genres=[]):
    movie_results = []
    query_list = re.split('[,\ !?|]\+\-\~', query)
    query_it = list(filter(None, query_list)) # Create list of words removing any empty strings
    query = ' '.join(query_it)

    ES_SCORE_WEIGHT = 0.6
    RATING_SCORE_WEIGHT = 2
    NEW_SCORE_WEIGHT = 20

    # movies = []
    # max_es_score = 0.0
    # for word in query_it:
    #     results = getMovies(word)
    #     for movie_result in results['hits']['hits']:
    #         if not movie_in_list(movie_result, movies):
    #             movies.append(movie_result)
    #     max_score = results['hits']['max_score']
    #     if max_score and max_score > max_es_score:
    #         max_es_score = results['hits']['max_score']

    results = {}
    if len(genres) == 0:
        results = getMovies(query)
    else:
        results = getMoviesWithGenres(query, genres)

    max_es_score = results['hits']['max_score']
    movies = results['hits']['hits']

    # Remove movies whose runtime are not known    
    movies_to_remove = []
    movies
    for movie in movies:
        if not 'movie_runtime' in movie['_source']:
            movies_to_remove.append(movie)
        elif movie['_source']['movie_runtime'] == None:
            movies_to_remove.append(movie)

    for movie_to_remove in movies_to_remove:
        for movie in movies:
            if movie['_id'] == movie_to_remove['_id']:
                movies.remove(movie)
                break

    # Custom scoring modify each movie score based on "movie_rating"
    for movie in movies:
        movie_rating = 0.0
        try:
            movie_rating = float(movie['_source']['movie_rating'])
        except:
            movie_rating = 0.0
        movie['_score'] = ES_SCORE_WEIGHT * (math.log(movie['_score']) - math.log(max_es_score))
        if movie_rating != 0.0:
            movie['_score'] += RATING_SCORE_WEIGHT * (math.log(movie_rating) - math.log(10))

        # If newer movies are preferred, add to score
        if preferred_new:
            MOVIE_YEAR_BASE = 1930
            movie_year = MOVIE_YEAR_BASE
            try:
                movie_year = int(movie['_source']['movie_year'])
            except:
                movie_year = MOVIE_YEAR_BASE
            
            movie['_score'] += NEW_SCORE_WEIGHT * (math.log(movie_year) - math.log(MOVIE_YEAR_BASE))
        


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
            # print(movie['_source']['movie_name'], movie['_score'])
            movie_results.append(movie)
            time_available -= movie_runtime

    return movie_results, movies
