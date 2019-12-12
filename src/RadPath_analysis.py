#!/usr/bin/python3

'''
Documentation
'''

import os
import sys
import h5py
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from check_parser import *
from analysis import *
import pandas as pd

from argparse import ArgumentParser, RawTextHelpFormatter

matplotlib.rcParams.update({'font.size': 15})


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description="Ciao")
    parser.add_argument("file", type=str, help="File name in HDF5 format")
    parser.add_argument("cut",  type=str, help="CUT file with the angular positions")
    parser.add_argument('-fwhm', '--fwhm', action='store_true', help="Return the beam FWHM" )
    parser.add_argument('-o', '--output', default="", type=str, help="Output Graph")
    parser.add_argument('-n', '--normalized', action='store_true', help="The radiation pattern is normalized to 1 in intensity, 0 in dB" )
    parser.add_argument('-cx', '--cross_level', action='store_true', help="Return the polarization cross level" )
    parser.add_argument('-g', '--show-graphic', action='store_true', help="Show the plot in a temporary canvas")
    parser.add_argument('-gt', '--graph-tile', default="Radiation Pattern", type=str, help="Plot Title")
    parser.add_argument('-ref', '--reference', default="", type=str, help="Simulated reference" )
    parser.add_argument('-pf', '--polynomial-fit', action='store_true', help="Main beam polynomial fit")
    parser.add_argument('-po', '--polynomial-order', default=2, type=int, help="Polynomial fit order")

    args_main = parser.parse_args()

    # Check the parser arguments
    try:
        chk_parser(parser)
    except NameError as NE:
        print(NE.args[0])
        quit()

    # Open File
    # The open funtion return a pandas dataset of pandas datasets.
    # Cut_name // Pandas_dataset with (Freq, Pos, Ampl)
    df = open_file(args_main)



    # Normalized Beam
    if args_main.normalized:
        df = beam_normalize(df)


    # FWHM evaluations
    # if args_main.fwhm:
    if args_main.fwhm:
        if args_main.normalized:
            df_fwhm = get_fwhm(df)
        else:
            temp_df = beam_normalize(df)
            df_fwhm = get_fwhm(temp_df)
        print(df_fwhm)

    # CX Polarization
    if args_main.cross_level:
        if args_main.normalized:
            df_cross = get_cross_level(df)
        else:
            temp_df = beam_normalize(df)
            df_cross = get_cross_level(temp_df)

        print(df_cross)


    # # Print Log_File
    #
    #
    # Show Graphic
    if args_main.show_graphic:
        for i in range(0, len(df.Cut)):
            for j in range(0, len(df.Data[i].Freq)):
                plt.plot(df.Data[i].Positions[j], df.Data[i].Ampl[j])
        plt.show()
