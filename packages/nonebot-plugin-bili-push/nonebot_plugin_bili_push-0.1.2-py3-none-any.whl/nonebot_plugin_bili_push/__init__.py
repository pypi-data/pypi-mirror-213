import os
import requests
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import json
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, MessageSegment
from nonebot import on_command
import sqlite3
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER
import random
from nonebot import require
import nonebot

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

config = nonebot.get_driver().config
# 读取配置
#
# 配置1：
# 管理员账号SUPERUSERS
# 需要添加管理员权限，参考如下：
# SUPERUSERS=["12345678"]
#
# 配置2：
# 文件存放目录
# 该目录是存放插件数据的目录，参考如下：
# bilipush_basepath="./"
# bilipush_basepath="C:/"
try:
    adminqq = config.superusers
    adminqq = list(adminqq)
except:
    adminqq = []
try:
    basepath = config.bilipush_basepath
except:
    basepath = "./"

# 创建基础参数
returnpath = ""
dbpath = basepath + 'botsdb/'
configpart = dbpath + 'config/'
fontdb = configpart + 'font.db'
livedb = dbpath + "live/Kanon_push.db"
emojidbname = dbpath + 'emoji/emoji.db'
dbpath = basepath + 'botsdb/'
pushlistdb = dbpath + "live/push_list.db"
livelistdb = dbpath + "live/livelist.db"
heartdb = basepath + 'local-ImgCache/heart.db'
configpart = dbpath + 'config/'
groupconfigdb = configpart + 'groupconfig.db'
half_text = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
             "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", ",",
             ".", "/", "\\", "[", "]", "(", ")", "!", "+", "-", "*", "！", "？", "。", "，", "{", "}", "、", "‘", "“",
             '"', "'", "！", " "]
url = "cdn.kanon.ink/api/image"


def get_emoji(emoji):
    cachepath = basepath + "cache/emoji/"
    if not os.path.exists(cachepath):
        os.makedirs(cachepath)
    cachepath = cachepath + emoji + ".png"
    if not cachepath.exists():
        url = "http://cdn.kanon.ink/api/emoji?imageid=" + emoji
        try:
            return_image = requests.get(url)
            return_image = Image.open(BytesIO(return_image.content))
            return_image.save(cachepath)
        except:
            print("api出错，请联系开发者")
            # api出错时返回空图
            return_image = Image.new("RGBA", (100, 100), color=(0, 0, 0, 100))
    else:
        return_image = Image.open("r", cachepath)
    return return_image


def is_emoji(emoji):
    url = "http://cdn.kanon.ink/json/emoji?imageid=" + emoji
    try:
        return_json = json.loads(requests.get(url).text)
        if return_json["code"] == 0:
            return True
        else:
            return False
    except:
        return False


def get_commands(message):
    # 获取发送的消息。使用第一个空格进行分段，无空格则不分段
    message = str(message)
    # 去除cq码
    message = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", message)
    commands = []

    if ' ' in message:
        messages = message.split(' ', 1)
        for command in messages:
            commands.append(command)
    else:
        commands.append(message)

    return commands


def circle_corner(img, radii):
    """
    圆角处理
    :param img: 源图象。
    :param radii: 半径，如：30。
    :return: 返回一个圆角处理后的图象。
    """

    # 画圆（用于分离4个角）
    circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形

    # 原图
    img = img.convert("RGBA")
    w, h = img.size

    # 画4个角（将整圆分离为4个部分）
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
    # alpha.show()

    img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
    return img


def new_background(image_x: int, image_y: int):
    image_x = int(image_x)
    image_y = int(image_y)
    # 创建 背景_背景
    new_image = Image.new(mode='RGB', size=(image_x, image_y), color="#d7f2ff")

    # 创建 背景_描边_阴影
    image_x -= 52
    image_y -= 52

    # 创建 背景_描边
    image_x -= 4
    image_y -= 4
    image_paste = Image.new(mode='RGB', size=(image_x, image_y), color="#86d6ff")
    image_paste = circle_corner(image_paste, radii=25)
    paste_x = int(int(new_image.width - image_paste.width) / 2)
    paste_y = int(int(new_image.height - image_paste.height) / 2)
    new_image.paste(image_paste,
                    (paste_x, paste_y, paste_x + image_paste.width, paste_y + image_paste.height),
                    mask=image_paste)
    # 创建 背景_底色
    image_x -= 3
    image_y -= 3
    # image_paste = Image.new(mode='RGB', size=(image_x, image_y), color="#f4fbfe")
    image_paste = Image.new(mode='RGB', size=(image_x, image_y), color="#eaf6fc")
    image_paste = circle_corner(image_paste, radii=25)
    paste_x = int(int(new_image.width - image_paste.width) / 2)
    paste_y = int(int(new_image.height - image_paste.height) / 2)
    new_image.paste(image_paste,
                    (paste_x, paste_y, paste_x + image_paste.width, paste_y + image_paste.height),
                    mask=image_paste)

    # 添加贴图
    # filepath = imagepath + 'config/背景图片.png'
    # image_paste = Image.open(filepath, mode="r")
    # filepath = str(imagepath + 'mask.png')
    # mask_image = Image.open(filepath, mode="r")
    # mask_image = mask_image.resize((800, 800))
    # image_x2 = image_x
    # image_y2 = image_y
    # numx = 1
    # while image_x2 >= 800:
    #     numx += 1
    #     image_x2 -= 800
    # numy = 1
    # while image_y2 >= 800:
    #     numy += 1
    #     image_y2 -= 800
    # printx = 0
    # while numx >= 1:
    #     numx -= 1
    #     printy = 0
    #     numy2 = numy
    #     while numy2 >= 1:
    #         numy2 -= 1
    #         new_image.paste(image_paste, (printx, printy, printx + 800, printy + 800), mask=mask_image)
    #         new_image.paste(image_paste, (printx, printy, printx + 800, printy + 800), mask=mask_image)
    #         printy += 800
    #     printx += 800

    return new_image


def image_resize2(image, size: [int, int], overturn=False):
    image_background = Image.new("RGBA", size=size, color=(0, 0, 0, 0))
    image_background = image_background.resize(size)
    w, h = image_background.size
    x, y = image.size
    if overturn:
        if w / h >= x / y:
            rex = w
            rey = int(rex*y/x)
            paste_image = image.resize((rex, rey))
            image_background.paste(paste_image, (0, 0))
        else:
            rey = h
            rex = int(rey*x/y)
            paste_image = image.resize((rex, rey))
            printx = int((w - rex) / 2)
            image_background.paste(paste_image, (printx, 0))
    else:
        if w/h >= x/y:
            print()
            rey = h
            rex = int(rey*x/y)
            paste_image = image.resize((rex, rey))
            printx = int((w - rex) / 2)
            printy = 0
            image_background.paste(paste_image, (printx, printy))
        else:
            print()
            rex = w
            rey = int(rex*y/x)
            paste_image = image.resize((rex, rey))
            printx = 0
            printy = int((h - rey) / 2)
            image_background.paste(paste_image, (printx, printy))

    return image_background


def draw_text(text: str,
              size: int,
              textlen: int = 20,
              fontfile: str = "./font/腾祥嘉丽中圆.ttf",
              biliemoji_infos=None,
              draw_qqemoji=False,
              calculate=False
              ):
    """
    - 文字转图片

    :param text: 输入的字符串
    :param size: 文字尺寸
    :param textlen: 一行的文字数量
    :param fontfile: 字体文字
    :param biliemoji_infos: 识别emoji
    :param draw_qqemoji: 识别qqemoji
    :param calculate: 计算长度。True时只返回空白图，不用粘贴文字，加快速度。

    :return: 图片文件（RGBA）
    """


    # 计算图片尺寸
    x_num = -1
    y_num = 0
    text_num = -1
    jump_num = 0
    for fort in text:
        text_num += 1
        if jump_num > 0:
            jump_num -= 1
        else:
            x_num += 1
            # 打印换行
            if x_num > textlen or fort == "\n":
                x_num = 0
                y_num += 1.2
                if fort == "\n":
                    x_num = -1
            biliemoji_name = ""
            if biliemoji_infos is not None:
                # 检测biliemoji
                if fort == "[":
                    testnum = 0
                    while testnum <= 55:
                        testnum += 1
                        findnum = text_num + testnum
                        if text[findnum] == "[":
                            testnum = 60
                        elif text[findnum] == "]":
                            biliemoji_name = "[" + text[text_num:findnum] + "]"
                            jump_num = len(biliemoji_name) - 1
                            testnum = 60
                if biliemoji_name != "":
                    # 粘贴biliemoji
                    for emoji_info in biliemoji_infos:
                        emoji_name = emoji_info["emoji_name"]
                        if emoji_name == biliemoji_name:
                            emoji_url = emoji_info["url"]
                            x_num += 1
            if biliemoji_name == "":
                conn = sqlite3.connect(emojidbname)
                cursor = conn.cursor()
                cursor.execute('select * from emoji where emoji = "' + fort + '"')
                data = cursor.fetchone()
                cursor.close()
                conn.close()
                if data is None:
                    # 打印文字
                    if fort in half_text:
                        x_num -= 0.4
                else:
                    # 打印表情
                    if not is_emoji(fort):
                        if fort in half_text:
                            x_num -= 0.4
    x = int((textlen + 1) * size)
    y = int((y_num + 1) * size * 1.2)

    image = Image.new("RGBA", size=(x, y), color=(0, 0, 0, 0))  # 生成透明图片
    draw_image = ImageDraw.Draw(image)
    fortsize = size
    font = ImageFont.truetype(font=fontfile, size=fortsize)

    if not calculate:
        x_num = -1
        y_num = 0
        text_num = -1
        jump_num = 0
        for fort in text:
            text_num += 1
            if jump_num > 0:
                jump_num -= 1
            else:
                x_num += 1
                # 打印换行
                if x_num > textlen or fort == "\n":
                    x_num = 0
                    y_num += 1.2
                    if fort == "\n":
                        x_num = -1
                biliemoji_name = ""
                if biliemoji_infos is not None:
                    # 检测biliemoji
                    if fort == "[":
                        testnum = 0
                        while testnum <= 55:
                            testnum += 1
                            findnum = text_num + testnum
                            if text[findnum] == "[":
                                testnum = 60
                            elif text[findnum] == "]":
                                biliemoji_name = text[text_num:findnum] + "]"
                                jump_num = len(biliemoji_name) - 1
                                testnum = 60
                    if biliemoji_name != "":
                        # 粘贴biliemoji
                        for emoji_info in biliemoji_infos:
                            emoji_name = emoji_info["emoji_name"]
                            if emoji_name == biliemoji_name:
                                emoji_url = emoji_info["url"]
                                response = requests.get(emoji_url)
                                paste_image = Image.open(BytesIO(response.content))
                                paste_image = paste_image.resize((int(fortsize * 1.2), int(fortsize * 1.2)))
                                image.paste(paste_image, (int(x_num * fortsize), int(y_num * fortsize)))
                                x_num += 1
                if biliemoji_name == "":
                    if is_emoji(fort):
                        paste_image = get_emoji(fort)
                        paste_image = paste_image.resize((int(fortsize * 1.1), int(fortsize * 1.1)))
                        image.paste(paste_image, (int(x_num * fortsize), int(y_num * fortsize)), mask=paste_image)
                    else:
                        draw_image.text(xy=(int(x_num * fortsize), int(y_num * fortsize)), text=fort,
                                        fill=(0, 0, 0), font=font)
                        if fort in half_text:
                            x_num -= 0.4

    return image


def get_draw(data):
    import time
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    date_year = str(time.strftime("%Y", time.localtime()))
    date_month = str(time.strftime("%m", time.localtime()))
    date_day = str(time.strftime("%d", time.localtime()))
    timenow = str(time.strftime("%H-%M-%S", time.localtime()))
    dateshort = date_year + date_month + date_day
    time_h = str(time.strftime("%H", time.localtime()))
    time_m = str(time.strftime("%M", time.localtime()))
    time_s = str(time.strftime("%S", time.localtime()))
    timeshort = time_h + time_m + time_s
    cachepath = basepath + "local-ImgCache/" + date_year + '/' + date_month + '/' + date_day + '/'

    qq = str(random.randint(10000, 99999))
    addimage = ""
    runcode = 1
    code = 0
    returnpath = ""
    run = 'on'  # 代码折叠
    if run == 'on':
        print('---开始获取数据----------')
        biliname = str(data["desc"]["user_profile"]["info"]["uname"])
        print('biliname:' + biliname)
        biliface = str(data["desc"]["user_profile"]["info"]["face"])
        print('biliface:' + biliface)
        biliface_round = str(data["desc"]["user_profile"]["pendant"]["image"])
        print('biliface_round:' + biliface_round)
        dynamicid = str(data["desc"]["dynamic_id"])
        print('dynamicid:' + dynamicid)
        timestamp = str(data["desc"]["timestamp"])
        print('timestamp:' + timestamp)
        timestamp = int(timestamp)
        timestamp = time.localtime(timestamp)
        timestamp = time.strftime("%Y年%m月%d日 %H:%M:%S", timestamp)
        print('timestamp:' + timestamp)
        bilitype = data["desc"]["type"]
        print('bilitype:' + str(bilitype))
        bilidata = data["card"]
        bilidata = json.loads(bilidata)
        try:
            emoji_infos = data["display"]["emoji_info"]["emoji_details"]
        except:
            emoji_infos = []

        fortsize = 30
        fontfile = './font/腾祥嘉丽中圆.ttf'
        font = ImageFont.truetype(font=fontfile, size=fortsize)

        # 转发动态
        if bilitype == 1:
            print('转发动态')
            card_message = bilidata["item"]["content"]
            print('card_message:' + str(card_message))
            origin_data = bilidata["origin"]
            origin_data = json.loads(origin_data)
            print('转发内容:')

            origin_type = bilidata["item"]["orig_type"]
            print('origin_type:' + str(origin_type))

            try:
                origin_emoji_infos = data["display"]["origin"]["emoji_info"]["emoji_details"]
            except:
                origin_emoji_infos = []

            # 测试用
            # origin_type = 0
            # code = 1
            # returnpath = "暂不支持动态类型"

            # 投稿视频
            if origin_type == 8:
                print(str(origin_data))
                print('转发的是视频')
                origin_biliname = origin_data["owner"]["name"]
                print('origin_biliname:' + str(origin_biliname))
                origin_biliface = origin_data["owner"]["face"]
                print('origin_biliface:' + str(origin_biliface))
                origin_timestamp = origin_data["ctime"]
                origin_timestamp = time.localtime(origin_timestamp)
                origin_timestamp = time.strftime("%Y年%m月%d日 %H:%M:%S", origin_timestamp)
                print('origin_timestamp:' + origin_timestamp)
                origin_title = origin_data["title"]
                print('origin_title:' + str(origin_title))
                origin_message = origin_data["desc"]
                print('origin_message:' + str(origin_message))
                origin_video_image = origin_data["pic"]
                print('origin_video_image:' + str(origin_video_image))

                print("开始绘图")
                if runcode == 1:
                    fortsize = 30
                    font = ImageFont.truetype(font=fontfile, size=fortsize)
                    origin_fortsize = 27
                    origin_font = ImageFont.truetype(font=fontfile, size=origin_fortsize)

                    image_x = 900
                    image_y = 140  # add base y
                    image_y += 125 + 35  # add hear and space
                    # 添加文字长度
                    paste_image = draw_text(card_message,
                                            size=30,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos,
                                            calculate=True)
                    w, h = paste_image.size
                    image_y += h
                    # 添加转发内容
                    origin_len_y = 120 + 90
                    # 添加转发的视频长度
                    origin_len_y += 220 + 20
                    # 将转发长度添加到总长度中
                    image_y += origin_len_y

                    # 开始绘制图像
                    image_x = int(image_x)
                    image_y = int(image_y)
                    draw_image = new_background(image_x, image_y)
                    draw = ImageDraw.Draw(draw_image)
                    # 开始往图片添加内容
                    # 添加头像
                    response = requests.get(biliface)
                    image_face = Image.open(BytesIO(response.content))
                    image_face = image_face.resize((125, 125))
                    imageround = get_emoji("imageround")
                    imageround = imageround.resize((129, 129))
                    draw_image.paste(imageround, (73, 73), mask=imageround)
                    imageround = imageround.resize((125, 125))
                    draw_image.paste(image_face, (75, 75), mask=imageround)

                    # 添加名字
                    cache_font = ImageFont.truetype(font=fontfile, size=35)
                    draw.text(xy=(230, 85), text=biliname, fill=(0, 0, 0), font=cache_font)

                    # 添加日期
                    draw.text(xy=(230, 145), text=timestamp, fill=(100, 100, 100), font=font)

                    # 添加动态内容
                    x = 75
                    y = 230
                    paste_image = draw_text(card_message,
                                            size=30,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)
                    w, h = paste_image.size
                    y += h
                    x = 65
                    # 添加转发内容
                    # 添加转发消息框
                    paste_image = Image.new("RGB", (776, origin_len_y + 4), "#FFFFFF")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x - 2, y - 2), mask=paste_image)

                    # 添加转发消息底图
                    paste_image = Image.new("RGB", (772, origin_len_y), "#f8fbfd")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)

                    # 添加转发头像
                    response = requests.get(origin_biliface)
                    image_face = Image.open(BytesIO(response.content))
                    image_face = image_face.resize((110, 110))
                    imageround = get_emoji("imageround")
                    imageround = imageround.resize((114, 114))
                    draw_image.paste(imageround, (x + 48, y + 48), mask=imageround)
                    imageround = imageround.resize((110, 110))
                    draw_image.paste(image_face, (x + 50, y + 50), mask=imageround)

                    # 添加名字
                    cache_font = ImageFont.truetype(font=fontfile, size=30)
                    draw.text(xy=(x + 190, y + 70), text=origin_biliname, fill=(0, 0, 0), font=cache_font)

                    # 添加日期
                    cache_font = ImageFont.truetype(font=fontfile, size=26)
                    draw.text(xy=(x + 190, y + 120), text=origin_timestamp, fill=(100, 100, 100), font=cache_font)

                    # 添加转发的内容
                    x += 20
                    y += 190

                    # 添加视频框
                    paste_image = Image.new("RGB", (730, 220), "#FFFFFF")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)
                    # 添加视频图像
                    response = requests.get(origin_video_image)
                    paste_image = Image.open(BytesIO(response.content))
                    paste_image = paste_image.resize((346, 216))
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x + 2, y + 2), mask=paste_image)
                    # 添加视频标题
                    x += 366
                    y += 20
                    fortsize = 27
                    cache_font = ImageFont.truetype(font=fontfile, size=27)

                    print_x = -1
                    print_y = 0
                    num = 0
                    jump_num = 0
                    textnum = 0
                    for text in origin_title:
                        textnum += 1
                        if jump_num > 0:
                            jump_num -= 1
                        else:
                            print_x += 1
                            num += 1
                            # 打印换行
                            if print_y >= 1 and print_x == 11:
                                text = "…"
                            if print_y >= 1 and print_x >= 12:
                                text = ""
                            elif print_y >= 2:
                                text = ""
                            if print_x > 12 or text == "\n":
                                num = 1
                                print_y += 1.2
                                print_x = 0
                                if text == "\n":
                                    print_x = -1

                            # 检测biliemoji
                            emoji_code = ""
                            if text == "[":
                                testnum = 1
                                while testnum <= 55:
                                    testnum += 1
                                    findnum = textnum + testnum
                                    if origin_title[findnum] == "-":
                                        testnum = 60
                                        emoji_code = ""
                                    elif origin_title[findnum] == "]":
                                        emoji_code = "[" + origin_title[textnum:findnum] + "]"
                                        jump_num = len(emoji_code) - 1
                                        testnum = 30
                                if emoji_code != "":
                                    # 粘贴biliemoji
                                    for emoji_info in origin_emoji_infos:
                                        emoji_name = emoji_info["emoji_name"]
                                        if emoji_name == emoji_code:
                                            emoji_url = emoji_info["url"]
                                            response = requests.get(emoji_url)
                                            paste_image = Image.open(BytesIO(response.content))
                                            paste_image = paste_image.resize((int(fortsize * 1.2), int(fortsize * 1.2)))
                                            draw_image.paste(paste_image,
                                                             (int(x + print_x * fortsize), int(y + print_y * fortsize)))
                                            print_x += 0.5

                            if emoji_code == "":
                                # 检测是否半格字符
                                conn = sqlite3.connect(emojidbname)
                                cursor = conn.cursor()
                                cursor.execute('select * from emoji where emoji = "' + text + '"')
                                data = cursor.fetchone()
                                cursor.close()
                                conn.close()
                                if data is None:
                                    # 打印文字
                                    draw.text(xy=(int(x + print_x * fortsize), int(y + print_y * fortsize)), text=text,
                                              fill=(0, 0, 0), font=cache_font)
                                    if text in half_text:
                                        print_x -= 0.4
                                else:
                                    # 打印表情
                                    try:
                                        paste_image = get_emoji(font)
                                        paste_image = paste_image.resize((int(fortsize * 1.1), int(fortsize * 1.1)))
                                        draw_image.paste(paste_image,
                                                         (int(x + print_x * fortsize), int(y + print_y * fortsize)))
                                    except:
                                        draw.text(xy=(int(x + print_x * fortsize), int(y + print_y * fortsize)),
                                                  text=text, fill=(0, 0, 0), font=cache_font)
                    # 添加视频简介
                    y += 70
                    fortsize = 25
                    cache_font = ImageFont.truetype(font=fontfile, size=25)

                    print_x = -1
                    print_y = 0
                    num = 0
                    jump_num = 0
                    textnum = 0
                    for text in origin_message:
                        textnum += 1
                        if jump_num > 0:
                            jump_num -= 1
                        else:
                            print_x += 1
                            num += 1
                            if print_y >= 2 and print_x == 12:
                                text = "…"
                            if print_y >= 2 and print_x >= 13:
                                text = ""
                            elif print_y >= 4:
                                text = ""
                            else:
                                # 打印换行
                                if print_x > 14 or text == "\n":
                                    num = 1
                                    print_y += 1.2
                                    print_x = 0
                                    if text == "\n":
                                        print_x = -1

                                # 检测biliemoji
                                emoji_code = ""
                                if text == "[":
                                    testnum = 1
                                    while testnum <= 55:
                                        testnum += 1
                                        findnum = textnum + testnum
                                        if origin_message[findnum] == "-":
                                            testnum = 60
                                            emoji_code = ""
                                        elif origin_message[findnum] == "]":
                                            emoji_code = "[" + origin_message[textnum:findnum] + "]"
                                            jump_num = len(emoji_code) - 1
                                            testnum = 30
                                    if emoji_code != "":
                                        # 粘贴biliemoji
                                        for emoji_info in origin_emoji_infos:
                                            emoji_name = emoji_info["emoji_name"]
                                            if emoji_name == emoji_code:
                                                emoji_url = emoji_info["url"]
                                                response = requests.get(emoji_url)
                                                paste_image = Image.open(BytesIO(response.content))
                                                paste_image = paste_image.resize(
                                                    (int(fortsize * 1.2), int(fortsize * 1.2)))
                                                draw_image.paste(paste_image,
                                                                 (int(x + print_x * fortsize),
                                                                  int(y + print_y * fortsize)))
                                                print_x += 0.5

                                if emoji_code == "":
                                    # 检测是否半格字符
                                    conn = sqlite3.connect(emojidbname)
                                    cursor = conn.cursor()
                                    try:
                                        cursor.execute('select * from emoji where emoji = "' + text + '"')
                                        data = cursor.fetchone()
                                    except:
                                        data = None
                                    cursor.close()
                                    conn.close()
                                    if data is None:
                                        # 打印文字
                                        draw.text(xy=(int(x + print_x * fortsize), int(y + print_y * fortsize)),
                                                  text=text,
                                                  fill=(100, 100, 100), font=cache_font)
                                        if text in half_text:
                                            print_x -= 0.4
                                    else:
                                        # 打印表情
                                        paste_image = get_emoji(font)
                                        paste_image = paste_image.resize((int(fortsize * 1.1), int(fortsize * 1.1)))
                                        draw_image.paste(paste_image,
                                                         (int(x + print_x * fortsize), int(y + print_y * fortsize)))

                    returnpath = cachepath + 'bili动态/'
                    if os.path.exists(returnpath):
                        print("已存在目录")
                    else:
                        os.makedirs(returnpath)
                    returnpath = returnpath + date + '_' + timenow + '_' + qq + '.png'
                    draw_image.save(returnpath)
                    print("returnpath" + returnpath)
                    print("运行bilinew成功")
                    code = 2

            # 图文动态
            elif origin_type == 2:
                print(str(origin_data))
                print('转发的是图文动态')
                origin_biliname = origin_data["user"]["name"]
                print('origin_biliname:' + str(origin_biliname))
                origin_biliface = origin_data["user"]["head_url"]
                print('origin_biliface:' + str(origin_biliface))
                origin_timestamp = origin_data["item"]["upload_time"]
                origin_timestamp = time.localtime(origin_timestamp)
                origin_timestamp = time.strftime("%Y年%m月%d日 %H:%M:%S", origin_timestamp)
                print('origin_timestamp:' + origin_timestamp)
                origin_message = origin_data["item"]["description"]
                print('origin_message:' + str(origin_message))
                origin_images = origin_data["item"]["pictures"]
                images = []
                for origin_image in origin_images:
                    image_url = origin_image["img_src"]
                    print('image_url:' + str(image_url))
                    images.append(image_url)
                try:
                    emoji_infos = data["display"]["emoji_info"]["emoji_details"]
                except:
                    emoji_infos = []

                print("开始绘图")
                if runcode == 1:
                    fortsize = 30
                    font = ImageFont.truetype(font=fontfile, size=fortsize)
                    origin_fortsize = 27
                    origin_font = ImageFont.truetype(font=fontfile, size=origin_fortsize)

                    image_x = 900
                    image_y = 140  # add base y
                    image_y += 125 + 65  # add hear and space
                    # 添加文字长度
                    paste_image = draw_text(card_message,
                                            size=30,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos,
                                            calculate=True)
                    w, h = paste_image.size
                    image_y += h
                    # 添加转发内容
                    origin_len_y = 120 + 60
                    # add message
                    paste_image = draw_text(origin_message,
                                            size=27,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos,
                                            calculate=True)
                    w, h = paste_image.size
                    origin_len_y += h

                    # 添加图片长度
                    imagelen = len(images)
                    if imagelen == 1:
                        # 单图，宽718
                        response = requests.get(images[0])
                        addimage = Image.open(BytesIO(response.content))
                        w, h = addimage.size
                        if h / w >= 1.8:
                            x = 718
                            y = int(718 * h / w)
                            addimage = addimage.resize((x, y))
                            w = 718
                            h = int(w * 1.8)
                        elif h / w <= 0.5:
                            y = 359
                            x = int(359 / h * w)
                            addimage = addimage.resize((x, y))
                            w = 718
                            h = 359
                        else:
                            y = int(718 * h / w)
                            x = 718
                            h = y
                            addimage = addimage.resize((x, y))
                        origin_len_y += h
                    elif imagelen == 2:
                        # 2图，图大小356
                        origin_len_y += 356 + 10
                    elif imagelen <= 4:
                        # 4图，图大小356
                        origin_len_y += 718 + 10
                    # elif imagelen <= 6:
                    else:
                        # 6图，图大小245
                        origin_len_y += 10
                        while imagelen >= 1:
                            imagelen -= 3
                            origin_len_y += 245 + 5

                    origin_len_y = int(origin_len_y)
                    # 将转发长度添加到总长度中
                    image_y += origin_len_y

                    image_x = int(image_x)
                    image_y = int(image_y)
                    draw_image = new_background(image_x, image_y)
                    draw = ImageDraw.Draw(draw_image)
                    # 开始往图片添加内容
                    # 添加头像
                    response = requests.get(biliface)
                    image_face = Image.open(BytesIO(response.content))
                    image_face = image_face.resize((125, 125))
                    imageround = get_emoji("imageround")
                    imageround = imageround.resize((129, 129))
                    draw_image.paste(imageround, (73, 73), mask=imageround)
                    imageround = imageround.resize((125, 125))
                    draw_image.paste(image_face, (75, 75), mask=imageround)

                    # 添加名字
                    cache_font = ImageFont.truetype(font=fontfile, size=35)
                    draw.text(xy=(230, 85), text=biliname, fill=(0, 0, 0), font=cache_font)

                    # 添加日期
                    draw.text(xy=(230, 145), text=timestamp, fill=(100, 100, 100), font=font)

                    # 添加动态内容
                    x = 75
                    y = 230
                    paste_image = draw_text(card_message,
                                            size=30,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)
                    w, h = paste_image.size
                    y += h
                    x = 65
                    # 添加转发内容
                    # 添加转发消息框
                    paste_image = Image.new("RGB", (776, origin_len_y + 4), "#FFFFFF")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x - 2, y - 2), mask=paste_image)

                    # 添加转发消息底图
                    paste_image = Image.new("RGB", (772, origin_len_y), "#f8fbfd")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)

                    # 添加转发头像
                    response = requests.get(origin_biliface)
                    image_face = Image.open(BytesIO(response.content))
                    image_face = image_face.resize((110, 110))
                    imageround = get_emoji("imageround")
                    imageround = imageround.resize((114, 114))
                    draw_image.paste(imageround, (x + 48, y + 48), mask=imageround)
                    imageround = imageround.resize((110, 110))
                    draw_image.paste(image_face, (x + 50, y + 50), mask=imageround)

                    # 添加名字
                    cache_font = ImageFont.truetype(font=fontfile, size=30)
                    draw.text(xy=(x + 190, y + 70), text=origin_biliname, fill=(0, 0, 0), font=cache_font)

                    # 添加日期
                    cache_font = ImageFont.truetype(font=fontfile, size=26)
                    draw.text(xy=(x + 190, y + 120), text=origin_timestamp, fill=(100, 100, 100), font=cache_font)

                    # 添加转发的内容
                    x += 35
                    y += 190
                    paste_image = draw_text(origin_message,
                                            size=28,
                                            textlen=22,
                                            biliemoji_infos=emoji_infos)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)
                    w, h = paste_image.size
                    x -= 10
                    y += h

                    print_y = y
                    print_x = x

                    # 添加图片
                    if imagelen == 1:
                        paste_image = addimage
                        paste_image = circle_corner(paste_image, 15)
                        draw_image.paste(paste_image, (x, y), mask=paste_image)
                    elif imagelen <= 4:
                        # 2图，图大小356
                        print_y = 0
                        print_x = -1
                        for image in images:
                            print_x += 1
                            if print_x >= 2:
                                print_x = 0
                                print_y += 1
                            response = requests.get(image)
                            paste_image = Image.open(BytesIO(response.content))
                            paste_image = image_resize2(image=paste_image, size=(356, 356),
                                                        overturn=True)
                            paste_image = circle_corner(paste_image, 15)
                            draw_image.paste(paste_image, (int(x + print_x * (356 + 5)), int(y + print_y * (356 + 5))),
                                             mask=paste_image)
                    else:
                        # 6图，图大小245
                        image_y += 506 + 15
                        num = 0
                        for image in images:
                            num += 1
                            if num >= 3:
                                print_x = x
                                print_y += 253 + 5
                            response = requests.get(image)
                            paste_image = Image.open(BytesIO(response.content))
                            paste_image = image_resize2(image=paste_image, size=(253, 253),
                                                        overturn=True)
                            paste_image = circle_corner(paste_image, 15)
                            draw_image.paste(paste_image, (int(print_x), int(print_y)), mask=paste_image)
                            print_x += 253 + 5

                    returnpath = cachepath + 'bili动态/'
                    if not os.path.exists(returnpath):
                        os.makedirs(returnpath)
                    returnpath = returnpath + date + '_' + timenow + '_' + qq + '.png'
                    draw_image.save(returnpath)
                    print("returnpath" + returnpath)
                    print("运行bilinew成功")
                    code = 2

            # 文字动态
            elif origin_type == 4:
                print(str(origin_data))
                print('转发的是文字动态')
                origin_biliname = origin_data["user"]["uname"]
                print('origin_biliname:' + str(origin_biliname))
                origin_biliface = origin_data["user"]["face"]
                print('origin_biliface:' + str(origin_biliface))
                origin_timestamp = origin_data["item"]["timestamp"]
                origin_timestamp = time.localtime(origin_timestamp)
                origin_timestamp = time.strftime("%Y年%m月%d日 %H:%M:%S", origin_timestamp)
                print('origin_timestamp:' + origin_timestamp)
                origin_message = origin_data["item"]["content"]
                print('origin_message:' + str(origin_message))

                print("开始绘图")
                if runcode == 1:
                    fortsize = 30
                    font = ImageFont.truetype(font=fontfile, size=fortsize)
                    origin_fortsize = 27
                    origin_font = ImageFont.truetype(font=fontfile, size=origin_fortsize)

                    image_x = 900
                    image_y = 140  # add base y
                    image_y += 125 + 35  # add hear and space
                    # 添加文字长度
                    paste_image = draw_text(card_message,
                                            size=30,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos,
                                            calculate=True)
                    w, h = paste_image.size
                    image_y += h
                    # 添加转发内容
                    origin_len_y = 120 + 90
                    # add message
                    paste_image = draw_text(origin_message,
                                            size=27,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos,
                                            calculate=True)
                    w, h = paste_image.size
                    origin_len_y += h
                    # 将转发长度添加到总长度中
                    image_y += origin_len_y

                    image_x = int(image_x)
                    image_y = int(image_y)
                    draw_image = new_background(image_x, image_y)
                    draw = ImageDraw.Draw(draw_image)
                    # 开始往图片添加内容
                    # 添加头像
                    response = requests.get(biliface)
                    image_face = Image.open(BytesIO(response.content))
                    image_face = image_face.resize((125, 125))
                    imageround = get_emoji("imageround")
                    imageround = imageround.resize((129, 129))
                    draw_image.paste(imageround, (73, 73), mask=imageround)
                    imageround = imageround.resize((125, 125))
                    draw_image.paste(image_face, (75, 75), mask=imageround)

                    # 添加名字
                    cache_font = ImageFont.truetype(font=fontfile, size=35)
                    draw.text(xy=(230, 85), text=biliname, fill=(0, 0, 0), font=cache_font)

                    # 添加日期
                    draw.text(xy=(230, 145), text=timestamp, fill=(100, 100, 100), font=font)

                    # 添加动态内容
                    x = 75
                    y = 230
                    paste_image = draw_text(card_message,
                                            size=30,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)
                    w, h = paste_image.size

                    y = y + h
                    x = 65
                    # 添加转发内容
                    # 添加转发消息框
                    paste_image = Image.new("RGB", (776, origin_len_y + 4), "#FFFFFF")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x - 2, y - 2), mask=paste_image)

                    # 添加转发消息底图
                    paste_image = Image.new("RGB", (772, origin_len_y), "#f8fbfd")
                    paste_image = circle_corner(paste_image, 15)
                    draw_image.paste(paste_image, (x - 2, y - 2), mask=paste_image)

                    # 添加转发头像
                    response = requests.get(origin_biliface)
                    image_face = Image.open(BytesIO(response.content))
                    image_face = image_face.resize((110, 110))
                    imageround = get_emoji("imageround")
                    imageround = imageround.resize((114, 114))
                    draw_image.paste(imageround, (x + 48, y + 48), mask=imageround)
                    imageround = imageround.resize((110, 110))
                    draw_image.paste(image_face, (x + 50, y + 50), mask=imageround)

                    # 添加名字
                    cache_font = ImageFont.truetype(font=fontfile, size=30)
                    draw.text(xy=(x + 190, y + 70), text=origin_biliname, fill=(0, 0, 0), font=cache_font)

                    # 添加日期
                    cache_font = ImageFont.truetype(font=fontfile, size=26)
                    draw.text(xy=(x + 190, y + 120), text=origin_timestamp, fill=(100, 100, 100), font=cache_font)

                    # 添加转发的内容
                    x = x + 75
                    y = y + 190
                    paste_image = draw_text(origin_message,
                                            size=28,
                                            textlen=24,
                                            biliemoji_infos=emoji_infos)
                    draw_image.paste(paste_image, (x, y), mask=paste_image)

                    returnpath = cachepath + 'bili动态/'
                    if os.path.exists(returnpath):
                        print("已存在目录")
                    else:
                        os.makedirs(returnpath)
                    returnpath = returnpath + date + '_' + timenow + '_' + qq + '.png'
                    draw_image.save(returnpath)
                    print("returnpath" + returnpath)
                    print("运行bilinew成功")
                    code = 2

        # 图文动态
        elif bilitype == 2:
            print('图文动态')
            card_message = bilidata["item"]["description"]
            print('card_message:' + str(card_message))
            card_images = bilidata["item"]["pictures"]
            images = []
            for card_image in card_images:
                image_url = card_image["img_src"]
                print('image_url:' + str(image_url))
                images.append(image_url)
            try:
                emoji_infos = data["display"]["emoji_info"]["emoji_details"]
            except:
                emoji_infos = []

            if runcode == 1:
                runcode = 0
                print("开始绘图")

                # 计算图片长度
                image_x = 900
                image_y = 140  # add base y
                image_y += 125 + 35  # add hear and space
                # 添加文字长度
                paste_image = draw_text(card_message,
                                        size=30,
                                        textlen=24,
                                        biliemoji_infos=emoji_infos,
                                        calculate=True)
                w, h = paste_image.size
                image_y += h
                # 添加图片长度
                imagelen = len(images)
                if imagelen == 1:
                    response = requests.get(images[0])
                    addimage = Image.open(BytesIO(response.content))
                    w, h = addimage.size
                    if h / w >= 1.8:
                        x = 770
                        y = int(770 * h / w)
                        addimage = addimage.resize((x, y))
                        w = 770
                        h = int(w * 1.8)
                        addimage = image_resize2(addimage, (w, h), overturn=True)
                    elif h / w <= 0.5:
                        y = 385
                        x = int(385 / h * w)
                        addimage = addimage.resize((x, y))
                        w = 770
                        h = 385
                        addimage = image_resize2(addimage, (w, h), overturn=True)
                    else:
                        y = int(770 * h / w)
                        x = 770
                        addimage = addimage.resize((x, y))
                        addimage = image_resize2(addimage, (x, y), overturn=True)
                    image_y += y
                elif imagelen == 2:
                    # 2图，图大小382
                    image_y += 382 + 10
                elif imagelen <= 4:
                    # 4图，图大小382
                    image_y += 764 + 15
                # elif imagelen <= 6:
                else:
                    # 6图，图大小253
                    image_y += 10
                    while imagelen >= 1:
                        imagelen -= 3
                        image_y += 253 + 5

                image_x = int(image_x)
                image_y = int(image_y)
                draw_image = new_background(image_x, image_y)
                draw = ImageDraw.Draw(draw_image)
                # 开始往图片添加内容
                # 添加头像
                response = requests.get(biliface)
                image_face = Image.open(BytesIO(response.content))
                image_face = image_face.resize((125, 125))
                imageround = get_emoji("imageround")
                imageround = imageround.resize((129, 129))
                draw_image.paste(imageround, (73, 73), mask=imageround)
                imageround = imageround.resize((125, 125))
                draw_image.paste(image_face, (75, 75), mask=imageround)

                # 添加名字
                cache_font = ImageFont.truetype(font=fontfile, size=35)
                draw.text(xy=(230, 85), text=biliname, fill=(0, 0, 0), font=cache_font)

                # 添加日期
                draw.text(xy=(230, 145), text=timestamp, fill=(100, 100, 100), font=font)

                # 添加动态内容
                x = 75
                y = 230
                paste_image = draw_text(card_message,
                                        size=30,
                                        textlen=24,
                                        biliemoji_infos=emoji_infos)
                draw_image.paste(paste_image, (x, y), mask=paste_image)
                w, h = paste_image.size

                x = 65
                y = 230 + h

                print_x = -1
                print_y = 0

                imagelen = len(images)
                if imagelen == 1:
                    paste_image = circle_corner(addimage, 15)
                    draw_image.paste(paste_image, (int(x), int(y)), mask=paste_image)
                elif imagelen <= 4:
                    # 2图，图大小382
                    for image in images:
                        print_x += 1
                        if print_x >= 2:
                            print_x = 0
                            print_y += 1

                        response = requests.get(image)
                        paste_image = Image.open(BytesIO(response.content))
                        paste_image = image_resize2(image=paste_image, size=(382, 382), overturn=True)
                        paste_image = circle_corner(paste_image, 15)
                        draw_image.paste(paste_image, (int(x + print_x * (382 + 5)), int(y + print_y * (382 + 5))),
                                         mask=paste_image)
                # elif imagelen <= 6:
                else:
                    # 6图，图大小253
                    for image in images:
                        print_x += 1
                        if print_x >= 3:
                            print_x = 0
                            print_y += 1

                        response = requests.get(image)
                        paste_image = Image.open(BytesIO(response.content))
                        paste_image = image_resize2(image=paste_image, size=(253, 253), overturn=True)
                        paste_image = circle_corner(paste_image, 15)
                        draw_image.paste(paste_image, (int(x + print_x * (253 + 5)), int(y + print_y * (253 + 5))),
                                         mask=paste_image)

                returnpath = cachepath + 'bili动态/'
                if not os.path.exists(returnpath):
                    os.makedirs(returnpath)
                returnpath = returnpath + date + '_' + timenow + '_' + qq + '.png'
                draw_image.save(returnpath)
                print("returnpath" + returnpath)
                print("运行bilinew成功")
                code = 2

        # 文字动态
        elif bilitype == 4:
            print('文字动态')

            card_message = bilidata["item"]["content"]
            print('card_message:' + str(card_message))
            try:
                emoji_infos = data["display"]["emoji_info"]["emoji_details"]
            except:
                emoji_infos = []

            if runcode == 1:
                runcode = 0
                print("开始绘图")
                fortsize = 30
                font = ImageFont.truetype(font=fontfile, size=fortsize)

                # 计算图片长度
                image_x = 900
                image_y = 140  # add base y
                image_y += 125 + 35  # add hear and space
                paste_image = draw_text(card_message,
                                        size=30,
                                        textlen=24,
                                        biliemoji_infos=emoji_infos,
                                        calculate=True)
                w, h = paste_image.size
                image_y += h

                image_x = int(image_x)
                image_y = int(image_y)
                draw_image = new_background(image_x, image_y)
                draw = ImageDraw.Draw(draw_image)
                # 开始往图片添加内容
                # 添加头像
                response = requests.get(biliface)
                image_face = Image.open(BytesIO(response.content))
                image_face = image_face.resize((125, 125))
                imageround = get_emoji("imageround")
                imageround = imageround.resize((129, 129))
                draw_image.paste(imageround, (73, 73), mask=imageround)
                imageround = imageround.resize((125, 125))
                draw_image.paste(image_face, (75, 75), mask=imageround)

                # 添加名字
                cache_font = ImageFont.truetype(font=fontfile, size=35)
                draw.text(xy=(230, 85), text=biliname, fill=(0, 0, 0), font=cache_font)

                # 添加日期
                draw.text(xy=(230, 145), text=timestamp, fill=(100, 100, 100), font=font)

                # 添加动态内容
                x = 75
                y = 230
                paste_image = draw_text(card_message,
                                        size=30,
                                        textlen=24,
                                        biliemoji_infos=emoji_infos)
                draw_image.paste(paste_image, (x, y), mask=paste_image)
                w, h = paste_image.size


                returnpath = cachepath + 'bili动态/'
                if os.path.exists(returnpath):
                    print("已存在目录")
                else:
                    os.makedirs(returnpath)
                returnpath = returnpath + date + '_' + timenow + '_' + qq + '.png'
                draw_image.save(returnpath)
                print("returnpath" + returnpath)
                print("运行bilinew成功")
                code = 2

        # 投稿视频
        elif bilitype == 8:
            print('投稿视频')
            print(str(bilidata))
            card_message = bilidata["dynamic"]
            print('card_message:' + str(card_message))
            card_title = bilidata["title"]
            print('card_title:' + str(card_title))
            card_vmessage = bilidata["desc"]
            print('card_vmessage:' + str(card_vmessage))
            card_image = bilidata["pic"]
            print('card_image:' + str(card_image))
            try:
                emoji_infos = data["display"]["emoji_info"]["emoji_details"]
            except:
                emoji_infos = []

            # 开始绘图
            image_x = 900
            image_y = 500
            # 添加文字长度
            paste_image = draw_text(card_message,
                                    size=30,
                                    textlen=24,
                                    biliemoji_infos=emoji_infos,
                                    calculate=True)
            w, h = paste_image.size
            image_y += h

            draw_image = new_background(image_x, image_y)
            draw = ImageDraw.Draw(draw_image)

            # 开始往图片添加内容
            # 添加头像
            response = requests.get(biliface)
            image_face = Image.open(BytesIO(response.content))
            image_face = image_face.resize((125, 125))
            imageround = get_emoji("imageround")
            imageround = imageround.resize((129, 129))
            draw_image.paste(imageround, (73, 73), mask=imageround)
            imageround = imageround.resize((125, 125))
            draw_image.paste(image_face, (75, 75), mask=imageround)

            # 添加名字
            cache_font = ImageFont.truetype(font=fontfile, size=35)
            draw.text(xy=(230, 85), text=biliname, fill=(0, 0, 0), font=cache_font)

            # 添加日期
            draw.text(xy=(230, 145), text=timestamp, fill=(100, 100, 100), font=font)

            # 添加动态内容
            x = 75
            y = 230
            print_x = -1
            print_y = 0
            num = 0
            jump_num = 0

            textnum = 0
            for text in card_message:
                if jump_num > 0:
                    jump_num -= 1
                else:
                    print_x += 1
                    textnum += 1
                    num += 1
                    # 打印换行
                    if num > 25 or text == "\n":
                        num = 1
                        print_y += 1.2
                        print_x = 0
                        if text == "\n":
                            print_x = -1

                    # 检测biliemoji
                    emoji_code = ""
                    if text == "[":
                        testnum = 1
                        while testnum <= 55:
                            testnum += 1
                            findnum = textnum + testnum
                            if card_message[findnum] == "]":
                                emoji_code = "[" + card_message[textnum:findnum] + "]"
                                jump_num = len(emoji_code) - 1
                                testnum = 60
                        if emoji_code != "":
                            print(emoji_code)
                            # 粘贴biliemoji
                            for emoji_info in emoji_infos:
                                emoji_name = emoji_info["emoji_name"]
                                if emoji_name == emoji_code:
                                    emoji_url = emoji_info["url"]
                                    response = requests.get(emoji_url)
                                    paste_image = Image.open(BytesIO(response.content))
                                    paste_image = paste_image.resize((int(fortsize * 1.2), int(fortsize * 1.2)))
                                    draw_image.paste(paste_image,
                                                     (int(x + print_x * fortsize), int(y + print_y * fortsize)))
                                    print_x += 0.5

                    if emoji_code == "":
                        # 检测是否半格字符
                        conn = sqlite3.connect(emojidbname)
                        cursor = conn.cursor()
                        cursor.execute('select * from emoji where emoji = "' + text + '"')
                        data = cursor.fetchone()
                        cursor.close()
                        conn.close()
                        if data is None:
                            # 打印文字
                            draw.text(xy=(int(x + print_x * fortsize), int(y + print_y * fortsize)), text=text,
                                      fill=(0, 0, 0), font=font)
                            if text in half_text:
                                print_x -= 0.4
                        else:
                            # 打印表情
                            paste_image = get_emoji(font)
                            paste_image = paste_image.resize((int(fortsize * 1.1), int(fortsize * 1.1)))
                            draw_image.paste(paste_image,
                                             (int(x + print_x * fortsize), int(y + print_y * fortsize)))

            y = int(y + (print_y + 1.5) * fortsize)
            x = 65
            # 添加视频消息边沿
            paste_image = Image.new("RGB", (776, 204), "#FFFFFF")
            paste_image = circle_corner(paste_image, 15)
            draw_image.paste(paste_image, (x - 2, y - 2), mask=paste_image)
            # 添加视频消息框
            paste_image = Image.new("RGB", (772, 200), "#f8fbfd")
            paste_image = circle_corner(paste_image, 15)
            draw_image.paste(paste_image, (x, y), mask=paste_image)
            # 添加视频图像
            x += 2
            y += 2
            response = requests.get(card_image)
            paste_image = Image.open(BytesIO(response.content))
            paste_image = image_resize2(paste_image, (313, 196))
            paste_image = circle_corner(paste_image, 15)
            draw_image.paste(paste_image, (x, y), mask=paste_image)
            # 添加视频标题
            x += 313 + 15
            y += 15
            if len(card_title) > 26:
                card_title = card_title[0:26] + "…"

            print_x = -1
            print_y = 0
            num = 0
            jump_num = 0
            cache_font = ImageFont.truetype(font=fontfile, size=27)

            textnum = 0
            for text in card_title:
                if jump_num > 0:
                    jump_num -= 1
                else:
                    print_x += 1
                    textnum += 1
                    num += 1
                    # 打印换行
                    if num > 14 or text == "\n":
                        num = 1
                        print_y += 1.2
                        print_x = 0
                        if text == "\n":
                            print_x = -1

                    # 检测biliemoji
                    emoji_code = ""
                    if text == "[":
                        testnum = 1
                        while testnum <= 55:
                            testnum += 1
                            findnum = textnum + testnum
                            if card_message[findnum] == "]":
                                emoji_code = "[" + card_message[textnum:findnum] + "]"
                                jump_num = len(emoji_code) - 1
                                testnum = 60
                        if emoji_code != "":
                            print(emoji_code)
                            # 粘贴biliemoji
                            for emoji_info in emoji_infos:
                                emoji_name = emoji_info["emoji_name"]
                                if emoji_name == emoji_code:
                                    emoji_url = emoji_info["url"]
                                    response = requests.get(emoji_url)
                                    paste_image = Image.open(BytesIO(response.content))
                                    paste_image = paste_image.resize((int(fortsize * 1.2), int(fortsize * 1.2)))
                                    draw_image.paste(paste_image,
                                                     (int(x + print_x * fortsize), int(y + print_y * fortsize)))
                                    print_x += 0.5

                    if emoji_code == "":
                        # 检测是否半格字符
                        conn = sqlite3.connect(emojidbname)
                        cursor = conn.cursor()
                        cursor.execute('select * from emoji where emoji = "' + text + '"')
                        data = cursor.fetchone()
                        cursor.close()
                        conn.close()
                        if data is None:
                            # 打印文字
                            draw.text(xy=(int(x + print_x * fortsize), int(y + print_y * fortsize)), text=text,
                                      fill=(0, 0, 0), font=cache_font)
                            if text in half_text:
                                print_x -= 0.4
                        else:
                            # 打印表情
                            paste_image = get_emoji(font)
                            paste_image = paste_image.resize((int(fortsize * 1.1), int(fortsize * 1.1)))
                            draw_image.paste(paste_image,
                                             (int(x + print_x * fortsize), int(y + print_y * fortsize)))

            # 添加视频简介
            x += 313 + 15
            y += 100
            if len(card_vmessage) > 26:
                card_vmessage = card_vmessage[0:26] + "…"

            x = 65 + 2 + 313 + 15
            print_x = -1
            print_y = 0
            num = 0
            jump_num = 0
            cache_font = ImageFont.truetype(font=fontfile, size=24)

            textnum = 0
            for text in card_vmessage:
                if jump_num > 0:
                    jump_num -= 1
                elif print_y > 2 and print_x >= 12:
                    text = "…"
                else:
                    if print_x == 11:
                        text = "…"
                    print_x += 1
                    textnum += 1
                    num += 1
                    # 打印换行
                    if num > 15 or text == "\n":
                        num = 1
                        print_y += 1.2
                        print_x = 0
                        if text == "\n":
                            print_x = -1

                    # 检测biliemoji
                    emoji_code = ""
                    if text == "[":
                        testnum = 1
                        while testnum <= 55:
                            testnum += 1
                            findnum = textnum + testnum
                            if card_message[findnum] == "]":
                                emoji_code = "[" + card_message[textnum:findnum] + "]"
                                jump_num = len(emoji_code) - 1
                                testnum = 60
                        if emoji_code != "":
                            print(emoji_code)
                            # 粘贴biliemoji
                            for emoji_info in emoji_infos:
                                emoji_name = emoji_info["emoji_name"]
                                if emoji_name == emoji_code:
                                    emoji_url = emoji_info["url"]
                                    response = requests.get(emoji_url)
                                    paste_image = Image.open(BytesIO(response.content))
                                    paste_image = paste_image.resize((int(fortsize * 1.2), int(fortsize * 1.2)))
                                    draw_image.paste(paste_image,
                                                     (int(x + print_x * fortsize), int(y + print_y * fortsize)))
                                    print_x += 0.5

                    if emoji_code == "":
                        # 检测是否半格字符
                        conn = sqlite3.connect(emojidbname)
                        cursor = conn.cursor()
                        cursor.execute('select * from emoji where emoji = "' + text + '"')
                        data = cursor.fetchone()
                        cursor.close()
                        conn.close()
                        if data is None:
                            # 打印文字
                            draw.text(xy=(int(x + print_x * fortsize), int(y + print_y * fortsize)), text=text,
                                      fill=(100, 100, 100), font=cache_font)
                            if text in half_text:
                                print_x -= 0.4
                        else:
                            # 打印表情
                            paste_image = get_emoji(font)
                            paste_image = paste_image.resize((int(fortsize * 1.1), int(fortsize * 1.1)))
                            draw_image.paste(paste_image,
                                             (int(x + print_x * fortsize), int(y + print_y * fortsize)))

            returnpath = cachepath + 'bili动态/'
            if os.path.exists(returnpath):
                print("已存在目录")
            else:
                os.makedirs(returnpath)
            returnpath = returnpath + date + '_' + timenow + '_' + qq + '.png'
            draw_image.save(returnpath)
            print("returnpath" + returnpath)
            print("运行bilinew成功")
            code = 2
        print('---结束获取数据----------')
    return [code, returnpath]


get_new = on_command("最新动态", aliases={'添加订阅', '删除订阅', '查看订阅', '帮助'}, block=False)


@get_new.handle()
async def _(bot: Bot, messageevent: MessageEvent):
    print("rubilibili_push")
    returnpath = ""
    code = 0
    qq = int(messageevent.get_user_id())
    message = messageevent.get_message()
    message = str(message)
    commands = get_commands(message)
    command = str(commands[0])
    command = command.removeprefix("/")
    print(command)
    if len(commands) >= 2:
        command2 = commands[1]
    else:
        command2 = ''
    if isinstance(messageevent, GroupMessageEvent):
        # 群消息才有群号
        groupcode = messageevent.group_id
        groupcode = str(groupcode)
        # 获取用户权限
        if await GROUP_ADMIN(bot, messageevent):
            info_premission = '5'  # 管理员
        elif await GROUP_OWNER(bot, messageevent):
            info_premission = '10'  # 群主
        else:
            info_premission = '0'  # 群员
    else:
        # 这是用户qq号
        groupcode = messageevent.get_user_id()
        groupcode = 'p' + str(groupcode)
        info_premission = '10'
    groupcode = "g" + groupcode

    import time
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    date_year = str(time.strftime("%Y", time.localtime()))
    date_month = str(time.strftime("%m", time.localtime()))
    date_day = str(time.strftime("%d", time.localtime()))
    timenow = str(time.strftime("%H-%M-%S", time.localtime()))
    dateshort = date_year + date_month + date_day
    time_h = str(time.strftime("%H", time.localtime()))
    time_m = str(time.strftime("%M", time.localtime()))
    time_s = str(time.strftime("%S", time.localtime()))
    timeshort = time_h + time_m + time_s

    cachepath = basepath + "local-ImgCache/" + date_year + '/' + date_month + '/' + date_day + '/'

    if command == "最新动态":
        print("command:查询最新动态")
        code = 0
        if "UID:" in command2:
            command2 = command2.removeprefix("UID:")
        try:
            command2 = int(command2)
            command2 = str(command2)
        except:
            command2 = ""
        if command2 == "":
            code = 1
            message = "请添加uid来查询最新动态"
        else:
            uid = command2
            print('-----------------------开始获取信息----------')
            url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=' + uid
            s = json.dumps({'key1': 'value1', 'key2': 'value2'})
            h = {'Content-Type': 'application/x-www-form-urlencoded'}
            returnjson = requests.post(url, data=s, headers=h).text
            returnjson = json.loads(returnjson)
            returncode = returnjson["code"]
            print('returncode:' + str(returncode))
            if returncode == 0:
                print('获取动态图片并发送')
                # 获取动态图片并发送
                draw_info = get_draw(returnjson["data"]["cards"][0])
                code = draw_info[0]
                returnpath = draw_info[1]
            else:
                print('returncode!=0')
                code = 1
                message = "获取动态失败"
    elif command == "添加订阅":
        if qq in adminqq:
            print("command:添加订阅")
            code = 0
            if "UID:" in command2:
                command2 = command2.removeprefix("UID:")
            try:
                command2 = int(command2)
                command2 = str(command2)
            except:
                command2 = ""
            if command2 == "":
                code = 1
                message = "请添加uid来添加订阅"
            else:
                uid = command2
                try:
                    # 数据库文件 如果文件不存在，会自动在当前目录中创建
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute('create table subscriptionlist '
                                   '(id int(10) primary key, groupcode varchar(10), uid int(10))')
                    cursor.close()
                    conn.close()
                except:
                    print('已存在订阅数据库，开始读取数据')
                conn = sqlite3.connect(livedb)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM subscriptionlist WHERE uid = " + str(uid) +
                               " AND groupcode = '" + str(groupcode) + "'")
                subscription = cursor.fetchone()
                cursor.close()
                conn.commit()
                conn.close()

                if subscription is None:
                    print("无订阅，添加订阅")
                    # 计算写入id
                    subid = 1
                    num = 60

                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    while num >= 1:
                        num -= 1
                        if num <= 10:
                            subid = random.randint(100, 9999)

                        cursor.execute("SELECT * FROM subscriptionlist WHERE id = " + str(subid))
                        data = cursor.fetchall()

                        if not data:
                            num = 0
                        else:
                            subid += 1
                    cursor.close()
                    conn.commit()

                    # 保存数据
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute(
                        'replace into subscriptionlist(id,groupcode,uid) values(' + str(subid) + ',"' + groupcode +
                        '","' + str(uid) + '")')
                    cursor.close()
                    conn.commit()
                    conn.close()

                    # 将历史动态存到数据库中
                    print('关注成功，将历史动态存到数据库中')
                    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=' + uid
                    s = json.dumps({'key1': 'value1', 'key2': 'value2'})
                    h = {'Content-Type': 'application/x-www-form-urlencoded'}
                    returnjson = requests.post(url, data=s, headers=h).text
                    returnjson = json.loads(returnjson)
                    returncode = returnjson["code"]
                    if returncode == 0:
                        print('获取动态图片并发送')
                        # 获取动态id并保存
                        return_datas = returnjson["data"]["cards"]

                        conn = sqlite3.connect(livedb)
                        cursor = conn.cursor()
                        for return_data in return_datas:
                            dynamicid = str(return_data["desc"]["dynamic_id"])
                            cursor.execute(
                                "replace into "+groupcode+"(dynamicid,uid) values('" + dynamicid + "','" + uid + "')")
                        cursor.close()
                        conn.commit()
                        conn.close()

                        code = 1
                        message = "添加订阅成功"
                    else:
                        code = 1
                        message = "保存数据库出错"
                else:
                    code = 1
                    message = "该up主已存在数据库中"
        else:
            code = 1
            message = "您无权限操作哦"
    elif command == "删除订阅":
        if qq in adminqq:
            print("command:取消订阅")
            code = 0
            if "UID:" in command2:
                command2 = command2.removeprefix("UID:")
            try:
                command2 = int(command2)
                command2 = str(command2)
            except:
                command2 = ""
            if command2 == "":
                code = 1
                message = "请添加uid来取消订阅"
            else:
                uid = command2
                try:
                    # 数据库文件 如果文件不存在，会自动在当前目录中创建
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute('create table subscriptionlist '
                                   '(id int(10) primary key, groupcode varchar(10), uid int(10))')
                    cursor.close()
                    conn.close()
                except:
                    print('已存在订阅数据库，开始读取数据')
                conn = sqlite3.connect(livedb)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM subscriptionlist WHERE uid = " + uid + " AND groupcode = '" + groupcode+"'")
                subscription = cursor.fetchone()
                cursor.close()
                conn.commit()
                conn.close()

                if subscription is None:
                    code = 1
                    message = "未订阅该up主"
                else:
                    subid = subscription[0]
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute('delete from subscriptionlist where uid = ' + uid)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    code = 1
                    message = "取消订阅成功"
        else:
            code = 1
            message = "您无权限操作哦"
    elif command == "查看订阅":
        try:
            # 数据库文件 如果文件不存在，会自动在当前目录中创建
            conn = sqlite3.connect(livedb)
            cursor = conn.cursor()
            cursor.execute('create table subscriptionlist '
                           '(id int(10) primary key, groupcode varchar(10), uid int(10))')
            cursor.close()
            conn.close()
        except:
            print('已存在订阅数据库，开始读取数据')
        conn = sqlite3.connect(livedb)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscriptionlist WHERE groupcode = '" + groupcode + "'")
        subscriptions = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        if not subscriptions:
            code = 1
            message = "该群无订阅"
        else:
            code = 1
            message = "订阅列表：\n"
            for subscription in subscriptions:
                uid = str(subscription[2])
                message += "UID:" + uid + "\n"
    elif command == "帮助":
        print()
        code = 1
        message = "Bili_Push：\n/添加订阅\n/删除订阅\n/查看订阅"

    if code == 1:
        msg = MessageSegment.text(message)
        await get_new.finish(msg)
    elif code == 2:
        msg = MessageSegment.image(r"file:///" + returnpath)
        await get_new.finish(msg)
    else:
        await get_new.finish()


@scheduler.scheduled_job("cron", minute="*/12", id="job_0")
async def run_every_6_minute():
    print("run bili push find")
    # ############获取动态更新，并绘制############
    import time
    date = str(time.strftime("%Y-%m-%d", time.localtime()))
    date_year = str(time.strftime("%Y", time.localtime()))
    date_month = str(time.strftime("%m", time.localtime()))
    date_day = str(time.strftime("%d", time.localtime()))
    timenow = str(time.strftime("%H-%M-%S", time.localtime()))
    dateshort = date_year + date_month + date_day
    time_h = str(time.strftime("%H", time.localtime()))
    time_m = str(time.strftime("%M", time.localtime()))
    time_s = str(time.strftime("%S", time.localtime()))
    timeshort = time_h + time_m + time_s
    cachepath = basepath + "local-ImgCache/" + date_year + '/' + date_month + '/' + date_day + '/'
    qq = str(random.randint(1000, 9999))
    message = ""

    botid = str(nonebot.get_bot())
    botid = botid.removeprefix("Bot(type='OneBot V11', self_id='")
    botid = botid.removesuffix("')")

    friends = await nonebot.get_bot().get_friend_list()
    friendlist = []
    for friendinfo in friends:
        friendlist.append(str(friendinfo['user_id']))

    groups = await nonebot.get_bot().get_group_list()
    grouplist = []
    for memberinfo in groups:
        grouplist.append(str(memberinfo['group_id']))

    # ############获取动态############s
    run = False  # 代码折叠
    if run:
        print('---------获取更新的动态----------')
        print("获取订阅列表")
        try:
            # 数据库文件 如果文件不存在，会自动在当前目录中创建
            conn = sqlite3.connect(livedb)
            cursor = conn.cursor()
            cursor.execute('create table subscriptionlist (id int(10) primary key, gruopcode varchar(10), uid int(10))')
            cursor.close()
            conn.close()
        except:
            print('已存在订阅数据库，开始读取数据')
        conn = sqlite3.connect(livedb)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscriptionlist")
        subscriptions = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()

        if not subscriptions:
            print("无订阅")
        else:
            subscriptionlist = []
            for subscription in subscriptions:
                uid = str(subscription[2])
                groupcode = subscription[1]
                if "p" in groupcode:
                    groupcode = groupcode.removeprefix("gp")
                    if groupcode in friendlist:
                        if uid not in subscriptionlist:
                            subscriptionlist.append(uid)
                else:
                    groupcode = groupcode.removeprefix("g")
                    if groupcode in grouplist:
                        if uid not in subscriptionlist:
                            subscriptionlist.append(uid)

            uids = ["1459104794", "171818544", "354218272"]
            for uid in uids:
                subscriptionlist.append(str(uid))

            for uid in subscriptionlist:
                print('-----------------------开始获取信息----------')
                url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=' + uid
                s = json.dumps({'key1': 'value1', 'key2': 'value2'})
                h = {'Content-Type': 'application/x-www-form-urlencoded'}
                returnjson = requests.post(url, data=s, headers=h).text
                returnjson = json.loads(returnjson)
                returncode = returnjson["code"]
                print('returncode:' + str(returncode))
                return_datas = returnjson["data"]
                return_datas = return_datas["cards"]
                print('获取数据成功')
                # 比较已保存内容
                try:
                    # 缓存文件，存储待发送动态 如果文件不存在，会自动在当前目录中创建
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute(
                        "create table 'wait_push' (dynamicid int(10) primary key, uid varchar(10), returnpath varchar(20))")
                    cursor.close()
                    conn.close()
                except:
                    print('已存在订阅数据库，开始读取数据')

                conn = sqlite3.connect(livedb)
                cursor = conn.cursor()
                for return_data in return_datas:
                    dynamicid = str(return_data["desc"]["dynamic_id"])

                    cursor.execute("SELECT * FROM 'wait_push' WHERE dynamicid = '" + dynamicid + "'")
                    data = cursor.fetchone()
                    if not data:
                        return_draw = get_draw(return_data)
                        print(str(return_draw))
                        if return_draw[0] != 2:
                            print("不支持类型")
                        else:
                            returnpath = return_draw[1]
                            # return_data = str(return_data)
                            cursor.execute("replace into wait_push(dynamicid,uid,returnpath) values(" +
                                           dynamicid + "," + uid + ',"' + returnpath + '")')

                cursor.close()
                conn.commit()
                conn.close()

    # ############推送动态############s
    run = True  # 代码折叠
    if run:
        conn = sqlite3.connect(livedb)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subscriptionlist")
        subscriptions = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()

        # 添加邦推送
        conn = sqlite3.connect(groupconfigdb)
        cursor = conn.cursor()
        cursor.execute("select * from groupconfig where bilibilidynamic = 'on'")
        configs = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()

        for config in configs:
            groupcode = str(config[0])
            uids = ["1459104794", "171818544", "354218272"]
            for uid in uids:
                subscription = []
                subscription.append("data")
                subscription.append(groupcode)
                subscription.append(uid)
                subscriptions.append(subscription)

        if not subscriptions:
            print("无订阅")
        else:
            for subscription in subscriptions:
                groupcode = subscription[1]
                uid = str(subscription[2])
                # 判断是否本bot以及是否主bot
                send = False
                # 读取主bot
                botswift = "off"
                try:
                    # 数据库文件 如果文件不存在，会自动在当前目录中创建
                    conn = sqlite3.connect(heartdb)
                    cursor = conn.cursor()
                    cursor.execute(
                        'create table ' + groupcode + '(botid VARCHAR(10) primary key, permission VARCHAR(20))')
                    cursor.close()
                    conn.close()
                except:
                    print('已存在锁定数据库，开始读取数据')
                conn = sqlite3.connect(heartdb)
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM ' + groupcode + ' WHERE permission = "10"')
                group_data = cursor.fetchone()
                cursor.close()
                conn.close()
                if group_data is None:
                    conn = sqlite3.connect(heartdb)
                    cursor = conn.cursor()
                    cursor.execute('replace into ' + groupcode + '(botid,permission) values("' + botid + '","10")')
                    cursor.close()
                    conn.commit()
                    conn.close()

                    botswift = 'on'
                else:
                    if group_data[0] == botid:
                        botswift = 'on'
                    else:
                        conn = sqlite3.connect(heartdb)
                        cursor = conn.cursor()
                        cursor.execute('select * from heart where botid = ' + str(group_data[0]))
                        data = cursor.fetchone()
                        cursor.close()
                        conn.close()

                        if data is not None:
                            if int(data[2]) >= 5:
                                botswift = 'on'

                        conn = sqlite3.connect(heartdb)
                        cursor = conn.cursor()
                        cursor.execute('SELECT * FROM ' + groupcode + ' WHERE permission = "5"')
                        data = cursor.fetchone()
                        cursor.close()
                        conn.close()
                        if data is None:
                            conn = sqlite3.connect(heartdb)
                            cursor = conn.cursor()
                            cursor.execute(
                                'replace into ' + groupcode + '(botid,permission) values("' + botid + '","5")')
                            cursor.close()
                            conn.commit()
                            conn.close()

                if botswift == "on":
                    if "p" in groupcode:
                        groupcode = groupcode.removeprefix("gp")
                        if groupcode in friendlist:
                            send = True
                        groupcode = "gp" + groupcode
                    else:
                        groupcode = groupcode.removeprefix("g")
                        if groupcode in grouplist:
                            send = True
                        groupcode = "g" + groupcode


                try:
                    # 缓存文件，存储待发送动态 如果文件不存在，会自动在当前目录中创建
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute(
                        "create table "+groupcode+" (dynamicid int(10) primary key, uid varchar(10))")
                    cursor.close()
                    conn.close()
                except:
                    print('已存在订阅数据库，开始读取数据')

                # 获取已推送的动态列表
                conn = sqlite3.connect(livedb)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM "+groupcode+" WHERE uid = " + uid)
                pushed_datas = cursor.fetchall()
                cursor.close()
                conn.commit()
                dynamicids = []
                for data in pushed_datas:
                    dynamicids.append(str(data[0]))

                # 获取新动态列表
                sqlite3.connect(livedb)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM 'wait_push' WHERE uid = '" + uid + "'")
                datas = cursor.fetchall()
                cursor.close()
                conn.commit()

                new_dynamicids = []
                for data in datas:
                    new_dynamicids.append(str(data[0]))

                pushlist = []
                if not dynamicids:
                    print("if not pushed_datas:")
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    for data in datas:
                        cursor.execute(
                            "replace into " + groupcode + "(dynamicid,uid) values(" +
                            str(data[0]) + "," + str(data[1]) + ")")
                    cursor.close()
                    conn.commit()
                    conn.close()
                    if new_dynamicids:
                        pushlist.append(new_dynamicids[0])

                elif dynamicids:

                    # 计算出未推送的动态
                    for new_dynamicid in new_dynamicids:
                        if new_dynamicid not in dynamicids:
                            if len(pushlist) <= 2:  # 限制单次发送条数
                                pushlist.append(new_dynamicid)
                print("未推送的动态" + str(pushlist))

                # 分别发送图片，并保存为已推送
                for dynamicid in pushlist:
                    conn = sqlite3.connect(livedb)
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM 'wait_push' WHERE dynamicid = " + dynamicid)
                    data = cursor.fetchone()
                    cursor.close()
                    conn.commit()
                    conn.close()

                    returnpath = data[2]
                    msg = MessageSegment.image(r"file:///" + returnpath)

                    sleeptime = random.randint(100, 500) / 10

                    if "p" in groupcode:
                        send_qq = groupcode.removeprefix("gp")
                        if send_qq in friendlist:
                            # bot已添加好友，发送消息
                            try:
                                await nonebot.get_bot().send_private_msg(user_id=send_qq, message=msg)
                                conn = sqlite3.connect(livedb)
                                cursor = conn.cursor()
                                cursor.execute(
                                    "replace into 'gp" + send_qq + "'(dynamicid,uid) values(" + dynamicid + "," + uid + ")")
                                cursor.close()
                                conn.commit()
                                conn.close()
                                print("发送私聊成功")
                            except:
                                print('私聊内容发送失败：send_qq：' + str(send_qq) + ",message:"
                                      + message + ",retrnpath:" + returnpath)
                            time.sleep(sleeptime)
                        else:
                            print("bot未入群")

                    else:
                        send_groupcode = groupcode.removeprefix("g")
                        print("groupcode:")
                        if send_groupcode in grouplist:
                            # bot已添加好友，发送消息
                            try:
                                print("开始发送群聊")
                                await nonebot.get_bot().send_group_msg(group_id=send_groupcode, message=msg)
                                conn = sqlite3.connect(livedb)
                                cursor = conn.cursor()
                                cursor.execute(
                                    "replace into 'g" + send_groupcode + "'(dynamicid,uid) values(" +
                                    dynamicid + "," + uid + ")")
                                cursor.close()
                                conn.commit()
                                conn.close()
                                print("发送群聊成功")
                            except:
                                print(
                                    '群聊内容发送失败：groupcode：' + str(send_groupcode) + ",message:"
                                    + message + ",retrnpath:" + returnpath)
                            time.sleep(sleeptime)
                        else:
                            print("bot未入群")

    print("run over")
    pass

