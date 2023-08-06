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

import pandas as pd
import copy

from wiliot_core.packet_data.packet import Packet
from wiliot_core.packet_data.packet_list import PacketList


class TagCollection(dict):
    def __init__(self, packet_list_obj=PacketList):
        self.tags = {}  # key is adv_address, value is Packet_list
        self.metadata = {}
        self.packet_list_obj = packet_list_obj
    
    def __len__(self):
        """
        Amount of tags
        """
        return len(self.tags)
    
    def __add__(self, other_multi_tag):
        """
        merge 2 MultiTag object using '+' sign: multi_tag1+multi_tag2

        :type other_multi_tag: TagCollection
        :param other_multi_tag:

        :return: merged other_multi_tag, not mandatory
        """
        for id in other_multi_tag.keys():
            if id not in self.tags.keys():
                self.tags[id] = other_multi_tag[id].copy()
            else:
                self.tags[id] = self.tags[id] + other_multi_tag[id]
        return self
    
    def get_slice(self, items):
        """
        gets list of init and last indices to take

        :return: tag_collection with tags by requested idx
        """
        tag_collection = TagCollection()
        
        if type(items) is int:
            items = [items, items + 1]
        if items[-1] > len(self):
            items[-1] = len(self)
        keys = list(self.tags)[items[0]:items[-1]+1]
        if len(list(keys)) == 1:
            keys = list(keys)
        for key in keys:
            tag_collection.tags[key] = self.tags[key]
            tag_collection.metadata[key] = self.metadata.get(key, {})
        return tag_collection
    
    def copy(self):
        return copy.deepcopy(self)
    
    def append(self, packet, ignore_sprinkler=False, packets_id=None) -> None:
        """
        Adds single Packet to TagCollection

        :type packet: Packet or DecryptedPacket
        :param packet: packet to be added to packet_list
        :type ignore_sprinkler: Bool
        :param ignore_sprinkler: allow duplicates packets from different sprinkler
        :type packets_id: str
        :param packets_id: the tags id which define the multi tag structure (according to adv address, uid, ..)

        :return: None
        """
        if packets_id is None:
            packets_id = packet.packet_data['adv_address']
        
        if packets_id not in self.tags.keys():
            self.tags[packets_id] = PacketList().copy()
        
        self.tags[packets_id].append(packet, ignore_sprinkler)
    
    def dump(self, packet_dict_list: list):
        """
        gets list of raw_packet or packet_dict and fill packet_list with data

        :type packet_dict_list: list
        :param packet_dict_list: gw list (get_packets), fill packet_list with data

        :return: bool status
        """
        try:
            for packet_dict in packet_dict_list:
                packet = Packet(packet_dict)
                if packet.is_valid_packet:
                    self.print_live_stream(packet)
                    self.append(packet)
            return True
        except Exception as e:
            print(e)
            return False
    
    def print_live_stream(self, packet):
        """
        for future use - implement output
        """
        # set parameters to filter view by
        pass
    
    def get_statistics_by_id(self, id):
        """
        Calculates statistics of self.
        @return dictionary with predefined statistics of the packetList.
        """
        return self.tags[id].get_statistics()
    
    def get_avg_rssi_by_id(self, id=''):
        """
        return tag average rssi (4 decimal points accuracy)
        :type id: str
        :param id: adv_address or tag_id of wanted tag
        :return: average rssi for tag
        """
        return self.tags[id].get_avg_rssi()
    
    def get_avg_tbp_by_id(self, id='', ignore_outliers=False):
        """
        return tag average tbp (4 decimal points accuracy)
        :param ignore_outliers: reject data outside the 2 std area
        :type ignore_outliers: bool
        :type id: str
        :param id: adv_address or tag id of wanted tag

        :return: average tbp for tag
        """
        return self.tags[id].get_avg_tbp(ignore_outliers=ignore_outliers)
    
    def to_csv(self, path, val='time_from_start'):
        multi_tag_df = self.get_df(val=val)
        multi_tag_df.to_csv(path)
    
    def get_statistics(self, id_name='adv_address'):
        statistics_df = pd.DataFrame()
        for id in self.tags.keys():
            id_statistics = self.get_statistics_by_id(id)
            id_statistics[id_name] = id
            id_statistics_df = pd.DataFrame(id_statistics, index=[0])
            statistics_df = pd.concat([statistics_df, id_statistics_df], axis=0)
        return statistics_df
    
    def get_statistics_list(self, attributes=['adv_address', 'num_cycles', 'num_packets', 'tbp_mean', 'rssi_mean']):
        statistics_df = self.get_statistics()
        statistics_list = []
        specific_statistics_df = statistics_df[attributes]
        
        for index, row in specific_statistics_df.iterrows():
            dict = {}
            for att in attributes:
                dict[att] = row[att]
            statistics_list.append(dict.copy())
        
        return statistics_list
    
    def get_df(self, val='time_from_start'):
        multi_tag_df = pd.DataFrame()
        for tag in self.tags:
            multi_tag_df = multi_tag_df.append(self.tags[tag].get_df())
        
        multi_tag_df = multi_tag_df.sort_values(by=val)
        multi_tag_df = multi_tag_df.reset_index()
        
        return multi_tag_df
    
    def to_packet_list(self):
        packet_list = self.packet_list_obj()
        for packet_list_per_tag in self.tags.values():
            packet_list.__add__(packet_list_per_tag.copy())
        return packet_list


if __name__ == '__main__':
    import os
    
    try:
        df_path = os.path.abspath('../../internal/data_samples_for_tests/offline_tester@packets_data.csv')
        packet_list = PacketList()
        packet_list = packet_list.import_packet_df(path=df_path, import_all=True)
        tag_list = packet_list.to_tag_list()
        t = tag_list.get_by_index([1, 30])
    except:
        pass
    print('done')
