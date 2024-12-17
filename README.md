# DFTB+ Lattice Optimization Tool
## Overview
The dftb_lattice_opt_tool is a Python script that simplifies the process of batch lattice optimization calculations using the DFTB+ (Density-Functional Tight-Binding) software. It automates the generation of hierarchical directories, assignment of lattice parameters, and creation of DFTB+ input files (.hsd) for multiple structures.
Key Features

-Pre-set angular momentum values for common chemical elements
-Ability to add or remove angular momentum for specific elements
-Automatic generation of directories based on the specified gradient and step length
-Assignment of geometry files (.gen) to the appropriate directories
-Generation and assignment of DFTB+ input files (.hsd) with the correct lattice parameters
-Copying of submission scripts (e.g., .sh) to the generated directories

## Usage
