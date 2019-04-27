import sys
from pathlib import Path
# set path to run GQF
path_GQF = Path('/Users/sunt05/Dropbox/6.Repos/GQF-PYQGIS3')
# path_GQF_data = path_GQF/'DataManagement'
# path_QGIS3 = Path('/Applications/QGIS3.6.app/Contents/MacOS/../Resources')
# path_QGIS3_lib = (path_QGIS3/'python')
# path_QGIS3_plugin = (path_QGIS3_lib/'plugins')
# sys.path.append(path_QGIS3_lib.as_posix())
# sys.path.append(path_QGIS3_plugin.as_posix())
# sys.path.append(path_QGIS3/'python/plugins')
# sys.path.append('/Applications/QGIS3.6.app/Contents/MacOS/lib/')
sys.path.append(path_GQF.as_posix())


# print(sys.path)


import os
os.chdir(path_GQF)
print(os.getcwd())


from GQF.Config import Config
from GQF.GreaterQF import Model
import random
import string

#print(sys.path)



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
config.saveNamelist(f'./SampleRun/history-runs/{rand_file}.nml')

model = Model()

model.setParameters('./GQF_Inputs_1/Parameters.nml')

model.setDataSources('./GQF_Inputs_1/DataSources.nml')

model.setConfig(config)

model.setOutputDir(f'./SampleRun/{rand_file}/')

model.processInputData()
model.setPreProcessedInputFolder(f'./SampleRun/{rand_file}/DownscaledData/')
# model.setPreProcessedInputFolder(f'./SampleRun/2C3V2J/DownscaledData/')

model.run()



