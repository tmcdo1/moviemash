import sys
import json
import src.ndcg as test
import src.ranking as ranking
from src.scraper.storage import getMovies, getMoviesWithGenres

new_movies = False
genres = []

def normalizeish(mylist):
    highest = mylist[0]
    lowest = mylist[len(mylist) - 1]
    diff = highest - lowest
    if lowest <= 0:
        for i in range(len(mylist)):
            mylist[i] += -lowest + 1
    return mylist

def main():
    for arg in sys.argv[1:]:
        hours = int(arg)

    #possible_hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    possible_hours = [10]#, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    line = "IMDB Keyword Query\t"
    for h in possible_hours:
        line += str(h) + "\t"
    print(line)

    for our_query in sys.stdin:
        if our_query == None:
            break

        query = our_query.strip()
        ndcg_scores = []
        for hours in possible_hours:
            our_results, gt = ranking.score_with_gt(query, hours*60, new_movies, genres)
            if len(our_results) == 0:
                ndcg_scores.append(0)
                continue

            #print(our_results)
            #print(gt)

            last_movie = our_results[len(our_results)-1]
            for i in range(len(gt)):
                if last_movie["_id"] == gt[i]["_id"]:
                    K = i + 1

            our_scores = []
            for our_result in our_results:
                for i, res in enumerate(gt):
                    if res["_id"] == our_result["_id"]:
                        our_scores.append(i)
                        break

            gt_scores = []
            for i, gt_entry in enumerate(gt):
                if i < K:
                    gt_scores.append(gt_entry["_score"])

            gt_scores = normalizeish(gt_scores)

            gt_titles = [movie['_source']['movie_name'] for movie in gt]
            gt_scores_str = [movie for movie in gt_scores]
            
            for i in range(len(gt_titles)):
                if i < K:
                    print(str(gt_titles[i]) + " " + str(gt_scores_str[i]))
            

            ndcg_scores.append(test.ndcg(gt_scores, our_scores))
            print(our_scores)
            #print(gt_scores)

        line = query + "\t"
        for ndcg_score in ndcg_scores:
            line += str(ndcg_score) + "\t"
        print(line)

if __name__ == "__main__":
    main()
