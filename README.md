# GQF-PYQGIS3
GQF for PYQGIS3

## Introduction
This is a PYQGIS3 ported version of [GQF](https://umep-docs.readthedocs.io/en/latest/processor/Urban%20Energy%20Balance%20GQ.html), which now only works in the python console of QGIS3 (tested with QGIS 3.4 and 3.6.2 under macOS 10.14.4).

## Usage
1. launch QGIS 3 and open its python console.
2. load the script `RunGQF.py`.
3. in `RunGQF.py`, set the path to `GQF` directory:
```
path_GQF = Path('your_path_to/GQF')
```
4. other GQF settings via two namelist files:
   1. `Parameters.nml`: under `GQF_Inputs_1`, details refer to [this page](https://umep-docs.readthedocs.io/en/latest/OtherManuals/GQF_Manual.html#id4).
   2. `DataSources.nml`: under `GQF_Inputs_1`, details refer to [this page](https://umep-docs.readthedocs.io/en/latest/OtherManuals/GQF_Manual.html#data-sources-file).
5. execute `RunGQF.py`.