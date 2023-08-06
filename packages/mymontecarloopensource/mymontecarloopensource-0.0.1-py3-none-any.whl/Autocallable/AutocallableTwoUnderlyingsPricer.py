import numpy as np
from scipy.stats import norm

class AutocallableTwoUnderlyingsPricer:

    @staticmethod
    def MC_naive_2(t_0, s1_0, s2_0, S1_ref, S2_ref, B, m, t, Q, h, r, b1, b2, sigma1, sigma2, rho, N):
        np.random.seed(22011977)
        mu1 = r - b1
        mu2 = r - b2
        V_naive = np.nan * np.ones(N)
        s1 = s1_0 * np.ones(N)
        s2 = s2_0 * np.ones(N)
        for j in range(m):
            if j > 0:
                dt = t[j] - t[j-1]
            else:
                dt = t[j] - t_0
            
            z = np.random.multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]], size=N)
            z1 = z[:, 0]
            z2 = z[:, 1]
            s1 = s1 * np.exp((mu1 - sigma1**2/2) * dt + sigma1 * np.sqrt(dt) * z1)
            s2 = s2 * np.exp((mu2 - sigma2**2/2) * dt + sigma2 * np.sqrt(dt) * z2)
            index = (np.isnan(V_naive) & (np.minimum(s1/S1_ref, s2/S2_ref) >= B))
            V_naive[index] = np.exp(-r * (t[j] - t_0)) * Q[j]
        index = np.isnan(V_naive)
        V_naive[index] = np.exp(-r * (t[j] - t_0)) * h(s1[index]/S1_ref, s2[index]/S2_ref)
        V_naive = np.sum(V_naive) / N
        return V_naive
    
    @staticmethod
    def MC_new_2(t_0, s1_0, s2_0, S1_ref, S2_ref, B, m, t, Q, h, r, b1, b2, sigma1, sigma2, rho, N):
        np.random.seed(22011977)
        mu1 = r - b1
        mu2 = r - b2
        alpha = 0.5 * (np.pi/2 - np.arctan(-rho/np.sqrt(1 - rho**2)))
        V_new = np.zeros(N)
        s1 = s1_0 * np.ones(N)
        s2 = s2_0 * np.ones(N)
        L = np.ones(N)
        for j in range(m):
            if j > 0:
                dt = t[j] - t[j-1]
            else:
                dt = t[j] - t_0
            C1 = (np.log(B*S1_ref/s1) - (mu1 - sigma1**2/2)*dt) / (sigma1*np.sqrt(dt))
            C2 = (np.log(B*S2_ref/s2) - (mu2 - sigma2**2/2)*dt) / (sigma2*np.sqrt(dt))
            u1 = np.random.rand(N)
            x1 = norm.ppf(u1)
            C = np.maximum((C1 - x1*np.cos(alpha)) / np.sin(alpha),
                        (C2 - rho*x1*np.cos(alpha) + np.sqrt(1 - rho**2)*x1*np.sin(alpha)) /
                        (rho*np.sin(alpha) + np.sqrt(1 - rho**2)*np.cos(alpha)))
            p = norm.cdf(C)
            V_new = V_new + (1 - p) * L * np.exp(-r * (t[j] - t_0)) * Q[j]
            L = L * p
            u2 = p * np.random.rand(N)
            x2 = norm.ppf(u2)
            y1 = x1 * np.cos(alpha) + x2 * np.sin(alpha)
            y2 = -x1 * np.sin(alpha) + x2 * np.cos(alpha)
            z1 = y1
            z2 = rho * y1 + np.sqrt(1 - rho**2) * y2
            s1 = s1 * np.exp((mu1 - sigma1**2/2) * dt + sigma1 * np.sqrt(dt) * z1)
            s2 = s2 * np.exp((mu2 - sigma2**2/2) * dt + sigma2 * np.sqrt(dt) * z2)
        V_new = V_new + L * np.exp(-r * (t[m-1] - t_0)) * h(s1/S1_ref, s2/S2_ref)
        V_new = np.sum(V_new) / N
        return V_new
        
