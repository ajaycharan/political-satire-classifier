import numpy as np
import re
import os
import codecs

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


def load_data_and_labels(positive_data_file_loc, negative_data_file_loc):
    """
    Loads MR polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    #positive_examples = list(open(positive_data_file, "r").readlines())
    #positive_examples = [s.strip() for s in positive_examples]
    #negative_examples = list(open(negative_data_file, "r").readlines())
    #negative_examples = [s.strip() for s in negative_examples]
    # Split by words
    category_names = ["positive", "negative"]
    categories_locs = [positive_data_file_loc, negative_data_file_loc]
    folders = ["train", 'test']
    data = {}
    for category_name, category_loc in zip(category_names, categories_locs):
        data[category_name] = {}
        for folder in folders:
            data[category_name][folder] = []
            for filename in os.listdir(os.path.join(category_loc, folder)):
                with codecs.open(os.path.join(category_loc, folder, filename), 'r', 'utf-8') as f:
                    data[category_name][folder].append(f.read())
    #x_text = [clean_str(sent) for sent in x_text]
    # Generate labels
    positive_labels_train = [[0, 1] for _ in data['positive']['train']]
    positive_labels_test = [[0, 1] for _ in data['positive']['test']]
    negative_labels_train = [[1, 0] for _ in data['negative']['train']]
    negative_labels_test = [[1, 0] for _ in data['negative']['test']]
    x_train = np.concatenate([data['positive']['train'], data['negative']['train']], 0)
    x_test = np.concatenate([data['positive']['test'], data['negative']['test']], 0)
    y_train = np.concatenate([positive_labels_train, negative_labels_train], 0)
    y_test = np.concatenate([positive_labels_test, negative_labels_test], 0)
    return [x_train, y_train, x_test, y_test]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
    """
    Generates a batch iterator for a dataset.
    """
    data = np.array(data)
    data_size = len(data)
    num_batches_per_epoch = int(len(data)/batch_size) + 1
    for epoch in range(num_epochs):
        # Shuffle the data at each epoch
        if shuffle:
            shuffle_indices = np.random.permutation(np.arange(data_size))
            shuffled_data = data[shuffle_indices]
        else:
            shuffled_data = data
        for batch_num in range(num_batches_per_epoch):
            start_index = batch_num * batch_size
            end_index = min((batch_num + 1) * batch_size, data_size)
            yield shuffled_data[start_index:end_index]
