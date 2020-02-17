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

#### Running the server

To run the server for development, use `python main.py`.

#### Dependencies

If adding dependencies to the project, make sure to update the `requirements.txt` with the correct package name and version number. You can use `pip freeze | grep <name>` to get the correct format with version.

#### Structure

All static files, such as JS and CSS, go into the `static/` directory.

All Jinja templates for the webpage go into the `templates/` directory.

All other code for ranking and logic goes into the `src/` directory.
