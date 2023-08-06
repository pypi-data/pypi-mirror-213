#  """
#    Copyright (c) 2016- 2023, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """
import logging

import numpy as np
import pandas as pd
import copy
import re
from enum import Enum
import os

packet_data_dict = {
    'adv_address': (0, 6),
    'en': (6, 1),
    'type': (7, 1),
    'data_uid': (8, 2),
    # 'group_id': (10, 3), #group id is only 22bits, we have a dedicated function for it
    'nonce': (13, 4),
    'enc_uid': (17, 6),
    'mic': (23, 6),
    'enc_payload': (29, 8),
}
gw_attributes = {
    'gw_packet': 'gw_packet',
    'rssi': 'rssi',
    'stat_param': 'stat_param',
    'time_from_start': 'time_from_start',
    'counter_tag': 'counter_tag',
    'is_valid_tag_packet': 'is_valid_tag_packet',
}
general_data = {
    'gw_process': 'gw_process',
    'is_valid_packet': 'is_valid_packet'
}
packet_length = 78
packet_tag_length = 74
rssi_char_last_index = 76
stat_param_last_index = 80

max_stat_param_val = 65535  # 2 bytes


class InlayTypes(Enum):
    TEO_086 = '086'
    TIKI_096 = '096'
    TIKI_099 = '099'
    BATTERY_107 = '107'
    TIKI_117 = '117'
    TIKI_118 = '118'
    TIKI_121 = '121'
    TIKI_122 = '122'


class Packet(object):
    """
    Wiliot Packet Object

        :param raw_packet: the raw packet to create a Packet object
        :type raw_packet: str or dict

        :return:
    """

    def __init__(self, raw_packet, time_from_start=None, custom_data=None,
                 inlay_type=None, logger_name=None):
        """
        :param raw_packet:
        :type raw_packet: str or dict
        :param logger_name: the log file we want to write into it.
        :type time_from_start: str
        :param time_from_start: the time when the packet was received according to the gw timer
        :type time_from_start: float
        :param custom_data: the packet custom data as dictionary
        :type custom_data: dict
        :param inlay_type: the antenna/ inlay type (e.g. tiki, teo)
        :type inlay_type: str
        """

        self.is_valid_packet = False
        if logger_name is not None:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = None

        if type(raw_packet) is dict:
            if raw_packet['is_valid_tag_packet']:
                get_packet_content = self.get_packet_content(raw_packet['packet'], get_gw_data=True)
                self.packet_data = {
                    'raw_packet': self.get_packet_content(raw_packet['packet']),
                    'adv_address': raw_packet['adv_address'],
                    'decrypted_packet_type': (int(raw_packet['packet'][24:25], 16) & 0xc) >> 2,
                    'group_id': self.extract_group_id(raw_packet['group_id'])
                }

                self.gw_data = {
                    'gw_packet': np.array(get_packet_content[packet_tag_length:]),
                    'rssi': np.array(raw_packet['rssi']),
                    'stat_param': np.array(raw_packet['stat_param']),  # gw_time
                    'time_from_start': np.array(raw_packet['time_from_start']),  # pc_time
                    'counter_tag': np.array(raw_packet['counter_tag']),
                    'is_valid_tag_packet': np.array(raw_packet['is_valid_tag_packet']),
                }
                self.gw_process = True
                self.is_valid_packet = True
            else:
                self.is_valid_packet = False
        elif type(raw_packet) is str:
            try:
                if not any(ext in raw_packet for ext in ['user_event', 'Command Complete Event']):
                    packet_data = self.get_packet_content(raw_packet)
                    raw_packet = self.get_packet_content(raw_packet, get_gw_data=True)
                    rssi_hex = raw_packet[packet_tag_length:rssi_char_last_index]
                    stat_param_hex = raw_packet[rssi_char_last_index:stat_param_last_index]

                    self.packet_data = {
                        'raw_packet': packet_data,
                        'adv_address': packet_data[:12],
                        'decrypted_packet_type': (int(packet_data[24:25], 16) & 0xc) >> 2,
                        'group_id': self.extract_group_id(packet_data[20:26]),
                    }

                    rssi_in = np.array(float('nan'))
                    stat_param_in = np.array(float('nan'))
                    if rssi_hex != '':
                        rssi_in = np.array(int(rssi_hex, base=16))
                    if stat_param_hex != '':
                        stat_param_in = np.array(int(stat_param_hex, base=16))
                    self.gw_data = {
                        'gw_packet': np.array(raw_packet[packet_tag_length:]),
                        'rssi': rssi_in,
                        'stat_param': stat_param_in,
                        'time_from_start': np.array(time_from_start),
                        'counter_tag': np.array(float('nan')),
                        'is_valid_tag_packet': np.array(float('nan')),
                    }

                    self.gw_process = False
                    self.is_valid_packet = True
                else:
                    self.is_valid_packet = False
            except Exception as e:
                self.printing_and_logging('got corrupted packet: {}'.format(raw_packet))

        if not self.is_valid_packet:
            self.printing_and_logging('Invalid Packet: {}'.format(raw_packet))
        self.decoded_data = {}
        if custom_data is not None:
            self.custom_data = custom_data
        else:
            self.custom_data = {}
        self.inlay_type = inlay_type
        if self.is_valid_packet:

            self.packet_data['flow_ver'] = hex(
                int(self.packet_data['adv_address'][0:2] + self.packet_data['adv_address'][-2:], 16))

            self.packet_data['test_mode'] = 0
            flow_version = hex(int(self.packet_data['flow_ver'], 16))

            for key in packet_data_dict.keys():
                packet_data_value = self.get_attribute(self.packet_data['raw_packet'], packet_data_dict.get(key))
                self.packet_data[key] = packet_data_value

            if flow_version < hex(0x42c):
                if 'FFFFFFFF' in self.packet_data['adv_address']:
                    self.packet_data['test_mode'] = 1
            elif flow_version < hex(0x500):
                if self.packet_data['adv_address'].startswith('FFFF') or self.packet_data['adv_address'].endswith(
                        'FFFF'):
                    self.packet_data['test_mode'] = 1
            else:
                if int(self.packet_data['data_uid'], 16) == 5:
                    self.packet_data['test_mode'] = 1
                    # TX LPM\HPM:
                    tx_lpm_hpm = self.packet_data['decrypted_packet_type'] & 1
                    self.decoded_data['tx_lpm_hpm'] = tx_lpm_hpm
                    if tx_lpm_hpm == 0:
                        self.decoded_data['tx_lpm_hpm_str'] = 'LPM'
                    else:
                        self.decoded_data['tx_lpm_hpm_str'] = 'HPM'
                    # battery mode:
                    battery_tag_ind = (self.packet_data['decrypted_packet_type'] & 2) >> 1
                    self.decoded_data['battery_tag_ind'] = battery_tag_ind

    def __len__(self):
        """
        gets number of sprinkler occurrences in packet
        """
        return self.gw_data['rssi'].size

    def __eq__(self, packet):
        """
        packet comparison
        """
        if self.is_same_sprinkler(packet):
            if packet.gw_data['gw_packet'].item() == self.gw_data['gw_packet'].item():
                return True
        return False

    def __str__(self):
        """
        packet print method
        """
        return str(
            'packet_data={packet_data}, gw_data={gw_data}'.format(packet_data=self.packet_data, gw_data=self.gw_data))

    def printing_and_logging(self, message):
        if self.logger:
            self.logger.info(message)
        else:
            print(message)

    def is_packet_from_bridge(self):
        return self.packet_data['raw_packet'][0] != '0'

    def get_payload(self):
        return self.packet_data['raw_packet'][16:74]

    def extract_group_id(self, raw_group_id, zero_bits=None, num_char=6):
        """
        extract group id from the raw group id packet
        :param raw_group_id: as it received by the gw
        :type raw_group_id: str
        :param zero_bits: number of bits from the group id that were taken to other feauture an should be ignored
        :type zero_bits: list
        :param num_char: number of group id charachters in the packets
        :type num_char: int
        :return: the group id
        :rtype: str
        """
        # need to zero 2 bits since 2 MSB bits of the group id are for decrypted_packet_type:
        # if raw group id is: 123456 --> the actual data is = 563412 --> the bit-location:{5: [16:20], 6:[20:24],
        # 3:[8:12], 4:[12:16], 1:[0:4], 2:[4:8]}
        if zero_bits is None:
            zero_bits = [16, 17]
        b = self.hex2bin(raw_group_id)
        if zero_bits is not None:
            b_list = list(b)
            for z in zero_bits:
                b_list[z] = '0'
            b = ''.join(b_list)
        return hex(int(b, 2))[2:].zfill(num_char)

    @staticmethod
    def hex2bin(hex, min_dig=0, zfill=True):
        b = bin(int(hex, 16))[2:]
        if zfill:
            b = bin(int(hex, 16))[2:].zfill(24)
        if len(b) > min_dig:
            pass
        else:
            b = b.zfill(min_dig)
        return b

    def set_inlay_type(self, inlay_type):
        self.inlay_type = inlay_type

    def is_in(self, packet):
        """
        is packet contains another packet

        :param packet: the other packet to verify
        :type packet: Packet

        :return: bool
        """
        if self.is_same_sprinkler(packet):
            if packet.gw_data['gw_packet'].item() in self.gw_data['gw_packet']:
                return True
        return False

    def get_packet(self):
        """
        gets raw packet string
        """
        return str(self.packet_data['raw_packet'])

    def split_packet(self, index):
        """
        split packet by index
        """
        packet_a = self.copy()
        packet_b = self.copy()
        remain = len(self) - index
        for key in self.gw_data.keys():
            for i in range(index):
                packet_a.gw_data[key] = np.delete(packet_a.gw_data[key], -1)

            for i in range(remain):
                packet_b.gw_data[key] = np.delete(packet_b.gw_data[key], 0)

        return packet_a, packet_b

    def copy(self):
        return copy.deepcopy(self)

    def sort(self):
        """
        sort gw_data lists according to gw_time
        """
        isort = np.argsort(self.gw_data['stat_param'])
        for key in self.gw_data.keys():
            self.gw_data[key] = self.gw_data[key][isort]

    def get_average_rssi(self):
        return np.average(self.gw_data['rssi'])

    # @staticmethod
    def is_short_packet(self):
        return len(self.get_packet_string(process_packet=False)) < packet_length

    @staticmethod
    def get_packet_content(raw_packet, get_gw_data=False):
        if 'process_packet' in raw_packet:
            raw_packet = raw_packet.split('(')[1]
            raw_packet = re.sub(r'\W+', '', raw_packet)

        if get_gw_data:
            return raw_packet
        else:
            return raw_packet[0:packet_tag_length]

    def get_packet_string(self, i=0, gw_data=True, process_packet=True):
        """
        gets process_packet string
        """
        process_packet_string = ['', '']
        if process_packet:
            process_packet_string = ['process_packet("', '")']

        if not self.is_valid_packet:
            return None
        if gw_data:
            gw_data = self.gw_data['gw_packet'].take(i)
        else:
            gw_data = ''
        return '{raw_packet}{gw_data}'.format(raw_packet=self.packet_data['raw_packet'],
                                              gw_data=gw_data).join(process_packet_string)

    def get_adva(self):
        return self.packet_data['adv_address']

    def get_flow(self):
        flow_version = hex(int(self.packet_data['flow_ver'], 16))
        return flow_version

    def get_rssi(self):
        return str(self.gw_data['rssi'])

    def get_packet_data_names(self):
        """
        extract all keys name which can potentially be a column in packet df
        :return:
        :rtype: list
        """
        dict_temp = self.__dict__
        keys = list(dict_temp.keys())
        for k in dict_temp.keys():
            if isinstance(dict_temp[k], dict):
                keys = keys + list(dict_temp[k].keys())
        return keys

    @staticmethod
    def get_attribute(raw_packet, loc_length):
        loc = loc_length[0] * 2
        length = loc_length[1] * 2
        return raw_packet[loc:loc + length]

    def is_same_sprinkler(self, packet):
        raw_packet = packet.packet_data['raw_packet']
        if raw_packet == self.packet_data['raw_packet']:
            return True
        return False

    def append_to_sprinkler(self, packet, output_log=True):
        status = True
        if self.is_same_sprinkler(packet):
            for i in range(len(packet)):
                try:
                    # stat param should be unique (time + rssi for same packet)- we make sure no duplications are added.
                    if np.take(packet.gw_data['stat_param'], i).item() not in self.gw_data['stat_param'] or \
                            np.take(packet.gw_data['time_from_start'], i).item() not in self.gw_data['time_from_start']:
                        for key in gw_attributes.keys():
                            self.gw_data[key] = np.append(self.gw_data[key], np.take(packet.gw_data[key], i))
                        for key in self.custom_data.keys():
                            if key in packet.custom_data.keys():
                                self.custom_data[key] = np.append(self.custom_data[key],
                                                                  np.take(packet.custom_data[key], i))
                            else:
                                self.custom_data[key] = np.append(self.custom_data[key], [None])
                    else:
                        if output_log:
                            self.printing_and_logging('Tried to add duplicated packet to sprinkler {}'.format(packet))
                except Exception as e:
                    self.printing_and_logging('Failed to add packet {} to sprinkler, exception: {}'
                                              .format(packet, str(e)))
        else:
            self.printing_and_logging('Not from the same sprinkler')
            status = False
        # self.sort()
        return status

    def as_dict(self, sprinkler_index=None):  # None not tested
        packet_data = self.packet_data.copy()
        sprinkler_gw_data = self.gw_data.copy()
        custom_data = self.custom_data.copy()
        if sprinkler_index is not None:
            if sprinkler_index > self.gw_data['stat_param'].size:
                return None
            for gw_attr in gw_attributes.keys():
                sprinkler_gw_data[gw_attr] = np.take(self.gw_data[gw_attr], sprinkler_index)
            for custom_attr in self.custom_data.keys():
                custom_data[custom_attr] = np.take(self.custom_data[custom_attr], sprinkler_index)
            dict_len = 1
        else:
            dict_len = len(self)
            for k, v in packet_data.items():
                packet_data[k] = [v] * dict_len

        data = {**packet_data, **sprinkler_gw_data, **custom_data}
        data['gw_process'] = [self.gw_process] * dict_len  # bool should be a list for pd.DataFrame.from_dict(data)
        data['is_valid_packet'] = [self.is_valid_packet] * dict_len  # bool should be a list
        data['inlay_type'] = [self.inlay_type] * dict_len
        return data

    def as_dataframe(self, sprinkler_index=None):
        data = self.as_dict(sprinkler_index=sprinkler_index)
        packet_df = pd.DataFrame.from_dict(data)

        return packet_df

    def get_per(self, expected_sprinkler_count=6):
        """
        Calculates the packet per at the sprinkler
        @param expected_sprinkler_count - in case of no beacons environment, sprinkler can be bigger than 6.
        @return packet per at percentage
        """
        return 100 * (1 - len(self) / expected_sprinkler_count)

    def get_tbp(self):
        """
        calculates the rate of packets from the same sprinkler
        :return: min_times_found - in msec
        :rtype: int
        """

        def triad_ratio_logic(diff_time_1, diff_time_2, ratio=1.0, error=10):
            """ estimate the time between successive packet according to only 3 packets out of 6 """
            if abs(diff_time_1 - ratio * diff_time_2) <= diff_time_2 / error:
                return True
            elif abs(diff_time_1 - (1 / ratio) * diff_time_2) <= diff_time_1 / error:
                return True
            else:
                return False

        def estimate_diff_packet_time(times_list, pc_time_list):
            if times_list.size < 3:
                return None
            sort_idx = pc_time_list.argsort()
            pc_time_list_sorted = pc_time_list.copy()[sort_idx]
            times_list_sorted = times_list.copy()[sort_idx]

            fix_sort_idx = []
            ind = 0
            pc_time_unique, pc_time_counts = np.unique(pc_time_list_sorted, return_counts=True)
            for unique, counts in zip(pc_time_unique, pc_time_counts):
                if counts > 1:  # several packets
                    ind_with_same_time = [i for i, t in enumerate(pc_time_list_sorted) if t == unique]
                    fix_sort_idx += list(times_list_sorted[ind_with_same_time].argsort() + ind_with_same_time[0])
                else:
                    fix_sort_idx.append(sort_idx[ind])
                ind += counts

            times_list_sorted = times_list_sorted[fix_sort_idx]

            dt = []
            for i, t_hw in enumerate(zip(times_list_sorted[1::], times_list_sorted[:-1])):
                dt_tmp = t_hw[0] - t_hw[1]
                if dt_tmp < 0:  # HW timing was zeroing during the same packets sprinkler
                    n_wrap = 1 + (round(
                        (pc_time_list_sorted[i + 1] - pc_time_list_sorted[i]) * 1000) // max_stat_param_val)
                    dt_tmp = (n_wrap * max_stat_param_val) + t_hw[0] - t_hw[1]
                dt.append(dt_tmp)

            return dt

        def check_if_nan(lst):
            is_nan = pd.isnull(lst)
            if (not isinstance(is_nan, np.ndarray) and is_nan) or (isinstance(is_nan, np.ndarray) and any(is_nan)):
                return True
            return False

        if check_if_nan(self.gw_data['time_from_start']) or check_if_nan(self.gw_data['stat_param']):
            return None

        estimate_diff_time = estimate_diff_packet_time(self.gw_data['stat_param'], self.gw_data['time_from_start'])
        if estimate_diff_time is None:
            return None
        elif len(self) == 3:
            if triad_ratio_logic(estimate_diff_time[0], estimate_diff_time[1], ratio=1):
                return None
            else:
                for ratio in [2, 3, 4]:
                    if triad_ratio_logic(estimate_diff_time[0], estimate_diff_time[1], ratio=ratio):
                        estimate_diff_time = [min(estimate_diff_time[0], estimate_diff_time[1]),
                                              max(estimate_diff_time[0], estimate_diff_time[1]) / ratio]
                        break
                if triad_ratio_logic(estimate_diff_time[0], estimate_diff_time[1], ratio=1.5):
                    estimate_diff_time = [min(estimate_diff_time[0], estimate_diff_time[1]) / 2,
                                          max(estimate_diff_time[0], estimate_diff_time[1]) / 3]

        return int(min(estimate_diff_time))

    def extract_packet_data_by_name(self, key):
        """
        extract data from all packet attribute according to the key name
        :param key: the name of the data (the key of the relevant dictionary)
        :type key: str
        :return: list of the data
        :rtype: list
        """

        if key in self.packet_data:
            data_attr = self.packet_data[key]
        elif hasattr(self, 'decoded_data') and key in self.decoded_data:
            data_attr = self.decoded_data[key]
        elif key in self.gw_data:
            data_attr = self.gw_data[key]
        elif key in self.custom_data:
            data_attr = self.custom_data[key]
        else:
            self.printing_and_logging('key:{} does not exist in packet structure')
            return None
        if isinstance(data_attr, np.ndarray):
            data_attr = data_attr.tolist()
        if not isinstance(data_attr, list):
            data_attr = [data_attr]
        return data_attr

    def filter_by_sprinkler_id(self, sprinkler_ids):
        """
        keep only specific sprinklers in a packet according to the sprinkler id
        :param sprinkler_ids:
        :type sprinkler_ids: list
        :return: filtered packet
        :rtype: Packet or DecryptedPacket
        """

        def filter_per_attr(data_attr):
            for key in data_attr.keys():
                if isinstance(data_attr[key], list) or \
                        (isinstance(data_attr[key], np.ndarray) and data_attr[key].size > 1):
                    filtered_data = [data_attr[key][i] for i in sprinkler_ids]
                    if isinstance(data_attr[key], np.ndarray):
                        data_attr[key] = np.array(filtered_data)
                    else:
                        data_attr[key] = filtered_data
            return data_attr

        filtered_packet = self.copy()
        filtered_packet.gw_data = filter_per_attr(filtered_packet.gw_data)
        filtered_packet.custom_data = filter_per_attr(filtered_packet.custom_data)

        return filtered_packet

    def add_custom_data(self, custom_data):
        for key in custom_data.keys():
            if isinstance(custom_data[key], list):
                if len(custom_data[key]) == self.__len__():
                    self.custom_data[key] = custom_data[key]
                else:
                    self.printing_and_logging('add_custom_data failed - '
                                              'the custom data is a list of a different length than'
                                              ' the number of packets')
            else:
                self.custom_data[key] = self.__len__() * [custom_data[key]]


if __name__ == '__main__':
    packet_1 = {'packet': '03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C404200486436AE8F',
                'is_valid_tag_packet': True, 'adv_address': '03B28DCD9920', 'group_id': 'FE0000', 'rssi': 54,
                'stat_param': 44687,
                'time_from_start': 1.528374, 'counter_tag': 1}
    packet_2 = {'packet': '03B28DCD99201EFF0005FE0000E0210FFF93B635EBFF1DB118C6D782DC2ED98C404200486436AE82',
                'is_valid_tag_packet': True, 'adv_address': '03B28DCD9920', 'group_id': 'FE0000', 'rssi': 60,
                'stat_param': 44688,
                'time_from_start': 2.528374, 'counter_tag': 2}

    p1 = Packet(packet_1)
    p2 = Packet(packet_2)

    print(p1.get_packet_string(0))
    print(p1.get_average_rssi())

    print(p1 == p2)
    print(p1.append_to_sprinkler(p2))

    print(len(p1))
    print(p1.get_average_rssi())

    p1_dict = p1.as_dict()
    p1_df = pd.DataFrame(data=p1_dict)
    print(p1_df)

    print('end')
