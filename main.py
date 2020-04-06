from flask import Flask, render_template, jsonify, request
import src.scraper.storage as store
import src.ranking as ranking
import json

app = Flask(__name__)

def print_results(res):
    #print(json.dumps(results, indent=4))
    print(str(len(res["hits"]["hits"])) + " results:")

    for result in res["hits"]["hits"]:
        print("ID " + result["_id"] + " SCORE " + str(result["_score"]))

@app.route('/')
def home():
    # examples = [
    #             {"id":"tt0081505", "name":"The Shining"},
    #             {"id":"tt0363771", "name":"Narnia"},
    #             {"id":"tt0000001", "name":"Carmencita"},
    #             {"id":"tt2294629", "name":"Frozen"},
    #             {"id":"tt1386492", "name":"This Is Not a Movie"}
    #         ]

    # for example in examples:
    #     synopsis = store.scrapeSynopsis(example["id"])
    #     store.addMovieSynopsis(example["id"], example["name"], synopsis)

    # results = store.getMovies('ice winter lamp post magic')
    # print_results(results)

    return render_template('index.html')

@app.route('/results', methods=['POST'])
def get_results():
    req_body = request.json
    query = req_body['query']
    hours = int(req_body['hours'])
    minutes = int(req_body['minutes'])
    new_movies = bool(req_body['new'])

    # TODO: get movies given info
    results = ranking.score(query, hours * 60 + minutes, new_movies)

    return jsonify({ 'movies': results })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
