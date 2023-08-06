import configparser
import json

class SOAPConfig():

    def __init__(self, config_file):
        cfg = configparser.ConfigParser()
        cfg.read(config_file)

        self.float_list = ["band_starts","band_ends","band_widths"]
        self.int_list = ["strides"]
        self.string_list = ["load_directory"]
        self.floats = ["band_load_size", "snr_width_line", "snr_width_signal", "prob_line", "left_right_prob", "det1_prob", "det2_prob"]
        self.ints = ["memory", "request_disk", "n_jobs", "n_summed_sfts"]

        self.config = self.parse_config(cfg)

    def __getitem__(self, key):
        return self.config[key]
    

    def load_list(self, val, partype):
        if "," in val:
            val = val.strip("[").strip("]").split(",")
        else:
            val = [val.strip("[").strip("]").strip(",")]
        
        if partype == "float":
            val = [float(v) for v in val]
        elif partype == "int":
            val = [int(v) for v in val]
        elif partype == "string":
            val = val
        else:
            raise Exception(f"Type {partype} not supported")

        return val

    def parse_config(self, cfg):

        parsed_dict = {}
        for key, val in cfg.items():
            parsed_dict[key] = {}
            for key2, val2 in val.items():
                # if comma then part of a list
                if key2 in self.float_list:
                    parsed_dict[key][key2] = self.load_list(val2, "float")
                elif key2 in self.int_list:
                    parsed_dict[key][key2] = self.load_list(val2, "int")
                elif key2 in self.string_list:
                    parsed_dict[key][key2] = self.load_list(val2, "string")
                elif key2 in self.floats:
                    parsed_dict[key][key2] = float(val2)
                elif key2 in self.ints:
                    parsed_dict[key][key2] = int(val2)
                else:
                    if val2 in ["none", "None"]:
                        parsed_dict[key][key2] = None
                    else:
                        parsed_dict[key][key2] = val2
                
        return parsed_dict