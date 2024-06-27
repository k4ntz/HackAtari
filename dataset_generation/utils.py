import pandas as pd
import torch
import numpy as np
from tqdm import tqdm

def classname(classstring):
    return str(type(classstring)).replace("<class '", "",).replace("'>", "")

def get_dtypes(df):
    dtypes = {}
    for col in df.columns:
        if isinstance(df[col][0], (np.ndarray, torch.Tensor)):
            main = classname(df[col][0])
            dtypes[col] = f"{main} of {df[col][0].dtype}, {tuple(df[col][0].shape)}"
        else:
            dtypes[col] = classname(df[col][0])
    return dtypes

def get_props(objects_list):
    return

def get_obj_props(objects_serie):
    samples = {}
    print("Generating objects properties list...")
    for i, objects in tqdm(objects_serie.items()):
        for obj in objects:
            if not isinstance(obj, tuple(samples.keys())):
                samples[obj.__class__] = obj
    props = {}
    for classname, obj in samples.items():
        props[obj.category] = obj.properties
    return props