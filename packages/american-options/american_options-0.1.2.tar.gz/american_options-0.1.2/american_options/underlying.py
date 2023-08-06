import numpy as np
import pandas as pd
from tqdm import tqdm

class Underlying:
    """
    Object representing underlying asset of the option

    Parameters
    ----------
    :param spot_price: initial value of the asset
    :type spot_price: float
    :param r: risk-free rate
    :type r: float


    Examples
    --------
    Creation of an asset
    >>> asset = Underlying(spot_price=100, r=0.06)
    """
    def __init__(self, spot_price, r):
        self.spot_price = spot_price
        self.r = r
        self.GBM_calibrated = False
        self.Bootstrap_calibrated = False
        self.RT_GBM_calibrated = False
        self.JD_calibrated = False
        self.ssp_calibrated = False

    def calibrate_GBM(self, sigma, values_per_year_GBM=255):
        """
        Method needs to be called when one wants to simulate with GBM

        Parameters
        ----------
        :param sigma: volatility of an asset
        :type sigma: float
        :param values_per_year_GBM: how many time-steps we want to include, default: 255 (number of trading days per year)
        :type values_per_year_GBM: int

        Examples
        --------
        Creation of an asset
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_GBM(0.4, 255)
        """
        self.sigma = sigma
        self.values_per_year_GBM = values_per_year_GBM
        self.GBM_calibrated = True

    def calibrate_Bootstrap(self, Historical_Data, values_per_year_Bootstrap=255):
        """
        Method needs to be called when one wants to simulate with Bootstrap

        Parameters
        ----------
        :param Historical_Data: Historical values that will be used for bootstrapping
        :type Historical_Data: pandas DataFrame
        :param values_per_year_GBM: how many time-steps we want to include, default 255(number of trading days per year)
        :type values_per_year_GBM: int

        Examples
        --------
        Creation of an asset using historical data
        >>> hist_data = pd.read_csv("your_data.csv") #hist_data is one-row dataframe of past asset prices
        >>> asset = Underlying(100, 0.06)
        >>> asset.calibrate_Bootstrap(Historical_Data = hist_data, values_per_year_Bootstrap = 255)

        """

        self.Historical_Data = Historical_Data
        self.values_per_year_Bootstrap = values_per_year_Bootstrap
        self.Bootstrap_calibrated = True

    def calibrate_RT_GBM(self, sigma, time_steps, successors):
        """
        Method needs to be called when one wants to simulate with random tree

        Parameters
        ----------
        :param sigma: volatility of an asset
        :type sigma: float
        :param time_steps: how many time-steps we want to include, REMARK: time_steps > 5 will take ages to compute
        :type time_steps: int
        :param successors: how many new nodes in one step we create from one node,\n
         the greater the value, the narrower thi interval. REMARK: successors > 6 will take long
        :type successors: int

        Examples
        --------
        Creation of an asset
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_RT_GBM(0.4, 4, 3)
        """

        self.sigma = sigma
        self.time_steps = time_steps
        self.successors = successors
        self.RT_GBM_calibrated = True

    def calibrate_JD(self, sigma, jump_intensity, values_per_year_JD=255, a=0.2, b=0.25):
        """
        Method needs to be called when one wants to simulate with jump-diffusion model \n

        Parameters a and b are chosen so that ln(Yi) ~ N(a, b^2),
        with Yi being random variable describing multiplicative jumps ($Yi = S_{\tau_i}/S_{\tau_i-}$)

        Parameters
        ----------
        :param sigma: volatility of an asset
        :type sigma: float
        :param jump_intensity: parameter of Poisson process that is responsible for jumps in the model
        :type jump_intensity: float
        :param values_per_year_JD: how many time-steps we want to include, default 255(number of trading days per year)
        :type values_per_year_JD: int
        :param a:
        :type a: float
        :param b:
        :type b: float

        Examples
        --------
        Creation of an asset
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_JD(0.4, 0.4)
        """

        self.sigma = sigma
        self.jump_intensity = jump_intensity
        self.values_per_year_JD = values_per_year_JD
        self.a = a
        self.b = b
        self.JD_calibrated = True

    def simulate(self, mode, size, T=1):
        """
        Method that simulates asset development paths used in pricing

        Parameters
        ----------
        :param mode: Model in which simulations are performed, available values: "GBM", "Bootstrap", "RT_GBM", "JD"
        :type mode: str
        :param size: How many paths to simulate
        :type size: int
        :param T: Time horizon for simulation
        :type T: float

        Returns
        -------
        :return: Data frame having one simulation in each row
        :rtype: pandas.DataFrame

        Examples
        --------
        Creation of an asset
        >>> asset = Underlying(spot_price=100, r=0.06)
        >>> asset.calibrate_GBM(0.4, 255)
        >>> asset.simulate('GBM', 3, T=1)
                  0           1           2    ...         253         254         255
        0   99.999996  101.323642  100.757084  ...  155.495649  158.356571  154.573858
        1   99.999997  100.407545  101.755996  ...  121.491351  118.305042  121.353466
        2  100.000003  100.581243   99.541965  ...   92.986666   90.186351   90.603168
        [3 rows x 256 columns]

        >>> asset.calibrate_Bootstrap(hist_data, 255)
        >>> asset.simulate('Bootstrap', 3, T=1)

            0	        1	        2		...		254	        255
        0	100.0	98.388416	98.466800	...	174.518918	180.565038
        1	100.0	101.641189	101.824047  ...	89.923103	90.955017
        2	100.0	100.925334	101.018876	...	115.799699	114.339994
        [3 rows × 256 columns]
        """
        if mode == "GBM":
            if self.GBM_calibrated: #simulating in risk-free measure
                price_moments = np.arange(0, self.values_per_year_GBM * T + 1)
                Sigma = 1/self.values_per_year_GBM*np.minimum(np.tile(price_moments,(len(price_moments),1)),np.tile(price_moments.reshape(-1,1),(1,len(price_moments))))
                B = pd.DataFrame(np.random.multivariate_normal(size=size, mean= np.zeros(len(price_moments)), cov = Sigma))
                sims = self.spot_price*np.exp((self.r - 0.5 * self.sigma**2) * price_moments / self.values_per_year_GBM + self.sigma * B)
                #print(sims.shape)
                return(sims)
            else:
                raise Exception("GBM model has not been calibrated yet. Calibrate it with calibrate_GBM method first")
        elif mode == "Bootstrap":
            if self.Bootstrap_calibrated:
                price_moments = np.arange(0, round(self.values_per_year_Bootstrap * T) + 1)
                daily_mult_price_changes = (self.Historical_Data.iloc[:, (-round(self.values_per_year_Bootstrap * T)):].values / self.Historical_Data.iloc[:, (-round(self.values_per_year_Bootstrap * T)-1):(-1)].values)[0]
                sims = pd.DataFrame(np.reshape(np.random.choice(daily_mult_price_changes,size=len(price_moments)*size,replace=True),newshape=(size,round(self.values_per_year_Bootstrap * T) + 1)))
                sims.iloc[:, 0] = 1
                return(self.spot_price*sims.cumprod(axis="columns"))
            else:
                raise Exception("Boostrap model has not been calibrated yet. Calibrate it with calibrate_Bootstrap method first")
        elif mode == "RT_GBM":
            if self.RT_GBM_calibrated:
                delta_t = T/self.time_steps
                sims = []
                for _ in tqdm(range(size)):
                    sim = pd.DataFrame(np.zeros((self.successors ** self.time_steps, self.time_steps+1)))
                    sim.iloc[0, 0] = self.spot_price
                    for i in range(self.time_steps):
                        for j in range(self.successors ** i):
                            norm_dist = np.random.normal(loc=0, scale=1, size=self.successors)
                            vec = sim.iloc[j,i] * np.exp((self.r - 0.5 * self.sigma **2) * delta_t + self.sigma * np.sqrt(delta_t) * norm_dist)
                            sim.iloc[(j*self.successors):((j+1)*self.successors), i+1] = vec
                    sims.append(sim)
                return sims
            else:
                raise Exception("Random tree model has not been calibrated yet. Calibrate it with calibrate_RT_GBM method first")
        elif mode == "JD":
            if self.JD_calibrated:
                dt = T / self.values_per_year_JD
                ti = self.values_per_year_JD * T
                l = self.jump_intensity
                simulated_paths = np.zeros([size, ti + 1])

                simulated_paths[:, 0] = self.spot_price

                Z_1 = np.random.normal(size=[size, ti])
                Z_2 = np.random.normal(size=[size, ti])
                Poisson = np.random.poisson(l * dt, [size, ti])

                for i in range(ti):
                    simulated_paths[:, i + 1] = simulated_paths[:, i] * np.exp((self.r - self.sigma ** 2 / 2) * dt +
                                                                               self.sigma * np.sqrt(dt) * Z_1[:, i] + self.a * Poisson[:, i]
                                                                               + np.sqrt(self.b ** 2) * np.sqrt(Poisson[:, i]) * Z_2[:, i])

                return pd.DataFrame(simulated_paths)
            else:
                raise Exception(
                    "Jump diffusion model has not been calibrated yet. Calibrate it with calibrate_JD method first")
        else:
            raise Exception('''Chosen mode is not implemented. Choose mode from: "GBM", "Bootstrap", 'RT_GBM', "JD" ''')

