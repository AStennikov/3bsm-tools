# This script generates magnetic pattern, displays it and prints a C string.

from magneticPattern import MagneticPattern
import matplotlib.pyplot as plt
import numpy as np

mp = MagneticPattern()

print('Pattern length: ' + str(len(mp.pattern)))
print('Pattern as a C-style array:')
for item in mp.pattern:
    print(str(int(item)) + ', ', end='')


fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Wavelet and magnetic pattern. Check terminal for c string')
ax1.plot(np.arange(len(mp.wavelet)), mp.wavelet)
ax2.plot(np.arange(len(mp.pattern)), mp.pattern)


plt.tight_layout()
plt.show()
