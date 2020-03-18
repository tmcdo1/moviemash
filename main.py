from flask import Flask, render_template

import scraper.storage as store

app = Flask(__name__)

@app.route('/')
def home():
    # TODO: Get list of genres and populate the index.html options with them.
    movieID = "tt0363771"
    synopsis = store.scrapeSynopsis(movieID)
    
    if synopsis != None:
        store.addMovieSynopsis(movieID, "Narnia", synopsis)
        print("Added movie")
    
    movies = store.getMovies('')
    print("Movies:")

    if (len(movies) > 100):
        print(movies[0:99])
    else:
        print(movies)

    print("... done with Movies")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
