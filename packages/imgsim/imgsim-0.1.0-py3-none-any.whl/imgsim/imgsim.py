import os
import sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, curdir)
model_path = os.path.join(curdir, 'data', 'model.pth')

import cv2
import numpy as np
from collections import OrderedDict

import torch
import torch.nn as nn
import torchvision.models as models

def normalize(Xs, mean, std):
    Xs_ = np.copy(Xs)
    for i in range(Xs_.shape[1]):
        Xs_[:,i,...] = (Xs_[:,i,...]-mean[i])/std[i]
    return Xs_

def distance(a, b):
    return np.sqrt(np.sum((a-b)**2))

def resize_short(img, size):
    short = min(img.shape[:2])
    scale = size/short
    new_shape = (int(max(img.shape[1] * scale, size)), int(max(img.shape[0] * scale, size)))
    resized = cv2.resize(img, new_shape)
    return resized


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.pre = models.resnet50(pretrained=False)
        self.pre.fc = nn.Linear(2048, 768)
        self.act = nn.Tanh()

    def forward(self, x):
        h = self.pre(x)
        h = self.act(h)
        return h


class Vectorizer:
    
    def __init__(self, device="cpu"):
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        
        self.device = torch.device(device)
        self.my_model = Net().to(self.device)
        
        state_dict = torch.load(model_path, map_location=device)
        state_dict_ = OrderedDict([])
        for name in state_dict.keys():
            name_ = name.replace("module.", "")
            state_dict_[name_] = state_dict[name]
        self.my_model.load_state_dict(state_dict_)
        
        self.my_model = self.my_model.eval()
        
    def vectorize(self, img):
        assert (
            img is not None and img.dtype == np.dtype('uint8') and len(img.shape)==3 and img.shape[2]==3
        ), "The images should be in uint8, with a size of (height, width, 3)."
        
        img = np.array([resize_short(img, 350)[...,::-1]/255.])
        Xs = torch.from_numpy(normalize(
            img.transpose([0,3,1,2]),
            mean=self.mean,
            std=self.std,
        ).astype(np.float32)).to(self.device)
        hs = self.my_model(Xs)
        out = hs.detach().cpu().numpy()[0]
        return out
