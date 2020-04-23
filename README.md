<div align="center">
    <h1>MovieMash</h1>
</div>

## Summary

MovieMash is a website that generates a list of movies for your next movie marathon or when you are in a bingey mood! Input the amount of time you have and other options and get a list of awesome movies!

## Development

### Getting Started

Install [Python3](https://www.python.org/downloads/). I would also recommend using [Virtualenv](https://virtualenv.pypa.io/en/stable/) to keep everything isolated for this project.

#### Virtualenv instructions

Go to project directory and enter `virtualenv env`.

Then, use `source env/bin/activate` to enter the environment. 

> Command is different for Windows users on CMD or PowerShell

#### Installation

Install the necessary packages: `pip install -r requirements.txt`

#### Running the application

To run the server for development, use `python main.py`.

To run the server for production, use `gunicorn --bind 0.0.0.0:5050 wsgi`

> Use whatever port and location you need

Visit the page in your browser and enjoy!

#### Running the scraper and other data population

To seed the database, make sure you are in the root directory of the project have ```movies.tsv``` with UTF-8 encoding in that directory.

`python seed.py`

will seed the database in batches of 1000 movies. For each batch, the entire batch is scraped for synopses before all 1000 are inserted into elasticsearch at once.

#### Running the time evaluation scripts

To evaluate the use of time for the project, there is a script that uses somewhat random but vague queries, and identifies the difference between the time input and the filled up time.

`python run_time_eval.py`

We also have the following bash scripts for running the evaluations on queries to get NDCG-Partial:

`./run_queries_eval.sh`
`./run_keywords_eval.sh`

where the latter writes the results to the file keywords_results.tsv. To evaluate your own query, you can enter:

`echo <query> | python evaluations.py`

To see the NDCG-Partial scores.

#### Dependencies

If adding dependencies to the project, make sure to update the `requirements.txt` with the correct package name and version number. You can use `pip freeze | grep <name>` to get the correct format with version.

The scraper relies on connecting to an Elasticsearch instance. You can use [Docker to create a single-node instance](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) or [install manually](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html). I would also recommend getting [Kibana](https://www.elastic.co/guide/en/kibana/current/install.html) as well to interact with and visualize Elasticsearch

> If using Mac or Linux, try using `start-docker.sh` and `stop-docker.sh` for starting and stopping the containers for both Elasticsearch and Kibana. It will also handle install

For this project, we use an Elasticsearch instance on AWS

#### Structure

All static files, such as JS and CSS, go into the `static/` directory.

All Jinja templates for the webpage go into the `templates/` directory.

All other code for ranking and logic goes into the `src/` directory.

Scripts for seeding and evaluating and the input files for them are all in the root directory for the project `/` and should be run from there.

## Resources

- [Elasticsearch Python](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
