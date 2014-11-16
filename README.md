resource_hot_update
===================

根据资源昨天的热度和昨天的下载量，更新资源今天的热度

resource_type.py
在该文件中添加了一个返回main_type总数的函数

resource_hot_update.py
该文件实现了对所有公有资源的每日热度更新

update_hot_day.py
执行该文件，调用resource_hot_update.py中的类，实现资源热度更新

