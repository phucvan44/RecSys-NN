from pv.model import Model
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from collections import Counter


def save_astype_json(data, name):
    with open(name, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        print("[+] Save", name, "success")


def load_data(fileName):
    with open(fileName, "rb") as f:
        return np.load(f)


def predict_rating():
    path = "../datasets/train_data/"
    X_test = load_data(path + "ValidationFeatures.npy")

    model = Model.load_model("./backup/model.backup")
    predict = model.predictions(X_test, batch_size=64)

    rating_test = pd.read_csv("../datasets/init_data/none_rating.csv")
    rating_test["rating"] = predict
    rating_test["timestamp"] = np.random.randint(100000000, 999999999, size=predict.shape)

    rating_train = pd.read_csv("../datasets/init_data/ratings.csv")

    frames = [rating_train, rating_test]
    rating_full = pd.concat(frames)
    print("[+] Prediction rating sucess")
    return rating_full


def make_info_movies():
    languages = ['Armenia', 'Bangla', 'Brazil', 'Catalan', 'China', 'Denmark', 'England', 'French', 'Hindi', 'Italy',
                 'Japan', 'Khmer', 'Laos', 'Korea', 'Thailand', 'Vietnam']
    json_lang = []
    for lang in languages:
        json_lang.append({
            "value": lang,
            "url": "./languages.html?lang="+lang
        })
    save_astype_json(json_lang, "../datasets/api_data/languages.json")
    languages = languages*500

    np.random.shuffle(languages)

    list_img = []

    for i in range(1, 91):
        url = "https://vuighe.net/anime/trang-" + str(i)
        req = requests.get(url=url)
        soup = BeautifulSoup(req.text, "html.parser")
        contents = soup.find("div", {"class": "tray-content"})
        imgs = contents.find_all("img")
        for img in imgs:
            list_img.append(img["data-src"])

    list_img = list_img * 10

    df = pd.read_csv("../datasets/init_data/movies.csv", encoding="latin-1")
    df["img"] = list_img[: len(df.values)]
    df["lang"] = languages[: len(df.values)]
    df.to_csv("../datasets/init_data/movie_full.csv", index=False)
    print("[+] Get image for movies success")


def top_movies_by_rating():
    rating = pd.read_csv("../datasets/init_data/ratings.csv")
    rating_table = rating.pivot_table(values="rating", columns="userId", index="movieId").fillna(0)
    mean_movies_rating = np.mean(rating_table.values, axis=1)
    movieId = rating_table.index
    top_rating = movieId[np.argsort(mean_movies_rating)[::-1][:10]]
    save_astype_json(top_rating.tolist(), "../datasets/api_data/top_10_movies.json")


def neighbors_by_rating(rating):
    rating_table = rating.pivot_table(values="rating", columns="userId", index="movieId").fillna(0)
    mean_movies_rating = np.mean(rating_table.values, axis=1)
    neighbors = np.zeros((len(mean_movies_rating), 12))

    for movie_idx, mean_rating in enumerate(mean_movies_rating):
        neighbor_movie = np.abs(mean_movies_rating - mean_rating)
        neighbor_movie[movie_idx] = 5.0
        neighbors[movie_idx] = np.argsort(neighbor_movie)[:12]

    neighbors = neighbors.astype("int64")
    save_astype_json(neighbors.tolist(), "../datasets/api_data/neighbors_rating.json")


def neighbors_by_tag():
    movies = pd.read_csv("../datasets/init_data/movie_full.csv")
    genres = []
    for genre in movies.genres:
        if "(" in genre and ")" in genre:
            continue
        genres += genre.split("|")

    genres = np.unique(genres)
    movies_genres = pd.DataFrame(columns=genres)
    for genre in genres:
        movies_genres[genre] = np.array([
            1 if genre in movies.genres[idx] else 0 for idx in range(len(movies))
        ])

    neighbors = movies_genres.values @ movies_genres.values.T
    np.fill_diagonal(neighbors, -1)

    for neighbor_idx, neighbor in enumerate(neighbors):
        neighbor = np.argsort(neighbor)
        neighbors[neighbor_idx] = neighbor[::-1]

    neighbors = neighbors[::, :12]
    save_astype_json(neighbors.tolist(), "../datasets/api_data/neighbors_tag.json")

    json_genres = []
    for gen in genres:
        json_genres.append({
            "value": gen.strip(" "),
            "url": "./genres.html?genre=" + gen.strip(" ")
        })
    save_astype_json(json_genres, "../datasets/api_data/genres.json")


def convert_movies_to_json():
    rating = pd.read_csv("../datasets/init_data/ratings.csv")
    rating_table = rating.pivot_table(values="rating", columns="userId", index="movieId").fillna(0)

    rating_bar = {}
    for movieId, movie_rating in zip(rating_table.index, rating_table.values):
        bar = dict(Counter(movie_rating))
        bar[0.0] = 0
        for score in range(1,6):
            if score not in bar:
                bar[score] = 0
            if score-0.5 not in bar:
                bar[score-0.5] = 0

        rating_bar[movieId] = bar

    movies = pd.read_csv("../datasets/init_data/movie_full.csv", encoding="latin-1")
    movies_json = []

    for idx, movie in enumerate(movies.values, 1):
        bar = {}
        if idx not in rating_bar:
            bar[0.0] = 0
            for score in range(1, 6):
                bar[score] = 0
                bar[score-0.5] = 0
        else:
            bar = rating_bar[idx]

        genres = []
        for genre in movie[2].split("|"):
            genre = genre.strip(" ")
            if "(" in genre and ")" in genre:
                continue
            genres.append({
                "value": genre,
                "url": "./genres.html?genre="+genre
            })
        movies_json.append({
            "id": idx-1,
            "title": movie[1],
            "url": "./detail.html?id=" + str(idx),
            "genres": genres,
            "img": movie[3],
            "bar": bar,
            "lang": movie[4]
        })

    save_astype_json(movies_json, "../datasets/api_data/movies.json")


if __name__ == "__main__":
    make_info_movies()
    rating = predict_rating()
    neighbors_by_rating(rating)
    neighbors_by_tag()
    top_movies_by_rating()
    convert_movies_to_json()
