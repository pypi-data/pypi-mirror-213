import numpy as np
import matplotlib.pyplot as plt
from AMoption import Option, Underlying

n = 10000
T = 0.5
sigma1 = 0.4
sigma2 = 0.3
r = 0.06
N = 100
n_bins = np.sqrt(n)
spot1 = 100
spot2 = 110
K1 = 100
K2 = 110

Aktywo = Underlying(spot_price=spot1, r=r)  # Aktywo = Underlying(100)
Aktywo.calibrate_GBM(sigma=sigma1, values_per_year_GBM=N)  # Aktywo.calibrate_GBM(0.3,0.07)
ti = int(Aktywo.values_per_year_GBM * T)

Aktywo2 = Underlying(spot_price=spot2, r=r)  # Aktywo = Underlying(100)
Aktywo2.calibrate_GBM(sigma=sigma2, values_per_year_GBM=N)  # Aktywo.calibrate_GBM(0.3,0.07)

def Double_Call_Payoff(sims_list, K1, K2):
    return (np.maximum(sims_list[0] - K1, 0) + np.maximum(sims_list[1] - K2, 0))

Opcja = Option(underlyings=(Aktywo, Aktywo2), strike=K1, payoff_func=lambda traj: Double_Call_Payoff(traj, K1, K2), T=T)
#Opcja2 = Option(underlyings=Aktywo, strike=K, payoff_func=lambda traj, K: np.maximum(K-traj, 0), T=T)
#Opcja3 = Option(underlyings=Aktywo, strike=K, payoff_func=lambda traj, K: np.maximum(traj - K, 0), T=T, path_dependent=True, pd_type='asian')

#Options = [Opcja, Opcja2, Opcja3, Opcja4, Opcja5, Opcja6, Opcja7, Opcja8, Opcja9, Opcja10, Opcja11, Opcja12, Opcja13, Opcja14]
    #types = ['call', 'put', 'asian call', 'geometric asian', 'asian strike call', 'geometric asian strike call', 'lookback minimum call',
    #         'lookback max call', 'up-and-out call (140)', 'up and in call(140)', ]
len(Opcja.underlyings)
Opcja.ssp(n,n_bins)
np.zeros((int(n_bins),1))



# Create a 2-dimensional array
arr = np.array([[1, 2, 3, 4,6,8],
                [4, 5, 6,6,2,3],
                [7, 8, 9,9,1,3],
                [7, 8, 9,9,1,3],
                [7, 8, 9,9,1,3],
                [7, 8, 9,9,1,3]])















# Calculate the median along each axis
#median_axis0 = np.quantile(arr, [0.25, 0.5, 0.75], axis=0)
#median_axis1 = np.quantile(arr, [0.25, 0.5, 0.75], axis=1)

# Create scatter plot
##x = np.arange(arr.shape[1])
#y = np.arange(arr.shape[0])

#fig, ax = plt.subplots()
#ax.scatter(x, median_axis0, label='Median along Axis 0')
#ax.scatter(median_axis1, y, label='Median along Axis 1')
#ax.legend()
#ax.set_xlabel('Index')
#x.set_ylabel('Value')
#ax.set_title('Quantiles in 2-Dimensional Array')
#plt.show()
