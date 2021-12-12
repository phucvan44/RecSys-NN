import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model


def mark_index_data():
    movies = pd.read_csv("../datasets/init_data/movies.csv", sep=";", encoding="latin-1")
    movies = movies.drop("Unnamed: 3", axis=1)

    # Parent for node
    parents = np.zeros((movies.movieId.max()+1, ), dtype="int64")

    # Find parent of node
    for idx, movie_id in enumerate(movies.movieId.values, 1):
        parents[movie_id] = idx
        movies.movieId.values[idx-1] = idx

    rating = pd.read_csv("../datasets/init_data/ratings.csv", sep=";")
    for idx, movie_id in enumerate(rating.movieId):
        rating.movieId.values[idx] = parents[movie_id]

    # Save file
    movies.to_csv("../datasets/init_data/movies.csv", index=False)
    rating.to_csv("../datasets/init_data/ratings.csv", index=False)


def get_none_rating():
    rating = pd.read_csv("../datasets/init_data/ratings.csv")
    df = rating.pivot_table(values="rating", columns="userId", index="movieId").fillna(0)

    movies = pd.read_csv("../datasets/init_data/movies.csv")
    len_movies = movies.movieId.values.max()
    movies_idx = np.unique(rating.movieId.values)
    movies_idx = movies_idx.reshape(len(movies_idx), )
    movies_idx = movies_idx.tolist()
    movie_axis = []

    for movie_id in range(1, len_movies + 1):
        if movie_id not in movies_idx:
            movie_axis.append(movie_id)

    len_users = rating.userId.values.max()

    movie_axis = np.array(movie_axis).reshape(-1, 1)
    user_axis = np.random.randint(1, len_users, size=(movie_axis.shape))

    none_rating = np.concatenate((movie_axis, user_axis), axis=1)
    df_none_rating = pd.DataFrame(none_rating, columns=["movieId", "userId"])
    return (df_none_rating, none_rating, rating)



def save_array(path, values):
    with open(path, "wb") as f:
        np.save(f, values)


if __name__ == "__main__":

    mark_index_data()

    df_none_rating, none_rating, dataset = get_none_rating()
    df_none_rating.to_csv("../datasets/init_data/none_rating.csv", index=False)

    n_movies = dataset["movieId"].max()
    n_users = dataset["userId"].max()

    train, test = train_test_split(dataset, test_size=0.3, random_state=42)

    movie_input = Input(shape=[1], name="Movie-Input")
    movie_embedding = Embedding(n_movies+1, 5, name="Movie-Embedding")(movie_input)
    movie_vec = Flatten(name="Flatten-Books")(movie_embedding)

    user_input = Input(shape=[1], name="User-Input")
    user_embedding = Embedding(n_users+1, 5, name="User-Embedding")(user_input)
    user_vec = Flatten(name="Flatten-Users")(user_embedding)

    conc = Concatenate()([movie_vec, user_vec])

    model = Model([user_input, movie_input], conc)
    model.compile('adam', 'mse')

    train_data = model.predict([train.userId, train.movieId])
    test_data = model.predict([test.userId, test.movieId])
    valid_data = model.predict([none_rating[:, 1], none_rating[:, 0]])

    save_array("../datasets/train_data/TrainingFeatures.npy", train_data)
    save_array("../datasets/train_data/TestingFeatures.npy", test_data)
    save_array("../datasets/train_data/ValidationFeatures.npy", valid_data)
    save_array("../datasets/train_data/TrainingLabels.npy", train.rating)
    save_array("../datasets/train_data/TestingLabels.npy", test.rating)

    print("Prepare data complete !")