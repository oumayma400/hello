import serial
import time
import getopt
import sys
from struct import *
import sys,os
from pathlib import Path

path = Path(os.path.abspath(__file__))
parrent_path = path.parent.absolute()
Read_ConfigLib = os.path.dirname(parrent_path) + os.path.sep + "Read_Config";
Read_ConfigLib2 = Read_ConfigLib.replace('\\', '/')
sys.path.append(Read_ConfigLib2)

# sys.path.append('C:/Users/g361355/Desktop/ROBOT_ECLIPSE/E2E-AUTO-SICONIA/Libraries/Read_Config')
import ReadConfigFile as conf

# SERIAL_PATH = '/dev/ttyACM0'
BAUD_RATE = 9600

commands = {
    'relay_1_on': 0x65,
    'relay_1_off': 0x6F,
    'relay_2_on': 0x66,
    'relay_2_off': 0x70,
    'info': 0x5A,
    'relay_states': 0x5B,
}

def send_command(PROJECT ,cmd, read_response = False):
    com = conf.ReadConfigFile.read(PROJECT,'com_relay')
    ser = serial.Serial(com, 9600)
    strcmd = chr(cmd)+'\n'
    ser.write(strcmd.encode())
    response = read_response and ser.read() or None
    ser.close()
    return response

def turn_relay_1_on(PROJECT):
    send_command(PROJECT,commands['relay_1_on'])

def turn_relay_1_off(PROJECT):
    send_command(PROJECT,commands['relay_1_off'])

def click_relay_1(PROJECT):
    send_command(PROJECT,commands['relay_1_on'])
    time.sleep(1)
    send_command(PROJECT,commands['relay_1_off'])

def turn_relay_2_on(PROJECT):
    send_command(PROJECT,commands['relay_2_on'])

def turn_relay_2_off(PROJECT):
    send_command(PROJECT, commands['relay_2_off'])

def click_relay_2(PROJECT):
    send_command(PROJECT, commands['relay_2_on'])
    time.sleep(1)
    send_command(PROJECT, commands['relay_2_off'])

def get_relay_states(PROJECT):
    states = send_command(PROJECT, commands['relay_states'], read_response=True)
    response = unpack('b',states)[0]
    states =  {
        0: {'1': False, '2': False},
        1: {'1': True, '2': False},
        2: {'1': False, '2': True},
        3: {'1': True, '2': True},
    }
    return states[response]

def usage():
    print ("""Change relay status:
    python rly02.py -r [1,2] -a [on, off, click]
Get device info:
    python rly02.py -i
Get relay states:
    python rly02.py -s
Help!;
    python rly02.py -h
""")

# turn_relay_1_on()
# time.sleep(3)
# turn_relay_1_off()
#
# if __name__ == '__main__':
#
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "hr:a:is", ["help",None, None, "info", "states"])
#         dict_opts = {}
#         for o,a in opts:
#             dict_opts[o] = a
#     except getopt.GetoptError:
#         print
#         usage()
#         sys.exit(2)
#
#     for o, a in opts:
#         if o in ("-r",):
#             if a in ['1', '2']:
#                 relay = a
#                 if dict_opts.has_key('-a') and\
#                     dict_opts['-a'] in ['on','off','click']:
#                     action = dict_opts['-a']
#
#                     actions = {
#                         '1_on' : lambda: turn_relay_1_on(),
#                         '1_off' : lambda: turn_relay_1_off(),
#                         '1_click' : lambda: click_relay_1(),
#                         '2_on' : lambda: turn_relay_2_on(),
#                         '2_off' : lambda: turn_relay_2_off(),
#                         '2_click' : lambda: click_relay_2(),
#                     }
#                     actions['%s_%s'%(relay, action)]()
#
#                     sys.exit()
#                 else:
#                     print "Action must be on, off or click"
#             else:
#                 print "Relay must be 1 or 2"
#
#         elif o in ("-s", "--states"):
#             print get_relay_states()
#             sys.exit()
#
#     usage()
#     sys.exit()
