import os, sys
from pathlib import Path
SRC_DIR = str(Path(os.getcwd()).parent)
sys.path.insert(0, SRC_DIR)

import config.conf as cfg
import requests
import json
import pandas as pd
from collections import defaultdict
import logging
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
import numpy as np

def create_base_path(url):
    base_path = ""
    if url.startswith("http"):
        base_path = ""
    elif url.startswith("product") or url.startswith("tmp"):
        base_path = "ts/"
    else:
        base_path = "media/catalog/product/"
    return base_path

def pred_img(link, final_df_dict, label):
    json_data = {'image_url': link}
    response = requests.post(url=cfg.PREDICT_API, json=json_data)
    res = json.loads(response.text)
    if not response.status_code == 200 or "Api Error" in res:
        print("Error link:", link)
        return
    final_df_dict["link"].append(link)
    final_df_dict["label"].append(label.lower())
    
    if res:
        max_pred = [None, -1]
        for r in res:
            if float(r['confidence']) > max_pred[1]:
                max_pred[1] = float(r['confidence'])
                max_pred[0] = r['brand_name']
        final_df_dict["prediction"].append(max_pred[0].lower())
        final_df_dict["confidence"].append(max_pred[1])
    else:
        final_df_dict["prediction"].append('others')
        final_df_dict["confidence"].append(0)

# Download data
os.system("gsutil cp gs://marketplace_ai_project/brand_recognition/testing/23_brands/nonlogo_prod_50000.csv ./nonlogo_prod_50000.csv")
os.system("gsutil cp gs://marketplace_ai_project/brand_recognition/testing/23_brands/prod_logo.csv ./prod_logo.csv")
os.system("gsutil cp gs://marketplace_ai_project/brand_recognition/testing/23_brands/{}_ID.txt ./{}_ID.txt".format( cfg.BRAND_IDS_NAME, cfg.BRAND_IDS_NAME ))

with open("{}_ID.txt".format(cfg.BRAND_IDS_NAME), "r") as f:
    brand_ids = f.readlines()
    brand_ids = [b_id.strip() for b_id in brand_ids]

# logo
df =  pd.read_csv(cfg.LOGO_FILENAME)
print(len(df))
df = df[df['class_id'].isin(brand_ids)]
print(len(df))

# nonlogo
df_non = pd.read_csv(cfg.NONLOGO_FILENAME)

print("Logo: {}".format(len(df)))
print("Non logo: {}".format(len(df_non)))

final_df_dict = defaultdict(list)

# predict logo
print("Predict logo...")
for index, row in df.iterrows():
    try:
        image_link = cfg.BASE_PATH_URL + row['base_path'] + row['image_url'] 
        pred_img(image_link, final_df_dict, row['class_name'])
    except Exception as E:
        print(image_link, E)
    
print("Predict nonlogo...")
# predict nonlogo
for index, row in df_non.iterrows():
    try:
        path = create_base_path(row['link_image'])
        image_link = cfg.BASE_PATH_URL + path + row['link_image'] 
        pred_img(image_link, final_df_dict, "Others")
    except Exception as E:
        print(image_link, E)
    
final_df = pd.DataFrame(final_df_dict)
final_df.to_csv("{}.csv".format(cfg.OUTPUT_NAME))

# Preprocessing result
for index, row in final_df.iterrows():
    final_df.at[index, 'label'] = row['label'].lower()
    if not isinstance(row['prediction'], str):
        final_df.at[index, 'prediction'] = "Others"
    else:
        final_df.at[index, 'prediction'] = row['prediction'].lower()

classes = final_df['label'].unique()
bot_classes = final_df['prediction'].unique()

logging.info(str(set(bot_classes) - set(classes)))

# Compute detail result
with open("{}_detail_result.txt".format(cfg.OUTPUT_NAME), "w") as f:
    for i, cl in enumerate(classes):
        f.write("{}. Class {}\n".format(str(i), cl))
        true = len(final_df[(final_df['label']==cl) & (final_df['prediction']==cl)])
        total = len(final_df[final_df['label']==cl])
        total_cl = len( df[ (df['label']==cl) & (df['label'].isin(classes)) ] )
        acc =  true / total
        f.write("Accuracy: {}/{}={}\n".format(true, total, acc))

ground_truths = final_df['label'].tolist()
bot_pred = final_df['prediction'].tolist()

class_names = list(set(ground_truths))
class_names.append('others')
#class_names.append(class_names.pop(class_names.index('others')))

# Create confusion matrices
cm = confusion_matrix(ground_truths, bot_pred, class_names, normalize='true')
logging.info(cm.shape)
fig, ax = plt.subplots(figsize=(30, 30))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(include_values=True, cmap=plt.cm.Blues, ax=ax, xticks_rotation='vertical', values_format='.2g')
plt.savefig("{}_confusion_matrix.jpg".format(cfg.OUTPUT_NAME))

# Upload result to google storage
os.system("gsutil cp ./{}.csv {}{}.csv".format( cfg.OUTPUT_NAME, cfg.GOOGLE_STORAGE_FOLDER, cfg.OUTPUT_NAME ))
os.system("gsutil cp ./{}_confusion_matrix.jpg {}{}_confusion_matrix.jpg".format(cfg.OUTPUT_NAME, cfg.GOOGLE_STORAGE_FOLDER, cfg.OUTPUT_NAME))
os.system("gsutil cp ./{}_detail_result.txt {}{}_detail_result.txt".format( cfg.OUTPUT_NAME, cfg.GOOGLE_STORAGE_FOLDER, cfg.OUTPUT_NAME ))

