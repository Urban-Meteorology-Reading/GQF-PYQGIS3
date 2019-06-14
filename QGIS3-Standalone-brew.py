
import sys,os
from pathlib import Path

# set up QGIS to run in non-GUI mode
path_QGIS_app = Path('/usr/local/opt/osgeo-qgis/QGIS.app')
path_QGIS3 = path_QGIS_app/'Contents/MacOS/../Resources'
path_QGIS3_lib = path_QGIS3/'python'
path_QGIS3_plugin = path_QGIS3_lib/'plugins'
sys.path.insert(0,path_QGIS3_lib.as_posix())
sys.path.insert(0,path_QGIS3_plugin.as_posix())

# Define Qt5 plugin path since Qt5 can't find it
# http://osgeo-org.1560.x6.nabble.com/QGIS-3-Standalone-Python-Script-tp5373335p5373573.html
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = (path_QGIS_app/'Contents/PlugIns').as_posix()

# initialise QGIS
from qgis.core import *
QgsApplication.setPrefixPath((path_QGIS_app/'Contents/MacOs').as_posix(), True)
app = QgsApplication([], False)
app.initQgis()


# initialise `processing`
import processing
from processing.core.Processing import Processing
Processing.initialize()

# load native algorithms for processing
from qgis.analysis import QgsNativeAlgorithms
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())

# print(QgsApplication.showSettings())

# set path to run GQF
path_GQF = Path('/Users/sunt05/Dropbox/6.Repos/GQF-PYQGIS3')  # /Users/suegrimmond/Documents/IQF/GQF-PYQGIS3
sys.path.append(path_GQF.as_posix())
os.chdir(path_GQF)
print(os.getcwd())

from GQF.Config import Config
from GQF.GreaterQF import Model
import random
import string

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

rand_file = random_generator()
# rand_file='QOIA4W'

config = Config()
b = {}
b['all_qf'] = 1
b['sensible_qf'] = 1
b['latent_qf'] = 1
b['wastewater_qf'] = 0
b['start_dates'] = '2015-01-01'
b['end_dates'] = '2015-01-02'
config.loadFromDictionary(b)
# config.saveNamelist(f'./SampleRun/history-runs/{rand_file}.nml')



model = Model()

# model.setParameters('./GQF_Inputs/1/Parameters.nml')
# model.setParameters('./GQF_Inputs/centralLondon/Parameters.nml')
model.setParameters('./GQF_Inputs/smalltestarea/Parameters.nml')

# model.setDataSources('./GQF_Inputs/1/DataSources.nml')
# model.setDataSources('./GQF_Inputs/centralLondon/DataSources.nml')
model.setDataSources('./GQF_Inputs/smalltestarea/DataSources.nml')

model.setConfig(config)

# rand_file='8RYVBK'

model.setOutputDir(f'./SampleRun/{rand_file}/')

model.processInputData()
model.setPreProcessedInputFolder(f'./SampleRun/{rand_file}/DownscaledData/')

model.run()

# finalise QGIS app
app.exitQgis()

print('GQF run finished!')


# df_res.describe()

# app.exitQgis()
