'''
脚本层的公共前置，后置，整个执行过程中执行一次
不用import，通过conftest文件名找到
'''

import pytest

from zonghe.caw import DataRead
from zonghe.caw.BaseRequests import BaseRequests


@pytest.fixture(scope='session')
def url():
    return DataRead.read_ini(r'test_env\env.ini','url')

@pytest.fixture(scope='session')
def db_info():
    #ini解析读出来的是字符串，但要使用的是字典用eval解析为原本格式
    s = DataRead.read_ini(r'test_env\env.ini', 'db_info')
    print('ssssssssssssssssssssssss',s)
    return eval(s)

@pytest.fixture(scope='session')
def baserequest():
    return BaseRequests()
