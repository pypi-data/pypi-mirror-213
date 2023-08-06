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

# ---------------------------------------
#               run in real time:
# ---------------------------------------
import threading
import time
from wiliot_core.local_gateway.local_gateway_core import WiliotGateway, ActionType, DataType

continue_until_empty = False


def recv_data_handler(action_type, data_type):
    """

    :type action_type:ActionType
    :type data_type: DataType
    :return:
    """
    print("DataHandlerProcess Start")
    while True:
        time.sleep(0)  # important for the processor - keep it for fast performance
        # check if there is data to read
        if ObjGW.is_data_available():
            # get data
            try:
                data_in = ObjGW.get_packets(action_type=action_type, num_of_packets=10,
                                            data_type=data_type, max_time=0.1, is_blocking=False)
                if not data_in:
                    print('did not get data')
                    time.sleep(0.1)
                    continue
                data_in = data_in[0]
                if data_type.value == 'raw':
                    print("{} : {}".format(data_in['raw'], data_in['time']))
                elif data_type.value == 'processed':
                    for key, element in data_in.items():
                        print("{} : {}".format(key, element))
            except Exception as e:
                print('we got exception during collecting packets: {}'.format(e))
                time.sleep(0.1)
        else:  # no available data
            if continue_until_empty:
                # stop the analysis process
                ObjGW.stop_continuous_listener()
                return


# Open GW connection
ObjGW = WiliotGateway(auto_connect=True)
is_connected, _, _ = ObjGW.get_connection_status()
if is_connected:
    # Config GW:
    ObjGW.config_gw(filter_val=False, pacer_val=0, energy_pattern_val=18, time_profile_val=[5, 15],
                    beacons_backoff_val=0, received_channel=37)
    ObjGW.check_current_config()
    # acquiring and processing in real time
    ObjGW.start_continuous_listener()
    
    dataHandlerListener = threading.Thread(target=recv_data_handler, args=(ActionType.FIRST_SAMPLES,
                                                                           DataType.PROCESSED))
    dataHandlerListener.start()
    
    # stop all process due to event:
    time.sleep(10)
    ObjGW.stop_continuous_listener()
    
    # complete acquiring data:
    time.sleep(0.1)
    continue_until_empty = True
    
    # Close GW connection:
    ObjGW.close_port(is_reset=True)

else:
    print("connection failed")

# clean exit:
ObjGW.exit_gw_api()
