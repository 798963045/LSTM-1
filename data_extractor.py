import numpy as np
from keras.utils import np_utils

usable_chars = [' ', 'ו', 'י', 'ה', 'מ', 'ל', 'א', 'ר', 'ב', 'נ', 'ת', 'ש', 'ע', 'כ', ',', 'ד', '.', 'ח', 'פ', 'ק',
                '-', 'צ', 'ג', 'ס', 'ז', '"', 'ט', '?', '!', ':', '\'', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '0']


# Converts a text file to numbers according to the usable_chars mapping
def letters_to_numbers(letters):
    data = []
    for letter in letters:
        data.append(usable_chars.index(letter))
    return np.asarray(data)


def format_dataset(data_x, data_y, seq_length=1):
    # reshape X to be [samples, time steps, features]
    x = np.reshape(data_x, (len(data_x), seq_length, 1))
    # normalize
    x = x / float(len(usable_chars))

    # one hot encode the output variable
    y = np_utils.to_categorical(data_y)

    return x, y


# Create the dataset in the right format for lstm.
def create_dataset(dataset, look_back=1):
    data_x, data_y = [], []
    for i in range(len(dataset) - look_back - 1):
        a = dataset[i:(i + look_back)]
        data_x.append(a)
        data_y.append(dataset[i + look_back])
    data_x, data_y = format_dataset(data_x, data_y, seq_length=look_back)
    return data_x, data_y


"""
Get a txt file name and returns a tuple of np arrays of x_data for train and test and y_data for train and test which
will be in the format of one shot np arrays according to the usable_chars mapping.
"""


def read_data(file_name, test_size, sequence=1):
    file = open(file_name, 'r', encoding='utf-8')
    text = file.readline()
    train_size = len(text) - test_size

    train_text = text[:train_size]
    test_text = text[train_size:]

    train_x = letters_to_numbers(train_text)
    test_x = letters_to_numbers(test_text)

    (train_x, train_y) = create_dataset(train_x, sequence)
    (test_x, test_y) = create_dataset(test_x, sequence)
    return (train_x, train_y, test_x, test_y)
