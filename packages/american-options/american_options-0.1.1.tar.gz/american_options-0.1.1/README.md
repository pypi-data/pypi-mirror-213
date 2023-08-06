# American Options Library
The Library that is using various methods to price the variety of options of american type.

### Installation
```
pip install american_options
```

### Get started
How to obtain option price with this library:

```Python
from american_options import Option, Underlying

#Set up your parameters
n_sims = 10000   
T = 1
sigma1 = 0.4
sigma2 = 0.8
r = 0.06
N = 255
spot1 = 100
spot2 = 120
K1 = 100
K2 = 110
```

First you need to create assets you want to write options on. You can do this in following way:
```Python
# Instantiate an Underlying object
asset1 = Underlying(spot_price=100, r=0.07)
asset2 = Underlying(spot_price=120, r=0.07)

```
Next step is to calibrate assets for the use of different models. 
```Python
# Calibrate created assets
asset1.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)
asset1.calibrate_JD(sigma=0.4, jump_intensity=1/3)
asset2.calibrate_GBM(sigma=0.4, values_per_year_GBM=N)
asset2.calibrate_JD(sigma=0.2, jump_intensity=1/2)

```
Now create options, for that we need payoff functions as well. You can import some of them from payoffs module:
```Python
from american_options.payoffs import *

option1 = Option(underlyings=asset1, payoff_func=lambda trajectory: payoff_creator_1d(trajectory, Call_Payoff, K=100, barrier=True, barrier_level=140), T=1)
option2 = Option(underlyings=(asset1, asset2), payoff_func=lambda trajectories: double_max_put(trajectories, 100), T=1)
```

And finally obtaining a price!
```Python
# Pricing with state space partitioning method
option1.ssp(n_sims=10000, mode='JD')
option2.ssp(n_sims=10000, mode='GBM')

# pPricing with Longstaff-Schwartz method
option1.LS(n_sims=10000, mode='JD')
option2.ssp(n_sims=10000, mode='GBM')
```