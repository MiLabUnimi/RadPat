import h5py
import numpy as np
import pandas as pd


def open_file(args_main):
    f = h5py.File(args_main.file, 'r')
    Freq = list(f['DUT'])

    c = pd.read_csv(args_main.cut, header=None, sep="\t")[0][0:186]
    df = pd.DataFrame(columns=['Freq', 'Positions', 'Ampl'])

    for i in Freq:
        print(i)
        Ampl_dB = np.sum(list(f["DUT"][i]["Ampl"]), axis=1)/201.0
        df = df.append({'Freq': i, 'Positions': c, 'Ampl': Ampl_dB}, ignore_index=True)

    return df


def beam_normalize(df):
    for i in range(0, len(df.Freq)):
        max = np.amax(df.Ampl[i])
        df.Ampl[i] = df.Ampl[i] - max

    return df
