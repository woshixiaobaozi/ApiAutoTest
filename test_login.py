import pytest

from zonghe.baw import Member
from zonghe.caw import DataRead
from zonghe.caw.MySqlOp import delete_user


@pytest.fixture(params=DataRead.read_Yaml(r'test_data/login_pass.yaml'))
def pass_data(request):
    return request.param

@pytest.fixture()
def register():
    #注册用户
    yield
    #删除用户
def test_login_pass(baserequest,url,pass_data,db_info):
    '''
    注册成功
    :return:
    '''
    #下发请求
    delete_user(db_info, pass_data['data']['mobilephone'])
    print('dbifo=========================', db_info)
    r = Member.register(baserequest, url, pass_data['data'])

    r = Member.login(baserequest, url, pass_data['data'])
    print('登录',r.text)
    assert r.json()['status'] == pass_data['expect']['status']
    assert r.json()['code'] == pass_data['expect']['code']
    assert r.json()['msg'] == pass_data['expect']['msg']
    # #清理环境：删除用户
    delete_user(db_info,pass_data['data']['mobilephone'])
@pytest.fixture(params=DataRead.read_Yaml(r'test_data/login_fail.yaml'))
def fail_data(request):
    return request.param
def test_login_fail(baserequest,url,pass_data,fail_data,db_info):
    '''
    注册成功
    :return:
    '''
    Member.register(baserequest, url, pass_data['data'])

    r = Member.login(baserequest, url, fail_data['data'])
    print('登录',r.text)
    assert r.json()['status'] == fail_data['expect']['status']
    assert r.json()['code'] == fail_data['expect']['code']
    assert r.json()['msg'] == fail_data['expect']['msg']
    #清理环境：删除用户
    delete_user(db_info,fail_data['data']['mobilephone'])