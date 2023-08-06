from wiliot_deployment_tools.calibration_mgmt.calibration_mgmt import CalibrationManagementClient
from wiliot_core import check_user_config_is_ok
from wiliot_deployment_tools.common.utils_defines import *
from argparse import ArgumentParser
import sys
import bitstruct


def main():
    # parser
    parser = ArgumentParser(prog='wlt-calibration-mgmt',
                            usage='%(prog)s -o OwnerID -brg BridgeID (-t) [mode]',
                            description='CLI Tool for using Wiliot Bridge calibration management functionality')
    parser.add_argument('-owner', type=str, help="Owner ID", required=True)
    parser.add_argument('-brg', type=str, help="Bridge ID", required=False)
    parser.add_argument('-t', action='store_true',
                        help='if flag used, use test environment (prod is used by default)')
    parser.add_argument('-gw', type=str, help="GW ID to configure bridge (required only for broadcast mode)", required=False)
    parser.add_argument('-m', type=int, help="Minutes timeout (not required, defaults to 5 minutes)", required=False, default=5)
    parser.add_argument('-mode', '--option', choices=[0,1,2], type=int, help="Calinration mode selection: 0 - regular 1 - 38,38,39 2 - 37 on data only", required=True)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args, unknown = parser.parse_known_args()
    if args.t:
        env = 'test'
    else:
        env = 'prod'
    owner_id = args.owner
    conf_env = env if env == 'prod' else 'non-prod'
    user_config_file_path, api_key, is_success = check_user_config_is_ok(owner_id, conf_env, 'edge')


    user_config_file_path, api_key, is_success = check_user_config_is_ok(owner_id, env, 'edge')
    if is_success:
        print('credentials saved/upload from {}'.format(user_config_file_path))
    else:
        raise Exception('invalid credentials - please try again to login')

    client = CalibrationManagementClient(api_key, owner_id, env)
    client.send_calibration_packet_until_ack(gateway_id = args.gw, bridge_id = args.brg, minutes_timeout=args.m,mode = args.option)


def main_cli():
    main()
if __name__ == '__main__':
    main()
