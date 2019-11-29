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
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--file', default="", type=str, help="File Name" )
    parser.add_argument('-c', '--cut',  default="", type=str, help="Cut File with the angular positions")
    parser.add_argument('-fwhm', '--fwhm', action='store_true', help="Return the beam FWHM" )
    parser.add_argument('-o', '--output', default="", type=str, help="Output Graph")
    parser.add_argument('-n', '--normalized', action='store_true', help="The radiation pattern is normalized to 1 in intensity, 0 in dB" )
    parser.add_argument('-cx', '--cross_level', action='store_true', help="Return the polarization cross level" )
    parser.add_argument('-g', '--show-graphic', action='store_true', help="Show the plot in a temporary canvas")
    parser.add_argument('-gt', '--graph-tile', default="Radiation Pattern", type=str, help="Plot Title")
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
    df = open_file(args_main)

    # Normalized Beam
    if args_main.normalized:
        df = beam_normalize(df)

    # Show Graphic
    if args_main.show_graphic:
        for i in range(0, 3):
            plt.plot(df.Positions[i], df.Ampl[i])
        plt.show()
