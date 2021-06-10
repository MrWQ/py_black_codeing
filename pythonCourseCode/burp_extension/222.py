#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# @Time     : 2020/12/1 10:04 
# @Author   : ordar
# @File     : 222.py  
# @Project  : pythonCourse
# @Python   : 3.7.5
a = """{
    "success": true,
    "error_code": 0,
    "data": {
        "is_login": false
    },
    "msg": "\u6210\u529f\uff01"
}"""

print(a)
print(a.decode('unicode_escape'))
