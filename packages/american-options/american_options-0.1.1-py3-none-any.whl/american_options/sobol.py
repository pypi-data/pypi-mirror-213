import numpy as np
import chaospy
import matplotlib.pyplot as plt
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D

#script showing how does the Sobol sequence work and why it is bebtter than random sampling for our case

dim = 2
n = 100
np.zeros((2,2,2))
sobol_sequence2d = chaospy.create_sobol_samples(n, dim)

# Generate a random sample from the uniform distribution
random_sample = np.random.uniform(0, 1, size=dim*n)
x2 = random_sample[:n]
y2 = random_sample[n:]

plt.scatter(x2, y2, label='Random uniform', s=1)
plt.scatter(sobol_sequence2d[0, :], sobol_sequence2d[1, :], label='Sobol sequence', s =1)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('2D Sobol sequence')
plt.legend()
plt.show()

#3D visualisation
dim = 3
n = 10
# Generate the Sobol sequence
sobol_sequence = chaospy.create_sobol_samples(n, dim)

x = sobol_sequence[0,:]
y = sobol_sequence[1,:]
z = sobol_sequence[2,:]

# Generate a random sample from the uniform distribution
random_sample = np.random.uniform(0, 1, size=dim*n)
x2 = random_sample[:n]
y2 = random_sample[n:2*n]
z2 = random_sample[2*n:]
# Create a figure and a 3D axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create the scatter plot
ax.scatter(x, y, z, label='Sobol sequence')
ax.scatter(x2, y2, z2, label='random uniform sequence')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Sobol sequence')
ax.legend()
# Show the plot
plt.show()


disc = np.exp(- r * dt)
n_bins = int(np.sqrt(n))
n_bins = 100
ti = 50
n_assets = 2
s = [0.3,0.4]
spot_price = [100, 110]
r = 0.06
dt = 1/ti
# generating Sobol sequence
# uniform
sobol_sequence = chaospy.create_sobol_samples(n_bins, n_assets)
representative_paths = np.zeros((n_bins, ti + 1, n_assets))  #
# representative paths

for a in range(n_assets):
    a = 0
    sobol_inv_norm = stats.norm.ppf(sobol_sequence[a, :])
    sigma = s[a]
    sobol_increments = np.hstack((np.zeros((n_bins, 1)),
                                  (r - sigma ** 2 / 2) * dt + sigma * np.sqrt(dt) * np.reshape(sobol_inv_norm,
                                                                                               (n_bins, ti))))
    sobol_increments = np.hstack((np.zeros((n_bins, 1)),np.tile(np.reshape((r - sigma ** 2 / 2) * dt + sigma * np.sqrt(dt) * (sobol_inv_norm), (n_bins, 1)), ti)))
    representative_paths[:, :, a] = spot_price[a] * np.exp(np.cumsum(sobol_increments, axis=1))



np.tile(np.reshape((r - sigma ** 2 / 2) * dt + sigma * np.sqrt(dt) * (sobol_inv_norm), (n_bins, 1)),5)