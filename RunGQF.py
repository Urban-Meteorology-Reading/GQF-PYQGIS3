
import sys
from pathlib import Path
# set path to run GQF
path_GQF = Path('/Users/sunt05/Dropbox/6.Repos/GQF-PYQGIS3')
sys.path.append(path_GQF.as_posix())



import os
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
model.setParameters('./GQF_Inputs/centralLondon/Parameters.nml')

# model.setDataSources('./GQF_Inputs/1/DataSources.nml')
model.setDataSources('./GQF_Inputs/centralLondon/DataSources.nml')

model.setConfig(config)

model.setOutputDir(f'./SampleRun/{rand_file}/')

model.processInputData()
model.setPreProcessedInputFolder(f'./SampleRun/{rand_file}/DownscaledData/')

model.run()



