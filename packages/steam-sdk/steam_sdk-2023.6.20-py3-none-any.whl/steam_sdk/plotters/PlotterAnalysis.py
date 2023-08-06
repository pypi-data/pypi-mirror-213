import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from steam_sdk.parsers.ParserMat import Parser_LEDET_Mat

class PlotterAnalysis:
    def __init__(self, base_path):
        self.base_path = base_path

        self.__values_dict = {
            #'Time': {'mat_label': 'time_vector', 'op': None, 'min': -0.05, 'max': 0.2, 'unit': 's'},
            'Time': {'mat_label': 'time_vector', 'op': None, 'min': -0.01, 'max': 3.5, 'unit': 's'},
            'Time adb': {'mat_label': 'time_vector_hs', 'op': None, 'min': -0.05, 'max': 3.5, 'unit': 's'},
            '$T_{max}$': {'mat_label': 'T_ht', 'op': 'max', 'min': 0, 'max': 200, 'unit': 'K'},
            '$T_{max adb}$': {'mat_label': 'T_hs', 'op': 'max', 'min': 0, 'max': 200, 'unit': 'K'},
            '$I_{A}$': {'mat_label': 'Ia', 'op': None, 'min': 0, 'max': 200, 'unit': 'A'},
            '$I_{B}$': {'mat_label': 'Ib', 'op': None, 'min': 0, 'max': 200, 'unit': 'A'},
            '$I_{CLIQ}$': {'mat_label': 'Ic', 'op': None, 'min': 0, 'max': 200, 'unit': 'A'},
            '$U_{max}$': {'mat_label': 'Uground_half_turns', 'op': 'max', 'min': 0, 'max': 200, 'unit': 'V'},
            '$U_{min}$': {'mat_label': 'Uground_half_turns', 'op': 'min', 'min': 0, 'max': 200, 'unit': 'V'},
            '$R_{mag}$': {'mat_label': 'R_CoilSections', 'op': 'max', 'min': 0, 'max': 200, 'unit': 'Ohm'}
        }

    def set_plot_style(self, style):

        styles_dict = {
            'poster': {'plot_width': 1.9*8.9/2.54, 'plot_height': 3.2*6.2/2.54, 'font_size': 24},
            'publication': {'plot_width': 8.9/2.54, 'plot_height': 4/2.54, 'font_size': 5},
            'presentation': {'plot_width': 25 / 2.54, 'plot_height': 16 / 2.54, 'font_size': 16}
        }
        self.cs = styles_dict[style]

    def read_sweep(self, input_sweep_file, case, x_var_name, y_var_name):
        df = pd.read_csv(input_sweep_file)
        case_values = df.loc[df['comments'] == case]
        self.sim_numbers = case_values['simulation_number'].tolist()
        self.x_var_vals = case_values[x_var_name].tolist()
        self.y_var_vals = case_values[y_var_name].tolist()

    def plot_sweep_2d(self, model_name, z_var_name):
        plt.style.use('_mpl-gallery-nogrid')

        x = np.array(self.x_var_vals)
        y = np.array(self.y_var_vals)
        z = []

        for sim_nr in self.sim_numbers:
            self.cvd = self.__values_dict[z_var_name]
            mat_file_obj = Parser_LEDET_Mat(self.base_path, model_name, sim_nr)
            #self.time_data[magnet_label][self.time_name][sim_nr] = mat_file_obj.data_1D(self.td['mat_label'], op=None)
            data = mat_file_obj.data_1D(self.cvd['mat_label'], op=self.cvd['op'])
            max_data = np.max(data)
            z.append(max_data)
        z = np.array(z)
        vmax = z.max()
        levels = np.linspace(z.min(), vmax, 12)

        # plot:
        fig, ax = plt.subplots(figsize=(self.cs['plot_width'], self.cs['plot_height']))

        ax.plot(x, y, 'o', markersize=2, color='grey')
        sc = ax.tricontourf(x, y, z, levels=levels, vmin=z.min(), vmax=vmax)
        #sc = ax.contourf(x, y, z, levels=levels, vmin=z.min(), vmax=vmax)

        offset = 0.1
        x_offset = offset * x.min()
        y_offset = offset * y.min()
        ax.set(xlim=(x.min()-x_offset, x.max()+x_offset), ylim=(y.min()-y_offset, y.max()+y_offset))
        cbar = fig.colorbar(sc)
        cbar.set_label(z_var_name)
        fig.tight_layout()
        plt.show()

    def read_data(self, model_names, model_labels, sim_nr_list_of_lists, values):
        self.names = ''
        self.numbers = ''
        self.data = {}
        self.time_data = {}
        self.values = values
        for magnet_name, magnet_label, sim_nr_list in zip(model_names, model_labels, sim_nr_list_of_lists):
            self.data[magnet_label] = {}
            self.names += f'{magnet_name},'
            for value in values:
                if value == '$T_{max adb}$':
                    self.time_name = 'Time adb'
                else:
                    self.time_name = 'Time'
                self.td = self.__values_dict[self.time_name]
                self.cvd = self.__values_dict[value]
                self.time_data[magnet_label] = {self.time_name: {}}
                self.data[magnet_label][value] = {}
                for sim_nr in sim_nr_list:
                    self.numbers += f'{sim_nr},'
                    mat_file_obj = Parser_LEDET_Mat(self.base_path, magnet_name, sim_nr)
                    self.time_data[magnet_label][self.time_name][sim_nr] = mat_file_obj.data_1D(self.td['mat_label'], op=None)
                    self.data[magnet_label][value][sim_nr] = mat_file_obj.data_1D(self.cvd['mat_label'], op=self.cvd['op'])

    def plot_selected_vs_time(self, use_markers=False, save=False, print_only=False):
        fig, ax = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(self.cs['plot_width'], self.cs['plot_height']))
        markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
        i = 0
        sim_names = {
            1: 'oQH', 2: 'iQH', 3: 'CLIQu', 13: 'CLIQi', 4: 'iQH&CLIQu', 14: 'iQH&CLIQi', 5: 'i&oQH', 6: 'oQH&CLIQu', 16: 'oQH&CLIQi', 7: 'o&iQH&CLIQu', 17: 'o&iQH&CLIQi',
            101: 'oQH', 102: 'iQH', 103: 'CLIQu', 113: 'CLIQi', 104: 'iQH&CLIQu', 114: 'iQH&CLIQi', 105: 'i&oQH', 106: 'oQH&CLIQu', 116: 'oQH&CLIQi', 107: 'o&iQH&CLIQu', 117: 'o&iQH&CLIQi'}

        for magnet_label, magnet_data in self.data.items():
            for value, value_dict in magnet_data.items():
                for sim_nr, sim_data in value_dict.items():
                    if sim_nr>100:
                        leng = 'L_'
                    else:
                        leng = 'S_'
                    if use_markers:     # user
                        marker = markers[i]
                    else:
                        marker = 'None'
                    if len(self.values) == 3:
                        label = f'{magnet_label},{value}:{leng + sim_names[sim_nr]}'
                    else:
                        #label = f'{magnet_label}:{leng + sim_names[sim_nr]}'
                        label = f'{sim_nr}'
                    ax.plot(self.time_data[magnet_label][self.time_name][sim_nr], self.data[magnet_label][value][sim_nr],
                            markevery=20, marker=marker, label=label)
                    i += 1
        ax.tick_params(labelsize=self.cs['font_size'])
        ax.set_xlabel(f"Time (s)", size=self.cs['font_size'])#.set_fontproperties(font)
        if len(self.values) == 3:   # CLIQ currents plot
            value = '$I_{A}, I_{B}, I_{CLIQ}$'
        ax.set_ylabel(f"{value} ({self.cvd['unit']})", size=self.cs['font_size'])#.set_fontproperties(font)
        ymin, ymax = ax.get_ylim()
        if self.cvd['op'] == 'min':
            ax.set_ylim(ymin=ymin, ymax=0)  # set y limit to zero
        elif self.cvd['op'] == 'max':
            ax.set_ylim(ymin=0, ymax=ymax)  # set y limit to zero
        ax.set_xlim(self.td['min'], self.td['max'])
        legend = plt.legend(loc="best", prop={'size': self.cs['font_size']})
        frame = legend.get_frame()  # sets up for color, edge, and transparency
        frame.set_edgecolor('black')  # edge color of legend
        frame.set_alpha(0)  # deals with transparency
        #plt.legend.set_fontproperties(font)
        fig.tight_layout()
        if save:
            out_dir = os.path.join(self.base_path, 'PlotterAnalysis')
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            fig.savefig(os.path.join(out_dir, f'{self.names}_{self.numbers}_{value}.svg'), dpi=300)
            #fig.savefig(os.path.join(out_dir, f'{"+".join(self.magnet_labels_list)}_{value}_{style}_{plot_type}.png'), dpi=300)
        else:
            plt.show()
        plt.close()

    def print_data(self):
        print(self.data)

if __name__ == "__main__":
    base_path = r"D:\tempLEDET\LEDET"   # path to ledet folder
    # model_names_list = [['robust_12T_50_mm_MQXF_cable_5_blocks_V2'], ['robust_12T_50_mm_MQXF_cable_6_blocks_V2'], ['robust_12T_56_mm_MQXF_cable_6_blocks_V2']]
    # model_labels_list = [['50mm,5b'], ['50mm,6b'], ['56mm,6b']]

    model_names_list = [['robust_12T_56_mm_MQXF_cable_6_blocks_V2']]
    model_labels_list = [['50mm,5b']]
    # model_names = ['robust_12T_50_mm_MQXF_cable_6_blocks_V2']
    # model_labels = ['50mm,6b']
    # model_names = ['robust_12T_56_mm_MQXF_cable_6_blocks_V2']
    # model_labels = ['56mm,6b']
    # sim_nr_list_of_lists = [[13, 113], [13, 113], [13, 113]]
    # #sim_nr_list_of_lists = [[3, 103], [3, 103], [3, 103]]
    # sim_nr_list_of_lists = [[3], [3], [3]]
    # sim_nr_list_of_lists = [[3]]
    #sim_nr_list_of_lists = [[3, 13], [3, 13], [3, 13]]
    #sim_nr_list_of_lists = [[13], [13], [13]]

    #sim_nr_list_of_lists = [[1, 2, 3, 13, 4, 14, 5, 6, 16, 7, 17]]
    sim_nr_list_of_lists = [
        #list(range(13001, 13019)),
        #list(range(13101, 13119)),
        #list(range(13201, 13219)),
        #list(range(13301, 13319)),
        #list(range(13401, 13419)),
        #list(range(13501, 13519)),
        # list(range(13601, 13619)),
        # list(range(13701, 13719)),
        # list(range(13801, 13819)),
        # list(range(13901, 13919)),
        # list(range(14001, 14019)),
        # list(range(14101, 14119)),
        # list(range(14201, 14219)),
        # list(range(14301, 14319)),
        # list(range(14401, 14419)),
        # list(range(14501, 14519)),
        # list(range(14601, 14619)),
        # list(range(14701, 14719)),
        # list(range(14801, 14819)),
        list(range(14901, 14919)),
        ]
    #sim_nr_list_of_lists = [[101, 102, 103, 113, 104, 114, 105, 106, 116, 107, 117]]

    #sim_nr_list_of_lists = [[3, 13, 4, 14, 6, 16, 7, 17]]
    #sim_nr_list_of_lists = [[103, 113, 104, 114, 106, 116, 107, 117]]
    #values = ['$I_{A}$', '$I_{B}$', '$I_{CLIQ}$']

    #values = ['$T_{max}$']
    values = ['$T_{max adb}$']
    #values = ['$U_{max}$']
    #values = ['$U_{min}$']
    #values = ['$R_{mag}$']
    #values = ['$I_{A}$']
    #values = ['$I_{CLIQ}$']
    style = 'presentation'


    path_to_sweep_file = r'E:\Python\m12t_r\model_long.csv'
    case = 'CLIQ only'
    #case = 'Inner QH  & CLIQ'
    case = 'Outer QH  & CLIQ'
    # case = 'Outer & Inner QH & CLIQ'

    magnet_name = 'robust_12T_50_mm_MQXF_cable_5_blocks_V2'
    #magnet_name = 'robust_12T_50_mm_MQXF_cable_6_blocks_V2'
    #magnet_name = 'robust_12T_56_mm_MQXF_cable_6_blocks_V2'

    x_var_name = 'Power_Supply.I_initial'
    y_var_name = 'Quench_Protection.CLIQ.C'
    z_var_name = '$T_{max adb}$'
    #z_var_name = '$I_{A}$'
    # z_var_name = '$U_{max}$'
    # z_var_name = '$I_{CLIQ}$'

    pa = PlotterAnalysis(base_path)
    pa.set_plot_style(style)
    # for model_names, model_labels in zip(model_names_list, model_labels_list):
    #     pa.read_data(model_names, model_labels, sim_nr_list_of_lists, values)
    #     pa.plot_selected_vs_time(use_markers=0, save=0)
    pa.read_sweep(path_to_sweep_file, case, x_var_name, y_var_name)
    pa.plot_sweep_2d(magnet_name, z_var_name)
    #pa.print_data()