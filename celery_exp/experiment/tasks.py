from __future__ import absolute_import, unicode_literals

from celery import shared_task
from time import sleep
from celery.utils.log import get_task_logger
from celery import group, chain
from django.apps import apps
from django.utils import timezone



@shared_task
def add(x, y):
    return x+y


logger = get_task_logger(__name__)

@shared_task
def run_parallel(id_):
    return group(parallel_task.si(i) for i in range(10))()


@shared_task
def chain_add():
    return chain(add.s(1,2), add.s(3), add.s(4))()


@shared_task
def parallel_task(id_):
    logger.info('-------> parallel task started %s' % id_)
    sleep(2)
    logger.info('-------> parallel task complete %s' % id_)


# celery -A celery_exp worker -l info --pool=gevent --concurrency=500
@shared_task
def make_lots_of_request_non_blocking(num):
    import grequests
    lst = []
    for i in range(num):
        url= 'https://jsonplaceholder.typicode.com/todos/1'
        res = grequests.get(url)
        lst.append(res)
    grequests.map(lst)
    logger.info('-----> make_lots_of_request task complete')

# celery -A celery_exp worker -l info 
@shared_task
def make_lots_of_request_blocking(num):
    import requests

    for i in range(num):
        url= 'https://jsonplaceholder.typicode.com/todos/1'
        res = requests.get(url)
        print("request number", i)
    logger.info('-----> make_lots_of_request task complete')