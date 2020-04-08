# Open the movies.tsv file and read in each movie row of the seed data
import scraper.storage as store

file = open("movies.tsv", 'r')

titles = file.readline().split('\t')
titles = [title.strip() for title in titles]

movieID = 0
movieType = 1
movieTitle = 2
movieRuntime = 3
movieGenres = 4
movieRating = 5
movieVotes = 6
movieYear = 7

num_indexed = 0
while True:
    movie_data = []
    num_at_a_time = 1000
    print("appending movie " + str(num_indexed) + " of " + str(534057) + "...") 
    for j in range(num_at_a_time):
        line = file.readline()
        if line == '':
            break
        entries = line.split('\t')
        entries = [entry.strip() for entry in entries]

        thisMovieID = entries[movieID]
        if (entries[movieRuntime] == '\\N'):
            thisMovieRuntime = None
        else:
            thisMovieRuntime = int(entries[movieRuntime])

        if (entries[movieGenres] == '\\N'):
            thisMovieGenre = None
        else:
            thisMovieGenre = entries[movieGenres].split(',')

        if (len(entries) == 8):
            if (entries[movieYear] == '\\N'):
                thisMovieYear = None
            else:
                thisMovieYear = int(entries[movieYear])
            thisMovieRating = float(entries[movieRating])
            thisMovieVotes = int(entries[movieVotes])
        elif (len(entries) == 7):
            print('error with length:')
            print(entries)
            exit()
        else:
            if (entries[movieYear-2] == '\\N'):
                thisMovieYear = None
            else:
                thisMovieYear = int(entries[movieYear-2])
            thisMovieRating = None
            thisMovieVotes = None

        movie_data.append((thisMovieID, thisMovieRuntime, thisMovieGenre, thisMovieRating, thisMovieVotes, thisMovieYear))
        num_indexed += 1
    print("Indexing last " + str(len(movie_data)) + " pages...")
    if len(movie_data) == 0:
        break
    elif len(movie_data) < num_at_a_time:
        store.appendBulkMovieInfo(movie_data)
        break
    store.appendBulkMovieInfo(movie_data)
    print("..." + str(num_indexed) + " of " + str(534057) + " pages complete")

print("Indexed " + str(num_indexed) + " movies")
file.close()
