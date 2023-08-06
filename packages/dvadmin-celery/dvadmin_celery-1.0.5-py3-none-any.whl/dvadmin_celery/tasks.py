# -*- coding: utf-8 -*-

"""
@author: 阿辉
@contact: QQ:2655399832
@Created on: 2022/9/21 16:30
@Remark:
"""
from application.celery import app

@app.task
def task__one():
    print(11111)


@app.task
def task__two():
    print(22222)


@app.task
def task__three():
    print(33333)


@app.task
def task__four():
    print(44444)
