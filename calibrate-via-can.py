import can
import cantools
import threading

# request user input
# which node to calibrate
print('Which node to calibrate? Enter 1, 2 or 3:')
node = input()
message_ids = []
if node == '1':
    message_ids = [1297, 1298, 1299]
elif node == '2':
    message_ids = [1313, 1314, 1315]
elif node == '3':
    message_ids = [1329, 1330, 1331]
else:
    print('Node ' + node + ' does not exist! Aborted.')
    quit()

numberOfPositions = 256

# set up can bus
bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=1000000)
bus.set_filters([
{"can_id": message_ids[0], "can_mask": 0x7ff, "extended": False},
{"can_id": message_ids[1], "can_mask": 0x7ff, "extended": False},
{"can_id": message_ids[2], "can_mask": 0x7ff, "extended": False}
])
db = cantools.db.load_file('canbus8.dbc')

# dictionary that holds raw CAN messages
CAN_messages = {message_ids[0]: [], message_ids[1]: [], message_ids[2]: []}

# function run in a separate thread, reads can messages and stores them in a dictionary
program_running = True
def can_process():
    for msg in bus:
        CAN_messages[msg.arbitration_id] = msg    # saves raw message in dictionary, to be processed later
        if program_running == False:
            break

# create and start can bus message processing thread
can_msg_input_thread = threading.Thread(target=can_process)
can_msg_input_thread.start()

# open a file for writing
f = open('sensor_positions.h', 'w')
f.write('// This sensor position data file is generated with calibrate-via-can.py script.\n')
f.write('#define POSITION_COUNT ' + str(numberOfPositions) + '\n')
#f.write('#define SENSOR_COUNT 20\n')
f.write('\n')
f.write('const uint32_t sensorValueTable[POSITION_COUNT][5] = {\n')


for position in range(numberOfPositions):
    print('Set module to position ' + str(position) + ' (' + hex(position) + ') and press "Enter"')
    input() # waits for enter, rest of the input string is not needed

    # decodes sensor readings from can messages
    group_1_2 = db.decode_message(CAN_messages[message_ids[0]].arbitration_id, CAN_messages[message_ids[0]].data)
    group_3_4 = db.decode_message(CAN_messages[message_ids[1]].arbitration_id, CAN_messages[message_ids[1]].data)
    group_5 = db.decode_message(CAN_messages[message_ids[2]].arbitration_id, CAN_messages[message_ids[2]].data)

    str1 = ('0x' +
    ''.join('{:02X}'.format(group_1_2.get('Sensor3'))) +
    ''.join('{:02X}'.format(group_1_2.get('Sensor2'))) +
    ''.join('{:02X}'.format(group_1_2.get('Sensor1'))) +
    ''.join('{:02X}'.format(group_1_2.get('Sensor0'))))
    str2 = ('0x' +
    ''.join('{:02X}'.format(group_1_2.get('Sensor7'))) +
    ''.join('{:02X}'.format(group_1_2.get('Sensor6'))) +
    ''.join('{:02X}'.format(group_1_2.get('Sensor5'))) +
    ''.join('{:02X}'.format(group_1_2.get('Sensor4'))))
    str3 = ('0x' +
    ''.join('{:02X}'.format(group_3_4.get('Sensor11'))) +
    ''.join('{:02X}'.format(group_3_4.get('Sensor10'))) +
    ''.join('{:02X}'.format(group_3_4.get('Sensor9'))) +
    ''.join('{:02X}'.format(group_3_4.get('Sensor8'))))
    str4 = ('0x' +
    ''.join('{:02X}'.format(group_3_4.get('Sensor15'))) +
    ''.join('{:02X}'.format(group_3_4.get('Sensor14'))) +
    ''.join('{:02X}'.format(group_3_4.get('Sensor13'))) +
    ''.join('{:02X}'.format(group_3_4.get('Sensor12'))))
    str5 = ('0x' +
    ''.join('{:02X}'.format(group_5.get('Sensor19'))) +
    ''.join('{:02X}'.format(group_5.get('Sensor18'))) +
    ''.join('{:02X}'.format(group_5.get('Sensor17'))) +
    ''.join('{:02X}'.format(group_5.get('Sensor16'))))

    f.write('{' +
    str1 + ', ' +
    str2 + ', ' +
    str3 + ', ' +
    str4 + ', ' +
    str5 +
    '},\n')

'''
    f.write('{' +
    str(group1.get('Sensor0')) + ', ' +
    str(group1.get('Sensor1')) + ', ' +
    str(group1.get('Sensor2')) + ', ' +
    str(group1.get('Sensor3')) + ', ' +
    str(group2.get('Sensor4')) + ', ' +
    str(group2.get('Sensor5')) + ', ' +
    str(group2.get('Sensor6')) + ', ' +
    str(group2.get('Sensor7')) + ', ' +
    str(group3.get('Sensor8')) + ', ' +
    str(group3.get('Sensor9')) + ', ' +
    str(group3.get('Sensor10')) + ', ' +
    str(group3.get('Sensor11')) + ', ' +
    str(group4.get('Sensor12')) + ', ' +
    str(group4.get('Sensor13')) + ', ' +
    str(group4.get('Sensor14')) + ', ' +
    str(group4.get('Sensor15')) + ', ' +
    str(group5.get('Sensor16')) + ', ' +
    str(group5.get('Sensor17')) + ', ' +
    str(group5.get('Sensor18')) + ', ' +
    str(group5.get('Sensor19')) +
    '},\n')
'''
'''
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
'''

# finish file writing
f.write('};\n')
f.close()

# signal thread to exit
program_running = False
