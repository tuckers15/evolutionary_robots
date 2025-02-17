import matplotlib.pyplot as plt
import numpy as np


frontLegData = np.load('data/frontLegValues.npy')
backLegData = np.load('data/backLegValues.npy')

plt.plot(frontLegData, label="Front Leg", linewidth="3")
plt.plot(backLegData, label="Back Leg")
plt.legend()
plt.show()