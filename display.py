# this file creates live plot which shows encoder position and PID loop information

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import can
import cantools
from magneticPattern import MagneticPattern
from encoder import Encoder

# creates magnetic pattern
mp = MagneticPattern()

# configures and connects to CAN bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)
db = cantools.db.load_file('canbus.dbc')


encoder1 = Encoder()
encoder2 = Encoder()
encoder3 = Encoder()

# plot setup
fig = plt.figure()
encoder1.pattern_axis = fig.add_subplot(321)
encoder1.pattern_axis.set_xlim(0, len(mp.pattern))
encoder1.pattern_axis.set_ylim(-2048,2048)
encoder1.pattern_line, = encoder1.pattern_axis.plot(0, 0)
encoder1.pattern_line.set_xdata(np.arange(len(mp.pattern)))
encoder1.pattern_line.set_ydata(mp.pattern)
encoder1.sensor_line, = encoder1.pattern_axis.plot(0, 0)
encoder1.sensor_line.set_xdata(np.arange(len(encoder1.sensor)))
encoder1.sensor_line.set_ydata(encoder1.sensor)
encoder1.sensor_position_line, = encoder1.pattern_axis.plot(0, 0)
encoder1.sensor_position_line.set_xdata([encoder1.position, encoder1.position])
encoder1.sensor_position_line.set_ydata([-2048, 2048])

encoder1.pid_axis = fig.add_subplot(322)
encoder1.pid_axis.set_xlim(0, encoder1.pid_plot_len)
encoder1.pid_axis.set_ylim(0,len(mp.pattern))
encoder1.pid_target_line, = encoder1.pid_axis.plot(0, 0)
encoder1.pid_target_line.set_xdata(np.arange(encoder1.pid_plot_len))
encoder1.pid_target_line.set_ydata(encoder1.pid_target_values)
encoder1.pid_position_line, = encoder1.pid_axis.plot(0, 0)
encoder1.pid_position_line.set_xdata(np.arange(encoder1.pid_plot_len))
encoder1.pid_position_line.set_ydata(encoder1.pid_position_values)

def update(frame):
    # get messages from bus
    for msg in bus:
        if msg.arbitration_id == 0x510:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.update_pid(dict.get('target'), dict.get('position'))
        if msg.arbitration_id == 0x511:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.sensor[0] = dict.get('Sensor0')
            encoder1.sensor[1] = dict.get('Sensor1')
            encoder1.sensor[2] = dict.get('Sensor2')
            encoder1.sensor[3] = dict.get('Sensor3')
        if msg.arbitration_id == 0x512:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.sensor[4] = dict.get('Sensor4')
            encoder1.sensor[5] = dict.get('Sensor5')
            encoder1.sensor[6] = dict.get('Sensor6')
            encoder1.sensor[7] = dict.get('Sensor7')
        if msg.arbitration_id == 0x513:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.sensor[8] = dict.get('Sensor8')
            encoder1.sensor[9] = dict.get('Sensor9')
            encoder1.sensor[10] = dict.get('Sensor10')
            encoder1.sensor[11] = dict.get('Sensor11')
        if msg.arbitration_id == 0x514:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.sensor[12] = dict.get('Sensor12')
            encoder1.sensor[13] = dict.get('Sensor13')
            encoder1.sensor[14] = dict.get('Sensor14')
            encoder1.sensor[15] = dict.get('Sensor15')
        if msg.arbitration_id == 0x515:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.sensor[16] = dict.get('Sensor16')
            encoder1.sensor[17] = dict.get('Sensor17')
            encoder1.sensor[18] = dict.get('Sensor18')
            encoder1.sensor[19] = dict.get('Sensor19')
            #print('Target: ' + str(encoder1.target) + ', position: ' + str(encoder1.position))
            break

    # update plot lines
    encoder1.sensor_line.set_xdata(np.arange(start=encoder1.position, stop = encoder1.position+len(encoder1.sensor)*4, step=4))
    encoder1.sensor_line.set_ydata(encoder1.sensor)
    encoder1.sensor_position_line.set_xdata([encoder1.position, encoder1.position])

    encoder1.pid_target_line.set_ydata(encoder1.pid_target_values)
    encoder1.pid_position_line.set_ydata(encoder1.pid_position_values)

    #ax1_line.set_ydata(sensorReadings)
    #return ax1_line,
    return encoder1.sensor_line, encoder1.sensor_position_line, encoder1.pid_target_line, encoder1.pid_position_line

ani = FuncAnimation(fig, update, interval=100, blit=True)

plt.tight_layout()
plt.show()

'''
ax1.set_xlim(0,20)
ax1.set_ylim(-2048,2048)
ax1.set_ylabel('value')
ax1.set_ylabel('sensor')

ax1_line, = ax1.plot(0, 0)
ax1_line.set_xdata(xData)
ax1_line.set_ydata(yData)'''
