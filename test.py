# me testing all sorts of python things here

# combining uint8_t[4] into a single uint32_t
char_array = [0xaa, 0xff, 0x11, 0x00]

line = '0x' + ''.join('{:02X}'.format(i) for i in char_array)
print(''.join('{:02X}'.format(char_array[0])) + ''.join('{:02X}'.format(char_array[1])))
#line = str(hex(char_array[0])) + str(hex(char_array[1]))[2:] + str(hex(char_array[2]))[2:] + str(hex(char_array[3]))[2:]
print(char_array)
print(line)
