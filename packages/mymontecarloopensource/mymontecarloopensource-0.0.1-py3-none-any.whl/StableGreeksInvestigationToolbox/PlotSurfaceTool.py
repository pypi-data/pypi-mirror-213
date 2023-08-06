import numpy as np
import matplotlib.pyplot as plt

from enum import Enum

from src.StableGreeksInvestigationToolbox.FunctionEvaluation import *


class PlotSettings(Enum):
    PresentValue = 1
    Delta = 2
    Gamma = 3
    
class PlotSurfaceTool:
    @staticmethod
    def runInvestigation(fixed_func, x, investigationSettings):
        if investigationSettings.PlotSetting == PlotSettings.PresentValue:
            print(investigationSettings.PlotSetting)
            y = FunctionEvaluation.evaluate_function(fixed_func, x)
            PlotSurfaceTool.plot_valuation_1d(x, y, 'Present value')
        elif investigationSettings.PlotSetting== PlotSettings.Delta:
            y = FunctionEvaluation.evaluate_function(fixed_func, x)
            delta = FunctionEvaluation.compute_delta(fixed_func, x, investigationSettings.FiniteDifferencesStepWidth)

            fig, axs = plt.subplots(1, 2, figsize=(10, 3))

            axs[0].plot(x, y)
            axs[0].set_xlabel('x')
            axs[0].set_ylabel('Value')
            axs[0].set_title('Present value')

            axs[1].plot(x, delta)
            axs[1].set_xlabel('x')
            axs[1].set_ylabel('Delta')
            axs[1].set_title('Delta')

            plt.tight_layout()
            plt.show()
        elif investigationSettings.PlotSetting == PlotSettings.Gamma:
            y = FunctionEvaluation.evaluate_function(fixed_func, x)
            delta = FunctionEvaluation.compute_delta(fixed_func, x, investigationSettings.FiniteDifferencesStepWidth)
            gamma = FunctionEvaluation.compute_gamma(fixed_func, x, investigationSettings.FiniteDifferencesStepWidth)

            fig, axs = plt.subplots(1, 3, figsize=(10, 3))

            axs[0].plot(x, y)
            axs[0].set_xlabel('x')
            axs[0].set_ylabel('Value')
            axs[0].set_title('Present value')

            axs[1].plot(x, delta)
            axs[1].set_xlabel('x')
            axs[1].set_ylabel('Delta')
            axs[1].set_title('Delta')

            axs[2].plot(x, gamma)
            axs[2].set_xlabel('x')
            axs[2].set_ylabel('Gamma')
            axs[2].set_title('Gamma')

            plt.tight_layout()
            plt.show()
    
    @staticmethod
    def plot_valuation_1d(x, y, title):
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(title)
        plt.show()
        
    @staticmethod
    def do_something(a, b, c):
        # Perform some computations
        result = a + b * c
        return result
        
        

# # Fixed parameters
# t_0 = 0.0
# S_ref = 4000.0
# B = 1.0
# m = 2
# t = np.array([1.0, 2.0])
# Q = np.array([110.0, 120.0])
# r = 0.04
# b = 0.0
# sigma = 0.3
# N = 10000
# def h(s):
#     return 100 * s
# # Pack to be investigated algorithm in a lambda-function:
# fixed_func = lambda s_0: PlotSurfaceTool.do_something(s_0 , b = 2, c = 3)

# ###
# ### 2. Investigation settings
# ###
# s_0 = np.arange(1000, 10000,1000) 

# ###
# ### 3. Run investigation
# ###
# PlotSurfaceTool.runInvestigation(fixed_func, s_0, InvestigationSettings.Gamma)




