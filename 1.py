
import torch
import argparse
from sys import platform


from torch.serialization import _open_file_like, _is_zipfile
from torch.serialization import *
from models import *  # set ONNX_EXPORT in models.py
from utils.datasets import *
from utils.utils import *


with _open_file_like('weights/lie8.pt', 'rb') as opened_file:
    if _is_zipfile(opened_file):
        print(1)