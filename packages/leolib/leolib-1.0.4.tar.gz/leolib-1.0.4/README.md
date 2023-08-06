# LEOLIB 利昂图书馆座位预约系统API

## 如何导入

`from leolib import User, get_day, get_time`

## 如何使用

```python
 from leolib import User, get_day, get_time


 # 用户对象
 user = User("username", "password", "zw.example.edu.cn")
 # 查看用户信息
 print(user.get_user_info())
 # 获取预约信息
 print(user.get_history())
 # 查看房间布局
 print(user.get_room_status(13, get_date()))
 # 查询座位情况
 print(user.search_seat(start_time=get_time(), end_time=get_time("19:00")))
```