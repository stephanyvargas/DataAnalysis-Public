import pandas as pd
import sys


board = sys.argv[1]
filename = '/home/stephy/ICECUBE/undershoot/20200609/Results_droop_undershoot.h5'
df = pd.read_hdf(filename)
erase_board = f'HVB_{board}'
df.drop(erase_board, level=0, inplace = True)
df.to_hdf(filename, key='new_df', mode='w')
