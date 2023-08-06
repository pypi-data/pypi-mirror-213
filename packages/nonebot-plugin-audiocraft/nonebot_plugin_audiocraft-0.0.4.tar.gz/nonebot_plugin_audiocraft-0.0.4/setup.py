# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_audiocraft']

package_data = \
{'': ['*']}

install_requires = \
['gradio-client>=0.2.5,<0.3.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-audiocraft',
    'version': '0.0.4',
    'description': "A nonebot plugin for facebook's audiocraft",
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-audiocraft\n</div>\n\n# 介绍\n- 本插件适配[Facebook开源的AI作曲模型](https://github.com/facebookresearch/audiocraft/)，在nonebot框架下调用已经部署好的模型后端服务器API进行AI作曲\n- 本插件需要配合部署好的audiocraft进行使用\n\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_audiocraft.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-audiocraft"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-audiocraft\n  ```\n# 后端服务器部署\n参考[官方仓库](https://github.com/facebookresearch/audiocraft#usage)部署好gradio后端，获得后端网址。（coblab上部署的可以开启gradio的外链分享）\n\n\n# 使用方法\n\n- 由于最近tx风控严重，go-cqhttp面临重启后可能掉账号的风险，所以插件使用给机器人发送消息配置后端服务器配置的方法。\n- 每次重启机器人后，使用 %%后端服务器地址 绑定audiocraft后端服务器。\n- 绑定后端服务器后，使用 AI作曲+乐曲的英文描述 即可触发AI作曲。\n- AI作曲的参数（如模型、时长）等通过代码进行修改，代码中有注释说明。\n\n# 效果\n\n![Alt](demo1.png)\n![Alt](demo2.png)\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
