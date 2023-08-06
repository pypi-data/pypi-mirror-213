import pkg_resources
import torch
import numpy as np
from .models import cnn
import configparser

def load_vitmap_model(fmin, obs_run = "O3", checkpoint_file = None):
    """
    Load the Viterbimap model for testing
    """
    if 40 < fmin < 500:
        brange = "40_500"
        stride = 1
    elif 500 < fmin < 1000:
        brange = "500_1000"
        stride = 2
    elif 1000 < fmin < 1500:
        brange = "1000_1500"
        stride = 3
    elif 1500 < fmin < 2000:
        brange = "1500_2000"
        stride = 4
        
    if np.round(fmin*10).astype(int) % stride*2 == 0:
        oddeven = "even"
    else:
        oddeven = "odd"
    
    if checkpoint_file is None:
        model_state = pkg_resources.resource_stream(__name__, "trained_models/{}/vitmap_F{}_{}.ckpt".format(obs_run,brange, oddeven))
    model_init = pkg_resources.resource_stream(__name__, "trained_models/{}/vitmap.ini".format(obs_run))
    
    config = read_config(model_init)

    # hardcoded input size at the moment
    model = cnn.CNN((156,89), 1, config["lin_layers"], config["conv_layers"] , device ="cpu", num_channels = 0)
    model.load_state_dict(torch.load(model_state))
    
    return model


def load_spect_model(fmin, obs_run = "O3"):

    if 40 < fmin < 500:
        brange = "40_500"
        stride = 1
    elif 500 < fmin < 1000:
        brange = "500_1000"
        stride = 2
    elif 1000 < fmin < 1500:
        brange = "1000_1500"
        stride = 3
    elif 1500 < fmin < 2000:
        brange = "1500_2000"
        stride = 4
        
    if np.round(fmin*10).astype(int) % stride*2 == 0:
        oddeven = "even"
    else:
        oddeven = "odd"

    model_state = pkg_resources.resource_stream(__name__, "trained_models/{}/vitmap_F{}_{}.ckpt".format(obs_run,brange, oddeven))
    model_init = pkg_resources.resource_stream(__name__, "trained_models/{}/vitmap.ini".format(obs_run))
    
    config = read_config(model_init)

    model = cnn.CNN((156,89), 1, config["lin_layers"], config["conv_layers"] , device ="cpu", num_channels = 2)
    model.load_state_dict(torch.load(model_state))
    
    return model


    
def read_config(config_file):
    cp = configparser.ConfigParser()
    cp.read(config_file.name)

    p = {}
    params = {"model": ["conv_num_filt", "conv_filt_size", "conv_max_pool", "lin_num_neuron", "lin_dropout", "learning_rate", "num_channels"],}

    for key,vals in params.items():
        for val in vals:
            try:
                p[val] = cp.get(key,val)
            except:
                p[val] = None
                print("No key: {}, {}".format(key,val))

    p["lin_layers"] = [int(n) for n in p["lin_num_neuron"].split(" ")]
    conv_num_filt = [int(n) for n in p["conv_num_filt"].split(" ")]
    conv_filt_size = [int(n) for n in p["conv_filt_size"].split(" ")]
    conv_max_pool = [int(n) for n in p["conv_max_pool"].split(" ")]
    p["conv_layers"] = [(conv_num_filt[i], conv_filt_size[i], conv_max_pool[i], 1) for i in range(len(conv_num_filt))]

    return p

