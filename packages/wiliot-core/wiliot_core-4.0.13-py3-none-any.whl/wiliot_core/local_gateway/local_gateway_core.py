"""
Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.

Redistribution and use of the Software in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice,
  this list of conditions and the following disclaimer.

  2. Redistributions in binary form, except as used in conjunction with
  Wiliot's Pixel in a product or a Software update for such product, must reproduce
  the above copyright notice, this list of conditions and the following disclaimer in
  the documentation and/or other materials provided with the distribution.

  3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
  may be used to endorse or promote products or services derived from this Software,
  without specific prior written permission.

  4. This Software, with or without modification, must only be used in conjunction
  with Wiliot's Pixel or with Wiliot's cloud service.

  5. If any Software is provided in binary form under this license, you must not
  do any of the following:
  (a) modify, adapt, translate, or create a derivative work of the Software; or
  (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
  discover the source code or non-literal aspects (such as the underlying structure,
  sequence, organization, ideas, or algorithms) of the Software.

  6. If you create a derivative work and/or improvement of any Software, you hereby
  irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
  royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
  right and license to reproduce, use, make, have made, import, distribute, sell,
  offer for sale, create derivative works of, modify, translate, publicly perform
  and display, and otherwise commercially exploit such derivative works and improvements
  (as applicable) in conjunction with Wiliot's products and services.

  7. You represent and warrant that you are not a resident of (and will not use the
  Software in) a country that the U.S. government has embargoed for use of the Software,
  nor are you named on the U.S. Treasury Department’s list of Specially Designated
  Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
  You must not transfer, export, re-export, import, re-import or divert the Software
  in violation of any export or re-export control laws and regulations (such as the
  United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
  and use restrictions, all as then in effect

THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
(SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
(A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
(B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
(C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
"""

import socket
import threading
import multiprocessing as mp
import serial
import datetime
import os
import time
import serial.tools.list_ports
from enum import Enum
from collections import deque
from queue import Queue, Empty
import logging
from wiliot_core.packet_data.packet_list import PacketList
from wiliot_core.local_gateway.continuous_listener import SerialProcess, SerialProcessState
from wiliot_core.packet_data.packet import Packet
import re
import subprocess
import shlex


DECRYPTION_MODE = False
try:
    from wiliot_core.packet_data.extended.decrypted_packet_list import DecryptedPacketList
    from wiliot_core.packet_data.extended.decrypted_packet import DecryptedPacket
    DECRYPTION_MODE = True
except Exception as e:
    # print(e)
    pass


# parameters:
packet_length = 78
packet_prefix_str = "process_packet"
sub_1g_min_pattern_num = 50
sub_1g_max_pattern_num = 61
valid_bb = (0, 2, 7, 12, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 33, 36, 40)
valid_sub1g_output_power = list(range(17, 29 + 1))
valid_output_power_vals = [
    {'abs_power': -21, 'gw_output_power': 'neg20dBm', 'bypass_pa': '1'},
    {'abs_power': -18, 'gw_output_power': 'neg16dBm', 'bypass_pa': '1'},
    {'abs_power': -15, 'gw_output_power': 'neg12dBm', 'bypass_pa': '1'},
    {'abs_power': -12, 'gw_output_power': 'neg8dBm', 'bypass_pa': '1'},
    {'abs_power': -8, 'gw_output_power': 'neg4dBm', 'bypass_pa': '1'},
    {'abs_power': -5, 'gw_output_power': 'pos0dBm', 'bypass_pa': '1'},
    {'abs_power': -2, 'gw_output_power': 'pos2dBm', 'bypass_pa': '1'},
    {'abs_power': -1, 'gw_output_power': 'pos3dBm', 'bypass_pa': '1'},
    {'abs_power': 0, 'gw_output_power': 'pos4dBm', 'bypass_pa': '1'},
    {'abs_power': 1, 'gw_output_power': 'pos5dBm', 'bypass_pa': '1'},
    {'abs_power': 2, 'gw_output_power': 'pos6dBm', 'bypass_pa': '1'},
    {'abs_power': 3, 'gw_output_power': 'pos7dBm', 'bypass_pa': '1'},
    {'abs_power': 4, 'gw_output_power': 'pos8dBm', 'bypass_pa': '1'},
    {'abs_power': 6, 'gw_output_power': 'neg12dBm', 'bypass_pa': '0'},
    {'abs_power': 10, 'gw_output_power': 'neg8dBm', 'bypass_pa': '0'},
    {'abs_power': 15, 'gw_output_power': 'neg4dBm', 'bypass_pa': '0'},
    {'abs_power': 20, 'gw_output_power': 'pos0dBm', 'bypass_pa': '0'},
    {'abs_power': 21, 'gw_output_power': 'pos2dBm', 'bypass_pa': '0'},
    {'abs_power': 22, 'gw_output_power': 'pos3dBm', 'bypass_pa': '0'}
]
cmds_no_default_ack = ['print', 'set_energizing_pattern', 'move_to_bootloader', 'version', 'pce', 'trigger_pl']


class ConfigParam:
    def __init__(self):
        self.energy_pattern = None
        self.received_channel = None
        self.time_profile_on = None
        self.time_profile_period = None
        self.beacons_backoff = None
        self.pacer_val = None
        self.filter = None
        self.pl_delay = None
        self.rssi_thr = None
        self.effective_output_power = None
        self.output_power = None
        self.bypass_pa = None


class PacketStruct:
    def __init__(self, packet):
        self.packet = packet
        self.adv_address = ''
        self.group_id = ''
        self.rssi = None
        self.stat_param = None

    def fill_packet(self, packet_content):
        self.packet = self.get_packet_content(packet_content)
        self.adv_address = self.packet[:12]
        self.group_id = self.packet[20:26]
        self.rssi = self.packet[74:76]
        self.stat_param = self.packet[76:80]

    @staticmethod
    def tag_packet_content(packet):
        if packet.startswith("process_packet"):
            try:
                packet_content = packet.split('"')[1]
            except Exception as e:
                print("Failed to get packet content from packet {} with exception: {}".format(packet, e))
                packet_content = ''
            return packet_content
        else:
            return ''

    @staticmethod
    def get_packet_content(packet_str):
        if packet_str.startswith("process_packet"):
            return packet_str.split('"')[1]
        else:
            return packet_str

    @staticmethod
    def is_short_packet(packet):
        return len(packet) < packet_length


class ActionType(Enum):
    ALL_SAMPLE = 'all_samples'
    FIRST_SAMPLES = 'first_samples'
    CURRENT_SAMPLES = 'current_samples'


class DataType(Enum):
    RAW = 'raw'
    PROCESSED = 'processed'
    PACKET_LIST = 'packet_list'
    DECODED = 'decoded_packet'


class DualGWMode(Enum):
    STATIC = 'static'  # the additional gw is on all the time
    MIRROR = 'mirror'  # the additional gw is on when the main gw is on and vice versa
    DYNAMIC = 'dynamic'  # the additional gw s on when the main gw is off and vice versa


class StatType(Enum):
    N_FILTERED_PACKETS = 'n_filtered_packets'
    GW_PACKET_TIME = 'gw_packet_time'


class WiliotGateway(object):
    """
    Wiliot Gateway (GW) API

    * the baud rate is defined to baud value and saved
    * If the port is defined (no None) than automatically try to connect to GW according to the port and baud.
    * If not, Run function FindCOMPorts to find all available ports and saves them
    * If the auto_connect is TRUE, then the function Open is running on each port until a connection is established.

    :type baud: int
    :param baud: the GW baud rate
    :type port: str
    :param port: The GW port if it is already know.
    :type auto_connect: bool
    :param auto_connect: If TRUE, connect automatically to the GW.

    :exception during open serial port process
    """

    def __init__(self, baud=921600, port=None, auto_connect=False, lock_print=None, logger_name=None, verbose=True,
                 socket_host='localhost', socket_port=2022, is_multi_processes=False, log_dir_for_multi_processes=None):
        """
        :type baud: int
        :param baud: the GW baud rate
        :type port: str
        :param port: The GW port if it is already know.
        :type auto_connect: bool
        :param auto_connect: If TRUE, connect automatically to the GW.
        :type lock_print: threading.Lock()
        :param lock_print: used for async printing
        :type logger_name: str
        :param logger_name: the logger name using 'logging' python package add printing information to the log.
                            (the default logger name when using 'logging' is 'root')

        :exception:
        * could not open port 'COMX'... - make sure the baud rate is correct. if port specified, check if correct
        """
        # Constants:
        self.valid_output_power_vals = valid_output_power_vals

        # initialization attributes:
        # -------------------------- #
        # locking variables:
        self._lock_read_serial = threading.Lock()
        if lock_print is None:
            self._lock_print = threading.Lock()
        else:
            self._lock_print = lock_print

        # flag variable:
        self._is_running_analysis = False
        self.available_data = False
        self.connected = False
        self.reading_exception = False
        self.verbose = verbose

        # serial port variables:
        self._comPortObj = None
        self.port = ''
        self.baud = baud
        self.write_wait_time = 0.001  # [sec]

        # GW variables:
        self.config_param = ConfigParam()
        self.sw_version = ''
        self.hw_version = ''

        # data variables:
        self.exceptions_threads = ['', '']
        self._processed = deque()
        self._port_listener_thread = None

        # multi-processing
        self.multi_process = is_multi_processes
        if self.multi_process:
            cmd_serial_process_q = mp.Queue(maxsize=100)
            com_rsp_str_input_q = mp.Queue(maxsize=100)
            com_pkt_str_input_q = mp.Queue(maxsize=1000)
            connected_event = mp.Event()
            read_error_event = mp.Event()
            self._port_listener_thread = mp.Process(target=SerialProcess,
                                                    args=(cmd_serial_process_q,
                                                          com_rsp_str_input_q,
                                                          com_pkt_str_input_q,
                                                          connected_event,
                                                          read_error_event,
                                                          log_dir_for_multi_processes))
            self._port_listener_thread.start()

            self.cmd_serial_process_q = cmd_serial_process_q
            self.com_rsp_str_input_q = com_rsp_str_input_q
            self.com_pkt_str_input_q = com_pkt_str_input_q
            self.connected_event = connected_event
            self.read_error_event = read_error_event
        else:
            self.cmd_serial_process_q = None
            self.connected_event = None
            self.read_error_event = None
            self.com_rsp_str_input_q = Queue(maxsize=100)
            self.com_pkt_str_input_q = Queue(maxsize=1000)

        self.start_time_lock = threading.Lock()
        self.stop_listen_event = threading.Event()

        self.continuous_listener_enabled = False
        self.start_time = datetime.datetime.now()

        # socket communication:
        self.server_socket = None
        self.client_conn = None
        self.try_to_connect_to_client = False
        self.socket_host = socket_host
        self.socket_port = socket_port
        self.init_socket_connection_thread = None

        # logging:
        if logger_name is None:
            self._do_log = True
            self.logger = logging.getLogger("root")
            if verbose:
                self.logger.setLevel(logging.DEBUG)
            else:
                self.logger.setLevel(logging.INFO)
        else:
            self._do_log = True
            self.logger = logging.getLogger(logger_name)

        # connection:
        # -------------- #
        # connect automatically if port is specified
        if port is not None:
            if self.open_port(port, self.baud):
                self._printing_func("connection was established: {}={}".format(self.hw_version, self.sw_version),
                                    'init')
                self.connected = True
                return

        # if port is None - let's search for all available ports
        self.available_ports = [s.device for s in serial.tools.list_ports.comports()
                                if 'Silicon Labs' in s.description or 'CP210' in s.description]
        if len(self.available_ports) == 0:
            self.available_ports = [s.name for s in serial.tools.list_ports.comports()
                                    if 'Silicon Labs' in s.description or 'CP210' in s.description]
            if len(self.available_ports) == 0:
                self._printing_func("no serial ports were found. please check your connections", "init", True)
                return

        # if user want to connect automatically - connecting to the first available COM with valid gw version
        if auto_connect:
            for p in self.available_ports:
                try:
                    if self.open_port(p, self.baud):
                        self._printing_func("connection was established: {}={} , port {}".
                                            format(self.hw_version, self.sw_version, p), 'init')
                        self.connected = True
                        break
                except Exception as e:
                    self._printing_func("tried to connect {} but failed, moving to the next port".format(p), 'init')

    def set_verbosity(self, verbose=True):
        self.verbose = verbose

    def check_gw_responds(self):
        if self.multi_process:
            max_try = 5  # [sec] <~4 seconds
            version_msg = ''
            self.reset_buffer()
            for i in range(max_try):  # try to get ping from gw
                self.cmd_serial_process_q.put({'cmd': SerialProcessState.WRITE, 'data': {'gw_cmd': '!version'}})
                try:
                    version_msg = self.com_rsp_str_input_q.get(timeout=1)
                    version_msg = version_msg['raw']
                    if 'WILIOT_GW' in version_msg:
                        break
                    elif version_msg != '':
                        self._printing_func("got the following msg, while waiting for version: {}".format(version_msg),
                                            'check_gw_responds')
                except Empty:
                    continue
            self.clear_rsp_str_input_q()
        else:
            self._write("!version")
            time.sleep(0.1)
            # read GW version:
            version_msg = self.read_specific_message(msg='SW_VER', read_timeout=3)

        return version_msg

    def is_gw_alive(self):
        gw_ver = self.check_gw_responds()
        return 'WILIOT_GW' in gw_ver

    def open_port(self, port, baud):
        """
        Open a serial connection according to the port and baud
        If the port is open, The GW version is read (All last messages are read since some messages can contains the tag
        packets)
        If the version name is valid (contains 'SW_VER') the GW type (BLE/WIFI/LTI) is saved together with the software
        version. If the version name is invalid, closing the serial port.

        :type  port: str
        :param port: The GW port - mandatory
        :type  baud: int
        :param baud: the GW baud rate - mandatory

        :return: TRUE if GW is connection and FALSE otherwise

        :exception:
        * could not open port 'COMX'... - make sure the baud rate and port are correct
        """
        if self.is_connected():
            self._printing_func("GW is already connected", 'open_port')
            return self.connected
        # open UART connection
        try:
            if self.multi_process:
                version_msg = ''
                self.cmd_serial_process_q.put({'cmd': SerialProcessState.CONNECT, 'data': {'port': port, 'baud': baud}})
                self.connected_event.wait(5)  # wait for few seconds is needed if the gw is already sending packets
                if self.connected_event.is_set():
                    self.connected = True
                    self.connected_event.clear()
                    version_msg = self.check_gw_responds()
                else:
                    self._printing_func('connection failed', 'open_port')
                    self.cmd_serial_process_q.put({'cmd': SerialProcessState.DISCONNECT})
            else:
                self._comPortObj = serial.Serial(port, baud, timeout=0.1)
                time.sleep(0.5)
                if self._comPortObj.isOpen():
                    self.connected = True
                    version_msg = self.check_gw_responds()
                else:
                    self.connected = False
                    return self.connected

            if 'WILIOT_GW' in version_msg:
                self.sw_version = version_msg.split('=', 1)[1].split(' ', 1)[0]
                self.hw_version = version_msg.split('=', 1)[0]
                self.port = port
                self.connected = True
                self.update_version(check_only=True)
                return self.connected
            else:
                # we read all the last lines and cannot find a valid version name
                self._printing_func('serial connection was established but gw version could not be read.\n'
                                    'Check your baud rate and port.\nDisconnecting and closing port', 'open_port')
                self.close_port(True)
                self.connected = False
                return self.connected

        except Exception as e:
            self._printing_func('connection failed', 'open_port')
            raise e

    def _write(self, cmd):
        """
        Check if the cmd is not empty, if not the function adds new lines characters ("\r\n")
        Then try to write the command to the  GW serial port

        :type cmd: str or bytes
        :param cmd: the command for the gw, not including "\r\n" - mandatory
        :return:
        """
        if self.multi_process:
            self._printing_func('not supported while using multi processes', 'write')
            return
        # write a single command - basic command
        if self.connected:
            if isinstance(cmd, str):
                cmd = cmd.encode()
            if self.verbose:
                self._printing_func(cmd.decode(), "GWwrite")
            if cmd != b'':
                if len(cmd) >= 2:  # check last characters
                    if cmd[-2:] != b'\r\n':
                        cmd += b'\r\n'
                else:
                    cmd += b'\r\n'
                if cmd[0:1] != b'!':  # check first character
                    cmd = b'!' + cmd

                try:
                    self._comPortObj.write(cmd)
                except Exception as e:
                    self._printing_func("failed to send the command to GW (check your physical connection:\n{}"
                                        .format(e), 'write')
                    raise e
        else:
            self._printing_func("gateway is not connected. please initiate connection and then send a command", 'write')
        self.quick_wait()  # wait to prevent buffer overflow:

    def write(self, cmd, with_ack=False, max_time=0.01):
        if not self.is_connected():
            self._printing_func("gateway is not connected. write can not be done", 'write')
        data_in, got_ack = self.write_get_response(cmd)
        if with_ack:
            if data_in is not None and not got_ack:
                t_i = datetime.datetime.now()
                dt = 0
                while not got_ack and dt < max_time:
                    data_in, got_ack = self.write_get_response(cmd, need_to_clear=False)
                    dt = (datetime.datetime.now() - t_i).total_seconds()

                self.clear_rsp_str_input_q()
        # print msg:
        msg = "For cmd {} GW responded with {}".format(cmd, data_in['raw'])
        if "UNSUPPORTED" in data_in['raw'].upper():
            self._printing_func(f"GW responded unsupported to cmd {cmd}, response: {data_in}",
                                'write', log_level=logging.WARNING)
        elif got_ack:
            self._printing_func(msg, 'write', log_level=logging.INFO)
        else:
            self._printing_func(f"GW did not respond with command complete event. cmd: {cmd}, response: {data_in}",
                                'write', log_level=logging.INFO)
        return data_in

    def write_get_response(self, cmd, need_to_clear=True):
        if need_to_clear:
            self.clear_rsp_str_input_q()
        if self.multi_process:
            self.cmd_serial_process_q.put({'cmd': SerialProcessState.WRITE, 'data': {'gw_cmd': cmd}})
        else:
            self._write(cmd)
        if self.continuous_listener_enabled or self.multi_process:
            try:
                data_in = self.com_rsp_str_input_q.get(timeout=0.1)
            except Empty as e:
                data_in = {'raw': '', 'time': 0}
                is_ack = False
                return data_in, is_ack

            if "energizing" in data_in['raw'].lower():
                try:
                    data_in_2nd_row = self.com_rsp_str_input_q.get(timeout=0.01)
                    data_in['raw'] += '\n{}'.format(data_in_2nd_row['raw'])
                    data_in_3rd_row = self.com_rsp_str_input_q.get(timeout=0.01)
                    data_in['raw'] += '\n{}'.format(data_in_3rd_row['raw'])
                except Exception as e:
                    print('could not found a second/third row to gw respond {}'.format(e))

            if "unsupported" in data_in['raw'].lower():
                is_ack = False
            else:
                if isinstance(cmd, bytes):
                    cmd = cmd.decode()
                is_ack = any([s in cmd for s in cmds_no_default_ack]) or \
                         "command complete event" in data_in['raw'].lower()

            return data_in, is_ack
        else:
            is_ack = True
            data = self.readline_from_buffer()
            self._printing_func(
                "GW write_get_response {} respond with {} is not supported "
                "without continuous_listener_enabled".format(cmd, data),
                "write_get_response")
            return {'raw': data, 'time': 0}, is_ack

    def get_curr_timestamp_in_sec(self):
        return (datetime.datetime.now() - self.start_time).total_seconds()

    def read_specific_message(self, msg, read_timeout=1, clear=False):
        """
        search for specific message in the input buffer
        :type msg: str
        :param msg: the message or part of the message that needed to be read
        :type read_timeout: int
        :param read_timeout: if until read_timeout in seconds the message was not found exit the function
        :return: if specific message has found, return it. if not return an empty string
        """
        if self.continuous_listener_enabled or self.multi_process:
            if clear:
                self.clear_rsp_str_input_q()
            time_start_msg = self.get_curr_timestamp_in_sec()
            dt_check_version = self.get_curr_timestamp_in_sec() - time_start_msg
            while True:
                try:
                    timeout = read_timeout - dt_check_version
                    if not self.com_rsp_str_input_q.empty():
                        data_in = self.com_rsp_str_input_q.get(timeout=None)
                    else:  # no messages in Q- wait for message:
                        if timeout > 0:
                            data_in = self.com_rsp_str_input_q.get(timeout=timeout)
                        else:
                            # we read all the last lines and cannot find the specific message till read timeout
                            return ""
                    if msg in data_in['raw']:
                        return data_in['raw']
                    else:
                        if self.verbose and data_in is not None and data_in != '':
                            self._printing_func(
                                "Discard GW data while waiting for specific data:\n {}".format(data_in['raw']),
                                "read_specific_message {}".format(msg))
                        if data_in['time'] > time_start_msg + read_timeout:
                            print("packet time {} is bigger than time: {}".format(data_in['time'],
                                                                                  time_start_msg + read_timeout))
                            return ''
                        dt_check_version = self.get_curr_timestamp_in_sec()
                except Empty as e:
                    return ''
                except Exception as e:
                    raise ValueError("Failed reading messages from rsp Queue!")
        else:
            with self._lock_read_serial:
                time_start_msg = self.get_curr_timestamp_in_sec()
                dt_check_version = self.get_curr_timestamp_in_sec() - time_start_msg
                while dt_check_version < read_timeout:
                    try:
                        data_in = self._comPortObj.readline().decode()
                        if msg in data_in:
                            return data_in
                        else:
                            if self.verbose and data_in is not None and data_in != '':
                                self._printing_func(
                                    "Discard GW data while waiting for specific data:\n {}".format(data_in),
                                    "read_specific_message {}".format(msg))
                    except Exception as e:
                        self.reading_exception = True
                        self._printing_func('could not read line fro serial', func_name='read_specific_message',
                                            log_level=logging.WARNING)
                        pass
                    dt_check_version = self.get_curr_timestamp_in_sec() - time_start_msg

                # we read all the last lines and cannot find the specific message till read timeout
                return ''

    def close_port(self, is_reset=False):
        """
        If is_reset is TRUE, running the Reset function.
        Closing GW serial port

        :type is_reset: bool
        :param is_reset: if TRUE, running the Reset function before closing the port
        :return:
        """
        # close UART connection
        if self.is_connected():
            if is_reset:
                # reset for stop receiving messages from tag.
                try:
                    self.reset_gw()
                except Exception as e:
                    raise e
            try:
                if self.multi_process:
                    self.cmd_serial_process_q.put({'cmd': SerialProcessState.DISCONNECT})
                    self.connected_event.wait(1)
                    if self.connected_event.is_set():
                        self.connected_event.clear()
                        self.connected = False
                else:
                    self.stop_continuous_listener()
                    self._comPortObj.close()
                    self.connected = self._comPortObj.isOpen()
            except Exception as e:
                self._printing_func('Exception during close_port:{}'.format(e), 'close_port')
        else:
            self._printing_func('The gateway is already disconnected', 'close_port')

    def get_read_error_status(self):
        """
        :return True if we got error during reading
        """
        if self.multi_process:
            self.reading_exception = self.read_error_event.is_set()
            self.read_error_event.clear()
        current_reading_exception = self.reading_exception
        self.reading_exception = False  # reset flag
        return current_reading_exception

    def reset_gw(self, reset_gw=True, reset_port=True):
        """
        Reset the GW serial port
        Flush and reset input buffer

        :type reset_gw: bool
        :param reset_gw: if True sends a reset command
        :type reset_port: bool
        :param reset_port: if True reset the serial port
        :return:
        """
        self._printing_func("reset_gw called", "reset_gw")
        if self.is_connected():
            if reset_port:
                try:
                    if self.multi_process:
                        self.cmd_serial_process_q.put({'cmd': SerialProcessState.RESET})
                    else:
                        self._comPortObj.flush()
                        self.reset_buffer()
                except Exception as e:
                    self._printing_func("Exception during reset port: {}\ncheck the gw physical connection to pc"
                                        .format(e), 'reset_gw')
                    raise e
            if reset_gw:
                try:
                    if self.multi_process:
                        self.cmd_serial_process_q.put({'cmd': SerialProcessState.WRITE, 'data': {'gw_cmd': '!reset'}})
                    else:
                        self._write(b'!reset\r\n')
                except Exception as e:
                    raise e
                time.sleep(.1)
        else:
            self._printing_func("gateway is not connected please initiate connection and then try to reset", 'reset_gw')

    def reset_buffer(self):
        """
        Reset input buffer of the GW serial COM and reset software queue (raw data and processed data)
        :return:
        """
        # reset software buffers:
        self.available_data = False
        # reset serial input buffer:
        if self.is_connected():
            # reset input buffer
            if self.multi_process:
                self.cmd_serial_process_q.put({'cmd': SerialProcessState.RESET})
            else:
                try:
                    if self._comPortObj.in_waiting:
                        self._comPortObj.reset_input_buffer()
                except Exception as e:
                    self._printing_func("Exception during reset_buffer:\n{}".format(e), 'reset_buffer',
                                        log_level=logging.WARNING)
                    raise e
        else:
            self._printing_func("GW is disconnected, can not reset buffer", 'reset_buffer')
        self.clear_pkt_str_input_q()
        self.clear_rsp_str_input_q()

    def stop_gw_app(self):
        rsp = self.write('!cancel', with_ack=True, max_time=0.100)
        if 'Command Complete Event' not in rsp['raw']:
            self._printing_func("Did not get ACK from GW to stop txrx: {}".format(rsp), 'stop_gw_app')
        self.reset_buffer()

    def config_gw(self, filter_val=None, pacer_val=None, energy_pattern_val=None, time_profile_val=None,
                  beacons_backoff_val=None, received_channel=None,
                  output_power_val=None, effective_output_power_val=None, sub1g_output_power_val=None,
                  bypass_pa_val=None, pl_delay_val=None, rssi_thr_val=None,
                  max_wait=1, check_validity=False, check_current_config_only=False, start_gw_app=True, with_ack=False,
                  combined_msg=False):
        """
        set all the input configuration

        :type filter_val: bool
        :param filter_val: set packet filter.
        :type pacer_val: int
        :param pacer_val: Set pacer interval
        :type energy_pattern_val: int or str
        :param energy_pattern_val: set Energizing Pattern
        :type time_profile_val: list
        :param time_profile_val: set Timing Profile where the first element is the ON value and the
                                 2nd element is the period value.
        :type beacons_backoff_val: int
        :param beacons_backoff_val: Set beacons backoff.
        :type received_channel: int
        :param received_channel: the rx channel.
        :param rssi_thr_val: the rssi threshold of the gw
        :type rssi_thr_val: int
        :param pl_delay_val: the production line delay. if specified the pl is trigger
        :type pl_delay_val: int
        :param effective_output_power_val: the effective output power of the gw according to valid_output_power_vals
        :type effective_output_power_val: int
        :param output_power_val: the gw output power according to the string convention (e.g. pos3dBm)
        :type output_power_val: str
        :param sub1g_output_power_val: the output power of the sub1g gw according to valid_sub1g_output_power
        :type sub1g_output_power_val: int
        :type max_wait: int
        :param max_wait: the time in milliseconds to wait for gw acknowledgement after sending the config command.
        :type check_validity: bool
        :param check_validity: if True, a validity check is done on the configuration parameters
        :type check_current_config_only: bool
        :param check_current_config_only: if True only print the current GW configuration without changing it
        :return: ConfigParam class with all the configuration parameters that were set
        :rtype: ConfigParam
        """

        def check_config_gw_validity():
            """
            Check all input configuration parameters and change them if are not valid.
            :return: T/F if the all config parameters are valid or not
            """

            is_config_valid = True
            # packet filter:
            # no validity tests

            # pacer interval:
            if pacer_val is not None:
                if pacer_val < 0 or pacer_val > 65535:  # max value is 2^16 (2 bytes)
                    self._printing_func("invalid pacer interval. please select a valid value: 0-65535",
                                        'config_gw')
                    is_config_valid = False

            # Energizing Pattern:
            energy_pattern_valid = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                                    24, 25, 26, 27, 28, 50, 51, 52)
            if energy_pattern_val is not None:
                if energy_pattern_val not in energy_pattern_valid:
                    self._printing_func("invalid energizing pattern. please select a valid value: "
                                        "[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,27,28,50,51,52]",
                                        'config_gw')
                    is_config_valid = False

            # Time Profile:
            if time_profile_val is not None:
                if time_profile_val[1] < 6 or time_profile_val[1] > 50:
                    self._printing_func("invalid period time (rx+tx time). please select a valid value: 6-50",
                                        'config_gw')
                    is_config_valid = False
                else:
                    if time_profile_val[0] < 0 or time_profile_val[0] > time_profile_val[1] - 3:
                        self._printing_func("invalid ON time (tx time). please select a valid value: 0 to 3 ms "
                                            "less than period time", 'config_gw')
                        is_config_valid = False

            # beacon backoff:
            valid_bb = (0, 2, 7, 12, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 33, 36, 40)
            if beacons_backoff_val is not None:
                if beacons_backoff_val not in valid_bb:
                    self._printing_func("invalid beacons backoff. "
                                        "please select a valid value: "
                                        "[0,2,7,12,19,20,21,22,23,24,25,27,29,30,33,36,40]",
                                        'config_gw')
                    is_config_valid = False

            # Received Channel:
            valid_received_channel = (37, 38, 39)
            if received_channel is not None:
                if received_channel not in valid_received_channel:
                    self._printing_func("invalid received channel. please select a valid value: [37,38,39]",
                                        'config_gw')
                    is_config_valid = False

            # update parameters
            return is_config_valid

        gateway_output = []
        combined_msg_str = '!gw_config'
        # config write wait time:
        self.write_wait_time = max_wait * 0.001
        # fix input type:
        if time_profile_val is not None and isinstance(time_profile_val, str):
            try:
                time_profile_val = [int(time_profile_val.split(',')[0]), int(time_profile_val.split(',')[1])]
            except Exception as e:
                self._printing_func("time_profile can be a string '5,15' or list of int [5,15]", 'config_gw')
                time_profile_val = None

        # check current configuration:
        if check_current_config_only:
            self.check_current_config()
            return {}
        # start configuration:

        # check the validity of the config parameters:
        if check_validity:
            if not check_config_gw_validity():
                self._printing_func("configuration failed", 'config_gw')
                return

        # check if we can merge commands (channel, cycle time, transmit time, energizing pattern):
        if received_channel is not None and time_profile_val is not None and energy_pattern_val is not None \
                and start_gw_app:
            merge_msg = True
        else:
            merge_msg = False

        # stop gateway app before configuration:
        # if start_gw_app:
        #     self.write('!cancel')

        # set Production Line:
        if pl_delay_val is not None:
            if combined_msg:
                combined_msg_str += ' pl {}'.format(pl_delay_val)
            else:
                gateway_response = self.write('!pl_gw_config 1', with_ack=with_ack)
                gateway_response['command'] = '!pl_gw_config 1'
                gateway_output.append(gateway_response)
                gateway_response = self.write('!set_pl_delay {}'.format(pl_delay_val), with_ack=with_ack)
                gateway_response['command'] = '!set_pl_delay {}'.format(pl_delay_val)
                gateway_output.append(gateway_response)
                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.pl_delay = None
                else:
                    self.config_param.pl_delay = pl_delay_val

        # set rssi threshold:
        if rssi_thr_val is not None:
            if combined_msg:
                combined_msg_str += ' rt {}'.format(rssi_thr_val)
            else:
                gateway_response = self.write('!set_rssi_th {}'.format(rssi_thr_val), with_ack=with_ack)
                gateway_response['command'] = '!set_rssi_th {}'.format(rssi_thr_val)
                gateway_output.append(gateway_response)

                gateway_response = self.write('!send_rssi_config 1', with_ack=with_ack)
                gateway_response['command'] = '!send_rssi_config 1'
                gateway_output.append(gateway_response)

                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.rssi_thr = None
                else:
                    self.config_param.rssi_thr = rssi_thr_val

        # set output power:
        if sub1g_output_power_val is not None:
            if combined_msg:
                combined_msg_str += ' sp {}'.format(sub1g_output_power_val)
            else:
                gateway_response = self.write('!set_sub_1_ghz_power {}'.format(sub1g_output_power_val),
                                              with_ack=with_ack)
                gateway_response['command'] = '!set_sub_1_ghz_power {}'.format(sub1g_output_power_val)
                gateway_output.append(gateway_response)

        if effective_output_power_val is not None:
            valid_output_power_vals_abs_power = [out_p['abs_power'] for out_p in self.valid_output_power_vals]
            abs_output_power_index = valid_output_power_vals_abs_power.index(effective_output_power_val)
            if combined_msg:
                combined_msg_str += ' pa {}'.format(self.valid_output_power_vals[abs_output_power_index]['bypass_pa'])
                combined_msg_str += ' op {}'.format(
                    self.valid_output_power_vals[abs_output_power_index]['gw_output_power'])
            else:
                gateway_response = self.write(
                    '!bypass_pa {}'.format(self.valid_output_power_vals[abs_output_power_index]['bypass_pa']),
                    with_ack=with_ack)
                gateway_response['command'] = '!bypass_pa {}'.format(
                    self.valid_output_power_vals[abs_output_power_index]['bypass_pa'])
                gateway_output.append(gateway_response)

                gateway_response = self.write(
                    '!output_power {}'.format(self.valid_output_power_vals[abs_output_power_index]['gw_output_power']),
                    with_ack=with_ack)
                gateway_response['command'] = '!output_power {}'.format(
                    self.valid_output_power_vals[abs_output_power_index]['gw_output_power'])
                gateway_output.append(gateway_response)

                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.effective_output_power = None
                else:
                    self.config_param.effective_output_power = effective_output_power_val

        else:
            if output_power_val is not None:
                if combined_msg:
                    combined_msg_str += ' op {}'.format(output_power_val)
                else:
                    gateway_response = self.write('!output_power {}'.format(output_power_val), with_ack=with_ack)
                    gateway_response['command'] = '!output_power {}'.format(output_power_val)
                    gateway_output.append(gateway_response)
                    if 'unsupported' in gateway_response['raw'].lower():
                        self.config_param.output_power = None
                    else:
                        self.config_param.output_power = output_power_val

            if bypass_pa_val is not None:
                if combined_msg:
                    combined_msg_str += ' pa {}'.format(bypass_pa_val)
                else:
                    gateway_response = self.write(('!bypass_pa {}'.format(bypass_pa_val)), with_ack=with_ack)
                    gateway_response['command'] = '!bypass_pa {}'.format(bypass_pa_val)
                    gateway_output.append(gateway_response)

        # set filter
        if filter_val is not None:
            if combined_msg:
                combined_msg_str += ' pf {}'.format(int(filter_val))
            else:
                if filter_val:
                    str_f = 'on'
                else:
                    str_f = 'off'
                gateway_response = self.write('!set_packet_filter_' + str_f, with_ack=with_ack)
                gateway_response['command'] = '!set_packet_filter_' + str_f
                gateway_output.append(gateway_response)

                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.filter = None
                else:
                    self.config_param.filter = filter_val

        # set pacer interval
        if pacer_val is not None:
            if combined_msg:
                combined_msg_str += ' pi {}'.format(pacer_val)
            else:
                gateway_response = self.write('!set_pacer_interval {}'.format(pacer_val), with_ack=with_ack)
                gateway_response['command'] = '!set_pacer_interval {}'.format(pacer_val)
                gateway_output.append(gateway_response)

                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.pacer_val = None
                else:
                    self.config_param.pacer_val = pacer_val

        # set Received Channel
        if received_channel is not None and (not merge_msg or combined_msg):
            if combined_msg:
                combined_msg_str += ' sc {}'.format(received_channel)
            else:
                gateway_response = self.write('!scan_ch {}'.format(received_channel), with_ack=with_ack)
                gateway_response['command'] = '!scan_ch {}'.format(received_channel)
                gateway_output.append(gateway_response)
                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.received_channel = None
                else:
                    self.config_param.received_channel = received_channel

        # set Time Profile
        if time_profile_val is not None and (not merge_msg or combined_msg):
            if combined_msg:
                combined_msg_str += ' tp {} {}'.format(time_profile_val[1], time_profile_val[0])
            else:
                gateway_response = self.write('!time_profile {} {}'.format(time_profile_val[1], time_profile_val[0]),
                                              with_ack=with_ack)
                gateway_response['command'] = '!time_profile {} {}'.format(time_profile_val[1], time_profile_val[0])
                gateway_output.append(gateway_response)

                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.time_profile_on = None
                    self.config_param.time_profile_period = None
                else:
                    self.config_param.time_profile_on = time_profile_val[0]
                    self.config_param.time_profile_period = time_profile_val[1]

        # set Beacons Backoff:
        if beacons_backoff_val is not None:
            if combined_msg:
                combined_msg_str += ' bb {}'.format(beacons_backoff_val)
            else:
                gateway_response = self.write('!beacons_backoff {}\r\n'.format(beacons_backoff_val), with_ack=with_ack)
                gateway_response['command'] = '!beacons_backoff {}\r\n'.format(beacons_backoff_val)
                gateway_output.append(gateway_response)

                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.beacons_backoff = None
                else:
                    self.config_param.beacons_backoff = beacons_backoff_val

        # set Energizing Pattern:
        if energy_pattern_val is not None and (not merge_msg or combined_msg):
            if combined_msg:
                combined_msg_str += ' ep {}'.format(energy_pattern_val)
            else:
                gateway_response = self.write('!set_energizing_pattern {}'.format(energy_pattern_val),
                                              with_ack=with_ack)
                gateway_response['command'] = '!set_energizing_pattern {}'.format(energy_pattern_val)
                gateway_output.append(gateway_response)
                if 'unsupported' in gateway_response['raw'].lower():
                    self.config_param.energy_pattern = None
                else:
                    self.config_param.energy_pattern = energy_pattern_val

        # starting transmitting + listening:
        if start_gw_app and (not merge_msg or combined_msg):
            if combined_msg:
                combined_msg_str += ' ga'
            else:
                gateway_response = self.write('!gateway_app', with_ack=with_ack)
                gateway_response['command'] = '!gateway_app'
                gateway_output.append(gateway_response)

        # send merge msg if available: (channel, cycle time, transmit time, energizing pattern)
        if merge_msg and not combined_msg:
            gateway_response = self.write(
                '!gateway_app {} {} {} {}'.format(received_channel, time_profile_val[1], time_profile_val[0],
                                                  energy_pattern_val), with_ack=with_ack)
            gateway_response['command'] = '!gateway_app {} {} {} {}'.format(received_channel, time_profile_val[1],
                                                                            time_profile_val[0],
                                                                            energy_pattern_val)
            gateway_output.append(gateway_response)
            if 'unsupported' in gateway_response['raw'].lower():
                self.config_param.energy_pattern = None
                self.config_param.received_channel = None
                self.config_param.time_profile_on = None
                self.config_param.time_profile_period = None
            else:
                self.config_param.energy_pattern = energy_pattern_val
                self.config_param.received_channel = received_channel
                self.config_param.time_profile_on = time_profile_val[0]
                self.config_param.time_profile_period = time_profile_val[1]

        if combined_msg:
            gateway_response = self.write(combined_msg_str, with_ack=with_ack)
            gateway_response['command'] = combined_msg_str
            gateway_output.append(gateway_response)
            if 'unsupported' not in gateway_response['raw'].lower():
                self.config_param.energy_pattern = energy_pattern_val
                self.config_param.received_channel = received_channel
                self.config_param.time_profile_on = time_profile_val[0]
                self.config_param.time_profile_period = time_profile_val[1]
                self.config_param.beacons_backoff = beacons_backoff_val
                self.config_param.pacer_val = pacer_val
                self.config_param.filter = filter_val
                self.config_param.pl_delay = pl_delay_val
                self.config_param.rssi_thr = rssi_thr_val
                self.config_param.effective_output_power = effective_output_power_val
                self.config_param.output_power = output_power_val
                self.config_param.bypass_pa = bypass_pa_val

        self._printing_func("configuration is set", 'config_gw')
        return self.config_param, gateway_output  # return the config parameters

    def check_current_config(self):
        """
        print the current gw configuration
        :return:
        """
        data_in = self.write("!print_config_extended")
        # read current configuration:
        if data_in != '':
            self._printing_func("current gateway configuration:\n{}".format(data_in), 'config_gw')
            return
        else:
            # we read all the last lines and cannot find a valid message
            self._printing_func("cannot read gateway configuration", 'config_gw')
            return

    def run_command(self, command):
        print('------------------------Starting to update GW FW------------------------')
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            output = process.stdout.readline().decode()
            if process.poll() is not None:
                break
            if output:
                print(output.strip())

    def update_version(self, version="Latest", versions_path="", check_only=False):
        """
        first check if the required version has a matched zip file under the gw versions folder.
        Then, compare the gw version with the required version. if the versions are different,
        then it checks if the required version has a matched zip file under the gw versions folder.
        if the file exists, a version update is done by send the gw to bootloader mode and burn the version
        using nRF utils

        :type versions_path: str
        :param versions_path: the path of the gateway version zip file. If defined, the update is run regardless to the
                              current gw version
        :type version: str
        :param version: the version string in the following format 'x.x.x'.
                        if version is 'Latest' than the latest version is selected
        :type check_only: bool
        :param check_only: if True the function only checks the version but does not update it
        :return: True if GW version is up to date, False if GW version is old and None if a problem occur
        """
        required_version = ''
        if versions_path == "":
            # check available versions:
            try:
                required_version, new_version_path = self.get_latest_version_number(version=version,
                                                                                    versions_path=versions_path)
            except Exception as e:
                raise e
            if not required_version:
                return

            # check if the GW is already with the right version:
            if self.sw_version == required_version:
                self._printing_func("Your Gateway is already updated", 'update_version')
                return True
            # The GW need to be updated
            if check_only:
                self._printing_func("Your Gateway needs to be updated", 'update_version')
                return False

            r_major, _, _ = required_version.split('.')
            c_major, _, _ = self.sw_version.split('.')

            if int(r_major) > int(c_major):
                # Major change - need to load boot loader:
                if int(r_major) == 4 and int(c_major) == 3:
                    pass  # no bootloader change was done between these versions
                elif "app" in new_version_path:
                    new_version_path = new_version_path.replace('app', 'sd_bl_gw_app')
                    if not os.path.isfile(new_version_path):
                        raise ValueError(f"Trying to upgrade major version "
                                         f"from {self.sw_version} to {required_version}.Could not find boot loader "
                                         f"version file {new_version_path}")
        else:
            new_version_path = '"{}"'.format(versions_path)  # to avoid failure when path contains spaces

        # a version need to be updated:

        # change the GW to bootloader state
        if self.is_connected():
            self.write('!move_to_bootloader')
            time.sleep(0.1)
            self.close_port()

            # run the nRF Util to burn the version:
            time.sleep(.1)
            # wait until burn was completed
            self._printing_func("please wait for approx. 30 seconds...", 'update_version')
            command = 'nrfutil -v -v dfu serial  --package {} -p {} -fc 0 -b 115200 -t 10'.format(new_version_path, self.port)
            self.run_command(command)

            self._printing_func("Rebooting and opening serial port again...", 'update_version')
            time.sleep(5)
            for i in range(5):
                time.sleep(1)
                # open GW again
                if self.open_port(self.port, baud=self.baud):
                    break
            if versions_path == "":
                if self.sw_version == required_version:
                    self._printing_func("Your Gateway is updated", 'update_version')
                    return True
                else:
                    self._printing_func("update failed. please try again", 'update_version')
                    return False
            else:
                # TODO: Add check of the version..
                return True
        else:
            self._printing_func("Gateway is not connected. please initiate connection before update versions",
                                'update_version')
            return False

    def exit_gw_api(self):
        """
        check that all threads are terminated and serial com is closed
        :return:
        """
        if self.multi_process:
            self.cmd_serial_process_q.put({'cmd': SerialProcessState.STOP})
            time.sleep(0.2)
            if self._port_listener_thread.is_alive():
                self._printing_func("listener Process is still running", 'exit_gw_api')
        else:
            if self._port_listener_thread is not None:
                if self._port_listener_thread.is_alive():
                    self.stop_continuous_listener()
                    time.sleep(0.2)
                    if self._port_listener_thread.is_alive():
                        self._printing_func("listener thread is still running", 'exit_gw_api')
            if self._comPortObj is not None:
                if self._comPortObj.isOpen():
                    self.close_port()
                    if self._comPortObj.isOpen():
                        self._printing_func("encounter a problem to close serial port", 'exit_gw_api')

        self.close_socket_connection()
        if self.init_socket_connection_thread is not None and self.init_socket_connection_thread.is_alive():
            self.init_socket_connection_thread.join()

    def _printing_func(self, str_to_print, func_name="MISSING", is_info=False, log_level=logging.INFO):
        if self.verbose or not is_info:
            with self._lock_print:
                self.logger.log(log_level, 'GW API: {}: {}'.format(func_name, str_to_print.strip()))

    def is_connected(self):
        if self.multi_process:
            connection_status_changed = self.connected_event.is_set()
            if connection_status_changed:
                self.connected = not self.connected
                self.connected_event.clear()
        return self.connected

    def get_connection_status(self, check_port=False):
        """
        :return: if gateway is connected, return True, the serial port and baud rate used for the connection.
                 if not, return False, and None for port and baud
        """
        if self.is_connected():
            if check_port:
                try:
                    self._write("!version")
                    version_msg = self.read_specific_message(msg='SW_VER', read_timeout=3)
                    # read GW version:
                    if version_msg != '':
                        self.sw_version = version_msg.split('=', 1)[1].split(' ', 1)[0]
                        self.hw_version = version_msg.split('=', 1)[0]
                    else:
                        self._printing_func("gw version could not be achieved")
                        self.close_port()
                        return False, None, None
                except Exception as e:
                    self._printing_func("while checking the gw version an error occurs: {}".format(e))
                    self.close_port()
                    return False, None, None
            return self.connected, self.port, self.baud
        return False, None, None

    def get_gw_version(self):
        """
        :return: the gateway software version, the gw hardware type
        """
        return self.sw_version, self.hw_version

    def get_latest_version_number(self, version="Latest", versions_path=""):
        """
        return the latest version in the gw_version folder or in versions_path if specified

        :type version: str
        :param version: the version string in the following format 'x.x.x'.
                        if version is 'Latest' than the latest version is selected
        :type versions_path: str
        :param versions_path: the folder path of the gateway versions zip files
        :return: the latest available version number to be installed and its path
        """
        # check available versions:
        if versions_path == "":
            versions_path = os.path.join(os.path.dirname(__file__),
                                         'local_gateway_versions')

        try:
            versions_files = [f for f in os.listdir(versions_path) if f.endswith(".zip")]
        except Exception as e:
            self._printing_func("while running update_version function:\n{}\n"
                                "check if the version_path is correct".format(e), 'update_version')
            raise e

        versions_num = []
        first_exception = None
        for version_file in versions_files:
            try:
                version_num = re.match('(\d+\.\d+\.\d+)', version_file).groups(1)[0]
                # versions_num.append(int(''.join(version_num)))
                versions_num.append(version_num)
            except Exception as e:

                self._printing_func("version zip file name should begin with x.x.x  Hence {} is not considered "
                                    "as a valid version file".format(version_file), 'update_version')
                first_exception = e
        if not versions_num:
            if first_exception:
                # no valid versions files
                self._printing_func("no valid version files have found - version update failed", 'update_version')
                raise first_exception
            else:
                # empty folder:
                self._printing_func("versions folder is empty - version update failed", 'update_version')
                return None, None
        # select the last version:
        latest_version = [0, 0, 0]
        for ver in versions_num:
            ver_arr = ver.split('.')
            for i, n in enumerate(ver_arr):
                if int(n) > latest_version[i]:
                    latest_version = [int(x) for x in ver_arr]
                    break
                elif int(n) < latest_version[i]:
                    break

        # select the relevant version to load
        if version == "Latest":
            required_version = '.'.join(str(n) for n in latest_version)
        else:
            if version in versions_num:
                required_version = version
            else:
                self._printing_func("no version file matches {} version".format(version), 'update_version')
                return None, None
        file_names_priority = [f"{required_version}_app.zip", f"{required_version}.zip", ]
        file_name = ''
        for file_name in file_names_priority:
            if file_name in versions_files:
                break
        new_version_path = os.path.join(versions_path, file_name)
        return required_version, new_version_path

    def is_rsp_available(self):
        return not self.com_rsp_str_input_q.empty()

    def get_gw_rsp(self):
        try:
            return self.com_rsp_str_input_q.get(timeout=0)
        except Empty:
            return None

    def is_data_available(self):
        """
        :return: True if data is available tp get, False otherwise
        """
        if self.continuous_listener_enabled or self.multi_process:
            return not self.com_pkt_str_input_q.empty()
        else:
            return self.available_data

    def clear_pkt_str_input_q(self):
        if self.multi_process:
            while True:
                try:
                    rsp = self.com_pkt_str_input_q.get(timeout=0)
                    self._printing_func('discarding gw packets before writing: {}'.format(rsp),
                                        'clear_rsp_str_input_q')
                except Empty:
                    break
        else:
            with self.com_pkt_str_input_q.mutex:
                self.com_pkt_str_input_q.queue.clear()

    def clear_rsp_str_input_q(self):
        if self.multi_process:
            while True:
                try:
                    rsp = self.com_rsp_str_input_q.get(timeout=0)
                    self._printing_func('discarding gw response before writing: {}'.format(rsp),
                                        'clear_rsp_str_input_q')
                except Empty:
                    break
        else:
            with self.com_rsp_str_input_q.mutex:
                self.com_rsp_str_input_q.queue.clear()

    def continuous_listener(self):
        """
        An infinite loop with the following stop-conditions:
            wait for stop event
        """
        if self.multi_process:
            self._printing_func('not supported with multi processing mode', 'continous_listener')
            return
        buf = b''
        n_packets = 0
        consecutive_exception_counter = 0
        self._printing_func("continuous_listener Start", 'continuous_listener', True)
        with self.start_time_lock:
            self.start_time = datetime.datetime.now()
        while not self.stop_listen_event.is_set():
            try:
                # if is_stop_conditions():
                #     self.stop_listen_event.set()
                # reading the incoming data:
                data = None
                with self._lock_read_serial:
                    data = self._comPortObj.readline()

                # data handler:
                if b'\n' in data:

                    # check if buffer is full:
                    if self._comPortObj.in_waiting > 1000:
                        self._printing_func("more than 1000 bytes are waiting in the serial port buffer",
                                            'continuous_listener')
                    # get data and check it:
                    buf += data
                    if isinstance(buf, bytes):
                        msg = buf.decode().strip(' \t\n\r')

                        timestamp = datetime.datetime.now() - self.start_time
                        # if self.verbose:
                        #     print(timestamp, " ", msg)
                        msg_dict = {'time': timestamp.total_seconds(), 'raw': msg}
                        if msg.startswith(packet_prefix_str):
                            if self.com_pkt_str_input_q.full():
                                dummy = self.com_pkt_str_input_q.get()
                                self._printing_func("pkt_str_input_q is full, dropping {}".format(dummy),
                                                    'continuous_listener')
                                self.com_pkt_str_input_q.put(msg_dict)
                            else:
                                n_packets += 1
                                self.available_data = True
                                self.com_pkt_str_input_q.put(msg_dict)
                        else:
                            if self.com_rsp_str_input_q.full():
                                dummy = self.com_rsp_str_input_q.get()
                                self._printing_func("rsp_str_input_q is full, dropping {}".format(dummy),
                                                    'continuous_listener', log_level=logging.DEBUG)
                            self.com_rsp_str_input_q.put(msg_dict)
                            self._printing_func("received msg from GW: {}".format(msg_dict['raw']),
                                                'run_packet_listener', log_level=logging.DEBUG)
                    buf = b''
                else:  # if timeout occurs during packet receiving, concatenate the message until '\n'
                    buf += data

                # complete the loop with no exceptions
                consecutive_exception_counter = 0

            except Exception as e:
                # saving the first exception
                self.reading_exception = True
                if consecutive_exception_counter == 0:
                    self.exceptions_threads[0] = str(e)
                self._printing_func("received: {}\ncomPortListener Exception({}/10):\n{}".
                                    format(data, consecutive_exception_counter, e), 'run_packet_listener')
                consecutive_exception_counter = consecutive_exception_counter + 1
                buf = b''
                if consecutive_exception_counter > 10:
                    self._printing_func("more than 10 Exceptions, stop comPortListener thread",
                                        'run_packet_listener')
                    if self._comPortObj.isOpen():
                        self._comPortObj.close()
                    else:
                        self._printing_func("gateway is not connected. please initiate connection and try to "
                                            "read data again", 'run_packet_listener')
                    return
                else:  # less than 10 successive exceptions
                    if self._comPortObj.isOpen():
                        pass
                    else:
                        self._printing_func("gateway is not connected. please initiate connection and try to "
                                            "read data again", 'run_packet_listener')
                        return

    def start_continuous_listener(self):
        """
        Runs the continuous_listener function as a thread
        """
        # non-blocking
        if not self.multi_process:
            if self._port_listener_thread is not None:
                if self._port_listener_thread.is_alive():
                    self.stop_continuous_listener()
                    self._port_listener_thread.join()

            self.stop_listen_event.clear()
            self._port_listener_thread = threading.Thread(target=self.continuous_listener,
                                                          args=[])
            self._port_listener_thread.start()
            self.continuous_listener_enabled = True
            return

    def stop_continuous_listener(self):
        """
        Set the stop_listen_event flag on
        """
        if not self.multi_process:
            self.stop_listen_event.set()
            self.continuous_listener_enabled = False

    def reset_listener(self):
        """
        Reset the queues and timers related to the listener
        """
        if self.multi_process:
            self.cmd_serial_process_q.put({'cmd': SerialProcessState.RESET})
        else:
            self.reset_start_time()
            self.reset_buffer()
            self.stop_listen_event.clear()

    def reset_start_time(self):
        if self.multi_process:
            self.cmd_serial_process_q.put({'cmd': SerialProcessState.READ})
        with self.start_time_lock:
            self.start_time = datetime.datetime.now()

    def get_packets(self, action_type=ActionType.FIRST_SAMPLES, num_of_packets=None, data_type=DataType.PACKET_LIST,
                    max_time=None, tag_inlay=None, is_blocking=True, send_to_additional_app=False):
        """
        Extract packets from the queue, process according to data_type value.
                action_type valid options:
                all_samples: return all available packets.
                first_samples: return all the X first packets (the oldest packets ) according to num_of_packages
        If num_of_packets is larger than the available packets, it will block till num_of_packets packets are available
        if is_clocking is False it shall return empty list/PacketList according to the data_type if not enough packets
        are available in the queue

        :type action_type: ActionType
        :param action_type: {'all_samples','first_samples'}.
                            the method of data extraction (see description).
        :type num_of_packets: int or None
        :param num_of_packets: number of packets to extract
        :type data_type: DataType
        :type max_time: float
        :param max_time: number of seconds to extract packets
        :param data_type: {'raw','processed','packet_list'}.
                          the data type to extract (see description)
        :type tag_inlay: InlayTypes
        :param tag_inlay: inlay type to calculate min tx if decryption is available
        :type is_blocking: bool
        :param is_blocking: if True and num of packet is specified functions waits until it collects all packets
        :type send_to_additional_app: bool
        :param send_to_additional_app: if True the packets are sent to tcp/ip socket
        :return: processed:
                     a list of dictionaries or on only dictionary (if only one packet has had received)
                     with all the extracted raw or processed data.
                     Dictionary keys of RAW: 'raw','time'
                     Dictionary keys of PROCESSED: 'packet','is_valid_tag_packet','adv_address','group_id','rssi',
                                                   'stat_param','time_from_start','counter_tag'
                PACKET_LIST:
                    Packet_List object
        """
        if not self.continuous_listener_enabled and not self.multi_process:
            raise ValueError("to use get_packet please first call start_continuous_listener() "
                             "or run using multi_process=True."
                             "to stop the listener after usage call stop_continuous_listener()")
        min_expected_packets = num_of_packets
        if data_type == DataType.PACKET_LIST:
            packet_list = PacketList()
        elif data_type == DataType.DECODED:
            if DECRYPTION_MODE:
                packet_list = DecryptedPacketList()
            else:
                data_type = DataType.PACKET_LIST
                packet_list = PacketList()
        else:
            packet_list = []
        # Check inputs:
        if action_type == action_type.ALL_SAMPLE:
            min_expected_packets = self.com_pkt_str_input_q.qsize()
            if max_time is None:
                num_of_packets = min_expected_packets
            else:
                num_of_packets = None

        elif max_time is None and num_of_packets is None:
            raise ValueError("bad input to get_packets: max_time and num_of_packets are none "
                             "while action type is NOT ALL_SAMPLE")

        elif num_of_packets is not None and is_blocking is False:
            # check if enough packets in the queue
            if num_of_packets > self.com_pkt_str_input_q.qsize():
                self._printing_func("there are not enough packets to extract ({} compare to {})".
                                    format(self.com_pkt_str_input_q.qsize(), num_of_packets), 'get_packets')
                return packet_list

        local_start_time = self.get_curr_timestamp_in_sec()
        num_collected_packets = 0
        timeout_occurred = False

        while not timeout_occurred and (num_of_packets is None or num_collected_packets < num_of_packets):
            data_in = None
            try:
                if max_time is not None:
                    curr_dt = self.get_curr_timestamp_in_sec() - local_start_time
                    timeout = max_time - curr_dt
                    if timeout > 0:
                        if not self.com_pkt_str_input_q.empty():
                            data_in = self.com_pkt_str_input_q.get(timeout=None)
                    else:
                        timeout_occurred = True
                elif not self.com_pkt_str_input_q.empty():  # max_time is None
                    data_in = self.com_pkt_str_input_q.get(timeout=None)
                else:  # queue is empty
                    if not is_blocking or not self._port_listener_thread.is_alive():
                        timeout_occurred = True
                    time.sleep(0.01)

            except Exception as e:
                raise ValueError("Failed reading messages from pkt Queue! {}".format(str(e)))

            if data_in:
                num_collected_packets += 1
                if data_type == DataType.RAW:
                    packet_list.append(data_in)
                elif data_type == DataType.PROCESSED:
                    data_in = self.process_one_packet(data_in["raw"], data_in["time"])
                    packet_list.append(data_in)
                elif data_type == DataType.PACKET_LIST:
                    proc_packet = Packet(data_in["raw"], data_in["time"], inlay_type=tag_inlay)
                    if proc_packet.is_valid_packet:
                        packet_content = proc_packet.get_packet_string(process_packet=False)
                        proc_packet.gw_data['is_valid_tag_packet'] = \
                            packet_content and not proc_packet.is_short_packet()
                    packet_list.append(proc_packet.copy())
                elif data_type == DataType.DECODED:
                    try:
                        proc_packet = DecryptedPacket(data_in["raw"], data_in["time"], inlay_type=tag_inlay)
                        if proc_packet.is_valid_packet:
                            packet_content = proc_packet.get_packet_string(process_packet=False)
                            proc_packet.gw_data['is_valid_tag_packet'] = \
                                packet_content and not proc_packet.is_short_packet()
                        packet_list.append(proc_packet)
                    except Exception as e:
                        pass
                else:
                    raise ValueError("datatype is not supported")
        if min_expected_packets and num_collected_packets < min_expected_packets:
            raise ValueError(f"get_packets collected {num_collected_packets} packets,expected minimum "
                             f"of {min_expected_packets}")
        if send_to_additional_app:
            self.send_data(packet_list)
        return packet_list

    def close_socket_connection(self):
        if self.server_socket is not None:
            self.server_socket.close()
        self.try_to_connect_to_client = False
        self.server_socket = None
        self.client_conn = None

    def init_socket_connection(self):
        self.try_to_connect_to_client = True
        self.server_socket = socket.socket()
        self.server_socket.settimeout(1)
        try:
            self.server_socket.bind((self.socket_host, self.socket_port))
        except Exception as e:
            self._printing_func('problem in bind the server socket: {}'.format(e), 'init_socket_connection',
                                log_level=logging.WARNING)
        self._printing_func('wait for client to connect', 'init_socket_connection')
        self.server_socket.listen(1)  # TODO enable the option to send data to multiple clients
        try:
            self.client_conn, client_address = self.server_socket.accept()
            self._printing_func('connected to: {}:{}'.format(client_address[0], client_address[1]),
                                'init_socket_connection')
        except socket.timeout:
            pass
        except Exception as e:
            print('while trying to connect to the socket an exception occurs: {}'.format(e))

        self.try_to_connect_to_client = False

    def send_data(self, data_list):
        """

        :param data_list:
        :type data_list: list or PacketList or DecryptedPacketList
        :return:
        :rtype:
        """
        if (self.server_socket is None or self.client_conn is None) and not self.try_to_connect_to_client:
            self.init_socket_connection_thread = threading.Thread(target=self.init_socket_connection, args=())
            self.init_socket_connection_thread.start()
        if self.client_conn is None:
            return

        data_to_send = []
        for data in data_list:
            if isinstance(data, dict):
                if 'raw' in data.keys():
                    raw_packet = data['raw'].split('process_packet("')[1].split('"')[0]
                elif 'packet' in data.keys():
                    raw_packet = data['packet']
                else:
                    raise ValueError('trying to send invalid raw packet: {}'.format(data))
                if 'time' in data.keys():
                    packet_time = data['time']
                elif 'time_from_start' in data.keys():
                    packet_time = data['time_from_start']
                else:
                    raise ValueError('trying to send invalid time: {}'.format(data))
                data_to_send.append('raw:{}, time:{},'.format(raw_packet, packet_time))

            elif isinstance(data, Packet):
                n_sprinkler = len(data)
                if n_sprinkler == 1:
                    raw_packet = data.get_packet_string(gw_data=True, process_packet=False)
                    packet_time = str(data.gw_data['time_from_start'])
                    data_to_send.append('raw:{}, time:{},'.format(raw_packet, packet_time))
                else:
                    for i in range(n_sprinkler):
                        raw_packet = data.get_packet_string(i=i, gw_data=True, process_packet=False)
                        packet_time = str(data.gw_data['time_from_start'][i])
                        data_to_send.append('raw:{}, time:{},'.format(raw_packet, packet_time))
            else:
                raise ValueError('trying to send data type: {}'.format(type(data)))
        try:
            for data in data_to_send:
                self.client_conn.send(str.encode(data))
        except Exception as e:
            print('during socket sending data an exception occurs: {}'.format(e))
            self.close_socket_connection()

    @staticmethod
    def process_one_packet(packet, packet_time):
        """
        internal function to process packets for backward compatibility with the previous data_type: 'processed'
        """
        new_proc = {}
        # arrange the received packet:
        new_packet = PacketStruct(packet)
        packet_content = new_packet.tag_packet_content(packet)
        if packet_content and not new_packet.is_short_packet(packet_content):
            new_packet.fill_packet(packet_content)
            new_proc['is_valid_tag_packet'] = True
        else:
            # invalid tag packet (short) or not a tag packet:
            new_proc['is_valid_tag_packet'] = False

        # update time:
        new_proc['time_from_start'] = packet_time

        # append data:
        new_proc['counter_tag'] = 1
        for key, value in new_packet.__dict__.items():
            try:
                if key == 'rssi' or key == 'stat_param':
                    if value is None:
                        new_proc[key] = value
                    else:
                        new_proc[key] = int(value, base=16)
                else:
                    new_proc[key] = value
            except Exception as e:
                print("Failed to process corrupted packet {} due to {}".format(packet, e))
                pass

        return new_proc

    def quick_wait(self):
        """
        this function replaces the time.sleep(self.write_wait_time) for more accurate wait time
        """
        t_i = datetime.datetime.now()
        dt = datetime.datetime.now() - t_i
        while dt.total_seconds() < self.write_wait_time:
            dt = datetime.datetime.now() - t_i
        return

    def set_gw_output_power_by_index(self, abs_output_power_index, with_ack):
        self.write('!bypass_pa {}'.format(self.valid_output_power_vals[abs_output_power_index]['bypass_pa']),
                   with_ack=with_ack)
        self.write('!output_power {}'.format(self.valid_output_power_vals[abs_output_power_index]['gw_output_power']),
                   with_ack=with_ack)

    def set_gw_max_output_power(self, with_ack=False):
        self.set_gw_output_power_by_index(-1, with_ack)

    def readline_from_buffer(self, timeout=1):
        if self.multi_process:
            self._printing_func('not supported while using multi processes', 'readline')
            return ''
        buf = b''
        msg = ''
        done = False
        local_start_time = self.get_curr_timestamp_in_sec()
        end_time = local_start_time + timeout
        while not done:
            try:
                if self.get_curr_timestamp_in_sec() > end_time and timeout > 0:
                    done = True
                # reading the incoming data:
                with self._lock_read_serial:
                    data = self._comPortObj.readline()
                # data handler:
                if b'\n' in data:
                    # get data and check it:
                    buf += data
                    if isinstance(buf, bytes):
                        msg = buf.decode().strip(' \t\n\r')
                    done = True
                elif data == '':
                    done = True
            except Exception as e:
                self._printing_func(f"Failed to readline with exception {str(e)}")
            if not done:
                time.sleep(0.1)
        return msg


if __name__ == '__main__':
    print(datetime.datetime.now())
    gw = WiliotGateway(auto_connect=True, is_multi_processes=True)
    if gw.is_connected():
        # gw.start_continuous_listener()
        gw.reset_gw(reset_port=False)
        print(f'is gw alive {gw.is_gw_alive()}')
        print(gw.write('!set_tester_mode 1', with_ack=True))
        gw.config_gw(energy_pattern_val=18, time_profile_val=[5, 15], effective_output_power_val=22,
                     beacons_backoff_val=0)
    print(datetime.datetime.now())
    gw.exit_gw_api()
