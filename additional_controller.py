import numpy as np
class FuzzyGasController:

    def __init__(self):
        pass
        

    def decide(self, center_dist):
        inference_low, inference_moderate, inference_high = self.inference(center_dist)
        return self.defuzzify(inference_low, inference_moderate, inference_high)
        
    def fuzzify (self, center_dist):
        def close(x):
            if x >= 0 and x <= 50 : 
                return (-1/50 * x) + 1
            else:
                return 0
                
        def moderate(x):
            if x >= 40 and x<= 50:
                return (1/10 * x) - 4
            elif x >= 50 and x <= 100:
                return (-1/50 * x) + 2
            else:
                return 0
                    
        def far(x):
            if x < 90 :
                return 0
            elif x >= 90 and x <= 200:
                return (1/110 * x) - (9/11)
            else:
                return 1
                        
        
        fuzzify_center = (close(center_dist), moderate(center_dist), far(center_dist))

        return fuzzify_center
    

    def inference(self, center_dist):
        fuzzify_center = self.fuzzify(center_dist)

        inference_low = fuzzify_center[0]
        inference_moderate = fuzzify_center[1]
        inference_high = fuzzify_center[2]

        return inference_low, inference_moderate, inference_high
    
    def defuzzify(self, inference_low, inference_moderate, inference_high):
        def low_gas(x):
            if x >= 0 and x <= 5 :
                return (1/5 * x)
            elif x >= 5 and x <= 10:
                return (-1/5 * x) + 2
            else:
                return 0
            
        def medium_gas(x):
            if x >= 0 and x <= 15:
                return (1/15 * x)
            elif x >= 15 and x <= 30:
                return (-1/15 * x) + 2
            else:
                return 0
            
        def high_gas(x):
            if x >= 25 and x <= 30:
                return (1/5 * x) - 5
            elif x >= 30 and x <= 90:
                return (-1/60 * x) + (3/2)
            else:
                return 0
            

        def low_gas_value(x, low_gas_mu):
            return low_gas(x) if low_gas(x) <= low_gas_mu else low_gas_mu
        
        def medium_gas_value(x, medium_gas_mu):
            return medium_gas(x) if medium_gas(x) <= medium_gas_mu else medium_gas_mu
        
        def high_gas_value(x, high_gas_mu):
            return high_gas(x) if high_gas(x) <= high_gas_mu else high_gas_mu
        
        x = np.arange(0, 90.01, 0.01)
        y = np.zeros_like(x)

        for i in range(len(x)):
            if x[i] >= 0  and x[i] <= 10 :
                y[i] = max(low_gas_value(x[i], inference_low),
                           medium_gas_value(x[i], inference_moderate))
                
            elif  x[i] >= 10 and x[i] <= 25:
                y[i] = medium_gas_value(x[i], inference_moderate)

            elif x[i] >= 25 and x[i] <= 30:
                y[i] = max(medium_gas_value(x[i], inference_moderate),
                           high_gas_value(x[i], inference_high))

            elif x[i] >= 30 and x[i] <= 90:
                y[i] = high_gas_value(x[i], inference_high)

        return np.trapz(y * x, x) / np.trapz(y, x)