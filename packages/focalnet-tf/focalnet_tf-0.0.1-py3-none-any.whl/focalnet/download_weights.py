# -*- coding: utf-8 -*-
from huggingface_hub import hf_hub_url, cached_download
import requests
import os 
import shutil
urls_focalnet = {"focalnet_tiny_srf":"focalnet_tiny_srf.h5",
        "focalnet_tiny_lrf":"focalnet_tiny_lrf.h5",
        "focalnet_small_srf":"focalnet_small_srf.h5",
        "focalnet_small_lrf":"focalnet_small_lrf.h5",
        "focalnet_base_srf":"focalnet_base_srf.h5",
        "focalnet_base_lrf":"focalnet_base_lrf.h5",
        "focalnet_large_fl3":"focalnet_large_fl3.h5",
        "focalnet_large_fl4":"focalnet_large_fl4.h5",
        "focalnet_xlarge_fl3":"focalnet_xlarge_fl3.h5",
        "focalnet_xlarge_fl4":"focalnet_xlarge_fl4.h5",
        #"focalnet_huge_fl3":"focalnet_huge_fl3.h5",
        #"focalnet_huge_fl4":"focalnet_huge_fl4.h5"
        }
        
FOLDER_WEIGHTS = "tmp"

def get_checkpoint_path():
    p = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    p = os.path.join(p, FOLDER_WEIGHTS)
    return p 

def download_checkpoint(model_name, folder=get_checkpoint_path()):
    REPO_ID = "Shiro/focalnet-tf"
    
    if model_name not in urls_focalnet.keys():
        raise("model name wrong, no pretrained checkpoints for :", model_name)
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    FILENAME = urls_focalnet[model_name]
        
       
    response = requests.get(hf_hub_url(REPO_ID, FILENAME))
    
    open(os.path.join(folder, FILENAME), "wb").write(response.content)
    print(f"checkpoint {FILENAME} downloaded in {folder}")


def clean_checkpoint():
    folder =  get_checkpoint_path() 
    shutil.rmtree(folder)