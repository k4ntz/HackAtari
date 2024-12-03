import torch
import numpy as np
from tqdm import tqdm


def classname(classstring):
    return (
        str(type(classstring))
        .replace(
            "<class '",
            "",
        )
        .replace("'>", "")
    )


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


def distance(obj1, obj2):
    return abs(obj1.x - obj2.x) + abs(obj1.y - obj2.y)


def get_closest_obj(obj, obj_list):
    candidates = [o for o in obj_list if o.category == obj.category]
    closest_c = [sorted(candidates, key=lambda x: distance(x, obj))[0]][0]
    return closest_c


def same_object_list(obj1, obj2):
    if len(obj1) != len(obj2):
        return False
    for o1, o2 in zip(
        sorted(
            obj1,
            key=lambda x: str(x),
        ),
        sorted(obj2, key=lambda x: str(x)),
    ):
        if o1.category != o2.category or o1.manathan_distance(o2) > 8:
            return False
    return True
