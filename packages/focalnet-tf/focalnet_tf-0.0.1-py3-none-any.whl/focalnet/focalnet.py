# --------------------------------------------------------
# FocalNets -- Focal Modulation Networks
# Licensed under The MIT License [see LICENSE for details]
# Written by Shiro-LK
# --------------------------------------------------------
import os 
import tensorflow as tf 
from tensorflow.keras.layers import Dense, Activation, Dropout, Conv1D, Conv2D, ZeroPadding2D, Activation, LayerNormalization, GlobalAveragePooling2D, Reshape, \
                                     GlobalAveragePooling1D, Input
import collections
from itertools import repeat
from focalnet.drop import DropPath
#from drop import DropPath

import numpy as np 
from tensorflow.keras import Model

def _ntuple(n):
    def parse(x):
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, str):
            return tuple(x)
        return tuple(repeat(x, n))
    return parse

to_2tuple = _ntuple(2)


class Identity(tf.keras.layers.Layer):
    def __init__(self):
        super().__init__()

    def call(self, x):
        return x 

class PatchEmbed(tf.keras.layers.Layer):
    r""" Image to Patch Embedding
    Args:
        img_size (int): Image size.  Default: 224.
        patch_size (int): Patch token size. Default: 4.
        in_chans (int): Number of input image channels. Default: 3.
        embed_dim (int): Number of linear projection output channels. Default: 96.
        norm_layer (nn.Module, optional): Normalization layer. Default: None
    """

    def __init__(self, img_size=(224, 224), patch_size=4, in_chans=3, embed_dim=96, use_conv_embed=False, norm_layer=None, is_stem=False):
        super().__init__()
        patch_size = to_2tuple(patch_size)
        patches_resolution = [img_size[0] // patch_size[0], img_size[1] // patch_size[1]]
        self.img_size = img_size
        self.patch_size = patch_size
        self.patches_resolution = patches_resolution
        self.num_patches = patches_resolution[0] * patches_resolution[1]

        self.in_chans = in_chans
        self.embed_dim = embed_dim

        if use_conv_embed:
            # if we choose to use conv embedding, then we treat the stem and non-stem differently
            if is_stem:
                kernel_size = 7; padding = 2; stride = 4
            else:
                kernel_size = 3; padding = 1; stride = 2
            
            self.pad_proj = ZeroPadding2D(padding=padding)
            self.proj = Conv2D(filters=embed_dim, kernel_size=kernel_size, strides=stride, padding='valid', name="proj_conv" )
        else:
            #print(embed_dim, patch_size)
            self.pad_proj = Identity()
            self.proj = Conv2D(filters=embed_dim, kernel_size=patch_size, strides=patch_size, name="proj_conv" )
        
        if norm_layer is not None:
            self.norm = norm_layer(epsilon=1e-5  )#norm_layer(embed_dim)
        else:
            self.norm = None
        self.flatten = Reshape(target_shape=(-1, embed_dim))
    def call(self, x):
        """Patchifies the image and converts into tokens.

        Args:
            x: Tensor of shape (B, H, W, C)

        Returns:
            A tuple of the processed tensor, height of the projected
            feature map, width of the projected feature map
        """

        B, H, W, C = x.shape

        x = self.pad_proj(x)
        x = self.proj(x)
        
        B, H, W, C = x.shape #tf.shape(x) 
        x = self.flatten(x) # x.flatten(2).transpose(1, 2)  # B Ph*Pw C
        if self.norm is not None:
            x = self.norm(x)
        return x, H, W



class Mlp(tf.keras.layers.Layer):
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer="gelu", drop=0.):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = Dense(hidden_features, name="fc1")
        self.act = Activation(act_layer, name="act")
        self.fc2 = Dense(out_features, name="fc2")
        self.drop = Dropout(drop, name="drop")

    def call(self, x):
        x = self.fc1(x)     
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x

class FocalModulation(tf.keras.layers.Layer):
    def __init__(self, dim, focal_window, focal_level, focal_factor=2, bias=True, proj_drop=0., use_postln_in_modulation=False, normalize_modulator=False):
        super().__init__()

        self.dim = dim
        self.focal_window = focal_window
        self.focal_level = focal_level
        self.focal_factor = focal_factor
        self.use_postln_in_modulation = use_postln_in_modulation
        self.normalize_modulator = normalize_modulator

        self.f = Dense(2*dim + (self.focal_level+1), use_bias=bias, name="f" ) # nn.Linear(dim, 2*dim + (self.focal_level+1), bias=bias)
        self.h = Conv2D(filters=dim, kernel_size=1, strides=1, use_bias=bias, name="h" )

        self.act = Activation("gelu") #nn.GELU()
        self.proj = Dense(dim, name="proj" ) #nn.Linear(dim, dim)
        self.proj_drop = Dropout(proj_drop)
        self.gap = GlobalAveragePooling2D(  keepdims=True)
        self.focal_layers = []
                
        self.kernel_sizes = []
        for k in range(self.focal_level):
            kernel_size = self.focal_factor*k + self.focal_window
            self.focal_layers.append(
                tf.keras.Sequential([
                        #ZeroPadding2D(padding=(kernel_size // 2, kernel_size // 2)),
                        Conv2D(filters=dim, kernel_size=kernel_size, strides=1, 
                        groups=dim, padding='same', use_bias=False ,
                        activation=tf.keras.activations.gelu, dtype=tf.keras.backend.floatx()
                        )]
                        )
                )              
            self.kernel_sizes.append(kernel_size)          
        if self.use_postln_in_modulation:
            self.ln = LayerNormalization(epsilon=1e-5  )

    def call(self, x, return_modulator):
        """
        Args:
            x: input features with shape of (B, H, W, C)
        """
        C = x.shape[-1]

        # pre linear projection
        x = self.f(x) #tf.transpose(self.f(x), perm=[0,3,1,2] ) #.permute(0, 3, 1, 2)#.contiguous()
        q, ctx, self.gates = tf.split(x, [C, C, self.focal_level+1], axis=-1)
        
        # context aggreation
        ctx_all = 0

        
        for l in range(self.focal_level):
            ctx = tf.cast(self.focal_layers[l](ctx), dtype=ctx.dtype)
            ctx_all = ctx_all + ctx*self.gates[..., l:l+1]
        ctx_global = self.act(  self.gap(ctx) ) #.mean(2, keepdim=True).mean(3, keepdim=True))
        ctx_all = ctx_all + ctx_global*self.gates[..., self.focal_level:]
        # normalize context
        if self.normalize_modulator:
            ctx_all = ctx_all / (self.focal_level+1)

        # focal modulation
        self.modulator = self.h(ctx_all)
        x_out = q*self.modulator
        #x_out = tf.transpose(x_out, perm=[0, 2, 3, 1]    ) #.permute(0, 2, 3, 1).contiguous()
        if self.use_postln_in_modulation:
            x_out = self.ln(x_out)
        
        # post linear porjection
        x_out = self.proj(x_out)
        x_out = self.proj_drop(x_out)
        if return_modulator:
            return x_out, self.modulator
        return x_out

    def extra_repr(self) -> str:
        return f'dim={self.dim}'



class FocalNetBlock(tf.keras.layers.Layer):
    r""" Focal Modulation Network Block.
    Args:
        dim (int): Number of input channels.
        input_resolution (tuple[int]): Input resulotion.
        mlp_ratio (float): Ratio of mlp hidden dim to embedding dim.
        drop (float, optional): Dropout rate. Default: 0.0
        drop_path (float, optional): Stochastic depth rate. Default: 0.0
        act_layer (nn.Module, optional): Activation layer. Default: nn.GELU
        norm_layer (nn.Module, optional): Normalization layer.  Default: nn.LayerNorm
        focal_level (int): Number of focal levels. 
        focal_window (int): Focal window size at first focal level
        use_layerscale (bool): Whether use layerscale
        layerscale_value (float): Initial layerscale value
        use_postln (bool): Whether use layernorm after modulation
    """

    def __init__(self, dim, input_resolution, mlp_ratio=4., drop=0., drop_path=0., 
                    act_layer=tf.keras.activations.gelu, norm_layer=LayerNormalization,
                    focal_level=1, focal_window=3,
                    use_layerscale=False, layerscale_value=1e-4, 
                    use_postln=False, use_postln_in_modulation=False, 
                    normalize_modulator=False, name=None, **kwargs):
        super().__init__(name=name)

        self.dim = dim
        self.input_resolution = input_resolution
        self.mlp_ratio = mlp_ratio

        self.focal_window = focal_window
        self.focal_level = focal_level
        self.use_postln = use_postln

        self.norm1 = norm_layer(epsilon=1e-5, name="norm1")
        self.modulation = FocalModulation(
            dim, proj_drop=drop, focal_window=focal_window, focal_level=self.focal_level, 
            use_postln_in_modulation=use_postln_in_modulation, normalize_modulator=normalize_modulator
        )

        self.drop_path = DropPath(drop_path) if drop_path > 0. else Identity()
        self.norm2 = norm_layer(epsilon=1e-5, name="norm2")
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)

        self.gamma_1 = 1.0
        self.gamma_2 = 1.0    
        if use_layerscale:
            self.gamma_1 =  tf.Variable(layerscale_value * tf.ones((dim)), trainable=True, name=name + "gamma_1" )
            self.gamma_2 = tf.Variable(layerscale_value * tf.ones((dim)), trainable=True, name=name + "gamma_2")

        self.H = None
        self.W = None
 
    def call(self, x, H, W, return_modulator):
        #H, W = self.H, self.W
        B, L, C = x.shape
        shortcut = x

        # Focal Modulation
        
        x = x if self.use_postln else self.norm1(x)
        x = tf.reshape(x, shape=[-1, H, W, C])
        if return_modulator:
            x, modulator = self.modulation(x, return_modulator=return_modulator)
        else:
            x = self.modulation(x, return_modulator=return_modulator)
        x = tf.reshape(x, [-1, H * W, C])
        x = x if not self.use_postln else self.norm1(x)

        # FFN
         
        x = shortcut + self.drop_path(tf.cast(self.gamma_1, dtype=x.dtype) * x) 
        x = x + self.drop_path(tf.cast(self.gamma_2, dtype=x.dtype) * (self.norm2(self.mlp(x)) if self.use_postln else self.mlp(self.norm2(x))))

        if return_modulator:
            return x, modulator
        return x

    def extra_repr(self) -> str:
        return f"dim={self.dim}, input_resolution={self.input_resolution}, " \
               f"mlp_ratio={self.mlp_ratio}"

    

class BasicLayer(tf.keras.layers.Layer):
    """ A basic Focal Transformer layer for one stage.
    Args:
        dim (int): Number of input channels.
        input_resolution (tuple[int]): Input resolution.
        depth (int): Number of blocks.
        window_size (int): Local window size.
        mlp_ratio (float): Ratio of mlp hidden dim to embedding dim.
        qkv_bias (bool, optional): If True, add a learnable bias to query, key, value. Default: True
        qk_scale (float | None, optional): Override default qk scale of head_dim ** -0.5 if set.
        drop (float, optional): Dropout rate. Default: 0.0
        drop_path (float | tuple[float], optional): Stochastic depth rate. Default: 0.0
        norm_layer (List, optional): Normalization layer. Default: nn.LayerNorm
        downsample (tf.keras.layers.Layer | None, optional): Downsample layer at the end of the layer. Default: None
        use_checkpoint (bool): Whether to use checkpointing to save memory. Default: False.
        focal_level (int): Number of focal levels
        focal_window (int): Focal window size at first focal level
        use_layerscale (bool): Whether use layerscale
        layerscale_value (float): Initial layerscale value
        use_postln (bool): Whether use layernorm after modulation
    """

    def __init__(self, dim, out_dim, input_resolution, depth,
                 mlp_ratio=4., drop=0., drop_path=0., norm_layer=LayerNormalization, 
                 downsample=None, use_checkpoint=False, 
                 focal_level=1, focal_window=1, 
                 use_conv_embed=False, 
                 use_layerscale=False, layerscale_value=1e-4, 
                 use_postln=False, 
                 use_postln_in_modulation=False, 
                 normalize_modulator=False, name=None, **kwargs):

        super().__init__(name=name)
         
        self.dim = dim
        self.input_resolution = input_resolution
        self.depth = depth
        #self.use_checkpoint = use_checkpoint
        
        # build blocks
        self.blocks = [
            FocalNetBlock(
                dim=dim, 
                input_resolution=input_resolution,
                mlp_ratio=mlp_ratio, 
                drop=drop, 
                drop_path=drop_path[i] if isinstance(drop_path, list) else drop_path,
                norm_layer=norm_layer,
                focal_level=focal_level,
                focal_window=focal_window, 
                use_layerscale=use_layerscale, 
                layerscale_value=layerscale_value,
                use_postln=use_postln, 
                use_postln_in_modulation=use_postln_in_modulation, 
                normalize_modulator=normalize_modulator, 
                name =  f"focalnet_block_{i}"
            )
            for i in range(depth)] 

        if downsample is not None:
            self.downsample = downsample(
                img_size=input_resolution, 
                patch_size=2, 
                in_chans=dim, 
                embed_dim=out_dim, 
                use_conv_embed=use_conv_embed, 
                norm_layer=norm_layer, 
                is_stem=False
            )
        else:
            self.downsample = None

    def call(self, x, H, W, return_modulator):
        modulators = []
        for blk in self.blocks:
            if return_modulator:
                x, modulator = blk(x, H, W, return_modulator=return_modulator)
                modulators.append(modulator)
            else:
                x = blk(x, H, W, return_modulator=return_modulator)
        #print(x.shape, H, W)
        if self.downsample is not None:
            x = tf.reshape(x, [-1,  H, W, x.shape[-1]])
            x, Ho, Wo = self.downsample(x)
        else:
            Ho, Wo = H, W

        if return_modulator:
            return x, Ho, Wo, modulators
        return x, Ho, Wo

    def extra_repr(self) -> str:
        return f"dim={self.dim}, input_resolution={self.input_resolution}, depth={self.depth}"
 



class FocalNet(tf.keras.Model):#
    r""" Focal Modulation Networks (FocalNets)
    Args:
        img_size (int | tuple(int)): Input image size. Default 224
        patch_size (int | tuple(int)): Patch size. Default: 4
        in_chans (int): Number of input image channels. Default: 3
        num_classes (int): Number of classes for classification head. Default: 1000
        embed_dim (int): Patch embedding dimension. Default: 96
        depths (tuple(int)): Depth of each Focal Transformer layer.
        mlp_ratio (float): Ratio of mlp hidden dim to embedding dim. Default: 4
        drop_rate (float): Dropout rate. Default: 0
        drop_path_rate (float): Stochastic depth rate. Default: 0.1
        norm_layer (nn.Module): Normalization layer. Default: nn.LayerNorm.
        patch_norm (bool): If True, add normalization after patch embedding. Default: True
        use_checkpoint (bool): Whether to use checkpointing to save memory. Default: False 
        focal_levels (list): How many focal levels at all stages. Note that this excludes the finest-grain level. Default: [1, 1, 1, 1] 
        focal_windows (list): The focal window size at all stages. Default: [7, 5, 3, 1] 
        use_conv_embed (bool): Whether use convolutional embedding. We noted that using convolutional embedding usually improve the performance, but we do not use it by default. Default: False 
        use_layerscale (bool): Whether use layerscale proposed in CaiT. Default: False 
        layerscale_value (float): Value for layer scale. Default: 1e-4 
        use_postln (bool): Whether use layernorm after modulation (it helps stablize training of large models)
    """
    def __init__(self, 
                img_size=224, 
                patch_size=4, 
                in_chans=3, 
                num_classes=1000,
                embed_dim=96, 
                depths=[2, 2, 6, 2], 
                mlp_ratio=4., 
                drop_rate=0., 
                drop_path_rate=0.1,
                norm_layer=LayerNormalization, 
                patch_norm=True,
                use_checkpoint=False,                 
                focal_levels=[2, 2, 2, 2], 
                focal_windows=[3, 3, 3, 3], 
                use_conv_embed=False, 
                use_layerscale=False, 
                layerscale_value=1e-4, 
                use_postln=False, 
                use_postln_in_modulation=False, 
                normalize_modulator=False, 
                pooling="avg",
                include_top=True,
                name=None,
                act_head=None,
                **kwargs):
        super().__init__(name=name)

        self.num_layers = len(depths)
        embed_dim = [embed_dim * (2 ** i) for i in range(self.num_layers)]

        self.num_classes = num_classes
        self.embed_dim = embed_dim
        self.patch_norm = patch_norm
        self.num_features = embed_dim[-1]
        self.mlp_ratio = mlp_ratio
        
        # split image into patches using either non-overlapped embedding or overlapped embedding
        self.patch_embed = PatchEmbed(
            img_size=to_2tuple(img_size), 
            patch_size=patch_size, 
            in_chans=in_chans, 
            embed_dim=embed_dim[0], 
            use_conv_embed=use_conv_embed, 
            norm_layer=norm_layer if self.patch_norm else None, 
            is_stem=True)

        num_patches = self.patch_embed.num_patches
        patches_resolution = self.patch_embed.patches_resolution
        self.patches_resolution = patches_resolution
        self.pos_drop = Dropout(drop_rate)

        # stochastic depth
        #print(0, drop_path_rate, sum(depths))
        dpr = [x for x in tf.linspace(0., drop_path_rate, sum(depths)).numpy()]  # stochastic depth decay rule
 
        # build layers
        self.layers_ = []
        for i_layer in range(self.num_layers):
            layer = BasicLayer(dim=embed_dim[i_layer], 
                               out_dim=embed_dim[i_layer+1] if (i_layer < self.num_layers - 1) else None,  
                               input_resolution=(patches_resolution[0] // (2 ** i_layer),
                                                 patches_resolution[1] // (2 ** i_layer)),
                               depth=depths[i_layer],
                               mlp_ratio=self.mlp_ratio,
                               drop=drop_rate, 
                               drop_path=dpr[sum(depths[:i_layer]):sum(depths[:i_layer + 1])],
                               norm_layer=norm_layer, 
                               downsample=PatchEmbed if (i_layer < self.num_layers - 1) else None,
                               focal_level=focal_levels[i_layer], 
                               focal_window=focal_windows[i_layer], 
                               use_conv_embed=use_conv_embed,
                               use_checkpoint=use_checkpoint, 
                               use_layerscale=use_layerscale, 
                               layerscale_value=layerscale_value, 
                               use_postln=use_postln,
                               use_postln_in_modulation=use_postln_in_modulation, 
                               normalize_modulator=normalize_modulator,
                               name=f"basic_layer_{i_layer}"
                    )
            self.layers_.append(layer)

        self.norm = norm_layer(epsilon=1e-5, name="norm")
        self.avgpool = GlobalAveragePooling1D() if pooling == "avg" else GlobalMaxPooling1D() if pooling == "max" else None
        self.head = Dense(num_classes, name="head", activation=act_head, dtype=tf.float32) if num_classes > 0 and include_top else  Identity()
        self.return_modulator = False
        self.build((1, img_size, img_size, 3))

    def set_return_modulator(self, do_return=True):
        self.return_modulator = do_return 

    def extract_features(self, x, return_modulator):
        x, H, W = self.patch_embed(x)
        x = self.pos_drop(x)
        for layer in self.layers_:
            if layer == self.layers_[-1] and return_modulator:
                x, H, W, modulators = layer(x, H, W, return_modulator)
            else:
                x, H, W = layer(x, H, W, return_modulator=False)
        x = self.norm(x)  # B L C
        #print(H, W)
        if return_modulator:
            return x, modulators
        return x

    def call(self, x):
        if self.return_modulator:
            x, modulators = self.extract_features(x, return_modulator=self.return_modulator)
        else:
            x = self.extract_features(x, return_modulator=self.return_modulator)
        if self.avgpool is not None:
            x = self.avgpool(x) 
        #print(x[0,:10])
        x = self.head(x)
        if self.return_modulator:
            return x, modulators
        return x
 





if __name__ == '__main__':
    import numpy as np 
    img_size = 224
    x = np.zeros((2, img_size, img_size, 3)) + 0.25 #np.random.uniform(0, 1, (2, img_size, img_size, 3))#.cuda()

    model_name = "focalnet_tiny_srf"
    # model = FocalNet(depths=[2, 2, 6, 2], embed_dim=96)
    # model = FocalNet(depths=[12], patch_size=16, embed_dim=768, focal_levels=[3], focal_windows=[3], focal_factors=[2])
    #model = FocalNet(depths=[2, 2, 6, 2], embed_dim=96, focal_levels=[3, 3, 3, 3]) 
    model = load_focalnet(model_name=model_name, input_shape=(224, 224, 3), pretrained=True)#, num_classes=0)
    #model.load_weights(f"h5/{model_name}.h5")#, by_name=True, skip_mismatch=True)
    #print(model); 
    out = model(x)
    print(out[0, :10])
    print(out.shape)
    