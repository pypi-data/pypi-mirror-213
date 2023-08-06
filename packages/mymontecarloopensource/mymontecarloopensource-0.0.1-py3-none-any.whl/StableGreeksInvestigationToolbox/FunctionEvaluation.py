
import numpy as np

class FunctionEvaluation:
    
    @staticmethod
    def evaluate_function(fixed_func, x):
        y = np.zeros(len(x))  # Create an array to store the y-values
        for i in range(0, len(x)):
            y[i] = fixed_func(x[i])
        return y
    
    @staticmethod
    def compute_delta(fixed_func, x, hFinDiff, hardCodedh = None):
        if hardCodedh is None:
            h = hFinDiff
        else:
            h = hardCodedh   
        delta = np.zeros(len(x))
        for i in range(0, len(x)):
            delta[i] = np.divide(fixed_func(x[i] + h) - fixed_func(x[i]), h)
        return delta
    
    @staticmethod
    def compute_gamma(fixed_func, x, hFinDiff, hardCodedh = None):
        if hardCodedh is None:
            h = hFinDiff
        else:
            h = hardCodedh   
        gamma = np.zeros(len(x))
        for i in range(0, len(x)):
            gamma[i] = np.divide(fixed_func(x[i] + h)  - 2*  fixed_func(x[i])  + fixed_func(x[i] - h) , h * h)
        return gamma