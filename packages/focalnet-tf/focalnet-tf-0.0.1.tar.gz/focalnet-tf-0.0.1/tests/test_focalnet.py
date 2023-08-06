import numpy as np
import sys
import os 
import cv2 
from focalnet.focalnet_utils import load_focalnet
import pytest 
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from tensorflow.keras import backend as K


@pytest.mark.unittest
def test_focalnet_tiny_srf():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_tiny_srf', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 768)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_tiny_srf', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1000)
    
@pytest.mark.unittest
def test_focalnet_tiny_lrf():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_tiny_lrf', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 768)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_tiny_lrf', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1000) 

@pytest.mark.unittest
def test_focalnet_small_srf():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_small_srf', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 768)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_small_srf', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1000)

@pytest.mark.unittest
def test_focalnet_small_lrf():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_small_lrf', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 768)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_small_lrf', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1000)

@pytest.mark.unittest
def test_focalnet_base_srf():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_base_srf', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1024)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_base_srf', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1000)

@pytest.mark.unittest
def test_focalnet_base_lrf():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (224, 224))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_base_lrf', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1024)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_base_lrf', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1000)
 
@pytest.mark.unittest
def test_focalnet_large_fl3():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_large_fl3', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1536)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_large_fl3', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 21842)

@pytest.mark.unittest
def test_focalnet_large_fl4():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_large_fl4', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 1536)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_large_fl4', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 21842)

@pytest.mark.unittest
def test_focalnet_xlarge_fl3():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_xlarge_fl3', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 2048)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_xlarge_fl3', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 21842)

@pytest.mark.unittest
def test_focalnet_xlarge_fl4():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    dummy = cv2.imread(f"{root_dir}/dog.jpg")
    dummy = cv2.resize(dummy, (384, 384))/255.0
    dummy =  np.expand_dims(dummy, axis=0)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_xlarge_fl4', pretrained=True, return_model=False, num_classes=0 )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 2048)

    K.clear_session()
    model = load_focalnet(model_name='focalnet_xlarge_fl4', pretrained=True, return_model=False  )
    prediction = model.predict(dummy)
    assert prediction.shape == (1, 21842)

'''
if __name__ == "__main__":
    test_focalnet_tiny_srf()
    test_focalnet_tiny_lrf()
    test_focalnet_small_srf()
    test_focalnet_small_lrf()
    test_focalnet_base_srf()
    test_focalnet_base_lrf()
    test_focalnet_large_fl3()
    test_focalnet_large_fl4()
    test_focalnet_xlarge_fl3()
    test_focalnet_xlarge_fl4()
'''