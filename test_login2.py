import pytest

from zonghe.baw import Member
from zonghe.caw import DataRead, Check

from zonghe.caw.MySqlOp import delete_user

#前置条件，注册数据
@pytest.fixture(params=DataRead.read_Yaml(r'test_data/login_setup.yaml'))
def setup_data(request):
    return request.param
#登录测试数据
@pytest.fixture(params=DataRead.read_Yaml(r'test_data/login_data.yaml'))
def login_data(request):
    return request.param
#测试前置和后置，环境准备和清理
@pytest.fixture()
def register(baserequest,url,db_info,setup_data):
    #注册用户
    delete_user(db_info, setup_data['data']['mobilephone'])
    print('dbifo=========================', db_info)
    r = Member.register(baserequest, url, setup_data['data'])
    yield
    #删除用户
    delete_user(db_info, setup_data['data']['mobilephone'])

def test_login(baserequest,url,register,login_data):
    # 下发登录请求
    r = Member.login(baserequest, url, login_data['data'])
    print('登录', r.text)
    #检查结果
    # assert r.json()['status'] == login_data['expect']['status']
    # assert r.json()['code'] == login_data['expect']['code']
    # assert r.json()['msg'] == login_data['expect']['msg']
    Check.equal(r.json(),login_data['expect'],'status,code,msg')

@pytest.fixture(params=DataRead.read_Yaml(r'test_data/login.yaml'))
def setup_data2(request):
    return request.param
def test_login2(db_info,baserequest,url,register,setup_data2):
    #注册用户
    delete_user(db_info, setup_data2['regdata']['mobilephone'])
    print('dbifo=========================', db_info)
    r = Member.register(baserequest, url, setup_data2['regdata'])
    # 下发登录请求
    r = Member.login(baserequest, url, setup_data2['logindata'])
    print('登录', r.text)
    #检查结果
    # assert r.json()['status'] == setup_data2['expect']['status']
    # assert r.json()['code'] == setup_data2['expect']['code']
    # assert r.json()['msg'] == setup_data2['expect']['msg']
    Check.equal(r.json(), setup_data2['expect'], 'status,code,msg')
    #删除用户
    delete_user(db_info, setup_data2['regdata']['mobilephone'])
