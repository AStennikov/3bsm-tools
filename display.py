# this file creates live plot which shows encoder position and PID loop information

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import can
import cantools
from magneticPattern import MagneticPattern
from encoder import Encoder
import threading

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

# dictionary that holds raw CAN messages
sensor_CAN = {0x510: [], 0x511: [], 0x512: [], 0x513: [], 0x514: [], 0x515: []}

# function run in a separate thread, reads can messages and stores them in a dictionary
program_running = True
def can_process():
    for msg in bus:
        sensor_CAN[msg.arbitration_id] = msg    # saves raw message in dictionary, to be processed later

        # unlike sensor messages, messages containing pid information must be processed
        if msg.arbitration_id == 0x510:
            dict = db.decode_message(msg.arbitration_id, msg.data)
            encoder1.update_pid(dict.get('target'), dict.get('position'))

        if program_running == False:
            break

# create and start can message input thread
can_msg_input_thread = threading.Thread(target=can_process)
can_msg_input_thread.start()


def update(frame):
    # update sensor data
    group1 = db.decode_message(sensor_CAN[0x511].arbitration_id, sensor_CAN[0x511].data)
    encoder1.sensor[0] = group1.get('Sensor0')
    encoder1.sensor[1] = group1.get('Sensor1')
    encoder1.sensor[2] = group1.get('Sensor2')
    encoder1.sensor[3] = group1.get('Sensor3')

    group2 = db.decode_message(sensor_CAN[0x512].arbitration_id, sensor_CAN[0x512].data)
    encoder1.sensor[4] = group2.get('Sensor4')
    encoder1.sensor[5] = group2.get('Sensor5')
    encoder1.sensor[6] = group2.get('Sensor6')
    encoder1.sensor[7] = group2.get('Sensor7')

    group3 = db.decode_message(sensor_CAN[0x512].arbitration_id, sensor_CAN[0x512].data)
    encoder1.sensor[8] = group3.get('Sensor8')
    encoder1.sensor[9] = group3.get('Sensor9')
    encoder1.sensor[10] = group3.get('Sensor10')
    encoder1.sensor[11] = group3.get('Sensor11')

    group4 = db.decode_message(sensor_CAN[0x512].arbitration_id, sensor_CAN[0x512].data)
    encoder1.sensor[12] = group4.get('Sensor12')
    encoder1.sensor[13] = group4.get('Sensor13')
    encoder1.sensor[14] = group4.get('Sensor14')
    encoder1.sensor[15] = group4.get('Sensor15')

    group5 = db.decode_message(sensor_CAN[0x512].arbitration_id, sensor_CAN[0x512].data)
    encoder1.sensor[16] = group5.get('Sensor16')
    encoder1.sensor[17] = group5.get('Sensor17')
    encoder1.sensor[18] = group5.get('Sensor18')
    encoder1.sensor[19] = group5.get('Sensor19')

    # update plot lines
    encoder1.sensor_line.set_xdata(np.arange(start=encoder1.position, stop = encoder1.position+len(encoder1.sensor)*4, step=4))
    encoder1.sensor_line.set_ydata(encoder1.sensor)
    encoder1.sensor_position_line.set_xdata([encoder1.position, encoder1.position])

    encoder1.pid_target_line.set_ydata(encoder1.pid_target_values)
    encoder1.pid_position_line.set_ydata(encoder1.pid_position_values)

    return encoder1.sensor_line, encoder1.sensor_position_line, encoder1.pid_target_line, encoder1.pid_position_line



ani = FuncAnimation(fig, update, interval=100, blit=True)

plt.tight_layout()
plt.show()

program_running = False    # this stops all threads
