import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model

if __name__ == "__main__":

    header = ['user_id','item_id','rating','timestamp']
    dataset = pd.read_csv('./datasets/u.data',sep = '\t',names = header)

    n_items = dataset["item_id"].max()
    n_users = dataset["user_id"].max()

    train, test = train_test_split(dataset, test_size=0.1, random_state=42)

    movie_input = Input(shape=[1], name="Movie-Input")
    movie_embedding = Embedding(n_items+1, 5, name="Movie-Embedding")(movie_input)
    movie_vec = Flatten(name="Flatten-Books")(movie_embedding)

    user_input = Input(shape=[1], name="User-Input")
    user_embedding = Embedding(n_users+1, 5, name="User-Embedding")(user_input)
    user_vec = Flatten(name="Flatten-Users")(user_embedding)

    conc = Concatenate()([movie_vec, user_vec])

    model_test = Model([user_input, movie_input], conc)
    model_test.compile('adam', 'mse')
    train_data = model_test.predict([train.user_id, train.item_id])
    test_data = model_test.predict([test.user_id, test.item_id])

    # print(type(output_arr))

    with open("./datasets/TrainingFeatures.npy", "wb") as f:
        np.save(f, train_data)

    with open("./datasets/TestingFeatures.npy", "wb") as f:
        np.save(f, test_data)

    with open("./datasets/TrainingLabels.npy", "wb") as f:
        np.save(f, train.rating)

    with open("./datasets/TestingLabels.npy", "wb") as f:
        np.save(f, test.rating)

    print("Compele. Run main.py")