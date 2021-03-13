# This file generates a magnetic pattern. To be used in other files.

import numpy as np

class MagneticPattern:
    sensorCount = 20
    angleBetweenSensors = 2.5

    wavelet = np.array([-25, -25, -50, -50, -75, -75, -75, -50, -25, 0, 270, 550, 900, 1500, 2200, 1500, 900, 550, 270, 0, -25, -50, -75, -75, -75, -50, -50, -25, -25])
    expansion = 4

    magnetAbsolutePositions = np.array(
        [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345])
    # magnetPolarities shows signal magnitude and direction, possible values -1, 0 and 1 stand for N pole, P pole and no magnet
    magnetPolarities = [-1, -1, 0, -1, -1, 1, -1, 0, 0, -1, 0, 1, -1, 1, 0, -1, 1, 1, 0, 0, 1, 0, 1, 1]

    def __init__(self):
        segmentsInFullCircle = 360 / self.angleBetweenSensors

        # constructing a whole pattern
        self.pattern = np.zeros(int(self.expansion * segmentsInFullCircle))

        # calculates where magnets are in an expanded circle
        magnetExpandedPositions = self.magnetAbsolutePositions * len(self.pattern) / 360

        # places wavelets into a pattern
        #oddOrEven = 0
        magnet = 0
        for offset in magnetExpandedPositions:
            offset = int(np.floor(offset))
            for i in range(len(self.wavelet)):
                circularOffset = (offset + i - int(np.floor(len(self.wavelet) / 2))) % len(self.pattern)
                self.pattern[circularOffset] = self.pattern[circularOffset] + self.wavelet[i]*self.magnetPolarities[magnet]
            magnet = magnet + 1
