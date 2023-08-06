import os 
import json as json
from focalnet.focalnet import FocalNet 
from focalnet.download_weights import download_checkpoint, FOLDER_WEIGHTS
from tensorflow.keras import Model 
from tensorflow.keras.layers import Input
IMAGENET_DEFAULT_MEAN = (0.485, 0.456, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)


def imagenet_1k():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    data = json.load(open(os.path.join(root_dir, "imagenet-1k.json"), 'r'))
    idx2label = [data[str(k)][1] for k in range(len(data))]
    return idx2label 


def imagenet_22k():
    root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
    data = json.load(open(os.path.join(root_dir, "imagenet-22k-reorder.json"), 'r')) 
    idx2label = [data[str(k)]  for k in range(len(data))]
    return idx2label 

imagenet1k = imagenet_1k()
imagenet22k = imagenet_22k()


def load_focalnet(model_name, input_shape=(224, 224, 3), pretrained=False, return_model=True, num_classes=None, **kwargs):
    #print(kwargs)
    focal_levels=[2,2,2,2]
    focal_windows = [3, 3, 3, 3]
    use_conv_embed = False 
    use_postln = False 
    use_layerscale = False 
    normalize_modulator = False
    use_postln_in_modulation=False

    if model_name == "focalnet_tiny_srf":
        depths = [2, 2, 6, 2]
        embed_dim=96
        default_classes = 1000
    elif model_name == "focalnet_tiny_lrf":
        depths = [2, 2, 6, 2]
        embed_dim = 96
        focal_levels=[3, 3, 3, 3]
        default_classes = 1000
    elif model_name == "focalnet_small_srf":
        depths = [2, 2, 18, 2]
        embed_dim=96 
        default_classes = 1000
    elif model_name == "focalnet_small_lrf":
        depths = [2, 2, 18, 2]
        embed_dim = 96
        focal_levels=[3, 3, 3, 3]
        default_classes = 1000
    elif model_name == "focalnet_base_srf":
        depths = [2, 2, 18, 2]
        embed_dim = 128 
        default_classes = 1000
    elif model_name == "focalnet_base_lrf":
        depths = [2, 2, 18, 2]
        embed_dim = 128 
        focal_levels=[3, 3, 3, 3]
        default_classes = 1000
    elif model_name == "focalnet_large_fl3":
        depths = [2, 2, 18, 2]
        embed_dim = 192
        focal_levels=[3, 3, 3, 3]
        focal_windows = [5, 5, 5, 5]
        use_conv_embed = True
        use_postln = True
        use_layerscale =  True # False #
        default_classes = 21842
    elif model_name == "focalnet_large_fl4":
        depths = [2, 2, 18, 2]
        embed_dim = 192
        focal_levels = [4, 4, 4, 4]
        focal_windows =[3, 3, 3, 3]
        use_conv_embed = True
        use_postln = True
        use_layerscale = True 
        normalize_modulator = True 
        default_classes = 21842
    elif model_name == "focalnet_xlarge_fl3":
        depths = [2, 2, 18, 2]
        embed_dim = 256
        focal_levels=[3, 3, 3, 3]
        focal_windows = [5, 5, 5, 5]
        use_conv_embed = True
        use_postln = True
        use_layerscale = True 
        default_classes = 21842
    elif model_name == "focalnet_xlarge_fl4":
        depths = [2, 2, 18, 2]
        embed_dim = 256
        focal_levels=[4, 4, 4, 4]
        focal_windows =[3, 3, 3, 3]
        use_conv_embed = True
        use_postln = True
        use_layerscale = True 
        default_classes = 21842
    elif model_name == "focalnet_huge_fl3":
        depths = [2, 2, 18, 2]
        embed_dim = 352
        focal_levels=[3, 3, 3, 3]
        focal_windows =[3, 3, 3, 3]
        use_conv_embed = True
        use_postln = True
        use_layerscale = True 
        use_postln_in_modulation= True 
        default_classes = 21842
    elif model_name == "focalnet_huge_fl4":
        depths = [2, 2, 18, 2]
        embed_dim = 352
        focal_levels=[4, 4, 4, 4]
        focal_windows =[3, 3, 3, 3]
        use_conv_embed = True
        use_postln = True
        use_layerscale = True 
        use_postln_in_modulation= True 
        default_classes = 21842
    else: 
        raise("model name not found")

    if num_classes is None and pretrained:
        num_classes = default_classes
    elif num_classes is None:
        num_classes = 0

    backbone = FocalNet(depths=depths, embed_dim=embed_dim, focal_windows=focal_windows, focal_levels=focal_levels, use_conv_embed=use_conv_embed, use_postln=use_postln,
                        use_layerscale=use_layerscale, normalize_modulator=normalize_modulator, use_postln_in_modulation=use_postln_in_modulation, num_classes=num_classes, **kwargs)
    if pretrained:
        root_dir = os.path.sep.join(os.path.abspath(__file__).split(os.path.sep)[:-1])
        filename = f"{root_dir}/{FOLDER_WEIGHTS}/{model_name}.h5"
        #print(filename)
        if not os.path.exists(filename):
            # download
            download_checkpoint(model_name)
            #print("file not here")

        backbone.load_weights(filename, by_name=True, skip_mismatch=True)
    
    if return_model:
        inputs = Input(input_shape)
        outputs = backbone(inputs)
        model = Model(inputs=inputs, outputs=outputs)
        return model 
    return backbone