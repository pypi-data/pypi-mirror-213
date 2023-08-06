<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/supergugugu/1.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/2.png" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-bili-push
 B订阅推送插件 
</div>

## 示例

![输入图片描述](README_md_files/9cf89890-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)
![输入图片描述](README_md_files/7fd7ee50-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)


## 安装
（以下方法三选一）

一.命令行安装：

    nb plugin install nonebot-plugin-bili-push
 二.使用插件文件安装：（不推荐） 
 
1.下载插件文件，放到plugins文件夹。

2.修改pyproject.toml使其可以加载插件

三.pip安装：（不推荐）
1.执行此命令

    pip install nonebot-plugin-bili-push
2.修改pyproject.toml使其可以加载插件

    plugins = [”nonebot-plugin-bili-push“]
 
## 配置
在 nonebot2 项目的`.env`文件中选填配置

配置管理员账户，只有管理员才能添加订阅

    SUPERUSERS=["12345678"] # 配置 NoneBot 超级用户
插件数据存放位置，默认为 “./”。

    bilipush_basepath="./"

刷新间隔：每次刷新间隔多少分钟，默认为12分钟。

    bilipush_waittime=12

发送间隔： 每次发送完成后等待的时间，单位秒，默认10-30秒。
时间为设置的时间再加上随机延迟10-20秒

    bilipush_sleeptime=10

## 参考内容
Mirai动态绘制插件 [BilibiliDynamic MiraiPlugin](https://github.com/Colter23/bilibili-dynamic-mirai-plugin)

## 交流
-   交流群[鸽子窝里有鸽子（291788927）](https://qm.qq.com/cgi-bin/qm/qr?k=QhOk7Z2jaXBOnAFfRafEy9g5WoiETQhy&jump_from=webapi&authKey=fCvx/auG+QynlI8bcFNs4Csr2soR8UjzuwLqrDN9F8LDwJrwePKoe89psqpozg/m)
-   有疑问或者建议都可以进群详谈。
