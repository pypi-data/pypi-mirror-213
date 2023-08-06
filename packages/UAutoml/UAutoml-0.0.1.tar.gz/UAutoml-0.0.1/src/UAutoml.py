import numpy as np
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.feature_selection import SelectFromModel, RFE
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import pandas as pd

def data_clean(x,y,target_column_name,df):
    
    c_x = x.columns.tolist() #columns name

    non_numeric_columns_x = []
    numeric_x = []

    for column in x.columns:
        if not pd.api.types.is_numeric_dtype(x[column]):
            non_numeric_columns_x.append(column)
        else:
            numeric_x.append(column)

    #for x data checking nan for non_numeric
    for i in range(0,len(non_numeric_columns_x)):    
        is_column_all_nan = x[non_numeric_columns_x[i]].isnull().all()
        if is_column_all_nan:
            x[non_numeric_columns_x[i]].fillna(0, inplace=True)
            
    #for x data checking nan for numeric
    for i in range(0,len(numeric_x)):    
        is_all_nan = x[numeric_x[i]].isnull().all()
        if is_all_nan:
            x[numeric_x[i]].fillna(0, inplace=True)
            
            
    #for x data
    for i in range(0,len(non_numeric_columns_x)):  
        x[non_numeric_columns_x[i]].fillna(method='ffill', inplace=True) # Forward fill missing string values
        x[non_numeric_columns_x[i]].fillna(method='bfill', inplace=True) # Backward fill missing string values
    
    
    #for x data
    for i in range(0,len(numeric_x)):
        missing_percentage = x[numeric_x[i]].isnull().sum() / len(x) * 100
        # Handle missing values using different methods
        if missing_percentage < 5: 
            x[numeric_x[i]].fillna(x[numeric_x[i]].mean(), inplace=True) # If missing values are less than 5%, use mean imputation
        elif missing_percentage < 30: 
            x[numeric_x[i]].fillna(x[numeric_x[i]].median(), inplace=True) # If missing values are less than 30%, use median imputation
        else:
            x[numeric_x[i]].interpolate(inplace=True) # If missing values are 30% or more, use interpolation
        
    #for y data
    try:
        missing_percentage = df[target_column_name].isnull().sum() / len(y) * 100
        if missing_percentage < 5:
            df[target_column_name].fillna(df[target_column_name].mean(), inplace=True) # If missing values are less than 5%, use mean imputation
        elif missing_percentage < 30:
            df[target_column_name].fillna(df[target_column_name].median(), inplace=True) # If missing values are less than 30%, use median imputation
        else:
            df[target_column_name].interpolate(inplace=True) # If missing values are 30% or more, use interpolation
    except Exception as e:
        print()
    
    
    #for x data
    for i in range(0,len(non_numeric_columns_x)):
        x[non_numeric_columns_x[i]] = x[non_numeric_columns_x[i]].astype('category').cat.codes

    #for y data
    try:
        y = y.astype('category').cat.codes
    except Exception as e:
        print()
        
        
    return(x,y)


def feature(x,y):
    
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42) #train_test splitting
    
    # LASSO Regularization
    lasso = Lasso(alpha=0.1)  # Adjust the regularization strength (alpha) as needed
    lasso.fit(X_train, y_train)
    
    # Select features using LASSO regularization
    lasso_selector = SelectFromModel(lasso, prefit=True)
    selected_features_lasso = X_train.columns[lasso_selector.get_support()]
    
    # Recursive Feature Elimination (RFE) with Linear Regression
    linear_reg = LinearRegression()  # Use a regression model of your choice
    rfe_selector = RFE(linear_reg, n_features_to_select=10)  # Select the desired number of features
    rfe_selector.fit(X_train, y_train)
    
    
    selected_features_rfe = X_train.columns[rfe_selector.support_] # Select features using RFE with Linear Regression
    selected_features = list(set(selected_features_lasso) | set(selected_features_rfe)) # Compare the selected features
    
    # Train and evaluate models with selected features
    X_train_selected = X_train[selected_features]
    X_test_selected = X_test[selected_features]
    
    model_lasso = Lasso(alpha=0.1)  # Adjust the regularization strength (alpha) as needed
    model_lasso.fit(X_train_selected, y_train)
    predictions_lasso = model_lasso.predict(X_test_selected)
    lasso_rmse = np.sqrt(mean_squared_error(y_test, predictions_lasso))
    
    model_lasso = Lasso(alpha=0.1)  # Adjust the regularization strength (alpha) as needed
    model_lasso.fit(X_train_selected, y_train)
    predictions_lasso = model_lasso.predict(X_test_selected)
    lasso_rmse = np.sqrt(mean_squared_error(y_test, predictions_lasso))
    model_lasso = Lasso(alpha=0.1)  # Adjust the regularization strength (alpha) as needed
    model_lasso.fit(X_train_selected, y_train)
    predictions_lasso = model_lasso.predict(X_test_selected)
    lasso_rmse = np.sqrt(mean_squared_error(y_test, predictions_lasso))
    
    model_rfe = LinearRegression()
    model_rfe.fit(X_train_selected, y_train)
    predictions_rfe = model_rfe.predict(X_test_selected)
    rfe_rmse = np.sqrt(mean_squared_error(y_test, predictions_rfe))
    
    if lasso_rmse > rfe_rmse:
        featuresss = selected_features_rfe
    else:
        featuresss = selected_features_lasso
        
        
    return featuresss


def models(x,y,featur,iteration):
    X = x[featur]
    Y = y      
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42) #train_test splitting 
    # Classification models  can add more if needed
    classification_models = [
        ('Decision Tree', DecisionTreeClassifier()),
        ('Support Vector Machine', SVC()),
        ('Logistic Regression', LogisticRegression()),
        ('Random Forest', RandomForestClassifier()),
        ('Multi-Layer Perceptron', MLPClassifier())
    ]
    
    # Regression models can add more if needed
    regression_models = [
        ('Decision Tree', DecisionTreeRegressor()),
        ('Support Vector Machine', SVR()),
        ('Linear Regression', LinearRegression()),
        ('Random Forest', RandomForestRegressor()),
        ('Multi-Layer Perceptron', MLPRegressor())
    ]
    
    epochs = iteration #can be modifed as necessary 
    
    # Evaluate classification models
    classification_scores = []
    for name, model in classification_models:
        try:
            scores = cross_val_score(model, X_train, y_train, cv=epochs, scoring='accuracy')
            classification_scores.append((name, scores.mean()))
        except Exception as e:
            print()
            continue
        
    # Evaluate regression models
    regression_scores = []
    for name, model in regression_models:
        try:
            scores = -cross_val_score(model, X_train, y_train, cv=epochs, scoring='neg_mean_squared_error')
            regression_scores.append((name, np.sqrt(scores.mean())))
        except Exception as e:
            print()
            continue
        
    best_classification_model = max(classification_scores, key=lambda x: x[1]) # Find the best classification model
    best_regression_model = min(regression_scores, key=lambda x: x[1]) # Find the best regression model
    
    
    
    return(classification_scores, regression_scores,best_classification_model,best_regression_model)
    
def Scores(classification_scores,regression_scores,best_classification_model,best_regression_model):
    # Print classification model scores
    print("Classification Model Scores:")
    for name, score in classification_scores:
        print(f"{name}: {score}")
        
    # Print regression model RMSE
    print("\nRegression Model RMSE:")
    for name, score in regression_scores:
        print(f"{name}: {score}")
        
    # Print best classification model
    print("\nBest Classification Model:")
    print(f"Model: {best_classification_model[0]}")
    print(f"Accuracy Score: {best_classification_model[1]}")
    
    # Print best regression model
    print("\nBest Regression Model:")
    print(f"Model: {best_regression_model[0]}")
    print(f"RMSE Score: {best_regression_model[1]}")

def H_optmization(x,y,featur):
    X = x[featur]
    Y = y      
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42) #train_test splitting 
    
    # Classification models
    classification_models = [
        ('Decision Tree', DecisionTreeClassifier(), {'max_depth': [3, 5, 10]}),
        ('Support Vector Machine', SVC(), {'C': [0.1, 1, 10]}),
        ('Logistic Regression', LogisticRegression(), {'C': [0.1, 1, 10]}),
        ('Random Forest', RandomForestClassifier(), {'n_estimators': [50, 100, 200]}),
        ('Multi-Layer Perceptron', MLPClassifier(), {'hidden_layer_sizes': [(50,), (100,), (200,)]})
    ]
    
   # Regression models
    regression_models = [
        ('Decision Tree', DecisionTreeRegressor(), {'max_depth': [3, 5, 10]}),
        ('Support Vector Machine', SVR(), {'C': [0.1, 1, 10]}),
        ('Linear Regression', LinearRegression(), {}),
        ('Random Forest', RandomForestRegressor(), {'n_estimators': [50, 100, 200]}),
        ('Multi-Layer Perceptron', MLPRegressor(), {'hidden_layer_sizes': [(50,), (100,), (200,)]})
    ]
    
    epochs = 5 #can be modifed as necessary 
    
    # Hyperparameter optimization for classification models
    classification_scores = []
    for name, model, param_grid in classification_models:
        try:
            grid_search = GridSearchCV(model, param_grid, cv=epochs, scoring='accuracy')
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            scores = cross_val_score(best_model, X_train, y_train, cv=epochs, scoring='accuracy')
            classification_scores.append((name, scores.mean()))
        except Exception as e:
            print()
            continue
            
    # Hyperparameter optimization for regression models
    regression_scores = []
    for name, model, param_grid in regression_models:
        try:
            grid_search = GridSearchCV(model, param_grid, cv=epochs, scoring='neg_mean_squared_error')
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            scores = np.sqrt(-cross_val_score(best_model, X_train, y_train, cv=epochs, scoring='neg_mean_squared_error'))
            regression_scores.append((name, np.mean(scores)))
        except Exception as e:
            print(f"Error occurred for {name}: {str(e)}")
            continue
        
    best_classification_model = max(classification_scores, key=lambda x: x[1]) # Find the best classification model
    best_regression_model = min(regression_scores, key=lambda x: x[1]) # Find the best regression model
    
    return(classification_scores, regression_scores,best_classification_model,best_regression_model)


def process_data(dataset_path, target_column_name1, use_hyperparameter_optimization=0, iteration=5):
    df = pd.read_csv(dataset_path) #Enter your dataset path 

    #target column name
    target_column_name = target_column_name1 #change to specific name

    x = df.drop(target_column_name, axis=1)
    y = df[target_column_name]

    st = use_hyperparameter_optimization


    xx,yy = data_clean(x,y,target_column_name,df)
    featur = feature(xx,yy)
    print("\n-------------------xxxx-------------------------")
    print("\n This features are selected: ", feature(xx,yy))
    print("\n-------------------xxxx-------------------------")
    if st == 0:
        c,r,bc,br = models(xx,yy,featur,iteration)
        print(Scores(c,r,bc,br))
    else:
        cc,rr,bbc,bbr = H_optmization(xx,yy,featur)
        print(Scores(cc,rr,bbc,bbr))



