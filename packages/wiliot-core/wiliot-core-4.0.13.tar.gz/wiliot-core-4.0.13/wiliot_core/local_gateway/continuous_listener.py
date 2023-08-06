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

import serial
import time
from multiprocessing import Process, Queue, Event
from queue import Empty
from enum import Enum
import datetime
import logging
import os
from wiliot_core.utils.utils import WiliotDir

packet_bytes = 100  # number of char
packet_prefix_str = 'process_packet'


class SerialProcessState(Enum):
    CONNECT = 'connect'
    WRITE = 'write'
    READ = 'read'
    DISCONNECT = 'disconnect'
    RESET = 'reset'
    STOP = 'stop'
    IDLE = 'idle'


class SerialProcess:
    """
    connect - connect to serial, return if connected (connected event)
    write - write command to serial, return the gw respond (add to rsp q)
    read - read specific msg from serial, return the gw respond (add to rsp/packet q)
    disconnect - close serial port, return if connected (connected event)
    reset - reset serial buffer
    check - number of bytes waiting in buffer (n_bytes Value
    stop - stop the process
    """
    def __init__(self, cmd_q, gw_rsp_q, packets_q, change_connection_status, error_event, log_dir_path=None):
        """

        :param cmd_q: queue of commands to the listener including cmd = the state in the state machine,
                      and data if needed
        :type cmd_q: Queue
        :param gw_rsp_q: the listener put into this queue the gw responds
        :type gw_rsp_q: Queue
        :param packets_q: the listener put into this queue the packets received from gw
        :type packets_q: Queue
        :param change_connection_status: listener set this event if there was a change in the connection status
        :type change_connection_status: Event
        :param error_event: listener set this event if an error occurs during run
        :type error_event: Event
        :param log_dir_path: the logging directory
        :type log_dir_path: str
        """
        # serial port variables:
        self._comPortObj = None
        self.write_wait_time = 0.001  # [sec]
        self.cmd_q = cmd_q
        self.gw_rsp_q = gw_rsp_q
        self.packets_q = packets_q
        self.change_connection_status = change_connection_status
        self.error_event = error_event
        self.connected = False
        self.gw_start_time = datetime.datetime.now()
        self.buf = b''

        # set logging:
        self.logger = logging.getLogger('WiliotListener')
        self.set_logger(log_dir_path)
        # start run:
        self.run_sm()

    def set_logger(self, logger_dir_path):
        formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        if logger_dir_path is None:
            wiliot_dir = WiliotDir()
            logger_dir_path = os.path.join(wiliot_dir.get_wiliot_root_app_dir(), 'wiliot_continuous_listener')
        if not os.path.isdir(logger_dir_path):
            os.mkdir(logger_dir_path)
        logger_name = 'listener_log_{}.log'.format(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        logger_path = os.path.join(logger_dir_path, logger_name)
        file_handler = logging.FileHandler(logger_path, mode='a')
        file_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.DEBUG)

    def run_sm(self):
        while True:
            try:
                cmd = self.cmd_q.get(timeout=0)
                state = cmd['cmd']
            except Empty:
                cmd = None
                state = SerialProcessState.IDLE

            if state == SerialProcessState.CONNECT:
                self.connect(port=cmd['data']['port'], baud=cmd['data']['baud'])
            elif state == SerialProcessState.WRITE:
                self.write(gw_cmd=cmd['data']['gw_cmd'])
                self.read()
            elif state == SerialProcessState.READ:
                self.gw_start_time = datetime.datetime.now()
                self.read()
            elif state == SerialProcessState.DISCONNECT:
                self.disconnect()
            elif state == SerialProcessState.RESET:
                self.reset()
                self.gw_start_time = datetime.datetime.now()
            elif state == SerialProcessState.STOP:
                self.disconnect()
                break
            elif state == SerialProcessState.IDLE:
                if self.connected:
                    self.read()
                else:
                    time.sleep(0.1)
                    continue
        self.logger.log(logging.INFO, 'serial process state machine is done')

    def connect(self, port, baud):
        if self.connected:
            self.change_connection_status.set()
        else:
            try:
                self._comPortObj = serial.Serial(port, baud, timeout=0.001)
                for i in range(5):
                    if self._comPortObj.isOpen():
                        break
                    time.sleep(0.1)
                    self._comPortObj = serial.Serial(port, baud, timeout=0.001)
                if self._comPortObj.isOpen():
                    self.change_connection_status.set()
                    self.connected = True
                    self.logger.log(logging.INFO, 'Connected to port: {}'.format(port))
            except Exception as e:
                self.logger.log(logging.WARNING, 'Exception during connection to port {}: {}'.format(port, e))

    def disconnect(self):
        if self.connected:
            try:
                self._comPortObj.close()
                self.change_connection_status.set()
                self.connected = False
            except Exception as e:
                self.logger.log(logging.WARNING, 'Exception during disconnect from serial: {}'.format(e))

    def write(self, gw_cmd):
        if self.connected:
            if isinstance(gw_cmd, str):
                gw_cmd = gw_cmd.encode()
            if gw_cmd != b'':
                if len(gw_cmd) >= 2:  # check last characters
                    if gw_cmd[-2:] != b'\r\n':
                        gw_cmd += b'\r\n'
                else:
                    gw_cmd += b'\r\n'
                if gw_cmd[0:1] != b'!':  # check first character
                    gw_cmd = b'!' + gw_cmd

                try:
                    self._comPortObj.write(gw_cmd)
                    self.logger.log(logging.DEBUG, "sent msg {}".format(gw_cmd))
                except Exception as e:
                    self.logger.log(logging.WARNING, "failed to send the command to GW (check your physical "
                                                     "connection:\n{}".format(e))

    def reset(self):
        if self.connected:
            try:
                self._comPortObj.flush()  # wait until all data is written to the comport
                if self._comPortObj.in_waiting:
                    self.logger.log(logging.WARNING, 'flush input buffer with {} bytes waiting'.format(
                        self._comPortObj.in_waiting))
                    self._comPortObj.reset_input_buffer()
            except Exception as e:
                self.logger.log(logging.WARNING, 'Exception during reset port: {}'.format(e))

    def read(self):
        if self.connected:
            try:
                data = self._comPortObj.readline()
                self.buf += data
                if b'\n' in data:
                    msg = self.buf.decode().strip(' \t\n\r')
                    packet_time = datetime.datetime.now() - self.gw_start_time
                    msg_dict = {'time': packet_time.total_seconds(), 'raw': msg}
                    self.logger.log(logging.DEBUG, "got msg {}".format(msg_dict))
                    if msg.startswith(packet_prefix_str):
                        # got a packet
                        if self.packets_q.full():
                            dummy = self.packets_q.get()
                            self.logger.log(logging.WARNING, "packets_q is full, dropping {}".format(dummy))
                        self.packets_q.put(msg_dict)
                    else:
                        # got a responds
                        if self.gw_rsp_q.full():
                            dummy = self.gw_rsp_q.get()
                            self.logger.log(logging.WARNING, "gw_rsp_q is full, dropping {}".format(dummy))
                        self.gw_rsp_q.put(msg_dict)
                    self.buf = b''

                # check buffer status:
                if self._comPortObj.in_waiting > 2 * packet_bytes:
                    self.logger.log(logging.WARNING, 'buffer contains {} bytes'.format(self._comPortObj.in_waiting))
            except serial.SerialException as e:
                self.logger.log(logging.WARNING, ' Serial Exception during reading: {}'.format(e))
                if 'PermissionError' in str(e):
                    self.logger.log(logging.WARNING, 'disconnecting')
                    self.disconnect()
            except Exception as e:
                self.error_event.set()
                self.logger.log(logging.WARNING, ' problem during reading: {}\nreset buffer'.format(e))
                self.reset()


if __name__ == '__main__':
    commands = Queue(maxsize=100)
    gw_rsp = Queue(maxsize=100)
    packets = Queue(maxsize=100)
    connection_status = Event()
    event_error = Event()

    p_thread = Process(target=SerialProcess, args=(commands, gw_rsp, packets, connection_status,event_error))
    p_thread.start()
    time.sleep(1)
    commands.put({'cmd': SerialProcessState.CONNECT, 'data': {'port': 'COM3', 'baud': 921600}})
    connection_status.wait(3)
    if connection_status.is_set():
        print('connected')
        commands.put({'cmd': SerialProcessState.WRITE, 'data': {'gw_cmd': '!version'}})
        try:
            version_msg = gw_rsp.get(timeout=1)
            print('got rsp: {}'.format(version_msg))
        except Empty:
            print('empty')
    else:
        print('problem during connection')
