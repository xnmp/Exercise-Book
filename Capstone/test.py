import random
import numpy as np
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Activation, Dropout

# load up our text
text = open('test.txt', 'r').read()

# extract all (unique) characters
# these are our "categories" or "labels"
chars = list(set(text))

# set a fixed vector size
# so we look at specific windows of characters
max_len = 20

model = Sequential()
model.add(LSTM(512, return_sequences=True, input_shape=(max_len, len(chars))))
model.add(Dropout(0.2))
model.add(LSTM(512, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# step size here is 3, but we can vary that
step = 3
inputs = []
outputs = []
for i in range(0, len(text) - max_len, step):
    inputs.append(text[i:i+max_len])
    outputs.append(text[i+max_len])


char_labels = {ch:i for i, ch in enumerate(chars)}
labels_char = {i:ch for i, ch in enumerate(chars)}

# using bool to reduce memory usage
X = np.zeros((len(inputs), max_len, len(chars)), dtype=np.bool)
y = np.zeros((len(inputs), len(chars)), dtype=np.bool)

# set the appropriate indices to 1 in each one-hot vector
for i, example in enumerate(inputs):
    for t, char in enumerate(example):
        X[i, t, char_labels[char]] = 1
    y[i, char_labels[outputs[i]]] = 1


# # more epochs is usually better, but training can be very slow if not on a GPU
epochs = 10
# model.fit(X, y, batch_size=128, nb_epoch=epochs)


def generate(temperature=0.35, seed=None, predicate=lambda x: len(x) < 100):
    if seed != None and len(seed) < max_len:
        raise Exception('Seed text must be at least {} chars long'.format(max_len))

    # if no seed text is specified, randomly select a chunk of text
    else:
        start_idx = random.randint(0, len(text) - max_len - 1)
        seed = text[start_idx:start_idx + max_len]

    sentence = seed
    generated = ''
    while predicate(generated):
        # generate the input tensor
        # from the last max_len characters generated so far
        x = np.zeros((1, max_len, len(chars)))
        for t, char in enumerate(sentence):
            x[0, t, char_labels[char]] = 1.

        # this produces a probability distribution over characters
        probs = model.predict(x, verbose=0)[0]

        # sample the character to use based on the predicted probabilities
        next_idx = sample(probs, temperature)
        next_char = labels_char[next_idx]

        generated += next_char
        sentence = sentence[1:] + next_char
        # print next_char
    return generated

def sample(probs, temperature):
    """samples an index from a vector of probabilities"""
    a = np.log(probs)/temperature
    a = np.exp(a)/np.sum(np.exp(a))
    samp = np.argmax(np.random.multinomial(1, a, 1))
    # print 'samp samp samp', samp
    return samp

for i in range(epochs):
    print 'epoch', i

    # set nb_epoch to 1 since we're iterating manually
    model.fit(X, y, batch_size=128, nb_epoch=1, verbose=0)

    # preview
    # for temp in [0.2, 0.5, 1., 1.2]:
        # print '\n\ttemperature:', temp
    temp = 1.2
    print generate(temperature=temp)
