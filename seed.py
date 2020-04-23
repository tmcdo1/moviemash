# Open the movies.tsv file and read in each movie row of the seed data
import src.scraper.storage as store
import io

file = io.open("movies.tsv", encoding="utf-8")
print("About to start...")
titles = file.readline().split('\t')
titles = [title.strip() for title in titles]

movieID = 0
movieType = 1
movieTitle = 2
runtime = 3
genres = 4

num_indexed = 0
lines_read = 0
starting_line = 444000
ending_line = 446000
while True:
    movie_data = []
    num_at_a_time = 1000
    print("Starting " + str(num_indexed) + "...")
    for j in range(num_at_a_time):
        line = file.readline()
        if line == '' or lines_read > ending_line:
            break
        while lines_read < starting_line:
            line = file.readline()
            lines_read += 1
            num_indexed += 1
        entries = line.split('\t')
        entries = [entry.strip() for entry in entries]
        thisMovieID = entries[movieID]
        thisMovieTitle = entries[movieTitle]
        synopsis = store.scrapeSynopsis(thisMovieID)
        movie_data.append((thisMovieID, thisMovieTitle, synopsis))
        num_indexed += 1
        lines_read += 1
        if num_indexed % 100 == 0:
            print(str(num_indexed + "..."))
    print("... finished scraping page " + str(num_indexed))
    print("Indexing last " + str(len(movie_data)) + " pages...")
    if len(movie_data) == 0:
        break
    elif len(movie_data) < num_at_a_time:
        store.addBulkMovieSynopses(movie_data)
        break
    store.addBulkMovieSynopses(movie_data)
    print("..." + str(num_indexed) + " of " + str(ending_line) + " pages complete")

print("Indexed " + str(num_indexed) + " movies")
file.close()
