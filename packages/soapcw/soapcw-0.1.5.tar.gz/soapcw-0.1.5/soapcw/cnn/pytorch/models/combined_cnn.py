import torch
import torch.nn as nn
import numpy as np
from .cnn import CNN

class VitmapSpectStatCNN(nn.Module):

    def __init__(self, input_dim, output_dim, fc_layers = [], conv_layers = [], stride = 1, device="cpu", dropout=0.0, inchannels = 1, stat_network = None, vitmap_network = None, spect_network = None, train_loaded_model = False):
        """
        args
        ----------
        input_dim: int
            length of input time series
        latent_dim: int
            number of variables in latent space
        output_dim: int
            number of output neurons
        fc_layers: list
            list of the fully connected layers [8, 4, 2] (8 neurons, 4 neurons, 2 neurons)
        conv_layers: list
            list of the convolutional layers [(8, 5, 2, 1), (4, 3, 2, 1)] (8 filters of size 5, 4 filters of size 3)
        """
        super().__init__()
        # define useful variables of network
        self.device = device
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.inchannels = inchannels

        # Define networks to load in
        self.stat_network = stat_network
        self.vitmap_network = vitmap_network
        self.spect_network = spect_network
        
        # convolutional parts
        self.fc_layers = fc_layers
        self.conv_layers = conv_layers
        self.num_conv = len(self.conv_layers)
        self.stride = stride

        self.activation = nn.LeakyReLU()
        self.out_activation = nn.Sigmoid()#nn.Softmax()
        self.drop = nn.Dropout(p=dropout)

        self.small_const = 1e-6

        # load or generate the spectrogram network
        if self.spect_network is not None:
            self.spect_network = torch.load(self.spect_network, map_location=self.device)
        else:
            self.spect_network = CNN(self.input_dim, self.output_dim, fc_layers = self.fc_layers, conv_layers =self.conv_layers, stride = self.stride, dropout = self.dropout, inchannels = 2)

        #load or generate the vitmap network
        if self.vitmap_network is not None:
            self.vitmap_network = torch.load(self.vitmap_network, map_location=self.device)
        else:
            self.vitmap_network = CNN(self.input_dim, self.output_dim, fc_layers = self.fc_layers, conv_layers =self.conv_layers, stride = self.stride, dropout = self.dropout, inchannels = 1)

        # load or generate the line aware stat network
        if self.stat_network is not None:
            self.stat_network = torch.load(self.stat_network, map_location = self.device)
        else:
            self.stat_network = nn.Sequential()
            self.stat_network.add_module("lin1",module=nn.Linear(1, 1))
            self.stat_network.add_module("act_lin1",module=self.out_activation)

        self.spect_network.lin_network = nn.Sequential(*list(self.spect_network.lin_network.children())[:-1])
        self.vitmap_network.lin_network = nn.Sequential(*list(self.vitmap_network.lin_network.children())[:-1])
        
        for net in [self.spect_network.lin_network, self.spect_network.conv_network, self.vitmap_network.lin_network, self.vitmap_network.conv_network]:
            for param in list(net.parameters()):
                param.requires_grad = train_loaded_model

        self.final_classifier = nn.Sequential()
        # we remove last layer from spect and vitmap networks so their outputs are of size fc_layers[-1]
        #we then add this to the output of stat network
        self.final_classifier.add_module("linout",module=nn.Linear(2*self.fc_layers[-1] + 1, self.output_dim))
        self.final_classifier.add_module("act_linout",module=self.out_activation)

        
    def forward(self, y_vitmap, y_spect, y_stat):
        """forward pass for training"""
        # run the vitmap network
        y_vitmap = torch.reshape(y_vitmap, (-1, self.vitmap_network.inchannels, self.input_dim[0], self.input_dim[1])) 
        vitmap_conv = self.vitmap_network.conv_network(y_vitmap)
        vitmap_lin = torch.flatten(vitmap_conv,start_dim=1)
        vitmap_out = self.vitmap_network.lin_network(vitmap_lin) # run fully connected network

        # run the spect network
        y_spect = torch.reshape(y_spect, (-1, self.spect_network.inchannels, self.input_dim[0], self.input_dim[1])) 
        spect_conv = self.spect_network.conv_network(y_spect)
        spect_lin = torch.flatten(spect_conv,start_dim=1)
        spect_out = self.spect_network.lin_network(spect_lin) # run fully connected network

        # run the stat network
        y_stat = torch.reshape(y_stat, (-1, 1)) 
        stat_out = self.stat_network(y_stat) # run fully connected network
        
        # combine all three outputs
        out = self.final_classifier(torch.cat([vitmap_out, spect_out, stat_out], dim = 1))

        return out
    
    def test(model, y_vitmap, y_spect, y_stat):
        """generating samples when testing the network """
        num_data = y_vitmap.size(0)                                                                                                                                                     
        x_out = []
        # encode the data into latent space with r1(z,y)          
        for i in range(num_data):
            x_out.append(model.forward(y_vitmap[i], y_spect[i], y_stat[i]).cpu().numpy())
        return np.array(x_out)




class VitmapStatCNN(nn.Module):

    def __init__(self, input_dim, output_dim, fc_layers = [], conv_layers = [], stride = 1, device="cpu", dropout=0.0, inchannels = 1, stat_network = None, vitmap_network = None, train_loaded_model = False):
        """
        args
        ----------
        input_dim: int
            length of input time series
        latent_dim: int
            number of variables in latent space
        output_dim: int
            number of output neurons
        fc_layers: list
            list of the fully connected layers [8, 4, 2] (8 neurons, 4 neurons, 2 neurons)
        conv_layers: list
            list of the convolutional layers [(8, 5, 2, 1), (4, 3, 2, 1)] (8 filters of size 5, 4 filters of size 3)
        """
        super().__init__()
        # define useful variables of network
        self.device = device
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.inchannels = inchannels

        # Define networks to load in
        self.stat_network = stat_network
        self.vitmap_network = vitmap_network
        
        # convolutional parts
        self.fc_layers = fc_layers
        self.conv_layers = conv_layers
        self.num_conv = len(self.conv_layers)
        self.stride = stride

        self.activation = nn.LeakyReLU()
        self.out_activation = nn.Sigmoid()#nn.Softmax()
        self.drop = nn.Dropout(p=dropout)

        self.small_const = 1e-6

        #load or generate the vitmap network
        if self.vitmap_network is not None:
            self.vitmap_network = torch.load(self.vitmap_network, map_location=self.device)
        else:
            self.vitmap_network = CNN(self.input_dim, self.output_dim, fc_layers = self.fc_layers, conv_layers =self.conv_layers, stride = self.stride, dropout = self.dropout, inchannels = 1)

        # load or generate the line aware stat network
        if self.stat_network is not None:
            self.stat_network = torch.load(self.stat_network, map_location = self.device)
        else:
            self.stat_network = nn.Sequential()
            self.stat_network.add_module("lin1",module=nn.Linear(1, 1))
            self.stat_network.add_module("act_lin1",module=self.out_activation)

        # remove last layer of vitmap network
        self.vitmap_network.lin_network = nn.Sequential(*list(self.vitmap_network.lin_network.children())[:-1])
        
        for net in [self.vitmap_network.lin_network, self.vitmap_network.conv_network]:
            for param in list(net.parameters()):
                param.requires_grad = train_loaded_model

        self.final_classifier = nn.Sequential()
        # we remove last layer from vitmap networks so their outputs are of size fc_layers[-1]
        #we then add this to the output of stat network
        self.final_classifier.add_module("linout",module=nn.Linear(self.fc_layers[-1] + 1, self.output_dim))
        self.final_classifier.add_module("act_linout",module=self.out_activation)

        
    def forward(self, y_vitmap, y_stat):
        """forward pass for training"""
        # run the vitmap network
        y_vitmap = torch.reshape(y_vitmap, (-1, self.vitmap_network.inchannels, self.input_dim[0], self.input_dim[1])) 
        vitmap_conv = self.vitmap_network.conv_network(y_vitmap)
        vitmap_lin = torch.flatten(vitmap_conv,start_dim=1)
        vitmap_out = self.vitmap_network.lin_network(vitmap_lin) # run fully connected network

        # run the stat network
        y_stat = torch.reshape(y_stat, (-1, 1)) 
        stat_out = self.stat_network(y_stat) # run fully connected network
        
        # combine all three outputs
        out = self.final_classifier(torch.cat([vitmap_out,  stat_out], dim = 1))

        return out
    
    def test(model, y_vitmap, y_stat):
        """generating samples when testing the network """
        num_data = y_vitmap.size(0)                                                                                                                                                     
        x_out = []
        # encode the data into latent space with r1(z,y)          
        for i in range(num_data):
            x_out.append(model.forward(y_vitmap[i], y_stat[i]).cpu().numpy())
        return np.array(x_out)

