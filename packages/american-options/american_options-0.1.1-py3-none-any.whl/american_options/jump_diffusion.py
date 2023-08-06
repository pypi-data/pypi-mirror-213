import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def jump_diffusion(spot_price, T=1, mu=0.12, sigma=0.3, Lambda=0.25,
                   a=0.2, b=0.2, values_per_year=252, n_sim=100):
    '''
    Monte Carlo simulation [1] of Merton's Jump Diffusion Model [2].
    The model is specified through the stochastic differential equation (SDE):

                        dS(t)
                        ----- = mu*dt + sigma*dW(t) + dJ(t)
                        S(t-)

    with:

    mu, sigma: constants, the drift and volatility coefficients of the stock
               price process;
    W: a standard one-dimensional Brownian motion;
    J: a jump process, independent of W, with piecewise constant sample paths.
       It is defined as the sum of multiplicative jumps Y(j).

    Input
    ---------------------------------------------------------------------------
    S: float. The current asset price.
    T: int or float. The maturity of the option contract, i.e. the final
       monitoring date.
    mu, sigma: float. Respectively, the drift and volatility coefficients of
               the asset price process.
    Lambda: float. The intensity of the Poisson process in the jump diffusion
            model ('lambda' is a protected keyword in Python).
    a, b: float. Parameters required to calculate, respectively, the mean and
          variance of a standard lognormal distribution, log(x) ~ N(a, b**2).
          (see code).
    values_per_year: int. The number of monitoring dates, i.e. the time steps.
    n_sim: int. The number of Monte Carlo simulations (at least 10,000 required
          to generate stable results).

    '''


    # Calculate the length of the time step
    dt = T/values_per_year
    ti =values_per_year * T


    '''
    Generate an Nsim x (Nsteps+1) array of zeros to preallocate the simulated
    paths of the Monte Carlo simulation. Each row of the matrix represents a
    full, possible path for the stock, each column all values of the asset at
    a particular instant in time.
    '''
    simulated_paths = np.zeros([n_sim, ti+1])

    # Replace the first column of the array with the vector of initial price S
    simulated_paths[:,0] = spot_price

    '''
    To account for the multiple sources of uncertainty in the jump diffusion
    process, generate three arrays of random variables.

     - The first one is related to the standard Brownian motion, the component
       epsilon(0,1) in epsilon(0,1) * np.sqrt(dt);
     - The second and third ones model the jump, a compound Poisson process:
       the former (a Poisson process with intensity Lambda) causes the asset
       price to jump randomly (random timing); the latter (a Gaussian variable)
       defines both the direction (sign) and intensity (magnitude) of the jump.
    '''
    Z_1 = np.random.normal(size=[n_sim, ti])
    Z_2 = np.random.normal(size=[n_sim, ti])
    Poisson = np.random.poisson(Lambda*dt, [n_sim, ti])

    # Populate the matrix with Nsim randomly generated paths of length ti
    for i in range(ti):
        simulated_paths[:,i+1] = simulated_paths[:,i]*np.exp((mu
                               - sigma**2/2)*dt + sigma*np.sqrt(dt) \
                               * Z_1[:,i] + a*Poisson[:,i] \
                               + np.sqrt(b**2) * np.sqrt(Poisson[:,i]) \
                               * Z_2[:,i])
    return simulated_paths
# Single out array of simulated prices at maturity T
T=1
r=0.06
values_per_year=255
ti = T*values_per_year
sims = jump_diffusion(spot_price=100,T=T,mu=r,values_per_year=values_per_year)

# Choose palette, figure size, and define figure axes
sns.set(palette='viridis')
plt.figure(figsize=(10,8))
ax = plt.axes()

# Generate t, the time variable on the abscissae
t = np.linspace(0, T, values_per_year+1) * ti

# Plot the Monte Carlo simulated stock price paths
jump_diffusion = ax.plot(t, sims.transpose());

# Make drawn paths thinner by decreasing line width
plt.setp(jump_diffusion, linewidth=1);

# Set title (LaTeX notation) and x- and y- labels
ax.set(title="Monte Carlo simulated stock price paths in Merton's jump \
diffusion model\n$S_0$ = {}, $\mu$ = {}, $\sigma$ = {}, $a$ = {}, $b$ = {}, \
$\lambda$ = {}, $T$ = {}, Nsteps = {}, Nsim = {}"\
       .format(S, mu, sigma, a, b, Lambda, T, Nsteps, Nsim), \
       xlabel='Time (days)', ylabel='Stock price')

# Display figure in a Python environment
plt.show()
