import unittest
import pandas as pd
import package
import pickle
from package import dataset
from package import train
from package import scores


class test2(unittest.TestCase):        
    def test_dataset(self):
       
        housing_prepared, housing_labels =dataset.load_housing_data("D:\Project\data\processed\test_housingprice.csv")
        housing_prepared_row=housing_prepared.shape[0]
        housing_labels_row=housing_prepared.shape[0]
        #row=341
        #print(row)
        self.assertEqual(housing_prepared_row, housing_labels_row,"dataset not successful")
        #if you want to know both error and success uncomment till print
        #assert row==341,"dataset not successful"
        #print("dataset is successful")
        
##    def test_train(self):
##       
##        result =dataset.load_housing_data("test_housingprice.csv")
##        housing_labels, housing_predictions=train.EDA_lr(result)
##
##        housing_labels_row=housing_labels.shape[0]
##        housing_predictions_row=housing_predictions.shape[0]
##        #print(row)
##        self.assertEqual(housing_labels_row,housing_predictions_row,"train not successful")
##        #if you only want to know error uncomment below till print
##        #assert housing_labels_row==housing_predictions_row,"train not successful"
##        #print("train is successful")
        
    def test_scores(self):
       
        housing_prepared, housing_labels=dataset.load_housing_data("D:\Project\data\processed\test_housingprice.csv")
        train.lr(housing_prepared, housing_labels)
        with open('train.pkl' , 'rb') as f:
            model = pickle.load(f)
        housing_predictions=model.predict(housing_prepared)
        rmse=round(scores.rmse(housing_labels, housing_predictions),3)
        mae=round(scores.mae(housing_labels, housing_predictions),3)
        #row=341
        #print(row)
        self.assertEqual(((rmse==26337.697) and (mae==19385.325)),True,"scores not successful")
        #if you only want to know error uncomment below till print
        #assert((rmse==26337.697) and (mae==19385.325))==True,"scores not successful"     
        #print("scores is successful")
        
  
    


# run the test
unittest.main()

