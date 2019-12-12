import h5py
import glob
import numpy as np
import pandas as pd


# Read the CUTs and split it into different
# pandas dataframes
def open_file(args_main):
    file_h5 = glob.glob(str(args_main.file)+"/*.h5")
    df_cut_planes = pd.DataFrame(columns=['Cut', 'Data'])
    for i in file_h5:
        f = h5py.File(i, 'r')
        Freq = list(f['DUT'])
        c = pd.read_csv(args_main.cut, header=None, sep="\t")[0][0:186] #has to be FIXED
        df = pd.DataFrame(columns=['Freq', 'Positions', 'Ampl'])
        for j in Freq:
            Ampl_dB = np.sum(list(f["DUT"][j]["Ampl"]), axis=1)/201.0
            df = df.append({'Freq': j, 'Positions': c, 'Ampl': Ampl_dB}, ignore_index=True)
        df_cut_planes = df_cut_planes.append({'Cut':i.split("/")[-1].split('.')[0], 'Data': df}, ignore_index=True)

    return df_cut_planes


def beam_normalize(df):
    # 0 - 5
    # 2 - 4
    max45  = np.array([])
    maxm45 = np.array([])
    for cut in range(0, len(df.Cut)):
        if cut == 0: # co 45
            for freq in range(0, len(df.Data[cut].Freq)):
                max = np.amax(df.Data[cut].Ampl[freq])
                max45 = np.append(max45, max)
                df.Data[cut].Ampl[freq] = df.Data[cut].Ampl[freq] - max

        if cut == 2: # co m45
            for freq in range(0, len(df.Data[cut].Freq)):
                max = np.amax(df.Data[cut].Ampl[freq])
                maxm45 = np.append(maxm45, max)
                df.Data[cut].Ampl[freq] = df.Data[cut].Ampl[freq] - max

        elif (cut == 1) or (cut == 3):
            for freq in range(0, len(df.Data[cut].Freq)):
                max = np.amax(df.Data[cut].Ampl[freq])
                df.Data[cut].Ampl[freq] = df.Data[cut].Ampl[freq] - max

        elif cut == 5:
            for freq in range(0, len(df.Data[cut].Freq)):
                df.Data[cut].Ampl[freq] = df.Data[cut].Ampl[freq] - max45[freq]

        elif cut == 4:
            for freq in range(0, len(df.Data[cut].Freq)):
                df.Data[cut].Ampl[freq] = df.Data[cut].Ampl[freq] - maxm45[freq]


    return df


def get_fwhm(df):

    df_fwhm = pd.DataFrame(columns=['Cut', 'Freq', 'FWHM'])
    for cut in range(0, len(df.Cut)-2):
        for freq in range(0, len(df.Data[cut].Freq)):
            Ampl = df.Data[cut].Ampl[freq]
            Pos  = df.Data[cut].Positions[freq]
            idx  = (Ampl > -3.0)
            estm = np.amin(Pos[idx])
            estM = np.amax(Pos[idx])
            fwhm = estM-estm
            df_fwhm = df_fwhm.append({'Cut': df.Cut[cut] , 'Freq':df.Data[cut].Freq[freq], 'FWHM':fwhm }, ignore_index=True)

    return df_fwhm


def get_cross_level(df):

    df_cx = pd.DataFrame(columns=['Freq', 'Cross'])
    for freq in range(0, 3):
        max_cx = -110
        for cut in range(4, 6):
            if np.amax(df.Data[cut].Ampl[freq]) > max_cx:
                max_cx = np.amax(df.Data[cut].Ampl[freq])
        df_cx = df_cx.append({'Freq':freq, 'Cross':max_cx}, ignore_index=True)

    return df_cx


def load_reference(args):

    df_ref = pd.DataFrame(columns=['Freq', 'Positions', 'Ampl'])

    ref_path  = args.reference_path
    ref_freq  = args.reference.split("E")

    for freq in ref_freq:
        print(freq)
        ref_specs = freq.split(",")
        file_name = "Phi"+ref_specs[1]+"_"+ref_specs[0]+"GHz.txt"



        try:
            print(file_name)
            a = np.loadtxt(ref_path+"/"+file_name, skiprows=2)
            Pos  = a[:,0]
            Ampl = a[:,2]
            print("Successfuly loaded")
        except IOError as e:
            print("File not found...")

        print("Beam normalize...")
        Ampl = Ampl - np.amax(Ampl)

        print("Append the frequency into the DataFrame")
        df_ref = df_ref.append({'Freq':ref_specs[0], 'Positions':Pos, 'Ampl':Ampl}, ignore_index=True)

    return df_ref
