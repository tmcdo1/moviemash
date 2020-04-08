from datetime import datetime
from elasticsearch import Elasticsearch, ElasticsearchException, helpers
import requests
from bs4 import BeautifulSoup

es = Elasticsearch(["https://search-moviemash-komc6gxtigbpu4dwoz4rchnzzu.us-east-2.es.amazonaws.com"])

missingSynopsisMessage = "It looks like we don't have a Synopsis for this title yet. Be the first to contribute! Just click the \"Edit page\" button at the bottom of the page or learn more in the Synopsis submission guide."

def addMovieSynopsis(id, name, synopsis):
    synopsis_doc = {
        'movie_id': id,
        'movie_name': name,
        'text': synopsis,
        'timestamp': datetime.now()
    }
    print('Indexing {}...'.format(name))
    try:
        res = es.index(index='movie-synopses', id=id, body=synopsis_doc)
        if(res['result'] == 'created'):
            print('{} is successfully indexed with id {}'.format(name, id))
        else:
            print('{} has been updated'.format(name))
    except:
        print('Error occurred while indexing {}'.format(name))
        print("Error:", e.error)

# Converts this format:
# movies_data = [("movie 1 id", "movie 1 title", "movie 1 synopsis"),
#                ("movie 2 id", "movie 2 title", "movie 2 synopsis"),...]
# to this format:
# actions = [
#        {
#           "_index": "movie-synopses",
#           "_type": "_doc",
#           "_id": "movie 1 id",
#           "_source": {
#               "movie_name": "movie 1 title",
#               "movie_id": "movie 1 id"
#               "text": "movie 1 synopsis",
#               "timestamp": datetime.now()
#           }
#        },
#        {
#           "_index": "movie-synopses",
#           "_type": "_doc",
#           "_id": "movie 2 id",
#           "_source": {
#               "movie_name": "movie 2 title",
#               "movie_id": "movie 2 id"
#               "text": "movie 2 synopsis",
#               "timestamp": datetime.now()
#           }
#        },...
#       ]
def get_actions(movies_data):
    actions = []
    id_idx = 0
    title_idx = 1
    synopsis_idx = 2
    for movie in movies_data:
        actions.append({
           "_index": "movie-synopses",
           "_type": "_doc",
           "_id": movie[id_idx],
           "_source": {
               "movie_name": movie[title_idx],
               "movie_id": movie[id_idx],
               "text": movie[synopsis_idx],
               "timestamp": datetime.now()
           }
        })
    return actions

def get_update_actions(movies_data):
    actions = []
    id_idx = 0
    runtime_idx = 1
    genre_idx = 2
    rating_idx = 3
    votes_idx = 4
    year_idx = 5
    for movie in movies_data:
        actions.append({
           "_op_type": "update",
           "_index": "movie-synopses",
           "_type": "_doc",
           "_id": movie[id_idx],
           "doc": {
               "movie_runtime": movie[runtime_idx],
               "movie_genre": movie[genre_idx],
               "movie_rating": movie[rating_idx],
               "movie_votes": movie[votes_idx],
               "movie_year": movie[year_idx],
               "timestamp": datetime.now()
           }
        })
    return actions

# Input for this function needs to be an array of tuples/arrays:
# movies_data = [("movie 1 id", "movie 1 title", "movie 1 synopsis"),
#                ("movie 2 id", "movie 2 title", "movie 2 synopsis"),...]
def addBulkMovieSynopses(movies_data):
    num_movies = len(movies_data)
    print('Indexing {} movies...'.format(num_movies))
    movies_actions = get_actions(movies_data)
    try:
        for was_success, info in helpers.parallel_bulk(es, movies_actions, thread_count=32):
            num_successful = info["index"]["_shards"]["successful"]
            num_failed = info["index"]["_shards"]["failed"]
            num_total = info["index"]["_shards"]["total"]

            if not was_success:
                print('Errors uploading in bulk: {} successful {} failed {} total', num_successful, num_failed, num_total)
            #else:
            #    print('{} movies successfully indexed '.format(num_successful))
    except Exception as e:
        print('Error occurred while indexing {} movies in bulk: {}'.format(num_movies, type(e).__name__))

# Input for this function needs to be an array of tuples/arrays:
# movies_data = [("movie 1 id", "movie 1 title", "movie 1 synopsis"),
#                ("movie 2 id", "movie 2 title", "movie 2 synopsis"),...]
def appendBulkMovieInfo(movies_data):
    num_movies = len(movies_data)
    print('Indexing {} movies...'.format(num_movies))
    movies_actions = get_update_actions(movies_data)
    try:
        for was_success, info in helpers.parallel_bulk(es, movies_actions, thread_count=32):
            num_successful = info["update"]["_shards"]["successful"]
            num_failed = info["update"]["_shards"]["failed"]
            num_total = info["update"]["_shards"]["total"]

            if not was_success:
                print('Errors uploading in bulk: {} successful {} failed {} total', num_successful, num_failed, num_total)
            #else:
            #    print('{} movies successfully indexed '.format(num_successful))
    except Exception as e:
        print('Error occurred while indexing {} movies in bulk: {}'.format(num_movies, type(e).__name__))
        file = open('out.txt','w+')
        file.write(str(e))
        file.close()
        exit()

# Full-text query docs can be found here: https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
def getMovies(query):
    res = es.search(index='movie-synopses', body={
        'query': {
            'simple_query_string': {
                'query': query,
                'fields': ['text', 'movie_genre', 'movie_name']
            }
        }
    })
    return res
    
# This might be up for experimentation
def formURL(movie_id):
    return "https://www.imdb.com/title/" + movie_id + "/synopsis"

def getSoup(movie_id):
    response = requests.get(formURL(movie_id))
    if response.status_code == requests.codes.ok:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None

# Get a "bag of strings" from the soup (not necessarily words-
# Just strings separated by spaces)
def extractBagOfStrings(soup):
    synopsis_soup = soup.find(id="plot-synopsis-content").text.strip()
    if synopsis_soup == missingSynopsisMessage:
        return [""]
    return synopsis_soup.split(' ')

# Catch the words separated by "--" and the like:
def fixMissingSpace(bag_of_strings, char):
    strings_to_remove = []
    for string in bag_of_strings:
        if char in string:
            # Get the strings in between the dashes
            fixed_string = string.replace(char, " ")
            detached_strings = fixed_string.split(" ")

            # Put those strings in the bag and mark this string
            # for deletion later (assuming order doesn't matter)
            for detached_string in detached_strings:
                if detached_string != "":
                    bag_of_strings.append(detached_string)
            strings_to_remove.append(string)

    for string_to_remove in strings_to_remove:
        bag_of_strings.remove(string_to_remove)
  
    return bag_of_strings

# Remove any leading/trailing non-letters and move to upper case
# Scans the word left to right, removing non-letters until it
# comes across a letter- then takes the continuous string of
# only letters starting from the first letter
# Examples:
# "Why?" => "WHY"
# "then," => "THEN"
# "\"She" => "SHE"
# "I'm" => "I"
# "'She'll" => "SHE"
# Note there is some truncating of some words which may or may
# not help. For example, it might accidentally give the name
# DON from the word don't. Maybe we should just use a library.
def formWord(string):
    word = ""
    found_letter = False
    for letter in string:
        if not letter.isalnum():
            if found_letter:
                break
            else:
                continue # until we see one or finish the word
        else:
            found_letter = True
            word += letter.upper()
#       if word != string.upper():
#           print("String: " + string + " Word: " + word)
    return word

def formBagOfWords(bag_of_strings):
#    bag_of_strings = fixMissingSpace(bag_of_strings, "-")
#    bag_of_strings = fixMissingSpace(bag_of_strings, ".")
    bag_of_words = []
    for string in bag_of_strings:
        word = form_word(string)
        if word != "":
            bag_of_words.append(word)
    return bag_of_words

def scrapeSynopsis(movieID):
    soup = getSoup(movieID)
    if soup == None:
        return None
    bag_of_strings = extractBagOfStrings(soup)
    return ' '.join(bag_of_strings)
#    bag_of_words = formBagOfWords(bag_of_strings)

# This is here for testing purposes
if __name__ == '__main__': 
    # Narnia example:
    #narniaID = "tt0363771"
    # carmencitaID = "tt0000001"
    #narniaSynopsis = scrapeSynopsis(narniaID)
    # carmencitaSynopsis = scrapeSynopsis(carmencitaID)

    #addMovieSynopsis(narniaID, "Narnia", narniaSynopsis)
    # addMovieSynopsis(carmencitaID, "Carmencita", carmencitaSynopsis)

    #addMovieSynopsis('aadsfa-aasdf-adsfadf', 'Cinderella', 'here is a synopsis of a movie. killed')
    #addMovieSynopsis('asdlfk-asdfa-adsfasd', 'The Lion King', 'A lion gets killed and the son takes over')

    res = getMovies('son killed')
    print("Got %d Hits:" % res['hits']['total']['value'])
    print('Max score:', res['hits']['max_score'])
    print(res['hits']['hits'][0])

