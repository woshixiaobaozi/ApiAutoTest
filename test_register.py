'''
测试注册用例
'''

import pytest

from zonghe.baw import Member
from zonghe.caw import DataRead, Check
from zonghe.caw.MySqlOp import delete_user


@pytest.fixture(params=DataRead.read_Yaml(r'test_data\register_fail.yaml'))
def fail_data(request):
    return request.param

def test_register_fail(baserequest,url,fail_data):
    '''
    注册失败脚本
    :return:
    '''
    print(fail_data)
    #下发请求
    r = Member.register(baserequest,url,fail_data['data'])
    print(r.text)
    #检查结果与预期结果一致
    assert r.json()['status'] == fail_data['expect']['status']
    assert r.json()['code'] == fail_data['expect']['code']
    assert r.json()['msg'] == fail_data['expect']['msg']



@pytest.fixture(params=DataRead.read_Yaml(r'test_data/register_pass.yaml'))
def pass_data(request):
    return request.param

def test_register_pass(baserequest,url,pass_data,db_info):
    '''
    注册成功
    :return:
    '''
    #下发请求
    delete_user(db_info, pass_data['data']['mobilephone'])
    print('dbifo=========================', db_info)
    r = Member.register(baserequest, url, pass_data['data'])
    print(r.text)
    # 检查结果与预期结果一致
    # assert r.json()['status'] == pass_data['expect']['status']
    # assert r.json()['code'] == pass_data['expect']['code']
    # assert r.json()['msg'] == pass_data['expect']['msg']
    Check.equal(r.json(), pass_data['expect'], 'status,code,msg')

    #检查用户在系统中注册成功
    s = Member.list(baserequest,url)
    assert pass_data['data']['mobilephone'] in s.text
    #清理环境：删除用户
    delete_user(db_info,pass_data['data']['mobilephone'])

    #原则：测试环境在执行脚本前是什么样的，执行完脚本后要恢复到之前的状态（清理环境）
    #原则二：脚本执行的依赖环境，要在脚本中自己构建 如
    #审核项目接口测试时依赖已有的项目，需要先调用添加项目的接口准备测试环境
    #脚本的健壮性、稳定性比较高

    #重复注册测试逻辑
    #下发注册请求
    #下发注册请求（检查结果，报错重复注册）
    #恢复环境删除用户

@pytest.fixture(params=DataRead.read_Yaml(r'test_data/register_pass2.yaml'))
def pass_data2(request):
    return request.param

def test_register_fail2(baserequest, url,db_info,pass_data2):
    '''
    注册成功
    :return:
    '''
    print('================================',pass_data2)
    # #下发请求
    delete_user(db_info, pass_data2['data']['mobilephone'])
    # print('dbifo=========================', db_info)
    Member.register(baserequest, url, pass_data2['data'])
    r = Member.register(baserequest, url, pass_data2['data'])
    print('111111111111111111111111',r.json()['status'])
    # assert r.json()['status'] == pass_data2['expect']['status']
    # assert r.json()['code'] == pass_data2['expect']['code']
    # assert r.json()['msg'] == pass_data2['expect']['msg']
    Check.equal(r.json(), pass_data2['expect'], 'status,code,msg')

    # #清理环境：删除用户
    delete_user(db_info,pass_data2['data']['mobilephone'])