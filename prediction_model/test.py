import numpy as np
import os
import sys
os.chdir(sys.path[0])


a = np.load(os.path.join('dataset', 'prediction_model_formula12', 'test', '100_blc_138.npy'))
print(a[0])