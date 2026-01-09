import readfiles
import intvalpy as ip
import numpy as np

filepath_y = "0.225_lvl_side_a_fast_data.bin"
filepath_x = "-0.205_lvl_side_a_fast_data.bin"

rad = 1/(2**14)

X_data_origin = readfiles.read_files(filepath_x)
Y_data_origin = readfiles.read_files(filepath_y)


np.savetxt("X.txt", X_data_origin)
np.savetxt("Y.txt", Y_data_origin)