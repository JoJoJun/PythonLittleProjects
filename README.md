# PythonLittleProjects
陆续添加一些比较短小的python小程序   
## ascii.py:  
将图片转化为字符,核心是计算灰度只映射到每个字符  
## 2048.py:  
不到200行实现简易的小黑框2048，主逻辑是根据状态返回对应函数
## calculator.py:
用wxpython实现的简易带GUI计算器 utf-8 Python2.7语法 ；  
利用wx中的BoxSizer和GridSizer,添加输入框和按钮；绑定按钮事件；eval()进行计算  
## snow.py:
今日下雪~所以写了个很简单的龙猫背景的实现动态下雪效果的小程序 简单练习pygame  配合龙猫背景图snow.jpg 
## plane_mouse
python3 鼠标控制的基于pygame的飞机打敌机游戏  多子弹 多敌机 gameover后可点击鼠标重新开始 图片在同一文件夹下
## markup:
python3给纯文本文件test.txt添加HTML标签，生成.html文件 只添加了处理一级标题、二级标题、列表项、超链接、普通段落、斜体字等标签的规则，需要用到re正则表达式的匹配 纯文本文件中以空行来分隔不同的block，不同的block为添加标签的基本单位
