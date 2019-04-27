import sys
from pathlib import Path
# set path to run GQF
path_GQF = Path('/Users/sunt05/Dropbox/6.Repos/GQF-PYQGIS3/GQF')

#sys.path.append('/Applications/QGIS3.app/Contents/Resources/python/plugins')
print(path_GQF.exists())
print((path_GQF/'DataManagement').exists())
sys.path.append(path_GQF)
sys.path.append(path_GQF/'DataManagement')


import os
os.chdir(path_GQF)
print(os.getcwd())


from Config import Config
from GreaterQF import Model
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
config.saveNamelist(f'./DataManagement/history-runs/{rand_file}.nml')

model = Model()

model.setParameters('./GQF_Inputs_1/Parameters.nml')

model.setDataSources('./GQF_Inputs_1/DataSources.nml')

model.setConfig(config)

model.setOutputDir(f'./SampleRun/{rand_file}/')

model.processInputData()
model.setPreProcessedInputFolder(f'./SampleRun/{rand_file}/DownscaledData/')
# model.setPreProcessedInputFolder(f'./SampleRun/2C3V2J/DownscaledData/')

model.run()



