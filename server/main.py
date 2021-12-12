from flask import Flask, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
import json


app = Flask(__name__)
CORS(app)


def load_json_file(name):
    path = os.path.join(app.root_path, "../datasets/api_data/" ,name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/navbar")
def navbar():
    genres = load_json_file("genres.json")
    languages = load_json_file("languages.json")

    return {"genres": genres, "languages": languages}



@app.route("/home")
def home():
    top_10_movies = load_json_file("top_10_movies.json")
    movies = load_json_file("movies.json")

    for idx in range(len(top_10_movies)):
        top_10_movies[idx] = movies[top_10_movies[idx]-1]


    return {"top-10": top_10_movies, "movies": movies[:20]}


@app.route("/movies/detail/<int:id>")
def movies_detail(id):
    movies = load_json_file("movies.json")
    movie = movies[id]
    neighbors_tag = load_json_file("neighbors_tag.json")
    neighbors_rating = load_json_file("neighbors_rating.json")

    neighbors_rating = neighbors_rating[id]
    neighbors_tag = neighbors_tag[id]

    for idx in range(12):
        neighbors_tag[idx] = movies[neighbors_tag[idx]]
        neighbors_rating[idx] = movies[neighbors_rating[idx]]

    return {"movie": movie, "neighbors_rating": neighbors_rating, "neighbors_tag": neighbors_tag}


@app.route("/movies/page/<int:number>")
def movies_page(number):
    movies = load_json_file("movies.json")
    number_page = len(movies)//20
    if 20*number_page < len(movies):
        number_page += 1
    
    if number > number_page:
        return {"Error":"Page index out of range"}
    
    limit_start = (number-1)*20
    limit_end = number*20

    return {"movies": movies[limit_start: limit_end], "pages": number_page}


@app.route("/movies/genres/<string:genres>")
def movies_genres(genres):
    movies = load_json_file("movies.json")

    movies_make = []

    for movie in movies:
        list_genre = [gen["value"] for gen in movie["genres"]]
        if genres in list_genre:
            movies_make.append(movie)
    
    return {"movies": movies_make}


@app.route("/movies/languages/<string:lang>")
def movies_languages(lang):
    movies = load_json_file("movies.json")

    movies_make = []

    for movie in movies:
        if lang == movie["lang"]:
            movies_make.append(movie)
    
    return {"movies": movies_make}