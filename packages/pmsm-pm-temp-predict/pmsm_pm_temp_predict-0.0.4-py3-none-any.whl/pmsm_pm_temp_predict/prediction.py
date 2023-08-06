import os
import pkg_resources
import pandas as pd
import numpy as np
from pickle import load
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from filesplit.merge import Merge

def temp_predict(u_q, u_d, i_d, i_q, coolant, stator_winding):
#    this_dir, this_filename = os.path.split(__file__)
#    merge = Merge(inputdir=os.path.join(this_dir, "data", "split"), outputdir=os.path.join(this_dir, "data"), outputfilename='fm.sav')
#    merge.merge()
#
#    DATA_PATH = os.path.join(this_dir, "data", "fm.sav")
#    model = load(open(DATA_PATH, 'rb'))
#
#    DATA_PATH = os.path.join(this_dir, "data", "minmax_scaler.pkl")
#    minmax_scaler = load(open(DATA_PATH, 'rb'))
#
#    DATA_PATH = os.path.join(this_dir, "data", "std_scaler.pkl")
#    std_scaler = load(open(DATA_PATH, 'rb'))
#
#    minmax_scaled = minmax_scaler.transform(pd.DataFrame({'coolant': [coolant], 'stator_winding': [stator_winding]}))
#    std_scaled = std_scaler.transform(pd.DataFrame({'u_q': [u_q], 'u_d': [u_d], 'i_d': [i_d], 'i_q': [i_q]}))
#
#    comb_scaled = np.concatenate((std_scaled, minmax_scaled), axis=1)
#
#    ds_scaled = pd.DataFrame(comb_scaled, columns=['u_q', 'u_d', 'i_d', 'i_q', 'coolant', 'stator_winding'])
#
#    result = model.predict(ds_scaled)
#
#    return float(result)
#    this_dir, this_filename = os.path.split(__file__)
#    merge = Merge(inputdir=os.path.join(this_dir, "data", "split"), outputdir=os.path.join(this_dir, "data"), outputfilename='fm.sav')
#    merge.merge()
    this_dir, this_filename = os.path.split(__file__)
    DATA_PATH = os.path.join(this_dir, "data", "minmax_scaler.pkl")
    minmax_scaler = load(open(DATA_PATH, 'rb'))

    DATA_PATH = os.path.join(this_dir, "data", "std_scaler.pkl")
    std_scaler = load(open(DATA_PATH, 'rb'))

    minmax_scaled = minmax_scaler.transform(pd.DataFrame({'coolant': [coolant], 'stator_winding': [stator_winding]}))
    std_scaled = std_scaler.transform(pd.DataFrame({'u_q': [u_q], 'u_d': [u_d], 'i_d': [i_d], 'i_q': [i_q]}))

    comb_scaled = np.concatenate((std_scaled, minmax_scaled), axis=1)

    ds_scaled = pd.DataFrame(comb_scaled, columns=['u_q', 'u_d', 'i_d', 'i_q', 'coolant', 'stator_winding'])

    return 1