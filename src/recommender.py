from pathlib import Path
from create_recommendation_dataset import build_model, roberta_encode, vectorize_name_description

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.applications.resnet50 import ResNet50
import tensorflow as tf

current_address = Path(__file__)
IMAGES_PATH = current_address.parents[1] / "data" / 'images'
arrays_path = current_address.parents[1]/'data'
images_arrays_path =arrays_path/'arr_images.npy'
names_arrays_path = arrays_path/'arr_text_names.npy'
descriptions_arrays_path = arrays_path/'arr_text_descriptions.npy'
tabular_dataset_path = arrays_path/'data.csv'

def vectorize_image(row):
    img_url = row['image url']
    image = Image.open(IMAGES_PATH / img_url)
    image = np.array(image)
    lst_= [tf.image.resize(image,size=(224,224))]
    model = ResNet50(include_top=True,input_shape=(224, 224, 3))

    ar = np.empty((1,1000))
    for i in range(len(lst_)):
        m = model(tf.expand_dims(lst_[i],0))
        ar = np.concatenate([ar,m])
    return ar

def calculate_price_diff(row_rec,df):
    price_diff = df['price'].apply(lambda x:(np.exp((x-row_rec['price'])/df['price'].max())))
    return price_diff

def make_store_and_brand_binary(row,df):
    store = row['store']
    brand = row['brand']
    store_match = (df['store']==store).astype(int).rename('store_match')
    brand_match = (df['brand']==brand).astype(int).rename('brand_match')

    total_match = pd.concat([store_match,brand_match],axis = 1)
    return total_match

def compute_cosine(vec_rec,matrix):
    cos_df = cosine_similarity([vec_rec],matrix)
    cos_df = np.squeeze(cos_df)
    return cos_df

def clean_tabular(data):
    data = data.dropna()
    data["item description"] = data["item description"].apply(lambda x : x.replace("\n\n\n", " "))
    data["item description"] = data["item description"].apply(lambda x : x.replace("\n", " "))
    data["item description"] = data["item description"].apply(lambda x : x.replace("\n\n", " "))
    data["item description"] = data["item description"].apply(lambda x : x.replace("\\", ""))
    return data

class Recommender:
    def __init__(
        self,
        name_array_path = names_arrays_path,
        description_array_path =descriptions_arrays_path,
        image_array_path = images_arrays_path,
        tabular_path = tabular_dataset_path,
        weights = [1/6]*6):
    
        with open(name_array_path,'rb') as f:
            self.name_array = np.load(f,allow_pickle=True)
        
        with open(description_array_path,'rb') as f:
            self.descriptions_array = np.load(f,allow_pickle=True)

        with open(image_array_path,'rb') as f:
            self.images_array = np.load(f,allow_pickle=True)
        self.tabular = clean_tabular(pd.read_csv(tabular_path))
        self.tabular['price'] = self.tabular.price.apply(lambda x:x.replace(',','')).astype(float)
        self.weights =np.array(weights,dtype = np.float32)
        # self.model = build_model()

    def predict(self,row_number):
        row = self.tabular.iloc[row_number]
        
        prices = calculate_price_diff(row,self.tabular)
        print('prices done')
        store_and_brand_match = make_store_and_brand_binary(row,self.tabular)
        print('store and brand done')
        name_similarities = compute_cosine(self.name_array[row_number,:],self.name_array)
        print('names done')
        description_similarities = compute_cosine(self.descriptions_array[row_number,:],self.descriptions_array)
        print('descriptions done')
        images_similarities = compute_cosine(self.images_array[row_number,:],self.images_array)
        print(images_similarities)
        print('images done')

        dataset = self.tabular.copy(deep = True)

        data_ = dataset[~dataset["image url"].duplicated()]['image url']
        image_to_cosine_sim_dict = {image_name:img_array for image_name,img_array in zip(data_.to_numpy(),images_similarities)}
        dataset['image similarities'] = dataset['image url'].map(image_to_cosine_sim_dict)
        dataset["name_similarities"] = name_similarities
        dataset["description_similarities"] = description_similarities
        dataset["prices"] = prices
        dataset = pd.concat([dataset,store_and_brand_match],axis = 1)

        scaler = MinMaxScaler()
        df_numeric = dataset.select_dtypes(include=np.number)
        df_numeric = pd.DataFrame(scaler.fit_transform(df_numeric,),columns=df_numeric.columns)
        df = pd.concat([df_numeric,dataset.select_dtypes(exclude=np.number)],axis = 1)

        df['weighted_sum'] = df["store_match"].astype(float)*self.weights[0] + \
            df["brand_match"].astype(float)*self.weights[1] + \
            df["name_similarities"].astype(float)*self.weights[2]  + \
            df["description_similarities"].astype(float)*self.weights[3] + \
            df["image similarities"].astype(float)*self.weights[4] + \
            df["prices"].astype(float)*self.weights[5]
        top5 = df["weighted_sum"].sort_values(ascending = False).index[:5]
        return df.iloc[top5]

if __name__=='__main__':
    rec = Recommender()
    print(rec.predict(0))
