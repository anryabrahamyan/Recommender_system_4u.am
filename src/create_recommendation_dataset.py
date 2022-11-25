"""
File for Generating the data necessart for recommender class
"""
import pandas as pd
import requests
from os import path
import urllib.parse
import numpy as np
from PIL import Image
from tensorflow.keras.applications.resnet50 import ResNet50
from transformers import RobertaTokenizer, TFRobertaModel
import os
import tensorflow as tf
from pathlib import Path


current_address = Path(__file__)
IMAGES_PATH = current_address.parents[1] / "data" / 'images'
if not os.path.isdir(IMAGES_PATH):
    os.mkdir(IMAGES_PATH)

DATA_PATH = current_address.parents[1] / 'data'
data = pd.read_csv(DATA_PATH/'data.csv')
data = data.dropna()
data["item description"] = data["item description"].apply(lambda x : x.replace("\n\n\n", " "))
data["item description"] = data["item description"].apply(lambda x : x.replace("\n", " "))
data["item description"] = data["item description"].apply(lambda x : x.replace("\n\n", " "))
data["item description"] = data["item description"].apply(lambda x : x.replace("\\", ""))

MODEL_NAME = "roberta-base"
MAX_LEN = 200


def download_images(data):
    """Download the images from the links stored in the dataset csv

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame created by the scraping script
    """
    for i in data["image url"]:
        img_data = requests.get(i).content
        url_parts = urllib.parse.urlparse(i)
        path_parts = url_parts[2].rpartition('/')
        IMAGES_PATH = current_address.parents[1] / "data" / 'images'
        address = IMAGES_PATH
        imgSaveDir = path.join(address, path_parts[2])
        with open(imgSaveDir, "wb") as handler:
            handler.write(img_data)

def vectorize_images():
    """convert images into vectors using a CNN

    Returns
    -------
    np.ndarray
        array of all of the vectors
    """
    lst = []
    for image in os.listdir(IMAGES_PATH):
        i = Image.open(IMAGES_PATH / image)
        i = np.array(i)
        lst.append(i)

    lst_= [tf.image.resize(img,size=(224,224)) for img in lst]
    model = ResNet50(include_top=True,input_shape=(224, 224, 3))
    os.chdir(current_address.parents[1] / 'data')

    ar = np.empty((1,1000))
    for i in range(len(lst_)):
        m = model(tf.expand_dims(lst_[i],0))
        ar = np.concatenate([ar,m])
    return ar


def roberta_encode(texts, tokenizer):
    """function used for encoding the texts given a tokenizer

    Parameters
    ----------
    texts : pd.Series[str]
        columns of texts to be encoded
    tokenizer : transformers tokenizer
        Tokenizer for preparing the inputs for the appropriate model
        as input

    Returns
    -------
    Dict[str,np.ndarray]
        Encodings returned by hte tokenizer
    """
    ct = len(texts)
    input_ids = np.ones((ct, MAX_LEN), dtype='int32')
    attention_mask = np.zeros((ct, MAX_LEN), dtype='int32')
    token_type_ids = np.zeros((ct, MAX_LEN), dtype='int32')  # Not used in text classification

    for k, text in enumerate(texts):
        # Tokenize
        tok_text = tokenizer.tokenize(text)

        # Truncate and convert tokens to numerical IDs
        enc_text = tokenizer.convert_tokens_to_ids(tok_text[:(MAX_LEN - 2)])

        input_length = len(enc_text) + 2
        input_length = input_length if input_length < MAX_LEN else MAX_LEN

        # Add tokens [CLS] and [SEP] at the beginning and the end
        input_ids[k, :input_length] = np.asarray([0] + enc_text + [2], dtype='int32')

        # Set to 1s in the attention input
        attention_mask[k, :input_length] = 1

    return {
        'input_word_ids': input_ids,
        'input_mask': attention_mask,
        'input_type_ids': token_type_ids
    }


def build_model():
    """Create the model for vectorizing texts

    Returns
    -------
    tf.Model
        model for predictions on the texts
    """
    input_word_ids = tf.keras.Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_word_ids')
    input_mask = tf.keras.Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_mask')
    input_type_ids = tf.keras.Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_type_ids')

    # Import RoBERTa model from HuggingFace
    roberta_model = TFRobertaModel.from_pretrained(MODEL_NAME)
    x = roberta_model(input_word_ids, attention_mask=input_mask, token_type_ids=input_type_ids)

    # Huggingface transformers have multiple outputs, embeddings are the first one,
    # so let's slice out the first position
    x = x[0]

    model = tf.keras.Model(inputs=[input_word_ids, input_mask, input_type_ids], outputs=x)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr=1e-4),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

    return model

def vectorize_name_description(data = data):
    """function used for vectorizing name and description
    columns of the data

    Parameters
    ----------
    data : pd.DataFrame, optional
        The dataset which has the appropriate columns, by default data

    Returns
    -------
    [np.ndarray,np.ndarray]
        The name and description columns in vectorized form
    """
    tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)

    name = data["product"]
    description = data["item description"]
    try:
        description.fillna('',inplace=True)
    except:
        print('predicting only for 1 row')

    encoded_product_name = roberta_encode(name, tokenizer)
    encoded_product_desc = roberta_encode(description, tokenizer)

    output_name = model.predict(encoded_product_name)
    output_name_reduced = np.sum(output_name,axis = 2)

    output_desc = model.predict(encoded_product_desc)
    output_desc_reduced = np.sum(output_desc,axis = 2)

    return output_name_reduced, output_desc_reduced

model = build_model()

def create_data():
    """
    Create the Existing data that will be used by the recommender class
    """
    with open(DATA_PATH / 'arr_images.npy', 'wb') as f:
        np.save(f, vectorize_images())
    vectors_name_desc = vectorize_name_description()
    with open(DATA_PATH /'arr_text_names.npy', 'wb') as f:
        np.save(f, vectors_name_desc[1])

    with open(DATA_PATH / 'arr_text_descriptions.npy', 'wb') as f:
        np.save(f, vectors_name_desc[0])


if __name__ == '__main__':
    download_images(data)
    create_data()
