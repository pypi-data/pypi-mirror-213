import datetime
import sys
import time
from wiliot_deployment_tools.api.extended_api import BridgeThroughGatewayAction, ExtendedEdgeClient, GatewayType
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.common.utils_defines import  SEC_TO_SEND


class CalibrationManagementError(Exception):
    pass
  

class CalibrationManagementClient(ExtendedEdgeClient):


    def get_bridge_relevant_gw(self, bridge_id):
        """
        Returns relevant GW for sending actions to bridge
        :param bridge_id: Bridge ID
        :rtype: str
        :return: relevant Gateway ID
        """

        # TODO - return list of potential GWs
        potential_gws = list()
        owner_gws = self.get_gateways()
        owner_gw_ids = []
        owner_gw_ids.extend(g['gatewayId'] for g in owner_gws)
        for gw in self.get_bridge(bridge_id)['connections']:
            if gw['gatewayId'] not in owner_gw_ids:
                continue
            gw_id = gw['gatewayId']
            gw_dict = self.get_gateway(gw_id)
            if gw['connected'] and \
                    bridge_id in self.get_seen_bridges(gw_id) and \
                    self.check_gw_compatible_for_action(gw_id):
                if bridge_id in self.get_seen_bridges(gw['gatewayId']):
                    potential_gws.append(gw['gatewayId'])
        if len(potential_gws) == 0:
            raise CalibrationManagementError(f'No relevant GW connected to bridge! Check deployment')
        return potential_gws[0]

    def get_relevant_bridges(self, gateway_id):
        """
        Returns seen bridges by gateway that are associated to owner and have ble version with calibration management support
        :type gateway_id: str
        :param gateway_id: gateway ID
        :rtype: list
        :return: list of relevant bridge IDs
        """
        bridges = self.get_seen_bridges(gateway_id)
        relevant_bridges = bridges
        for bridge in bridges:
            brg_ble = self.get_brg_ble_version(bridge)
            if not self.check_ble_calibration_mgmt_support(brg_ble):
                # debug_print(f'Bridge {bridge} does not support calibration management!')
                relevant_bridges.remove(bridge)
        return relevant_bridges


    @staticmethod
    def check_ble_calibration_mgmt_support(ble_ver):
        """
        checks if calibration management is supported for BLE version
        :rtype: bool
        :return: True if supported, False otherwise
        """
        ble_ver = ble_ver.split('.')
        if not ((int(ble_ver[0]) > 3) or
                (int(ble_ver[0]) > 2 and int(ble_ver[1]) > 14) or \
                (int(ble_ver[0]) > 2 and int(ble_ver[1]) > 13 and int(ble_ver[2]) > 61)):
            return False
        else:
            return True


    def send_calib_mgmt_pkt(self, bridge_id, payload, gateway_id=None,
                          silent=False, seconds_to_send=1):
        """
        send calibration management packet to bridge
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: CalibrationManagementPacket
        :param packet: packet to send to bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type silent: bool
        :param silent: print calibration management packet parameters
        :type seconds_to_send: int
        :param seconds_to_send: seconds to repeat packet
        :rtype: bool
        :return: True if sent, False otherwise
        """
        if gateway_id is None:
            via_gw = self.get_bridge_relevant_gw(bridge_id)
        else:
            via_gw = gateway_id
        brg_version = None
        brg_version = self.get_brg_ble_version(bridge_id)
        gw_version = self.get_gw_ble_version(via_gw)
        for version in filter(None, [brg_version, gw_version]):
            if not self.check_ble_calibration_mgmt_support(version):
                return False
        rxtx = datetime.timedelta(milliseconds=
                                  self.get_gateway(via_gw)['reportedConf']['additional']['rxTxPeriodMs'])
        seconds_to_send = datetime.timedelta(seconds=seconds_to_send)
        reps = seconds_to_send // rxtx + 1
        if not silent:
            debug_print(f'Sending packet through GW {via_gw} for {seconds_to_send.total_seconds()} seconds, rxTx = {int(rxtx.total_seconds()*1000)} ms, reps = {reps}')
        res = self.send_bridge_action_through_gw(gateway_id,
                                                 BridgeThroughGatewayAction.SPARSE_37,
                                                 payload, bridge_id, reps=reps)
        return res

    
    def check_calib_mgmt_received(self, gateway_id, bridge_id, payload, time_sent):
        """
        check if calibration management packet was received by bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: CalibrationManagementPacket
        :param packet: packet to check
        :type time_sent: datetime
        :param time_sent: time packet was sent
        :rtype bool
        :return: True if packet was received, None otherwise
        """
        hours_back = (datetime.datetime.now() - time_sent + datetime.timedelta(seconds=5)).total_seconds() / 3600
        acks = self.get_acks(gateway_id, hours_back)
        if acks is None:
            return None
        acks = acks[(acks['actionType'] == BridgeThroughGatewayAction.SPARSE_37) &
                    (acks['bridgeId'] == bridge_id) &
                    (acks['payload'].apply(lambda x: x[1])
                     == payload[1])] 
        if len(acks) > 0:
            return acks.to_dict()
        return None

   
    def send_calibration_packet_until_ack(self, gateway_id, bridge_id, minutes_timeout=3, mode=0):
        """
        send calibration management packet repeatedly until it is received by the bridge
        :type gateway_id: str
        :param gateway_id: Gateway ID
        :type bridge_id: str
        :param bridge_id: Bridge ID
        :type packet: CalibrationManagementPacket
        :param packet: packet to send
        :type minutes_timeout: int
        :param minutes_timeout: timeout
        :rtype: dict
        :return: dict of {bridgeID: ack status (bool)} pairs
        """
        time_sent = datetime.datetime.now()
        payload = '0{:01d}{:019d}'.format(mode, 0)
        debug_print(f'Configuring {bridge_id} To Calibration mode {mode} | Max Waiting time {minutes_timeout} minutes')
        self.send_calib_mgmt_pkt(bridge_id, payload, gateway_id, silent=False, seconds_to_send=SEC_TO_SEND)
        time_gw_stops = time_sent + datetime.timedelta(seconds=SEC_TO_SEND)
        time_end = time_sent + datetime.timedelta(minutes=minutes_timeout)
        curr_time = time_sent
        ack = None
        print('Waiting For Ack...', end='', flush=True)
        while curr_time < time_end and ack is None:
            curr_time = datetime.datetime.now()
            if curr_time > time_gw_stops - datetime.timedelta(seconds=1):  # 1 second buffer
                self.send_calib_mgmt_pkt(bridge_id, payload, gateway_id, silent=True, seconds_to_send=SEC_TO_SEND)
                time_gw_stops = datetime.datetime.now() + datetime.timedelta(seconds=SEC_TO_SEND)
                print('!', end='')
                sys.stdout.flush()
            time.sleep(0.5)
            print('.', end='')
            sys.stdout.flush()
            ack = self.check_calib_mgmt_received(gateway_id, bridge_id, payload, time_sent)
        print()  # enter newline
        ack_received = False
        if ack is not None:
            ack_received = True
            debug_print(f'Ack Received after {datetime.datetime.now() - time_sent}')
        else:
            debug_print(f'Ack not received after {datetime.datetime.now() - time_sent}!')
        return {bridge_id: ack_received}