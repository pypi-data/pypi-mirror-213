from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import logging
logger = logging.getLogger(__name__)
def rmse(housing_labels, housing_predictions):
    """
    It gives the root mean square error
    between actual values and predicted values
        :intput: actual target values and predicted target values
        :output: value(float)
    """
    lin_mse = mean_squared_error(housing_labels, housing_predictions)
    lin_rmse = np.sqrt(lin_mse)
    logger.info("rmse is working")
    return lin_rmse
def mae(housing_labels, housing_predictions):
    """
    It gives the mean absolute error
    between actual values and predicted values
        :intput: actual target values and predicted target values::
        :output: value(float)::
    """
    lin_mae = mean_absolute_error(housing_labels, housing_predictions)
    logger.info("mae is working")
    return lin_mae
