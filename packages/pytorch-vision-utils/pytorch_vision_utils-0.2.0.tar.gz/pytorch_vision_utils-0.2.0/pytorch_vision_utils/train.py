import argparse
import numpy as np
import matplotlib.pyplot as plt
import torch
import os
import seaborn as sns
import random
import json

from datetime import datetime
from PIL import Image
from statistics import mean
from torch import nn, optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
from pretrainedmodels.models.xception import Xception
from custom_models.MobileNetV2 import MobileNetV2
from Utilities import DataVizUtilities, Training_Utilities


##################### D E F A U L T S #####################

parser = argparse.ArgumentParser(description="Picks which model we're going to train.")
parser.add_argument("--model_name", type=str)
args = parser.parse_args().__dict__
MODEL_NAME = args["model_name"] # "xception"


# DIRECTORY NAMES
cwd = os.getcwd()
MODEL_DIR = str(os.path.join(cwd, "saved_models"))
MEDIA_DIR = str(os.path.join(cwd, 'media'))
RESULTS_DIR = str(os.path.join(cwd, "model_results"))
INC_DIR = str(os.path.join(cwd, "incorrect_images"))
DATA_DIR = str(os.path.join(cwd, "data"))

train_utils = Training_Utilities(data_dir=DATA_DIR)
dataviz_utils = DataVizUtilities()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using: ", device)


##################### T R A I N I N G #####################
loss, acc = train_utils.train(model_name=MODEL_NAME, model_path=MODEL_DIR, inc_path=INC_DIR, show_graphs=True, dry_run=False)

with open(RESULTS_DIR+"/"+MODEL_NAME+".txt", "w+") as f:
    f.write(f"Loss: {loss}\tAccuracy: {acc}")

