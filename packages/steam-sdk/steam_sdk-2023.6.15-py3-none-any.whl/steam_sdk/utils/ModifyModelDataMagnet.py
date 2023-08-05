import os
from pathlib import Path
import yaml
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from steam_sdk.parsers.ParserYAML import dict_to_yaml

if __name__ == "__main__":
    path_models = Path.joinpath(Path(__file__).parent.parent.parent, 'C:\\Users\emm\cernbox\SWAN_projects\steam_models\magnets')
    path_models = Path.joinpath(Path(__file__).parent.parent.parent, r'C:\Users\jlidholm\cernbox\Git-projects\steam_models\magnets')
    #path_models = Path.joinpath(Path(__file__).parent.parent.parent, 'tests/builders/model_library/magnets')
    models = [x.parts[-1] for x in Path(path_models).iterdir() if x.is_dir()]
    #models = ['MQXA']

    for mm in models:
        # Read file
        file_model_data = Path.joinpath(path_models, mm, 'input', 'modelData_' + mm + '.yaml')
        if os.path.isfile(file_model_data):
            # Load yaml keys into DataAnalysis dataclass
            with open(file_model_data, "r") as stream:
                dictionary_yaml = yaml.safe_load(stream)
                model_data = DataModelMagnet(**dictionary_yaml)  # TODO here we're ignoring any comment present in the file and forgetting about them
            print(f'Read file: {file_model_data}')

            # Note: Obsolete keys in yaml file will automatically be deleted
            # Note: New keys added to DataModelMagnet will automatically be added to the yaml file (UNLESS A VALUE IS ASSIGNED BELOW, THEIR VALUES WILL BE INITIALIZED TO DEFAULT)

            # Example to assign value to new keys in model data
            # model_data.Options_LEDET.magnet_inductance.flag_calculate_inductance = True

            # Example to change positions of key keeping its value (IF THIS IS NOT DONE THE INFOMRATION IN THE ORIGINAL YAML FILE WILL BE LOST!)
            # Note: The following will raise an exception if the keys do not exist in the original yaml file
            # model_data.Options_LEDET.magnet_inductance.LUT_DifferentialInductance_current = dictionary_yaml['GeneralParameters']['magnet_inductance']['fL_I']
            # model_data.Options_LEDET.magnet_inductance.LUT_DifferentialInductance_inductance = dictionary_yaml['GeneralParameters']['magnet_inductance']['fL_L']
            #
            # model_data.Options_LEDET.heat_exchange.heat_exchange_max_distance = dictionary_yaml['CoilWindings']['heat_exchange']['heat_exchange_max_distance']
            # model_data.Options_LEDET.heat_exchange.iContactAlongWidth_pairs_to_add = dictionary_yaml['CoilWindings']['heat_exchange']['iContactAlongWidth_pairs_to_add']
            # model_data.Options_LEDET.heat_exchange.iContactAlongWidth_pairs_to_remove = dictionary_yaml['CoilWindings']['heat_exchange']['iContactAlongWidth_pairs_to_remove']
            # model_data.Options_LEDET.heat_exchange.iContactAlongHeight_pairs_to_add = dictionary_yaml['CoilWindings']['heat_exchange']['iContactAlongHeight_pairs_to_add']
            # model_data.Options_LEDET.heat_exchange.iContactAlongHeight_pairs_to_remove = dictionary_yaml['CoilWindings']['heat_exchange']['iContactAlongHeight_pairs_to_remove']
            # model_data.Options_LEDET.heat_exchange.th_insulationBetweenLayers = dictionary_yaml['CoilWindings']['heat_exchange']['th_insulationBetweenLayers']
            #
            # model_data.Options_LEDET.conductor_geometry_used_for_ISCL.alphaDEG_ht = dictionary_yaml['CoilWindings']['multipole']['alphaDEG_ht']
            # model_data.Options_LEDET.conductor_geometry_used_for_ISCL.rotation_ht = dictionary_yaml['CoilWindings']['multipole']['rotation_ht']
            # model_data.Options_LEDET.conductor_geometry_used_for_ISCL.mirror_ht = dictionary_yaml['CoilWindings']['multipole']['mirror_ht']
            # model_data.Options_LEDET.conductor_geometry_used_for_ISCL.mirrorY_ht = dictionary_yaml['CoilWindings']['multipole']['mirrorY_ht']
            #model_data.Quench_Protection.Quench_Heaters.turns_sides = ["O"] * len(model_data.Quench_Protection.Quench_Heaters.iQH_toHalfTurn_From)
            model_data.Quench_Protection.Quench_Heaters.N_strips = len(model_data.Quench_Protection.Quench_Heaters.t_trigger)



            model_data.Options_SIGMA.time_vector_solution.time_step = [[0.0, 0.001, 0.05], [0.05, 0.01, 0.25]]

            model_data.Options_SIGMA.quench_initialization.num_qh_div = [10]*len(model_data.Quench_Protection.Quench_Heaters.t_trigger)
            model_data.Options_SIGMA.quench_initialization.quench_init_heat = 500000.0
            model_data.Options_SIGMA.quench_initialization.quench_init_HT = ["CO_P0_W0_B0_HT0"]
            model_data.Options_SIGMA.quench_initialization.quench_stop_temp = 10



            model_data.Options_SIGMA.postprocessing.out_2D_at_points.variables = ["mf.normB", "mf.Bx", "mf.By"]
            model_data.Options_SIGMA.postprocessing.out_2D_at_points.time = [[0.0, 0.01, 0.02], [0.0, 0.15, 0.2], [0.0, 0.15, 0.2]]
            model_data.Options_SIGMA.postprocessing.out_2D_at_points.map2d =model_data.Sources.magnetic_field_fromROXIE

            model_data.Options_SIGMA.postprocessing.out_1D_vs_times.variables =["I", "QHComp.ht2.QH_1_Coil_Temperature.Tave", "QHComp.ht2.QH_2_Coil_Temperature.Tave"]
            model_data.Options_SIGMA.postprocessing.out_1D_vs_times.time = [[0.0, 0.01, 0.02], [0.0, 0.15, 0.2], [0.0, 0.15, 0.2]]
            model_data.Options_SIGMA.postprocessing.out_1D_vs_all_times.variables =["I", "QHComp.ht2.QH_1_Coil_Temperature.Tave", "QHComp.ht2.QH_2_Coil_Temperature.Tave"]
            model_data.Options_SIGMA.quench_heaters.th_coils = [0]*model_data.Quench_Protection.Quench_Heaters.N_strips

            # Check and reformat the key values
            model_data = DataModelMagnet(**model_data.dict())

            # Write file
            # file_model_data_output = Path.joinpath(path_models, mm, 'input', 'modelData_' + mm + '_MODIFIED.yaml')  # use this line if you wish to test the results of this script
            file_model_data_output = file_model_data  # use this line if you wish to really update all yaml input files
            all_data_dict = {**model_data.dict()}
            dict_to_yaml(all_data_dict, file_model_data_output, list_exceptions=['Conductors'])
            print(f'Written file: {file_model_data_output}')
        else:
            print(f'WARNING: File {file_model_data} not found.')
