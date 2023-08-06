import torch
import torch.nn as nn
import os
import h5py
import numpy as np
from soapcw.cnn.pytorch import models
import argparse
import time

class LoadData(torch.utils.data.Dataset):

    def __init__(self, noise_load_directory, signal_load_directory, load_types = ["stats", "vit_imgs", "H_imgs", "L_imgs"], shuffle=True):
        self.load_types = load_types
        self.noise_load_directory = noise_load_directory
        self.signal_load_directory = signal_load_directory
        self.get_filenames()
        self.n_load_types = len(self.load_types) - 1 if "H_imgs" in self.load_types else len(self.load_types)
        self.shuffle = shuffle

    def __len__(self,):
        return min(len(self.noise_filenames), len(self.signal_filenames))

    def __getitem__(self, idx):
        """_summary_

        Args:
            idx (int): index

        Returns:
            _type_: data, truths arrays
        """
        noise_data, pars, pname = self.load_file(self.noise_filenames[idx])
        signal_data, pars, pname = self.load_file(self.signal_filenames[idx]) 

        tot_data = [torch.cat([torch.Tensor(noise_data[i]), torch.Tensor(signal_data[i])], dim=0) for i in range(self.n_load_types)]
        
        truths = torch.cat([torch.zeros(len(noise_data[0])), torch.ones(len(signal_data[0]))])
        if self.shuffle:
            shuffle_inds = np.arange(len(truths))
            np.random.shuffle(shuffle_inds)
            truths = truths[shuffle_inds]
            tot_data = [tot_data[i][shuffle_inds] for i in range(len(tot_data))]
        return tot_data, truths 

    def load_file(self, fname):
        """loads in one hdf5 containing data 

        Args:
            fname (string): filename

        Returns:
            _type_: data and parameters associated with files
        """
        with h5py.File(fname, "r") as f:
            output_data = []
            imgdone = False
            for data_type in self.load_types:
                if data_type in ["H_imgs", "L_imgs"]:
                    if imgdone:
                        continue
                    elif data_type == "H_imgs" and "L_imgs" in self.load_types:
                        output_data.append(np.transpose(np.concatenate([np.expand_dims(f["H_imgs"], -1), np.expand_dims(f["L_imgs"], -1)], axis=-1), (0,3,2,1)))
                        imgdone = True
                else:
                    output_data.append(np.array(f[data_type]))

            pars = np.array(f["pars"])
            parnames = list(f["parnames"])

        return output_data, pars, parnames

    def get_filenames(self):

        self.noise_filenames = [os.path.join(self.noise_load_directory, fname) for fname in os.listdir(self.noise_load_directory)]
        self.signal_filenames = [os.path.join(self.signal_load_directory, fname) for fname in os.listdir(self.signal_load_directory)]


def train_batch(model, optimiser, loss_fn, batch_data, batch_labels, model_type="spectrogram", train=True, device="cpu"):
    model.train(train)
    if train:
        optimiser.zero_grad()

    if model_type == "spectrogram":
        output = model(torch.Tensor(batch_data[0]).to(device))
        loss = loss_fn(output.flatten(), batch_labels.to(device).flatten())
        if train:
            loss.backward()
            optimiser.step()
    
    return loss.item()

def train_model(model_type, save_dir, load_dir, learning_rate, img_dim, conv_layers, fc_layers, device="cpu", load_model=None, bandtype="even", snrmin=40,snrmax=200, fmin=20,fmax=500, n_epochs=10):

    train_noise_dir = os.path.join(load_dir, "train", bandtype, f"band_{fmin}_{fmax}", "snr_0.0_0.0")
    train_signal_dir = os.path.join(load_dir, "train", bandtype, f"band_{fmin}_{fmax}", f"snr_{float(snrmin)}_{float(snrmax)}")

    val_noise_dir = os.path.join(load_dir, "validation", bandtype, f"band_{fmin}_{fmax}", "snr_0.0_0.0")
    val_signal_dir = os.path.join(load_dir, "validation", bandtype, f"band_{fmin}_{fmax}", f"snr_{float(snrmin)}_{float(snrmax)}")

    if model_type == "spectrogram":
        load_types = ["H_imgs", "L_imgs"]
        model = models.cnn.CNN(input_dim=img_dim, output_dim=1, fc_layers=fc_layers, conv_layers=conv_layers, inchannels=2, device=device).to(device)
    elif model_type == "vitmap":
        load_types = ["vit_imgs"]
        model = models.cnn.CNN(input_dim=img_dim, output_dim=1, fc_layers=fc_layers, conv_layers=conv_layers, inchannels=1, device=device).to(device)
    elif model_type == "vitmapspect":
        load_types = ["vit_imgs", "H_imgs", "L_imgs"]
        model = models.cnn.CNN(input_dim=img_dim, output_dim=1, fc_layers=fc_layers, conv_layers=conv_layers, inchannels=3, device=device).to(device)
    elif model_type == "vitmapspectstat":
        load_types = ["vit_imgs", "H_imgs", "L_imgs", "stat"]
    else:
        raise Exception(f"Load type {model_type} not defined select from [spectrogram, vitmap, vit_imgs, vitmapspect, vitmapspectstat]")

    print("model loaded")

    train_dataset = LoadData(train_noise_dir, train_signal_dir, load_types=load_types)
    validation_dataset = LoadData(val_noise_dir, val_signal_dir, load_types=load_types)
    print("data loaded")

    optimiser = torch.optim.Adam(model.parameters(), lr = learning_rate)
    loss_fn = torch.nn.BCELoss()

    if load_model is not None:
        checkpoint = model.load(load_model)
        model.load_state_dict(checkpoint["model_state_dict"])
        optimiser.load_state_dict(checkpoint["optimiser_state_dict"])


    all_losses = []
    all_val_losses = []
    print("training....")
    for epoch in range(n_epochs):

        epoch_start = time.time()
        losses = []
        mean_batch_time = []
        for batch_data, batch_labels in train_dataset:
            bt_start = time.time()
            loss = train_batch(model, optimiser, loss_fn, batch_data, batch_labels, device=device)    
            losses.append(loss)
            batch_time = time.time() - bt_start
            mean_batch_time.append(batch_time)
            print(f"batch_time: {batch_time}")

        print(f"mean_batch_time: {np.mean(mean_batch_time)}")
        
        with torch.no_grad():
            val_losses = []
            for batch_data, batch_labels in validation_dataset:
                loss = train_batch(model, optimiser, loss_fn, batch_data, batch_labels, train=False, device=device)    
                val_losses.append(loss)
        
        all_losses.append(np.mean(losses))
        all_val_losses.append(np.mean(val_losses))
        print(f"Epoch: {epoch}, Loss: {np.mean(losses)} val_loss: {np.mean(val_losses)}, epoch_time: {time.time() - epoch_start}")
        if epoch % 100 == 0:
            torch.save({
                "model_state_dict": model.state_dict(),
                "optimiser_state_dict": optimiser.state_dict(),
            }, os.path.join(save_dir, f"model_{model_type}.pt"))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', help='display status', action='store_true')
    parser.add_argument("-c", "--config-file", help="config file contatining parameters")

    device = "cuda:0"

    try:                                                     
        args = parser.parse_args()  
    except:  
        sys.exit(1)

    from soapcw.soap_config_parser import SOAPConfig

    if args.config_file is not None:
        cfg = SOAPConfig(args.config_file)

    train_model(cfg["model"]["model_type"], 
                cfg["model"]["save_dir"], 
                cfg["general"]["save_dir"], 
                cfg["model"]["learning_rate"], 
                cfg["model"]["img_dim"], 
                cfg["model"]["conv_layers"], 
                cfg["model"]["fc_layers"],
                n_epochs = cfg["model"]["n_epochs"],
                device=device)


if __name__ == "__main__":
    main()