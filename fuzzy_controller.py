import numpy as np
import matplotlib.pyplot as plt

class FuzzyController:
    """
    #todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self):
        pass


    def decide(self, left_dist,right_dist):
        """
        main method for doin all the phases and returning the final answer for rotation
        """
        inference_left, inference_right, inference_nothing = self.inference(left_dist,right_dist)
        return self.defuzzify(inference_left, inference_right, inference_nothing)
    
    def fuzzify (self, left_dist,right_dist):
        """
        fuzzify the input
        """

        def close(x):
            if x >= 0 and x <= 50 : 
                return (-1/50 * x) + 1
            else:
                return 0
            
        def moderate(x):
            if x >= 35 and x <= 50:
                return (1/15 * x) - (7/3)
            elif x >= 50 and x <= 65:
                return (-1/15 * x) + (13/3)
            else:
                return 0
                
        def far(x):
            if x >= 50 and x <= 100:
                return (1/50 * x) - 1
            else:
                return 0
                    
        
        fuzzify_left = (close(left_dist),moderate(left_dist),far(left_dist))
        fuzzify_right = (close(right_dist),moderate(right_dist),far(right_dist))

        return fuzzify_left, fuzzify_right


    def inference(self, left_dist,right_dist):
        """
        inference the input
        """
        fuzzify_left, fuzzify_right = self.fuzzify(left_dist,right_dist)

        low_right = min(fuzzify_left[0],fuzzify_right[1])
        low_left = min(fuzzify_left[1],fuzzify_right[0])

        high_right = min(fuzzify_left[0],fuzzify_right[2])
        high_left = min(fuzzify_left[2],fuzzify_right[0])

        nothing = min(fuzzify_left[1],fuzzify_right[1])

        inference_left = (low_left, high_left)
        inference_right = (low_right, high_right)
        inference_nothing = nothing

        return inference_left, inference_right, inference_nothing
    
    def defuzzify(self, inference_left, inference_right, inference_nothing):

        def high_right(x):
            if x >= -50 and x <= -20:
                return (1/30 * x) + (5/3)
            elif x >= -20 and x <= -5:
                return (-1/15 * x) - (1/3)
            else:
                return 0
            
        def low_right(x):
            if x >= -20 and x <= -10:
                return (1/10 * x) + 2
            elif x >= -10 and x <= 0:
                return (-1/10 * x)
            else:
                return 0
            
        def nothing(x):
            if x >= -10 and x <= 0:
                return (1/10 * x) + 1
            elif x >= 0 and x <= 10:
                return (-1/10 * x) + 1
            else:
                return 0
            
        def low_left(x):
            if x >= 0 and x <= 10:
                return (1/10 * x)
            elif x >= 10 and x <= 20:
                return (-1/10 * x) + 2
            else:
                return 0
            
        def high_left(x):
            if x >= 5 and x <= 20:
                return (1/15 * x) - (1/3)
            elif x >= 20 and x <= 50:
                return (-1/30 * x) + (5/3)
            else:
                return 0
            
        def high_right_value(x, high_right_mu):
            return high_right(x) if high_right(x) <= high_right_mu else high_right_mu
        
        def low_right_value(x, low_right_mu):
            return low_right(x) if low_right(x) <= low_right_mu else low_right_mu
        
        def nothing_value(x, nothing_mu):
            return nothing(x) if nothing(x) <= nothing_mu else nothing_mu
        
        def low_left_value(x, low_left_mu):
            return low_left(x) if low_left(x) <= low_left_mu else low_left_mu
        
        def high_left_value(x, high_left_mu):
            return high_left(x) if high_left(x) <= high_left_mu else high_left_mu
        
            
        x = np.arange(-50,50,0.1)
        y = np.zeros_like(x)

        for i in range(len(x)):
            if x[i] >= -50 and x[i] <= -20:
                y[i] = high_right_value(x[i], inference_right[1])

            elif x[i] >= -20 and x[i] <= -10:
                y[i] = max(low_right_value(x[i], inference_right[0]),
                            high_right_value(x[i], inference_right[1]))
                
            elif x[i] >= -10 and x[i] <= 0:
                y[i] = max(nothing_value(x[i], inference_nothing),
                            low_right_value(x[i], inference_right[0]),
                            high_right_value(x[i], inference_right[1]))
                
            elif x[i] >= 0 and x[i] <= 10:
                y[i] = max(nothing_value(x[i], inference_nothing),
                            low_left_value(x[i], inference_left[0]),
                            high_left_value(x[i], inference_left[1]))
                
            elif x[i] >= 10 and x[i] <= 20:
                y[i] = max(low_left_value(x[i], inference_left[0]),
                            high_left_value(x[i], inference_left[1]))
                
            elif x[i] >= 20 and x[i] <= 50:
                y[i] = high_left_value(x[i], inference_left[1])

        plt.plot(x,y)
        plt.grid(True)

        answ = np.trapz(y * x, x) / np.trapz(y, x)

        return answ
            


    
