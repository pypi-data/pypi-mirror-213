# FocalNet: Focal Modulation Networks for Tensorflow 

This repository contains a TensorFlow implementation of the paper Focal Modulation Networks. The paper proposes an attention-free architecture called focal modulation, which can dynamically adjust the focus of convolutional neural networks on different regions of the input. Focal modulation can improve the performance of various vision tasks, such as image classification, object detection, semantic segmentation and face recognition.

Focal Modulation  brings several merits:

* **Translation-Invariance**: It is performed for each target token with the context centered around it.
* **Explicit input-dependency**: The *modulator* is computed by aggregating the short- and long-rage context from the input and then applied to the target token.
* **Spatial- and channel-specific**: It first aggregates the context spatial-wise and then channel-wise, followed by an element-wise modulation.
* **Decoupled feature granularity**: Query token preserves the invidual information at finest level, while coarser context is extracted surrounding it. They two are decoupled but connected through the modulation operation.
* **Easy to implement**: We can implement both context aggregation and interaction in a very simple and light-weight way. It does not need softmax, multiple attention heads, feature map rolling or unfolding, etc.

<p align="center">
<img src="figures/focalnet-model.png" width=80% height=80% 
class="center">
</p>

This repository aims to reproduce the results of the paper using TensorFlow 2.4.1 and provide a modular and easy-to-use implementation of focal modulation networks. The code is based on the official PyTorch implementation of the paper, which can be found on the offical repository [here](https://github.com/microsoft/FocalNet) . Only the classification part is implemented. Pretrained checkpoints have been converted on Tensorflow.

<p align="center">
<img src="figures/modulator.JPG" width=80% height=80% 
class="center">
</p>

# Installation

> pip install focalnet-tf

# Example 

```

import cv2
import sys
import numpy as np
import os 
import tensorflow as tf
from focalnet import load_focalnet, IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD, imagenet1k, imagenet22k

def preprocess_image(image ):
    image = image/255.0
    image = (image - IMAGENET_DEFAULT_MEAN)/IMAGENET_DEFAULT_STD
    return np.expand_dims(image, axis=0)

def center_crop(image, output_shape):
    # Get the input shape
    h, w, c = image.shape

    # Get the output shape
    h_desired, w_desired = output_shape

    # Check if the output shape is valid
    if h_desired > h or w_desired > w  :
        raise ValueError("Output shape must be smaller than or equal to input shape and have the same number of channels.")

    # Compute the crop coordinates
    h_start = (h - h_desired) // 2
    h_end = h_start + h_desired
    w_start = (w - w_desired) // 2
    w_end = w_start + w_desired

    # Crop the image and return it
    return image[h_start:h_end, w_start:w_end, :]

image = cv2.cvtColor(cv2.imread("tests/dog.jpg"), cv2.COLOR_BGR2RGB)
image_crop = center_crop(image, (768, 768))
output_shape = (224, 224)
image_resized = cv2.resize(image_crop, output_shape)
inputs = preprocess_image(image_crop)

model = load_focalnet(model_name='focalnet_tiny_srf', pretrained=True, return_model=False, act_head="softmax")
output = model.predict(inputs)
print(output[0, np.argmax(output)])
print(imagenet22k[np.argmax(output)])

```

# Acknowledgement

- paper : https://arxiv.org/abs/2203.11926 from Jianwei Yang et al.
- pytorch implementation : https://github.com/microsoft/FocalNet

