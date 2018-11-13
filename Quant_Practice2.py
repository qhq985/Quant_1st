import numpy as np
import math
import scipy.stats as sp
import time
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

# Initial the variables
ttm = 3.0
tSteps = 25
r = 0.03
d = 0.02 # dividend
sigma = 0.2
strike = 100
spot = 100

def call_payoff(spot):
    global strike
    return max(spot-strike, 0)


dt = ttm/tSteps
up = math.exp((r - d - sigma**2/2)*dt + sigma*math.sqrt(dt))
down = math.exp((r - d -sigma**2/2)*dt - sigma*math.sqrt(dt))
discount = math.exp(-r*dt)

# Construct the binary tree
lattice = np.zeros((tSteps+1,tSteps+1))
lattice[0][0] = spot
for i in range(tSteps):
    for j in range(i+1):
        lattice[i+1][j+1] = up*lattice[i][j]
    lattice[i+1][0] = down * lattice[i][0]

print(lattice)
plt.figure()
plt.plot(lattice[tSteps])
plt.title('Distribution of binary price', fontsize = 20)



plt.show()


