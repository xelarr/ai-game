#sources of information: https://keras.io/


import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense, Dropout

dataset = read_csv("connect4.csv", delimiter=",") #reads in file. http://archive.ics.uci.edu/ml/datasets/connect-4

X = dataset.iloc[:,0:42].values 
Y = dataset.iloc[:,42:43].values

le = preprocessing.LabelEncoder()
X_encoded = le.fit_transform(X)

ohe = OneHotEncoder(categorical_features=[0..42])
X_onehot = ohe.fit_transform(X).toarray()

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(32, activation='relu', input_dim=100))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))


model.compile(optimizer='rmsprop', loss='binary_crossentropy',metrics=['accuracy'])

model.fit(x_train, y_train, epochs=20,batch_size=128)

score = model.evaluate(x_test, y_test, batch_size=128)

pred = model.predict(x_test)
