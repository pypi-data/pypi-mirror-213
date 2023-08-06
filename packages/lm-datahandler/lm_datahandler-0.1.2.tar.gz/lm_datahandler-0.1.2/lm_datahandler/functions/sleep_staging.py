import numpy as np
import lightgbm as lgb
import pandas as pd
from lm_datahandler.postprocess.label_smooth import pp_label_smooth
import os

def sleep_staging_with_features(features, model_path, use_acc, use_time, context_mode=1):
    clf = None
    feature_for_predict = None
    if model_path is not None:
        clf = lgb.Booster(model_file=model_path)
    else:
        model_name = "sleep_staging.txt"
        if use_acc:
            model_name = 'acc_' + model_name

        if use_time:
            model_name = 'time_' + model_name

        if context_mode == 2:
            model_name = "wholenight_" + model_name
        elif context_mode == 1:
            model_name = "realtime_" + model_name

        clf = lgb.Booster(model_file="models/"+model_name)

    feature_name = clf.feature_name()
    feature_for_predict = features[feature_name]
    predictions = clf.predict(feature_for_predict)
    predictions = np.argmax(predictions, axis=1)

    classes_with_alphabet_order = np.array(['N1/N2', 'N3', 'REM', 'Wake'])
    predictions = classes_with_alphabet_order[predictions]
    df_hypno = pd.Series(predictions)
    df_hypno.replace({'N3': 0, 'N1/N2': 1, 'REM': 2, 'Wake': 3}, inplace=True)

    predictions = df_hypno.to_numpy()
    pp_predictions = pp_label_smooth(np.copy(predictions), window=2)

    return predictions, pp_predictions