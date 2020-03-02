from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch()

def addMovieSynopsis(id, name, synopsis):
    synopsis_doc = {
        'movie_id': id,
        'movie_name': name,
        'text': synopsis,
        'timestamp': datetime.now()
    }
    print(f'Indexing {name}...')
    try:
        res = es.index(index='movie-synopses', id=id, body=synopsis_doc)
        if(res['result'] == 'created'):
            print(f'{name} is successfully indexed with id {id}')
        else:
            print(f'{name} has been updated')
    except:
        print(f'Error occurred while indexing {name}')

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
    

# This is here for testing purposes
if __name__ == '__main__': 
    addMovieSynopsis('aadsfa-aasdf-adsfadf', 'Cinderella', 'here is a synopsis of a movie. killed')
    addMovieSynopsis('asdlfk-asdfa-adsfasd', 'The Lion King', 'A lion gets killed and the son takes over')

    res = getMovies('son killed')
    print("Got %d Hits:" % res['hits']['total']['value'])
    print(res)