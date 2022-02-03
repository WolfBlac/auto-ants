#!/usr/bin/python3

from ants_common import print_rsp
import logging
import pickle
from datetime import datetime
# from hexdump import hexdump
import os
from struct import pack
import sys
# import codecs
import re

# import sys
# logging.getLogger("scapy").setLevel(1)
# logging.basicConfig(stream = sys.stdout, level = logging.INFO)

from scapy.all import sniff, TCPSession, conf, wrpcap, IFACES
from scapy.utils import PcapWriter
from scapy.layers.l2 import Ether
from colorama import init, Fore

conf.use_pcap = True

SOME_IP = '75.2.101.205'
ANOTHER_IP = '99.83.178.222'

ANTS_IP = [ANOTHER_IP, SOME_IP]

MACOS_INTERFACE = 'en0'
LINUX_INTERFACE = 'eth0'
WIN_INTERFACE = 'vEthernet (BluestacksNxt)'

MY_BS_IP = '172.31.142'
MY_LOCAL_IP = '192.168.50'

if os.name == 'nt':
    INTERFACE = WIN_INTERFACE
    MY_IP = MY_BS_IP
elif os.name == 'posix':
    INTERFACE = MACOS_INTERFACE
    MY_IP = MY_LOCAL_IP
# define colors
GREEN = Fore.GREEN
RED   = Fore.RED
RESET = Fore.RESET

current_time = datetime.now().strftime("%H-%M-%S")
filename = "pcap/session-{}.pcap".format(current_time)
pktdump = PcapWriter(filename, append=True, sync=True)

SKIP_KEYWORDS = [
    # trash
    'AllianceBattle',
    'AllianceHelp',
    'AllianceTech', 'AllianceTechInfoRsp', 'AllianceTechRedPoint',
    'AllianceTechInfoParams',
    'ChatNotice',
    'ClaimAllianceGiftParams',
    'Heartbeat',
    'ItemInfos',
    'MapIntoInnerCityParams',
    'MapMarchLine',
    'MapMatrixInfoParams', 'MapMatrixInfoRsp',
    'ResourceInfosParams',
    'SyncTimeParams', 'SyncTimeRsp'
    'UpgradeEvent',
    'UsePassCardItem',
    # unneeded params with needed responses
    'WallDurabilityParams',
    'GetUserInfoParams'
]

SKIP_NEXT_LIST = [
    'MapMatrixInfoParams',
]

# ActivityBriefInfo
# AddCityBuffParams
# AllianceDailyInfoParams
# AllianceDailyInfoRsp
# AllianceDonateParams
# AllianceMemberPos
# AllianceStockNotify
# AllianceTech
# AllianceTechInfoRsp
# AllianceTechRedPoint
# BestWarZoneStageTypeParams # BestWarZoneStageTypeRsp
# BroadcastHeroNtf
# BuffBySourceNotify
# BuffItem
# BuildingFinishRsp
# BuildingUpgradeParams # BuildingUpgradeRsp
# ChangeHeroStatusParams
# FodderProduceFinishRsp
# GetUserInfoParams # UserInfoRsp
# HistoryParams
# ItemUseParams
# MissionAttackResult
# OtherBdInfosNotify
# RankParam
# ReqPlayerCrystalInfoParams
# ResAmountInfos
# RspPlayerCrystalInfo
# SendChatParams
# TechFinishRsp
# TechUpgradeParams
# TechUpgradeRsp
# TranslateParams # TranslateRsp
# TransResToBuildingParams # TransToBuildingRsp # TransEventFinishRsp
# UserGetHero
# UserTotalPower
# WallDurabilityParams # WallDurabilityRsp
# VisitAssistParams
# ModifyAPCParams

WHITELIST = ['NoticeNewsInfo', 'NotifyInfo']


def show_interfaces(resolve_mac=True):
    """Print list of available network interfaces"""
    return IFACES.show(resolve_mac)



def resolve_package(packet):
    pktdump.write(packet)
    # if packet.name in ['ARP', 'Ethernet']:
    #     return '\r'
    # result = packet.sprintf("{IP:%IP.src% -> %IP.dst%}")
    raw_data = packet.sprintf('{Raw:%Raw.load%}')

    data = raw_data
    if any(ext in data for ext in SKIP_KEYWORDS):
        data = ''
    # result = numpy.frombuffer(packet.original)
    # data = pickle.loads(bytes(data, 'utf-8'))
    if data:
        print('{}{}{}'.format(GREEN, raw_data, RESET))
        print_rsp(data)
        print_rsp(data, True)
    # for keyword in WHITELIST:
    #     data = data.replace(keyword, '{}{}{}'.format(RED, keyword, RESET))
    # data_result = data
    # for c in data:
    #     if chr(int(c, 16)) or hex(int(c, 16)):
    #         data_result += c
    #     else:
    #         data_result += codecs.encode(packet.original, 'hex')

    # return '{}\n{}\n' \
    #     .format(result, data) \
    #     .replace(MY_IP, 'WOOF')


def resolve_shields(packet):
    # result = packet.sprintf("{IP:%IP.src% -> %IP.dst%}")
    raw_data = packet.sprintf('{Raw:%Raw.load%}')

    data = raw_data
    if 'WallDurabilityRsp' not in data:
        return

    print('{}{}{}'.format(GREEN, raw_data, RESET))
    print_rsp(data)
    print_rsp(data, True)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        init()
        # logging.info(IFACES.data)
        # raise RuntimeError('dbg')
        capture = sniff(
            iface=INTERFACE,
            filter='host {} or host {}'.format(SOME_IP, ANOTHER_IP),
            # session=TCPSession,
            # prn=resolve_package,
            prn=resolve_shields,
            store=False,
            # count=200
        )

    except KeyboardInterrupt as e:
        logging.error(e)
        print('written to {}'.format(filename))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    except RuntimeError as e:
        logging.error(e)
    except OSError as e:
        logging.error(e)
    except Exception as e:
        logging.exception(e)
