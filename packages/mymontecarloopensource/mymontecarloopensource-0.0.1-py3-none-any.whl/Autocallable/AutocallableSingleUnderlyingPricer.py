import numpy as np
from scipy.stats import norm

class AutocallableSingleUnderlyingPricer:

    @staticmethod
    def MC_naive_1(t_0, s_0, S_ref, B, m, t, Q, h, r, b, sigma, N):
        np.random.seed(22011977)
        mu = r - b
        V_naive = np.nan * np.ones(N)
        s = s_0 * np.ones(N)
        for j in range(m):
            if j > 0:
                dt = t[j] - t[j-1]
            else:
                dt = t[j] - t_0
            
            z = norm.ppf(np.random.rand(N))
            s = s * np.exp((mu - sigma**2/2) * dt + sigma * np.sqrt(dt) * z)
            index = np.isnan(V_naive) & (s/S_ref >= B)
            V_naive[index] = np.exp(-r * (t[j] - t_0)) * Q[j]
        index = np.isnan(V_naive)
        V_naive[index] = np.exp(-r * (t[j] - t_0)) * h(s[index]/S_ref)
        V_naive = np.sum(V_naive) / N
        return V_naive
    
    @staticmethod
    def MC_new_1(t_0, s_0, S_ref, B, m, t, Q, h, r, b, sigma, N):
        np.random.seed(22011977)
        mu = r - b
        V_new = np.zeros(N)
        s = s_0 * np.ones(N)
        L = np.ones(N)
        for j in range(m):
            if j > 0:
                dt = t[j] - t[j-1]
            else:
                dt = t[j] - t_0
            p = norm.cdf((np.log(B * S_ref / s) - (mu - sigma**2/2) * dt) / (sigma * np.sqrt(dt)))
            V_new = V_new + (1 - p) * L * np.exp(-r * (t[j] - t_0)) * Q[j]
            L = L * p
            u = np.random.rand(N)
            s = s * np.exp((mu - sigma**2/2) * dt + sigma * np.sqrt(dt) * norm.ppf(p * u))
        V_new = V_new + L * np.exp(-r * (t[m-1] - t_0)) * h(s/S_ref)
        V_new = np.sum(V_new) / N
        return V_new
