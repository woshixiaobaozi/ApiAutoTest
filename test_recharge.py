#前置条件，注册数据
import pytest

from zonghe.baw import Member
from zonghe.caw import DataRead, Check
from zonghe.caw.MySqlOp import delete_user

#注册数据
@pytest.fixture(params=DataRead.read_Yaml(r'test_data/login_setup.yaml'))
def setup_data(request):
    return request.param
#充值测试数据
@pytest.fixture(params=DataRead.read_Yaml(r'test_data/register_data.yaml'))
def register_data(request):
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

def test_recharge(register,baserequest, url,register_data):
    r = Member.recharge(baserequest, url, register_data['data'])
    #{"status":0,"code":"20104","data":null,"msg":"此手机号对应的会员不存在"}
    print(r.text)
    Check.equal(r.json(), register_data['expect'], 'status,code,msg')