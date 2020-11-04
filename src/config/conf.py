import os
import sys
from datetime import datetime
from pytz import timezone, utc
import logging

def localTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("Asia/Ho_Chi_Minh")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()

logging.basicConfig(
    format="""%(asctime)s %(processName)-10s %(name)s %(levelname)-8s - %(message)s""", 
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

logging.Formatter.converter = localTime

local_config_dict = {
    "ENV"                           : "dev",

    "WORKERS"                       : "8",

    "NONLOGO_FILENAME"              : "nonlogo_prod_50000.csv",
    "LOGO_FILENAME"                 : "prod_logo.csv",
    "BASE_PATH_URL"                 : "https://salt.tikicdn.com/",
    "PREDICT_API"                   : "http://0.0.0.0:5000/brand/predict",
    "GOOGLE_STORAGE_FOLDER"         : "gs://marketplace_ai_project/brand_recognition/testing/23_brands/",
    "BRAND_IDS_NAME"                : "7brands",
    "OUTPUT_NAME"                   : "yolov4_7brands"
}

# Local initial
for key, value in local_config_dict.items():
    if os.environ.get(key) is None:
        os.environ[key] = value

# For changing environment
ENV = os.environ.get("ENV")

WORKERS = int(os.environ["WORKERS"])
BASE_PATH_URL = os.environ["BASE_PATH_URL"]
LOGO_FILENAME = os.environ["LOGO_FILENAME"]
NONLOGO_FILENAME = os.environ["NONLOGO_FILENAME"]
GOOGLE_STORAGE_FOLDER = os.environ["GOOGLE_STORAGE_FOLDER"]
PREDICT_API = os.environ["PREDICT_API"]
OUTPUT_NAME = os.environ["OUTPUT_NAME"]
BRAND_IDS_NAME = os.environ["BRAND_IDS_NAME"]