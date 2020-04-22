import sys
import json
import src.ndcg as test
import src.ranking as ranking
from src.scraper.storage import getMovies, getMoviesWithGenres

hours = 4
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
    for our_query in sys.stdin:
        if our_query == None:
            break
        query = our_query.strip()
        our_results, gt = ranking.score_with_gt(query, hours*60, new_movies, genres)
        if len(our_results) == 0:
            print(query + "\t0")
            continue

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
        
        print(query + "\t" + str(test.ndcg(gt_scores, our_scores)))

if __name__ == "__main__":
    main()
