import numpy as np
import sys
import os 
import cv2 
from focalnet.focalnet_utils import load_focalnet
from focalnet_pt import load_focalnet as load_focalnetPT
import pytest 
import torch 
from tensorflow.keras import backend as K
torch.set_grad_enabled(False)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
"""
    Compare pytorch vs TF output
    need to store in tests/ckpt pytorch checkpoints

"""

@pytest.mark.reproductibletest
def test_focalnet_tiny_srf_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_tiny_srf'
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_tiny_srf.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 768)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False   )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_tiny_srf.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 1000)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    
@pytest.mark.reproductibletest
def test_focalnet_tiny_lrf_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_tiny_lrf'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_tiny_lrf.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 768)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_tiny_lrf.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 1000)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_small_srf_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_small_srf'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_small_srf.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()

    assert prediction.shape == (1, 768)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False  )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_small_srf.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 1000)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_small_lrf_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_small_lrf'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_small_lrf.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 768)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False  )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_small_lrf.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 1000)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_base_srf_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_base_srf'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_base_srf.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 1024)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False  )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_base_srf.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 1000)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_base_lrf_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_base_lrf'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_base_lrf.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 1024)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_base_lrf.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 1000)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 
 
@pytest.mark.reproductibletest
def test_focalnet_large_fl3_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_large_fl3'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_large_lrf_384.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 1536)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_large_lrf_384.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 21842)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_large_fl4_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_large_fl4'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_large_lrf_384_fl4.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 1536)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False   )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_large_lrf_384_fl4.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 21842)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_xlarge_fl3_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_xlarge_fl3'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_xlarge_lrf_384.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()

    assert prediction.shape == (1, 2048)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False   )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_xlarge_lrf_384.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 21842)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_xlarge_fl4_reproductible():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)
    dummy_pt = torch.as_tensor(dummy).permute((0,3,1,2)).float()
    model_name = 'focalnet_xlarge_fl4'
    
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False, num_classes=0 )
    model_pt = load_focalnetPT(model_name=model_name, num_classes=0 ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_xlarge_lrf_384_fl4.pth", map_location="cpu")["model"], strict=False)
    prediction = model.predict(dummy) 
    prediction_pt = model_pt(dummy_pt).numpy()
    
    assert prediction.shape == (1, 2048)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2
    K.clear_session()
    model = load_focalnet(model_name=model_name, pretrained=True, return_model=False   )
    model_pt = load_focalnetPT(model_name=model_name ).eval()
    model_pt.load_state_dict(torch.load(f"{root_dir}/ckpt/focalnet_xlarge_lrf_384_fl4.pth", map_location="cpu")["model"], strict=True)
 
    prediction = model.predict(dummy)
    prediction_pt = model_pt(dummy_pt).numpy()
    assert prediction.shape == (1, 21842)
    assert np.abs(prediction - prediction_pt).mean() < 1e-2 

@pytest.mark.reproductibletest
def test_focalnet_huge_fl3_reproductible():
    pass

@pytest.mark.reproductibletest
def test_focalnet_huge_fl4_reproductible():
    pass 

if __name__ == "__main__":
    test_focalnet_tiny_srf_reproductible()
    test_focalnet_tiny_lrf_reproductible()
    test_focalnet_small_srf_reproductible()
    test_focalnet_small_lrf_reproductible()
    test_focalnet_base_srf_reproductible()
    test_focalnet_base_lrf_reproductible()
    test_focalnet_large_fl3_reproductible()
    test_focalnet_large_fl4_reproductible()
    test_focalnet_xlarge_fl3_reproductible()
    test_focalnet_xlarge_fl4_reproductible()