# Automated Machine Learning Framework for Data Analysis

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   


## Key Features

- Automated Model Selection: The framework automatically selects the most suitable machine learning model based on the characteristics of the dataset.
- Feature Engineering: It automatically applies various feature engineering techniques to preprocess the data and enhance the predictive power of the models.
- Hyperparameter Optimization: The library performs hyperparameter optimization to fine-tune the models and improve their performance.
- Performance Evaluation: It provides comprehensive evaluation metrics to assess the performance of the models and compare different approaches.

## Usage

- Make sure you have Python installed in your system.
- Run Following command in the Terminal.
 ```
  pip install UAutoml
  ```
## Example

 ```
# test.py
from UAutoml import process_data

## Make sure u have follwing paramters
dataset = '/Path'
Target = 'Column_Name'

(this are optional)
Hyper_optimazation: If needed set value to 1 or in default 0
epochs: IN default its 5 you can set your requirements

# To run
r = process_data(dataset,Target)

```

## Run the following Script.
 ```
  python test.py
 ```

## Note 
- I have tried to implement all the functionality, it might have some bugs also. Ignore that or please try to solve that bug.
