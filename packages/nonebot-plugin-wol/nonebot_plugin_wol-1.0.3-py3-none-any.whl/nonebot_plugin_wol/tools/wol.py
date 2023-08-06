import binascii
import os
import socket
import nonebot
import yaml
from ping3 import ping
from nonebot.log import logger
import asyncio


def wol(mac, ip):
    split = mac[2]
    packet = "FF" * 6
    packet += "".join(mac.split(split) * 16)
    udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM, proto=socket.IPPROTO_UDP)
    result = udp.sendto(binascii.unhexlify(packet), (ip, 9))
    udp.close()
    if result == len(binascii.unhexlify(packet)):
        return True
    else:
        return False


def get_args(information):
    return (i for i in information)


def get_yaml(f):
    json = yaml.load(f, yaml.FullLoader)
    if json is None:
        json = {}
    return json


def save_monitering_yaml(json, ip, id, f, name):
    if json is None:
        json = {}
    json["monitering"] = {name: {"ip": ip, "user_id": id}}
    yaml.dump(json, f)


async def check_alive():
    wol_path = os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(wol_path + "/../data/data.yaml"):
        with open(wol_path + "/../data/data.yaml", "r") as f:
            json = yaml.load(f, yaml.FullLoader)
            if json is None:
                return

        if json.get("monitering") is not None:
            del_list = []
            for i in json["monitering"]:
                result = ping(json["monitering"][i]["ip"])
                if result is None:
                    logger.info(f"{i}仍未在线")
                else:
                    bot = nonebot.get_bot()
                    if i == "tmp":
                        msg = "上线了"
                    else:
                        msg = f"{i}上线了"
                    await asyncio.gather(*[bot.send_msg(message=msg, user_id=json["monitering"][i]["user_id"])])
                    del_list.append(i)
            if del_list:
                for i in del_list:
                    del json["monitering"][i]
                with open(wol_path + "/../data/data.yaml", "w") as f:
                    yaml.dump(json, f)