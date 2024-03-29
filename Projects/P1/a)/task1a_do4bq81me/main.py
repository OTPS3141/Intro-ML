# This serves as a template which will guide you through the implementation of this task. It is advised
# to first read the whole template and get a sense of the overall structure of the code before trying to fill in any of the TODO gaps
# First, we import necessary libraries:
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge

### Read data

# df_sample = pd.read_csv('/home/otps3141/Documents/Dokumente/ETH QE/Semester 2/Intro ML/Projects/P1/a)/task1a_do4bq81me/sample.csv')
# df_train = pd.read_csv('/home/otps3141/Documents/Dokumente/ETH QE/Semester 2/Intro ML/Projects/P1/a)/task1a_do4bq81me/train.csv')


def fit(X, y, lam):
    """
    This function receives training data points, then fits the ridge regression on this data
    with regularization hyperparameter lambda. The weights w of the fitted ridge regression
    are returned. 

    Parameters
    ----------
    X: matrix of floats, dim = (135,13), inputs with 13 features
    y: array of floats, dim = (135,), input labels)
    lam: float. lambda parameter, used in regularization term

    Returns
    ----------
    w: array of floats: dim = (13,), optimal parameters of ridge regression
    """
    # w = np.zeros((13,))

    ### Closed form
    w_star = np.linalg.inv(X.T@X + lam * np.identity(13))@(X.T@y)


    ### Sklearn

    # Define Ridge Regression model
    reg = Ridge(lam)
    reg.fit(X, y)
    
    w = reg.coef_


    assert w_star.shape == (13,)
    return w_star




def calculate_RMSE(w, X, y):
    """This function takes test data points (X and y), and computes the empirical RMSE of 
    predicting y from X using a linear model with weights w. 

    Parameters
    ----------
    w: array of floats: dim = (13,), optimal parameters of ridge regression 
    X: matrix of floats, dim = (15,13), inputs with 13 features
    y: array of floats, dim = (15,), input labels

    Returns
    ----------
    RMSE: float: dim = 1, RMSE value
    """
    # Calculate predicted y value
    y_pred = X.dot(w)
    
    # Determine mean squared error
    RMSE = mean_squared_error(y, y_pred)**0.5
    
    assert np.isscalar(RMSE)
    return RMSE


def average_LR_RMSE(X, y, lambdas, n_folds):
    """
    Main cross-validation loop, implementing 10-fold CV. In every iteration (for every train-test split), the RMSE for every lambda is calculated, 
    and then averaged over iterations.
    
    Parameters
    ---------- 
    X: matrix of floats, dim = (150, 13), inputs with 13 features
    y: array of floats, dim = (150, ), input labels
    lambdas: list of floats, len = 5, values of lambda for which ridge regression is fitted and RMSE estimated
    n_folds: int, number of folds (pieces in which we split the dataset), parameter K in KFold CV
    
    Returns
    ----------
    avg_RMSE: array of floats: dim = (5,), average RMSE value for every lambda
    """
    RMSE_mat = np.zeros((n_folds, len(lambdas)))

    # Define cross validation model
    kf = KFold(n_folds)
    
    # Fill in all entries in the matrix 'RMSE_mat'
    mat_i = 0
    mat_j = 0
    
    for lam in lambdas:
        for train_index, test_index in kf.split(X):
            X_train = X[train_index]
            y_train = y[train_index]
            
            w = fit(X_train, y_train, lam)
            
            X_test = X[test_index]
            y_test = y[test_index]
            
            RMSE_mat[mat_i,mat_j] = calculate_RMSE(w, X_test, y_test)
            
            mat_i = mat_i + 1
        
        mat_i = 0
        mat_j = mat_j + 1

    
    # TODO: Enter your code here. Hint: Use functions 'fit' and 'calculate_RMSE' with training and test data
    # and fill all entries in the matrix 'RMSE_mat'

    avg_RMSE = np.mean(RMSE_mat, axis=0)
    assert avg_RMSE.shape == (5,)
    return avg_RMSE


# Main function. You don't have to change this
if __name__ == "__main__":
    # Data loading
    data = pd.read_csv("/home/otps3141/Documents/Dokumente/ETH QE/Semester 2/Intro ML/Projects/P1/a)/task1a_do4bq81me/train.csv")
    y = data["y"].to_numpy()
    data = data.drop(columns="y")
    # print a few data samples
    # print(data.head())
    # print(y)

    X = data.to_numpy()
    # print(X)
    # The function calculating the average RMSE
    lambdas = [0.1, 1, 10, 100, 200]
    n_folds = 10
    avg_RMSE = average_LR_RMSE(X, y, lambdas, n_folds)

    print(average_LR_RMSE(X, y, lambdas, 10))
    # print(fit(X, y, 0))

    # Save results in the required format
    np.savetxt("Projects/Own solutions/P1/a)/sample.csv", avg_RMSE, fmt="%.12f")
