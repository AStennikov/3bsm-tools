# this is just a class for common encoder variables

import numpy as np

class Encoder:
    # data from CAN bus
    target = 0
    position = 0
    pwm = 0
    kpi = 0
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
    pid_pwm_values = np.zeros(pid_plot_len)
    pit_pwm_line = []
    pid_kpi_values = np.zeros(pid_plot_len)
    pit_kpi_line = []

    def update_pid(self, newTarget, newPosition, newPWM, newKPI):
        self.target = newTarget
        self.position = newPosition
        self.pwm = newPWM
        self.kpi = newKPI
        self.pid_target_values = np.roll(self.pid_target_values, -1)
        self.pid_target_values[self.pid_plot_len-1] = newTarget
        self.pid_position_values = np.roll(self.pid_position_values, -1)
        self.pid_position_values[self.pid_plot_len-1] = newPosition
        self.pid_pwm_values = np.roll(self.pid_pwm_values, -1)
        self.pid_pwm_values[self.pid_plot_len-1] = newPWM
        self.pid_kpi_values = np.roll(self.pid_kpi_values, -1)
        self.pid_kpi_values[self.pid_plot_len-1] = newKPI
