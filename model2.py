import numpy as np
import pandas as pd
import os
import warnings
import tensorflow as tf
from keras import backend as K
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.layers import Input, Embedding, Flatten, Dot, Dense, Concatenate
from keras.models import Model
warnings.filterwarnings('ignore')
header = ['user_id','item_id','rating','timestamp']
dataset = pd.read_csv('./datasets/ml-100k/u.data',sep = '\t',names = header)

print(dataset)
user2user_encoded = {x: i for i, x in enumerate(dataset["user_id"].unique().tolist())}
movie_encoded2movie = {i: x for i, x in enumerate(dataset["item_id"].unique().tolist())}
print(np.max(dataset.item_id))
n_users = dataset["user_id"].max()
n_items = dataset["item_id"].max()
train, test = train_test_split(dataset, test_size=0.1, random_state=42)

# creating book embedding path
# creating book embedding path
movie_input = Input(shape=[1], name="Movie-Input")
movie_embedding = Embedding(n_items+1, 5, name="Movie-Embedding")(movie_input)
movie_vec = Flatten(name="Flatten-Books")(movie_embedding)

# creating user embedding path
user_input = Input(shape=[1], name="User-Input")
user_embedding = Embedding(n_users+1, 5, name="User-Embedding")(user_input)
user_vec = Flatten(name="Flatten-Users")(user_embedding)
# concatenate features
conc = Concatenate()([movie_vec, user_vec])
# # Tesst
# model_test = Model([user_input, movie_input], conc)
# model_test.compile('adam', 'mse')
# output_arr = model_test.predict([train.user_id, train.item_id])
# output_arr1 = model_test.predict([test.user_id, test.item_id])
# print(type(output_arr))
# with open("trainigMK.npy", "wb") as f:
#     np.save(f, output_arr)
# with open("testingMK.npy", "wb") as f:
#     np.save(f, output_arr1)
# with open("ratingTrain.npy", "wb") as f:
#     np.save(f, train.rating)
# with open("ratingTest.npy", "wb") as f:
#     np.save(f, test.rating)
#========

# add fully-connected-layers
fc1 = Dense(128, activation='relu')(conc)
fc2 = Dense(32, activation='relu')(fc1)
out = Dense(1)(fc2)
# Create model and compile it
model = Model([user_input, movie_input], out)
model.compile(
    loss=tf.keras.losses.MeanSquaredError(),
    optimizer=tf.keras.optimizers.Adam(lr=0.0005)
)
data_train = [train.user_id, train.item_id]
history = model.fit(data_train, train.rating, epochs=2, verbose=1)
predictions = model.predict([test.user_id.head(10), test.item_id.head(10)])
[print(predictions[i], test.rating.iloc[i]) for i in range(0,10)]