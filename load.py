import struct
import numpy as np
import matplotlib.pyplot as plt

class SG2():
    def __init__(self, sg2_path, header_rows=0x2b0, header_rows_each=0x480-0x2b0, ch_num=24, data_num=1024, sampling_rate=1024):
        # load constants
        self.ch_num = ch_num
        self.data_num = data_num
        self.sampling_rate = sampling_rate

        # open data
        binary_data = open(sg2_path, mode="rb")
        
        # discard header lines
        binary_data.read(header_rows)
        binary_data.read(header_rows_each)

        # prepare numpy array
        self.wave_data = np.zeros((ch_num, data_num))

        # load data
        for i in range(ch_num):
            for j in range(data_num):
                temp = binary_data.read(4)
                self.wave_data[i][j] = struct.unpack("<f", temp)[0]
            binary_data.read(header_rows_each + 4 * 12)
    
    def draw_figure(self):
        fig, axes = setup_figure(num_row=self.ch_num, height=16)

        x_time = np.linspace(0, self.data_num/self.sampling_rate, self.data_num)
        for i, ax in enumerate(axes.flat):
            ax.plot(x_time, self.wave_data[i])
        plt.show()


def setup_figure(num_row=1, num_col=1, width=6, height=6, left=0.125, right=0.9, hspace=0.2, wspace=0.2):
    fig, axes = plt.subplots(num_row, num_col, figsize=(width, height))
    fig.subplots_adjust(left=left, right=right, hspace=hspace, wspace=wspace)
    return (fig, axes)


