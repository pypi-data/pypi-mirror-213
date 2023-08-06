from src.StableGreeksInvestigationToolbox import *
from src.StableGreeksInvestigationToolbox.FunctionEvaluation import *

        
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
        
        
        
        
    