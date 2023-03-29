import matplotlib.pyplot as plt
import numpy as np

img = np.full((255, 255), 1)
img[:] = np.arange(0, 255)

fig = plt.figure()
ax1, ax2 = fig.subplots(2, 1)
ax1.imshow(img)
ax2.plot(range(20), "r^")

print("Plot View - Python Debug")