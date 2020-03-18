from datetime import datetime
from elasticsearch import Elasticsearch, ElasticsearchException
import requests
from bs4 import BeautifulSoup

es = Elasticsearch()

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
    except ElasticsearchException as e:
        print('Error occurred while indexing {}'.format(name))
        print("Error:", e.error)

# Full-text query docs can be found here: https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
def getMovies(query):
    print(query.split(' '))
    res = es.search(index='movie-synopses', body={
        'query': {
            'simple_query_string': {
                'query': query,
                'fields': ['text']
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
        return BeautifulSoup(response.content)
    else:
        return None

# Get a "bag of strings" from the soup (not necessarily words-
# Just strings separated by spaces)
def extractBagOfStrings(soup):
    synopsis_soup = soup.find(id="plot-synopsis-content").text
    return str(synopsis_soup).split(' ')

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
    # Narnie example:
    movieID = "tt0363771"
    synopsis = scrapeSynopsis(movieID)

    addMovieSynopsis(movieID, "Narnia", synopsis)

    addMovieSynopsis('aadsfa-aasdf-adsfadf', 'Cinderella', 'here is a synopsis of a movie. killed')
    addMovieSynopsis('asdlfk-asdfa-adsfasd', 'The Lion King', 'A lion gets killed and the son takes over')

    res = getMovies('son killed')
    print("Got %d Hits:" % res['hits']['total']['value'])
    print(res)
