import sys
import importlib

if sys.platform == 'darwin':
    import_path = 'metalayer.macos'
else:
    raise NotImplementedError('Unsupported platform')

battery = importlib.import_module(import_path + '.battery')
capture = importlib.import_module(import_path + '.capture')
utils = importlib.import_module(import_path + '.utils')
