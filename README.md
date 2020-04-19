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

Run the scraper to insert movies into the database and scrape movie synopses from IMDB



#### Dependencies

If adding dependencies to the project, make sure to update the `requirements.txt` with the correct package name and version number. You can use `pip freeze | grep <name>` to get the correct format with version.

The scraper relies on connecting to an Elasticsearch instance. You can use [Docker to create a single-node instance](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html) or [install manually](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html). I would also recommend getting [Kibana](https://www.elastic.co/guide/en/kibana/current/install.html) as well to interact with and visualize Elasticsearch

> If using Mac or Linux, try using `start-docker.sh` and `stop-docker.sh` for starting and stopping the containers for both Elasticsearch and Kibana. It will also handle install

For this project, we use an Elasticsearch instance on AWS

#### Structure

All static files, such as JS and CSS, go into the `static/` directory.

All Jinja templates for the webpage go into the `templates/` directory.

All other code for ranking and logic goes into the `src/` directory.

## Resources

- [Elasticsearch Python](https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html)
