from Stock_Prediction_Base import SP_Paras
from Stock_Prediction_Model_Stateless_LSTM import rnn_lstm_classification
from Stock_Prediction_Model_DBN import dbn_classification
from Stock_Prediction_Model_Random_Forrest import random_forrest_classification
from Stock_Prediction_Model_Random_Forrest_1 import random_forrest_regression
from Stock_Prediction_Model_XgBoost import xgboost_classification
from Stock_Prediction_Recommand_System import recommand_system


import sys, os, time, datetime, warnings, configparser
import tensorflow as tf
import pandas as pd
from keras import backend

cur_path = os.path.dirname(os.path.abspath(__file__))
for _ in range(2):
    root_path = cur_path[0:cur_path.rfind('/', 0, len(cur_path))]
    cur_path = root_path
sys.path.append(root_path + "/" + 'Source/FetchData/')
sys.path.append(root_path + "/" + 'Source/DataBase/')
from Fetch_Data_Stock_US_Daily import updateStockData_US_Daily, getStocksList_US
from Fetch_Data_Stock_CHN_StockList import getStocksList_CHN


def run_lstm_classification(root_path, train_symbols, predict_symbols, need_training, need_plot_training_diagram, need_predict):
    paras = SP_Paras('lstm', root_path, train_symbols, predict_symbols)
    paras.save = True
    paras.load = False
    paras.plot = need_plot_training_diagram
    # 0_index: no norm   1_index: standard norm   2_index: minmax norm   3_index: zscore norm
    paras.features = {'0_0':['frac_change', 'frac_high', 'frac_low'], 
                      '0_0':['c_2_o', 'h_2_o', 'l_2_o', 'c_2_h', 'h_2_l', 'vol'],
                      '2_0':['buy_amount', 'sell_amount', 'even_amount'],
                      '2_0':['buy_volume', 'sell_volume', 'even_volume'], 
                      '2_0':['buy_max', 'buy_min', 'buy_average', 'sell_max', 'sell_min', 'sell_average', 'even_max', 'even_min', 'even_average']} 
    #paras.features = [['top', 'middle', 'bottom'], ['volume'], ['vol_stat'], ['close_-5_r', 'close_-10_r', 'close_-20_r', 'close_-60_r']]
    #paras.window_len = [2, 4, 9]
    paras.window_len = [120]
    paras.pred_len = 1
    paras.valid_len = 20
    paras.start_date = '2016-11-01'
    paras.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    paras.verbose = 1
    
    paras.batch_size = 64
    paras.epoch = 100
    #paras.model['hidden_layers'] = [[256, 128, 64], [256, 128, 64], [256, 128, 64]]
    paras.model['hidden_layers'] = [[240, 120, 60]]
    #paras.model['dropout'] = [[0.7, 0.5, 0.3], [0.6, 0.5, 0.4], [0.6, 0.5, 0.4]]
    paras.model['dropout'] = [[0.7, 0.5, 0.3]]
    #paras.model['activation'] = [['relu', 'relu', 'relu'], ['relu', 'relu', 'relu'], ['relu', 'relu', 'relu']]
    paras.model['activation'] = [['relu', 'relu', 'relu']]
    #paras.model['optimizer'] = ['adam', 'adam', 'adam']
    paras.model['optimizer'] = ['adam']

    paras.out_class_type = 'classification'
    paras.n_out_class = 7  # ignore for regression
    paras.model['out_layer'] = paras.n_out_class
    paras.model['loss'] = 'categorical_crossentropy'
    paras.model['out_activation'] = 'softmax'

    # run
    lstm_cla = rnn_lstm_classification(paras)
    lstm_cla.run(need_training, need_predict)
    return paras


def run_dbn_classification(root_path, train_symbols, predict_symbols, need_training, need_plot_training_diagram, need_predict):
    paras = SP_Paras('dbn', root_path, train_symbols, predict_symbols)
    paras.save = True
    paras.load = False
    paras.plot = need_plot_training_diagram
    # 0_index: no norm   1_index: standard norm   2_index: minmax norm   3_index: zscore norm
    paras.features = {'0_0':['frac_change', 'frac_high', 'frac_low'], 
                      '3_0':['volume']} 
    #paras.window_len = [2, 4, 9]
    paras.window_len = [2]
    paras.pred_len = 1
    paras.valid_len = 20
    paras.start_date = '2016-01-03'
    paras.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    paras.verbose = 1

    paras.batch_size = 64
    paras.epoch = 100
    #paras.model['hidden_layers'] = [[256, 128, 64], [256, 128, 64], [256, 128, 64]]
    paras.model['hidden_layers'] = [[256, 128, 64]]
    #paras.model['dropout'] = [[0.7, 0.5, 0.3], [0.6, 0.5, 0.4], [0.6, 0.5, 0.4]]
    paras.model['dropout'] = [0.2]
    #paras.model['activation'] = [['relu', 'relu', 'relu'], ['relu', 'relu', 'relu'], ['relu', 'relu', 'relu']]
    paras.model['activation'] = ['relu']
    #paras.model['optimizer'] = ['adam', 'adam', 'adam']
    paras.model['optimizer'] = ['adam']

    paras.out_class_type = 'classification'
    paras.n_out_class = 7  # ignore for regression
    paras.model['out_layer'] = paras.n_out_class
    paras.model['loss'] = 'categorical_crossentropy'
    paras.model['out_activation'] = 'softmax'

    # run
    dbn_cla = dbn_classification(paras)
    dbn_cla.run(need_training, need_predict)
    return paras


def run_rf_classification(root_path, train_symbols, predict_symbols, need_training, need_plot_training_diagram, need_predict):
    paras = SP_Paras('randomForrest', root_path, train_symbols, predict_symbols)
    paras.save = True
    paras.load = False
    paras.plot = need_plot_training_diagram
    # 0_index: no norm   1_index: standard norm   2_index: minmax norm   3_index: zscore norm
    paras.features = {#'0_0':['frac_change', 'frac_high', 'frac_low'], 
                      #'0_0':['rsi_7', 'rsi_14', 'rsi_21', 'kdjk_9', 'kdjk_14', 'wr_9', 
                      #       'wr_14', 'close_-5_r', 'close_-10_r', 'close_-20_r']
                      '0_0':['c_2_o', 'h_2_o', 'l_2_o', 'c_2_h', 'h_2_l', 'vol']
                      #'3_0':['volume']
                     } 
                      
    #paras.window_len = [5, 10, 20]
    paras.window_len = [0]
    paras.pred_len = 1
    paras.valid_len = 20
    paras.start_date = '2016-01-03'
    paras.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    paras.verbose = 0

    # paras.tree_min = [10, 22, 46] # times 16x = trees
    # paras.tree_max = [12, 24, 48] # times 16x = trees
    # paras.feature_min = np.array(paras.window_len) * paras.n_features
    # paras.feature_max = np.array(paras.window_len) * paras.n_features
    # paras.window_min = 1
    # paras.window_max = 1

    paras.tree_min = [1] # times 16x = trees
    paras.tree_max = [10] # times 16x = trees
    paras.feature_min = [1]
    paras.feature_max = [paras.n_features]
    paras.window_min = 44
    paras.window_max = 44

    paras.out_class_type = 'classification'
    paras.n_out_class = 7  # ignore for regression

    # run
    rf_cla = random_forrest_classification(paras)
    rf_cla.run(need_training, need_predict)
    return paras

def run_rf_regression(root_path, train_symbols, predict_symbols, need_training, need_plot_training_diagram, need_predict):
    paras = SP_Paras('randomForrest', root_path, train_symbols, predict_symbols)
    paras.save = True
    paras.load = False
    paras.plot = need_plot_training_diagram
    # 0_index: no norm   1_index: standard norm   2_index: minmax norm   3_index: zscore norm
    paras.features = {#'0_0':['frac_change', 'frac_high', 'frac_low'], 
                      #'0_0':['rsi_7', 'rsi_14', 'rsi_21', 'kdjk_9', 'kdjk_14', 'wr_9', 
                      #       'wr_14', 'close_-5_r', 'close_-10_r', 'close_-20_r']
                      '0_0':['c_2_o', 'h_2_o', 'l_2_o', 'c_2_h', 'h_2_l', 'vol']
                      #'3_0':['volume']
                     } 
                      
    #paras.window_len = [5, 10, 20]
    paras.window_len = [0]
    paras.pred_len = 1
    paras.valid_len = 20
    paras.start_date = '2016-01-03'
    paras.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    paras.verbose = 0

    # paras.tree_min = [10, 22, 46] # times 16x = trees
    # paras.tree_max = [12, 24, 48] # times 16x = trees
    # paras.feature_min = np.array(paras.window_len) * paras.n_features
    # paras.feature_max = np.array(paras.window_len) * paras.n_features
    # paras.window_min = 1
    # paras.window_max = 1

    paras.tree_min = [1] # times 16x = trees
    paras.tree_max = [10] # times 16x = trees
    paras.feature_min = [1]
    paras.feature_max = [paras.n_features]
    paras.window_min = 44
    paras.window_max = 44

    paras.out_class_type = 'regression'
    paras.n_out_class = 7  # ignore for regression

    # run
    rf_cla = random_forrest_regression(paras)
    rf_cla.run(need_training, need_predict)
    return paras

def run_recommand_system(root_path, train_symbols, predict_symbols, need_training, need_plot_training_diagram, need_predict):
    paras = SP_Paras('recommandSystem', root_path, train_symbols, predict_symbols)
    paras.save = True
    paras.load = False
    paras.plot = need_plot_training_diagram
    paras.window_len = [3, 5, 7]
    paras.pred_len = 1
    paras.valid_len = 20
    paras.start_date = '2016-01-03'
    paras.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    paras.verbose = 0
    paras.epoch = 200

    paras.out_class_type = 'classification'
    paras.n_out_class = 2  # ignore for regression

    # run
    rs = recommand_system(paras)
    rs.run(need_training, need_predict)


def run_xgboost_classification(root_path, train_symbols, predict_symbols, need_training, need_plot_training_diagram, need_predict):
    paras = SP_Paras('xgboost', root_path, train_symbols, predict_symbols)
    paras.save = True
    paras.load = False
    paras.run_hyperopt = True
    paras.plot = need_plot_training_diagram
    # 0_index: no norm   1_index: standard norm   2_index: minmax norm   3_index: zscore norm
    paras.features = {#'0_0':['frac_change', 'frac_high', 'frac_low'], 
                      '0_0':['c_2_o', 'h_2_o', 'l_2_o', 'c_2_h', 'h_2_l', 'vol'],
                      '1_0':['buy_amount', 'sell_amount', 'even_amount'],
                      '1_0':['buy_volume', 'sell_volume', 'even_volume'], 
                      '1_0':['buy_max', 'buy_min', 'buy_average', 'sell_max', 'sell_min', 'sell_average', 'even_max', 'even_min', 'even_average']} 
    
    paras.window_len = [3]
    paras.pred_len = 1
    paras.valid_len = 20
    paras.start_date = '2016-11-01'
    paras.end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    paras.verbose = 1
    
    paras.batch_size = 64
    paras.epoch = 100
    
    paras.out_class_type = 'classification'
    paras.n_out_class = 7  # ignore for regression
    paras.model['out_layer'] = paras.n_out_class
    paras.model['loss'] = 'categorical_crossentropy'
    paras.model['out_activation'] = 'softmax'

    from hyperopt import hp
    paras.hyper_opt = {"max_depth"        :hp.randint("max_depth",       10),
                       "n_estimators"     :hp.randint("n_estimators",    20),  #[0,1,2,3,4,5] -> [50,]
                       "gamma"            :hp.randint("gamma",            4),  #0-0.4
                       "learning_rate"    :hp.randint("learning_rate",    6),  #[0,1,2,3,4,5] -> 0.05,0.06
                       "subsample"        :hp.randint("subsample",        4),  #[0,1,2,3] -> [0.7,0.8,0.9,1.0]
                       "min_child_weight" :hp.randint("min_child_weight", 5), 
        }

    # run
    xgboost_cla = xgboost_classification(paras)
    xgboost_cla.run(need_training, need_predict)
    return paras


if __name__ == "__main__":
    pd.set_option('precision', 3)
    pd.set_option('display.width',1000)
    warnings.filterwarnings('ignore', category=pd.io.pytables.PerformanceWarning)
    tf.logging.set_verbosity(tf.logging.ERROR)
    
    

    predict_symbols = ['AMD', 'WDC', 'SINA', 'WB', 'CTRP', 'NTES', 'ATVI', 'FB', 'GLUU', 'NVDA', 'NFLX', 
                       'MRVL', 'SMCI', 'JD', 'INTC', 'AMZN', 'BIDU', 'BGNE', 'QIWI', 'MOMO', 'YY']

    now = datetime.datetime.now().strftime("%Y-%m-%d")

    config = configparser.ConfigParser()
    config.read(root_path + "/" + "config.ini")
    storeType = int(config.get('Setting', 'StoreType'))

    # if storeType == 1:
    #     from Start_DB_Server import StartServer, ShutdownServer
    #     # start database server (async)
    #     thread = StartServer(root_path)
        
    #     # wait for db start, the standard procedure should listen to 
    #     # the completed event of function "StartServer"
    #     time.sleep(5)

    #updateStockData_US_Daily(root_path, "1990-01-01", now, storeType)

    #paras = run_lstm_classification(root_path, predict_symbols, predict_symbols, True, False, True)
    #paras = run_dbn_classification(root_path, predict_symbols, predict_symbols, True, False, True)
    #paras = run_rf_classification(root_path, predict_symbols, predict_symbols, True, False, True)

    #run_recommand_system(root_path, predict_symbols, predict_symbols, True, False, True)
    #paras = run_rf_regression(root_path, predict_symbols, predict_symbols, True, False, True)
    
    # if storeType == 1:
    #     # stop database server (sync)
    #     time.sleep(5)
    #     ShutdownServer()

    df = getStocksList_CHN(root_path)
    df.index = df.index.astype(str).str.zfill(6)
    df = df.sort_index(ascending = True)
    symbols = df.index.values.tolist()
    # symbols = ['000001']
    paras = run_xgboost_classification(root_path, symbols, symbols, True, False, True)

    backend.clear_session()
