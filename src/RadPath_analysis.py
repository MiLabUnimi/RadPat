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
    parser.add_argument('-ref_path', '--reference_path', default="", type=str, help="Path that contains the Simulated references")
    parser.add_argument('-ref', '--reference', default="", type=str, help="Simulated reference" )
    parser.add_argument('-show_ref', '--show_reference', action='store_true', help="Show the reference graphic")
    parser.add_argument('-show_diff', '--show_difference', action='store_true', help='Show the difference between Simulation and Meausured')
    parser.add_argument('-pf', '--polynomial-fit', action='store_true', help="Main beam polynomial fit")
    parser.add_argument('-po', '--polynomial-order', default=2, type=int, help="Polynomial fit order")
    parser.add_argument('-shift', '--shift_positions', default=0.0, type=float, help='Shift angle of the reference')

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

    # Show Graphic
    if args_main.show_graphic:
        for freq in range(0, 3):
            plt.figure(freq)
            plt.title(freq)
            for cut in range(0, 6):
                plt.plot(df.Data[cut].Positions[freq], df.Data[cut].Ampl[freq])
        plt.show()

    if args_main.reference != "":
        # Load the reference file
        df_ref = load_reference(args_main)
        # just to remeber
        # 0      KIDS_45
        # 1       KIDS_H
        # 2     KIDS_m45
        # 3       KIDS_E
        # 4    KIDS_Xm45
        # 5     KIDS_X45
        if (args_main.reference.split("E")[1]).split(",")[1] == "0":
            cut = 1
        if (args_main.reference.split("E")[1]).split(",")[1] == "90":
            cut = 3
        if (args_main.reference.split("E")[1]).split(",")[1] == "45":
            cut = 0
        if (args_main.reference.split("E")[1]).split(",")[1] == "m45":
            cut = 2

        df_ref_diff = get_diff(df, df_ref, cut)

        if args_main.show_reference:
            for freq in range(0, 3):
                plt.figure(freq)
                plt.title(freq)
                plt.plot(df.Data[cut].Positions[freq], df.Data[cut].Ampl[freq])
                plt.plot(df_ref.Positions[freq], df_ref.Ampl[freq])
            plt.show()

        if args_main.show_difference:
            for freq in range(0, 3):
                plt.title("Difference Simulated // Measured")
                plt.plot(df_ref_diff.Positions[freq], df_ref_diff.AmplDiff[freq])
            plt.show()
    else:
        print("No reference..")
