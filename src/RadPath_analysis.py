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

from argparse import ArgumentParser, RawTextHelpFormatter

matplotlib.rcParams.update({'font.size': 15})


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-f', '--file', default = "", type=str, help = "File Name" )
    parser.add_argument('-fwhm', '--fwhm', action ='store_true', help = "Return the beam FWHM" )
    parser.add_argument('-o', '--output', default = "", type = str, help = "Output Graph")
    parser.add_argument('-n', '--normalized', action = 'store_true', help = "The radiation pattern is normalized to 1 in intensity, 0 in dB" )
    parser.add_argument('-cx', '--cross_level', action = 'store_true', help = "Return the polarization cross level" )
    parser.add_argument('-g', '--show-graphic', action = 'store_true', help = "Show the plot in a temporary canvas")
    parser.add_argument('-pf', '--polynomial-fit', action = 'store_true', help = "Main beam polynomial fit")
    parser.add_argument('-po', '--polynomial-order', default = 2, type = int, help = "Polynomial fit order" )

    args_main = parser.parse_args()

    try:
        chk_parser(parser)
    except NameError as NE:
        print(NE.args[0])
        quit()

    # Open File
    f = h5py.File(args_main.file, 'r')
    Freq = list(f['Frequencies'])

    Ampl_dB_F1 =list(f["DUT"]["F_0"]["Ampl"])





# data = Dataset('MERRA2_100.inst1_2d_int_Nx.19800101.SUB.nc', mode='r')
# lons = data.variables['lon'][:]
# lats = data.variables['lat'][:]
# T2M = data.variables['TQV'][:,:,:]
#
#
#
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
# from mpl_toolkits.basemap import Basemap
#
# # Tenerife Island
# m = Basemap(llcrnrlon=-20.,llcrnrlat=26.,urcrnrlon=-10.,urcrnrlat=31.,
#             projection='lcc',lat_1=20.,lat_2=40.,lon_0=-60.,
#             resolution ='l',area_thresh=1000.)
#
#
# lon, lat = np.meshgrid(lons, lats)
# xi, yi = m(lon, lat)
#
# ## Plot data:
#
# for i in range(0,24):
#     cs = m.pcolor(xi,yi,np.squeeze(T2M[i,:,:]), vmin=np.min(T2M[0,:,:]), vmax=np.max(T2M[0,:,:]), cmap=cm.jet)
#     cs.set_edgecolor('face')
#     m.drawparallels(np.arange(26., 31., 1.), labels=[1,0,0,0], fontsize=5)
#     m.drawmeridians(np.arange(-20., -10., 1.), labels=[0,0,0,1], fontsize=4)
#     m.drawcoastlines()
#     m.drawstates()
#     m.drawcountries()
#
#     cbar = m.colorbar(cs, location='bottom', pad="10%")
#     cbar.set_label('kg/m^2')
#     cbar.ax.tick_params(labelsize=10)
#     plt.title('MERRA-2 2-meter PWV (1980-01-01) ore: '+ str(i) )
#
#     figure = plt.figure(1)
#     str_out = "MERRA" + str(i) + ".png"
#     figure.savefig(str_out, format='png', dpi=360)
#     plt.clf()
