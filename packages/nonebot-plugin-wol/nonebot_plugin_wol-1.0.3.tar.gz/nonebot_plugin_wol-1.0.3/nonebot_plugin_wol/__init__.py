
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import Message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent, PrivateMessageEvent
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from .config import Config
from .tools.wol import *
import os
from ping3 import ping
from nonebot_plugin_apscheduler import scheduler
from typing import Union


wol_path = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(wol_path + "/data/data.yaml"):
    os.mkdir(wol_path + "/data")
    open(f"{wol_path}/data/data.yaml", "w+").close()

send_wol = on_command("开机", aliases={"wol"}, permission=SUPERUSER, priority=20)
@send_wol.handle()
async def send_wol_handler(event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        information = args.extract_plain_text().split()
        if len(information) == 2:  # 直接唤醒不用别名
            with open(f"{wol_path}/data/data.yaml", "r") as f:
                json = get_yaml(f)
                if json.get("tmp") is not None:
                    await send_wol.finish("请等待上一个wol命令检查完成")
                ip, mac = get_args(information)
                result = wol(mac, ip)
                logger.info(f"唤醒电脑, 状态：{result}")
                if result:
                    save_monitering_yaml(json, ip, event.sender.user_id, f, "tmp")
                    await add_wol.finish("成功唤醒，请等待检测结果")
                else:
                    await add_wol.finish("唤醒失败，请检查ip和mac")

        with open(f"{wol_path}/data/data.yaml", "r") as f:
            json = yaml.load(f, yaml.FullLoader)
        if json is None:
            await add_wol.finish("没有创建配置，请使用命令  /添加电脑  创建配置")
        if len(information) == 1:
            if json.get(information[0]) is None:
                await add_wol.finish("没有此配置, 请检查别名")
            else:
                name = information[0]
                print(json)
                print(name)
                print(information)
                if json.get(name) is None:
                    await add_wol.finish("没有此电脑，请确认电脑名称")
                mac = json[name]["mac"]
                ip = json[name]["ip"]
                result = wol(mac, ip)
                logger.info(f"唤醒电脑{name}, 状态：{result}")
                if result:
                    with open(f"{wol_path}/data/data.yaml", "w") as f:
                        save_monitering_yaml(json, ip, event.sender.user_id, f, name)
                    await add_wol.finish("成功唤醒，请等待检测结果")
                else:
                    await add_wol.finish("唤醒失败，请检查ip和mac")
        else:
            await add_wol.finish("参数数量错误， 用法：/wol 别名\t或\t/wol ip, mac")

add_wol = on_command("添加电脑", aliases={"wol添加"}, permission=SUPERUSER, priority=20)
@add_wol.handle()
async def add_wol_handler(event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        information = args.extract_plain_text().split()
        if len(information) != 3:
            await add_wol.finish("请输入正确的格式：名称，ip，mac")
        name, ip, mac = get_args(information)
        logger.info(f"添加电脑，{name}, {ip}, {mac}, {information}")
        with open(f"{wol_path}/data/data.yaml", "r") as f:
            json = get_yaml(f)
            if json.get(name) is not None:
                await add_wol.finish("此配置已经存在")
            json[name] = {"ip": ip, "mac": mac}
        with open(f"{wol_path}/data/data.yaml", "w") as f:
            yaml.dump(json, f)
        await add_wol.finish(f"添加成功, 名称:{name}, ip:{ip}, mac:{mac}")

check_status = on_command("查看状态", aliases={"ping"}, permission=SUPERUSER, priority=20)
@check_status.handle()
async def check_status_handler(event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        msg = args.extract_plain_text().strip()
        if not msg:
            await check_status.finish("地址不能为空")
        result = ping(msg)
        if result is None:
            await check_status.finish("未在线")
        else:
            await check_status.finish("在线")

check_config = on_command("查看配置", aliases={"config"}, permission=SUPERUSER, priority=20)
@check_config.handle()
async def check_config_handler(event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        with open(f"{wol_path}/data/data.yaml", "r") as f:
            await check_config.finish(f.read())

show_help = on_command("wolhelp", permission=SUPERUSER, priority=20)
@show_help.handle()
async def show_help_handler(event: Union[PrivateMessageEvent, GroupMessageEvent], args: Message = CommandArg()):
    if isinstance(event, PrivateMessageEvent):
        await check_config.finish("唤醒\n·/wol ip mac 为直接唤醒\n·/wol 名称\t使用配置名称唤醒\n\n添加配置\n·/wol添加 名称 ip mac\n\nping\n·/ping ip\n\n查看帮助\n·/wolhelp\n\n查看当前配置名称\n·/config")

require("nonebot_plugin_apscheduler")
scheduler.add_job(check_alive, "interval", seconds=15, id="check_alive", misfire_grace_time=90)
