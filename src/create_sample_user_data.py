import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append('../src/')

from tqdm import tqdm

from recommender import Recommender

current_address = Path(__file__)
DATA_PATH = current_address.parents[1] / "data"/"sample.csv"

rec = Recommender()
table = rec.tabular
table.reset_index(inplace=True)
users = list(range(1,10001))

all_cases = []

def create_user_trial(id_ = None,item_index = None):
    case = dict()
    if id_ is None:
        sample_user = np.random.choice(users)
    else:
        sample_user = id_

    if item_index is None:
        sample_item = table.sample(1)
        item_index = sample_item.index[0]
    else:
        item_index = item_index

    rec_items = rec.predict(item_index)
    chance_conv = np.random.random()

    if chance_conv<0.1:
        converted = 1
    else:
        converted = 0

    chance_follow_up = np.random.random()

    if chance_follow_up<0.05:
        follow_up_item = rec_items.sample().index[0]
        case['Follow up item'] = follow_up_item
        create_user_trial(sample_user,follow_up_item)
    else:
        case['Follow up item'] = None

    case['UserID'] = sample_user
    case['ItemID'] = item_index
    case['Rec1'] = rec_items.index[0]
    case['Rec2'] = rec_items.index[1]
    case['Rec3'] = rec_items.index[2]
    case['Rec4'] = rec_items.index[3]
    case['Rec5'] = rec_items.index[4]
    case['Converted'] = converted

    case_df = pd.DataFrame([case])
    all_cases.append(case_df)


if __name__=='__main__':
    for i in tqdm(range(10000)):
        create_user_trial()
        if i%100==0:
            print(len(all_cases))
    dataset = pd.concat(all_cases)
    dataset.to_csv(DATA_PATH,index = False)
