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
（以下方法二选一）

~~命令行安装：（未完成）~~

    pip install nonebot-plugin-bili-push
 使用插件文件安装：
 下载插件文件，放到plugins文件夹，并修改pyproject.toml使其可以加载插件
## 配置

 
在 nonebot2 项目的`.env`文件中选填配置
配置管理员账户，只有管理员才能添加订阅

    SUPERUSERS=["12345678"] # 配置 NoneBot 超级用户
插件数据存放位置，默认为 “./”。

    bilipush_basepath="./"


