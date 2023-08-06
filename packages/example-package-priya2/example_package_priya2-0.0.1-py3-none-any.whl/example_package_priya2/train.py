from sklearn.linear_model import LinearRegression
import pickle
import logging
logger = logging.getLogger(__name__)
def lr(housing_prepared, housing_labels):
    """
    Trains the model\n
    It creates a pickle file of the trained model\n
    we can use this pickle file whenever we want to use same mode
        :input: independent and traget variables
        :output: pickle file gets generated
    """

    

    lin_reg = LinearRegression()
    lin_reg.fit(housing_prepared, housing_labels)
    file=open('artifacts/train.pkl','wb')
    pickle.dump(lin_reg,file)
    file.close()
    logger.info("train is working")
    #housing_predictions = lin_reg.predict(housing_prepared)
    #return(housing_labels, housing_predictions)


