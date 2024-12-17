# DFTB+ Lattice Optimization Tool
## Overview
The dftb_lattice_opt_tool is a Python script that simplifies the process of batch lattice optimization calculations using the DFTB+ (Density-Functional Tight-Binding) software. It automates the generation of hierarchical directories, assignment of lattice parameters, and creation of DFTB+ input files (.hsd) for multiple structures.
Key Features

- Pre-set angular momentum values for common chemical elements
- Ability to add or remove angular momentum for specific elements
- Automatic generation of directories based on the specified gradient and step length
- Assignment of geometry files (.gen) to the appropriate directories
- Generation and assignment of DFTB+ input files (.hsd) with the correct lattice parameters
- Copying of submission scripts (e.g., .sh) to the generated directories

## Usage
```python
###Import the necessary modules:

import numpy as np
from ase import io
import ase
import os
from ase.geometry.analysis import Analysis
import shutil
import pandas as pd
import re

###Initialize the lattice_opt class:
lo = lattice_opt()

###Set the required parameters:
lo.save_parameters(
    gradient_number=5,
    step_length=0.01,
    folder_name="lattice_optimization",
    folder_path="/path/to/output/directory",
    output="dftb_in.gen",
    subdir_layernum=2
)

###Prepare the angular momentum dictionary:
angular_m_dic = lo.pre_set_momenta()

###Read the input geometry files:
geo_path_list = lo.read_path("/path/to/input/directory")

###Generate the geometry files with varying lattice parameters:
geo_collect_all = []
for geo_path in geo_path_list:
    geo = io.read(geo_path)
    geo_collect = lo.lattice_sep(geo)
    geo_collect_all.append(geo_collect)

###Create the directories and assign the geometry files:
lo.folders_make(geo_path_list)
lo.assign_geo(geo_collect_all, geo_path_list)

###Generate and assign the DFTB+ input files (.hsd):
hsd_collect = lo.generate_hsd(
    geo_list=geo_collect_all,
    path_hsd_template="/path/to/hsd/template.hsd",
    angular_m_dic=angular_m_dic,
    layer_sep_index=[None, 10, 20]
)
lo.assign_hsd(geo_collect_all, hsd_collect, geo_path_list)

###Assign the submission scripts (e.g., .sh) to the directories:
lo.assign_submit(geo_collect_all, "/path/to/submit/template.sh", geo_path_list)
```

## Customization

- The pre_set_momenta() method provides a dictionary of pre-defined angular momentum values for common elements. You can use the add_momenta() and delete_momenta() methods to customize the angular momentum settings as needed.
- The save_parameters() method allows you to set the specific parameters for your lattice optimization, such as the gradient number, step length, output directory, and more.
- The script assumes the existence of a DFTB+ input file (.hsd) template. You can modify the generate_hsd() method to generate the input files according to your specific requirements.
- The assign_submit() method copies a submission script (e.g., .sh) to the generated directories. You can customize the submission script as needed for your computing environment.

## Contributing
Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please feel free to open a new issue or submit a pull request.

## License
This project is licensed under the MIT License.
