from pydantic import BaseModel


class DataSettings(BaseModel):
    """
        Dataclass of settings for STEAM analyses
        This will be populated either form a local settings file (if flag_permanent_settings=False)
        or from the keys in the input analysis file (if flag_permanent_settings=True)
    """
    comsolexe_path:        str = None  # full path to comsol.exe, only COMSOL53a is supported
    JAVA_jdk_path:         str = None  # full path to folder with java jdk
    CFunLibPath:           str = None  # full path to dll files with material properties
    ANSYS_path:            str = None  # full path to ANSYS executable
    COSIM_path:            str = None  # full path to STEAM-COSIM executable
    Dakota_path:           str = None  # full path to Dakota executable
    FiQuS_path:            str = None  # Full path to FiQuS repository (FiQuS or FiQuS-dev should work)
    GetDP_path:            str = None  # Full path to getdp.exe (OneLab or CERN builds should work)
    LEDET_path:            str = None  # full path to STEAM-LEDET executable
    ProteCCT_path:         str = None  # full path to STEAM-ProteCCT executable
    PSPICE_path:           str = None  # full path to PSPICE executable
    PyBBQ_path:            str = None  #
    XYCE_path:             str = None  #
    PSPICE_library_path:   str = None  #
    local_ANSYS_folder:    str = None  # full path to local ANSYS folder
    local_COSIM_folder:    str = None  # full path to local COSIM folder
    local_Dakota_path:     str = None  # full path to local Dakota folder
    local_FiQuS_folder:    str = None  # full path to local FiQuS folder
    local_LEDET_folder:    str = None  # full path to local LEDET folder
    local_ProteCCT_folder: str = None  # full path to local ProteCCT folder
    local_PSPICE_folder:   str = None  # full path to local PSPICE folder
    local_PyBBQ_folder:    str = None  # full path to local PyBBQ folder
    local_SIGMA_folder:    str = None  # full path to local SIGMA folder
    local_XYCE_folder:     str = None  # full path to local PSPICE folder
    MTF_credentials_path:  str = None  # full path to the txt file containing the credentials for MTF login
