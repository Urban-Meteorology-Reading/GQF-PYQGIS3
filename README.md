# GQF-PYQGIS3
GQF for PYQGIS3

## Introduction
This is a PYQGIS3 ported version of [GQF](https://umep-docs.readthedocs.io/en/latest/processor/Urban%20Energy%20Balance%20GQ.html), which now only works in the python console of QGIS3.

NOTE: tested with **QGIS 3.4 and 3.6.2 under macOS 10.14.4**.

## Usage

### within QGIS console
1. launch QGIS 3 and open its python console.
2. load the script `RunGQF.py`.
3. in `RunGQF.py`, set the path to `GQF` directory:
```
path_GQF = Path('your_path_to/GQF')
```
4. set other GQF configurations via the two namelist files:
   1. `Parameters.nml`: under `GQF_Inputs_1`, details refer to [this page](https://umep-docs.readthedocs.io/en/latest/OtherManuals/GQF_Manual.html#id4).
   2. `DataSources.nml`: under `GQF_Inputs_1`, details refer to [this page](https://umep-docs.readthedocs.io/en/latest/OtherManuals/GQF_Manual.html#data-sources-file).
5. execute `RunGQF.py`.

### standalone Python environment without QGIS GUI
*Note: this approach is only tested with the osgeo4mac distribution of QGIS3; but should similarly work with other configurations.*

1. install [`osgeo4mac`](https://github.com/OSGeo/homebrew-osgeo4mac)-brewed QGIS (for sure you need [`homebrew`](https://brew.sh) first):
```shell
brew tap osgeo/osgeo4mac
brew install osgeo-qgis
```

2. run `QGIS3-Standalone-brew.py` with the `homebrew`-ed `python3`:
```
python3 QGIS3-Standalone-brew.py
```
see `QGIS3-Standalone-brew.py` for configuration details.

Please [report your issues](https://github.com/Urban-Meteorology-Reading/GQF-PYQGIS3/issues/new) if any configuration steps missed here.