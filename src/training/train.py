# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import os
import json
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#  with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], "r") as f:
#      key = json.loads(f.read(), strict=False)
#
#  with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], "w") as f:
#      json.dump(key, f)

os.environ["MLFLOW_TRACKING_URI"]="http://mlflow-tracking.tiki.services"

import warnings
import sys
import numpy as np
import pandas as pd
import mlflow

experiment = 'darknet_training'
#  if not mlflow.get_experiment_by_name(experiment):
#      client = mlflow.tracking.MlflowClient()
#      client.create_experiment(experiment)
#  mlflow.set_experiment(experiment)

def init_experiment(experiment_name):
    existing_experiments = mlflow.tracking.MlflowClient(os.environ['MLFLOW_TRACKING_URI']).list_experiments()
    logging.info(existing_experiments)
    if experiment_name in [exp.name for exp in existing_experiments]:
        mlflow.set_experiment(experiment_name)
    else:
        mlflow.create_experiment(experiment_name)

init_experiment(experiment)
    
def reset_mlflow_env():
    env_vars = ['MLFLOW_RUN_ID', 'MLFLOW_EXPERIMENT_ID']
    for e in env_vars:
        if e in os.environ:
            del os.environ[e]

#  reset_mlflow_env()


if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    
    # Get darknet data
    # with mlflow.start_run():

        #mlflow.log_param("l1_ratio", l1_ratio)
        #mlflow.log_metric("rmse", rmse)
        #mlflow.log_metric("r2", r2)
        #mlflow.log_metric("mae", mae)
        #mlflow.sklearn.save_model(lr, "model")
        
        #mlflow.sklearn.log_model(lr, "model")
    while(1):
        continue
