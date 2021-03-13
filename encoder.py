# this is just a class for common encoder variables

import numpy as np

class Encoder:
    # data from CAN bus
    target = 0
    position = 0
    sensor = np.zeros(20)

    # chart related variables
    pattern_axis = []
    pattern_line = []   # line that holds magnetic pattern
    sensor_line = []    # line that holds sensor data
    sensor_position_line = []  # vertical line that shows position

    pid_axis = []
    pid_plot_len = 20
    #pid_xval = np.arange(pid_plot_len)
    #encoder1_pid_yval = np.zeros(pid_plot_len)
    pid_target_values = np.zeros(pid_plot_len)
    pid_target_line = []
    pid_position_values = np.zeros(pid_plot_len)
    pit_position_line = []

    def update_pid(self, newTarget, newPosition):
        self.target = newTarget
        self.position = newPosition
        self.pid_target_values = np.roll(self.pid_target_values, -1)
        self.pid_target_values[self.pid_plot_len-1] = newTarget
        self.pid_position_values = np.roll(self.pid_position_values, -1)
        self.pid_position_values[self.pid_plot_len-1] = newPosition
