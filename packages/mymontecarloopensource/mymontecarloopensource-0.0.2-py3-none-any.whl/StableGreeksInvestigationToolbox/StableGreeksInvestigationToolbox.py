import numpy as np
import matplotlib.pyplot as plt
from enum import Enum


        
class StableGreeksInvestigationToolbox:
    @staticmethod
    def runInvestigation(fixed_func, x, investigationSettings):
        if investigationSettings.DetectInstabilities:
            StableGreeksInvestigationToolbox.instabilityDetectionDelta(fixed_func, x, investigationSettings)
            StableGreeksInvestigationToolbox.instabilityDetectionGamma(fixed_func, x, investigationSettings)
            
        PlotSurfaceTool.runInvestigation(fixed_func, x, investigationSettings)
        
    @staticmethod
    def instabilityDetectionDelta(fixed_func, x, investigationSettings):
        
        print("Instability detection for Delta started:")
        
        delta1 = FunctionEvaluation.compute_delta(fixed_func, x, investigationSettings,0.1)
        delta2 = FunctionEvaluation.compute_delta(fixed_func, x, investigationSettings,0.001)
        delta3 = FunctionEvaluation.compute_delta(fixed_func, x, investigationSettings,0.00001)
        
        instabilityDetected = False
        
        for i in range(0, len(x)):
            if (delta1[i] != 0 and delta2[i] != 0 and delta3[i] != 0):
                ratio1 = np.abs(np.divide(delta2[i] , delta1[i]))
                ratio2 = np.abs(np.divide(delta3[i] , delta2[i]))
                                
                if (ratio1 > ratio2 * 2 ):
                    print("Delta jump detected for x = " + str(x[i]))
                    instabilityDetected = True
                    print("Stopping investigation for Delta (stopping on first hit)")
                    break
        if (not instabilityDetected):        
            print("Instability detection for Delta done: No instabilities detected")
                
                
    @staticmethod
    def instabilityDetectionGamma(fixed_func, x, investigationSettings):
        
        print("Instability detection for Gamma started:")
        
        gamma1 = FunctionEvaluation.compute_gamma(fixed_func, x, investigationSettings,0.1)
        gamma2 = FunctionEvaluation.compute_gamma(fixed_func, x, investigationSettings,0.01)
        gamma3 = FunctionEvaluation.compute_gamma(fixed_func, x, investigationSettings,0.001)
        
        instabilityDetected = False
        
        for i in range(0, len(x)):
            if (gamma1[i] != 0 and gamma2[i] != 0 and gamma3[i] != 0):
                ratio1 = np.abs(np.divide(gamma2[i] , gamma1[i]))
                ratio2 = np.abs(np.divide(gamma3[i] , gamma2[i]))
                if (ratio1 > ratio2 * 2 ):
                    print("Gamma jump detected for x = " + str(x[i]))
                    instabilityDetected = True
                    print("Stopping investigation for Gamma (stopping on first hit)")
                    break
        if (not instabilityDetected): 
            print("Instability detection for Gamma done: No instabilities detected")
        
        
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
        
    
class InvestigationSettings:
    def __init__(self):
        self._plot_setting = None
        self._h_finite_differences = None
        self._detect_instabilities = False

    @property
    def PlotSetting(self):
        return self._plot_setting

    def set_PlotSetting(self, value):
        self._plot_setting = value

    @property
    def FiniteDifferencesStepWidth(self):
        return self._h_finite_differences

    def set_FiniteDifferencesStepWidth(self, value):
        self._h_finite_differences = value
        
    @property
    def DetectInstabilities(self):
        return self._detect_instabilities

    def set_DetectInstabilities(self, value):
        self._detect_instabilities = bool(value)
        


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