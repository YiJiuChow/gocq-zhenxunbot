from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Bot,Message,GroupMessageEvent
from . import data_source
from nonebot.adapters.cqhttp.message import MessageSegment

__zx_plugin_name__ = "点歌"
__plugin_usage__ = """
usage：
    在线点歌
    指令：
        点歌 歌曲名 
        点歌 歌曲名 歌手名 
        网易点歌 歌曲名 
        网易点歌 歌曲名 
""".strip()
__plugin_des__ = "为你点播了一首曾经的歌"
__plugin_cmd__ = ["点歌 [歌名]"]
__plugin_type__ = ("一些工具",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["点歌"],
}

qqmusic = on_command("点歌", priority=5)

@qqmusic.handle()
async def handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    msg = ''  
    if args !='':
        id =await data_source.qq_search(args)
        if id != '':
            msg=MessageSegment.music(type_='qq',id_=id)
    Msg = Message(msg)
    await qqmusic.finish(Msg)

music = on_command("网易点歌", priority=5)

@music.handle()
async def handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    msg = ''  
    if args !='':
        id =await data_source.neteasy_search(args)
        if id != '':
            msg=MessageSegment.music(type_='163',id_=id)
    Msg = Message(msg)
    await music.finish(Msg)

