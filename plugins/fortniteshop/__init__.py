import httpx
import PIL.Image as Image
import os 
from bs4 import BeautifulSoup
from utils.utils import scheduler, get_bot
from nonebot import on_message
from utils.manager import group_manager
from configs.path_config import IMAGE_PATH
from utils.message_builder import image
from nonebot.adapters.cqhttp.exception import ActionFailed
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from services.log import logger
from nonebot import on_command
from nonebot.typing import T_State
from configs.path_config import IMAGE_PATH

__zx_plugin_name__ = "堡垒之夜每日商城"
__plugin_usage__ = """
usage：
    堡垒之夜每日商城
    指令：
        商城
""".strip()
__plugin_type__ = ("被动相关",)
__plugin_des__ = "堡垒之夜每日商城"
__plugin_cmd__ = ["商城"]
__plugin_version__ = 0.1
__plugin_author__ = "YiJiu Chow"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商城"],
}


@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=5,
)
async def dailyshop():
    try:
        shopdata=httpx.get('https://fnitemshop.com',headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34'})
        shophtml=shopdata.text
        shopsoup = BeautifulSoup(shophtml, 'lxml')
        n = 1
        for item in shopsoup.select('p a'):
            imgurl=item.get('href')
            if imgurl[len(imgurl)-3:len(imgurl)] == 'jpg':
                # skinimg = imgurl[0:len(imgurl)-9] + "bg.png"  png
                r = httpx.get(imgurl)
                with open('img/' + str(n) + '.png', 'wb') as f:
                    f.write(r.content)         
                n+=1
    except Exception as e:
        return logger.error(f"商城图片下载失败{e}")
    IMAGE_ROW = 5 # 行
    IMAGE_COLUMN = 9 # 列
    to_image = Image.new('RGB', (IMAGE_COLUMN * 1024, IMAGE_ROW * 1024),(64,224,208)) #创建一个新图
    # 把每张图片按顺序粘贴到对应位置上
    n=1
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            if os.path.exists('img/' + str(n) +'.png'):
                from_image = Image.open('img/'+ str(n) +'.png' ).resize(
                (1024, 1024),Image.ANTIALIAS)
                to_image.paste(from_image, ((x - 1) * 1024, (y - 1) * 1024))
                os.remove('img/' + str(n) +'.png')
            else:
                to_image.paste(Image.new('RGB',(1024,1024),(64,224,208)),((x - 1) * 1024, (y - 1) * 1024))
            n+=1
    to_image.save(IMAGE_PATH + 'fortniteshop/0.png')
    os.remove(IMAGE_PATH + 'fortniteshop/1.png')
    if n == 46:
        to_image2 = Image.new('RGB', (IMAGE_COLUMN * 1024, IMAGE_ROW * 1024),(64,224,208))
        for y in range(1, IMAGE_ROW + 1):
            for x in range(1, IMAGE_COLUMN + 1):
                if os.path.exists('img/' + str(n) +'.png'):
                    from_image = Image.open('img/'+ str(n) +'.png' ).resize(
                    (1024, 1024),Image.ANTIALIAS)
                    to_image2.paste(from_image, ((x - 1) * 1024, (y - 1) * 1024))
                    os.remove('img/' + str(n) +'.png')
                else:
                    to_image2.paste(Image.new('RGB',(1024,1024),(64,224,208)),((x - 1) * 1024, (y - 1) * 1024))
                n+=1
        to_image2.save(IMAGE_PATH + 'fortniteshop/1.png')
    try:
        bot = get_bot()
        gl = [754044548,913941037]
        for g in gl:
            imgnum = sum([os.path.isfile(listx) for listx in os.listdir(IMAGE_PATH + 'fortniteshop')])
            for s in imgnum:
                result = image(str(s) + ".png","fortniteshop")
                try:
                    await bot.send_group_msg(group_id=str(g), message=result)
                except ActionFailed:
                    logger.warning(f"{g} 群被禁言中，无法发送早安")
    except Exception as e:
        logger.error(f"商城错误 e:{e}")

shopshop = on_command("商城", priority=5, block=True)    
@shopshop.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    await shopshop.send(image("0.png","fortniteshop"))
    if os.path.exists(IMAGE_PATH + 'fortniteshop/1.png'):
        await shopshop.send(image("1.png","fortniteshop"))