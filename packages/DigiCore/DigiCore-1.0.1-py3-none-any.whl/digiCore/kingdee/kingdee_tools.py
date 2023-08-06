# _*_ coding: utf-8 _*_
# @Time : 2023/5/19
# @Author : yuza
# @Email ： yuw@doocn.com
# @File : DigiCore
# @Desc :
from typing import Optional

from pydantic import BaseModel, validator

from digiCore import format_error_msg, logger
import json
from concurrent.futures import ThreadPoolExecutor
from k3cloud_webapi_sdk.main import K3CloudApiSdk


class SdkConfig(BaseModel):
    """
    初始化sdk传参
    """
    acct_id: Optional[str]
    user_name: Optional[str]
    app_id: Optional[str]
    app_secret: Optional[str]
    server_url: Optional[str]
    lcid: Optional[int]
    connect_timeout: Optional[int] = 300
    request_timeout: Optional[int] = 300

    @validator("*", pre=True, always=True)
    def check_missing(cls, v):
        """
        判断参数是否存在
        """
        if v is None:
            raise ValueError('missing value')
        else:
            return v


class KingdeeTools():
    def __init__(self, config):
        """
        初始化kingdee sdk
        支持配置文件，和直接传参两种方式
        :param config: dict or str
            配置的详细数据，dict类型 需要包含以下字段
                acct_id: Optional[str] 第三方系统登录授权的账套ID
                user_name: Optional[str] 第三方系统登录授权的用户
                app_id: Optional[str] 第三方系统登录授权的应用ID
                app_secret: Optional[str] 第三方系统登录授权的应用密钥
                server_url: Optional[str] 服务Url地址(私有云需要配置自己的K3Cloud地址，公有云无需配置)
                lcid: Optional[int] 账套语系，默认2052
                connect_timeout: Optional[int] = 300 允许的最大连接延时，单位为秒
                request_timeout: Optional[int] = 300  允许的最大读取延时，单位为秒
            配置ini文件，str类型, config为该文件的完全路径，文件也应包含以上字段
        """
        self.api_sdk = K3CloudApiSdk(timeout=300)

        if isinstance(config, dict):
            try:
                config_new = SdkConfig(**config)
            except ValueError as e:
                logger.info(e)
                return
            self.api_sdk.InitConfig(acct_id=config_new.acct_id,
                                    user_name=config_new.user_name,
                                    app_id=config_new.app_id,
                                    app_secret=config_new.app_secret,
                                    server_url=config_new.server_url,
                                    lcid=config_new.lcid,
                                    connect_timeout=300,
                                    request_timeout=300
                                    )
        else:
            self.api_sdk.Init(config_path=config, config_node='config')

    def save_kg_model(self, formid: str, model: dict):
        """
        保存金蝶数据
        :param formid: 保存数据的类型编号
        :param model: 需要保存的数据（json格式）
        :return bool: 保存成功True， 保存失败False
        """
        data = dict()
        data['model'] = model
        try:
            response = self.api_sdk.Save(formid, data)
        except Exception as e:
            format_error_msg(e)
            return False
        res = json.loads(response)
        if res.get("Result").get("ResponseStatus").get("MsgCode") == 0:
            return True
        else:
            return False

    def save_kd_model_list(self, formid: str, model_list: list):
        """
        批量保存金蝶数据
        :param formid: 保存数据的类型编号
        :param model_list: 需要保存的数据
        :return bool: 保存成功True， 保存失败False
        """
        data = dict()
        data['model'] = model_list
        try:
            response = self.api_sdk.BatchSave(formid, data)
        except Exception as e:
            format_error_msg(e)
            return
        res = json.loads(response)
        if res.get("Result").get("ResponseStatus").get("MsgCode") == 0:
            return True
        else:
            return False

    def save_kd_model_list_multithread(self, formid: str, model_list: list, max_worker: int = 5, per_size: int = 200):
        """
        开启多线程保存金蝶数据
        :param formid:保存数据的类型编号
        :param model_list: 需要批量保存的数据条数
        :param max_worker: 开启的线程数, 默认五个
        :param per_size: 每个任务的大小（数据量）， 默认两百条
        """
        model_list_new = [model_list[i:i + per_size] for i in range(0, len(model_list), per_size)]
        with ThreadPoolExecutor(max_workers=max_worker) as executor:
            [executor.submit(self.save_kd_model_list, formid, task_data) for task_data in model_list_new]

    def query_kd_data(self, formid: str, data=None):
        """
        查询金蝶数据
        :param formid: 编号
        :param data: 需要查询字段的条件，字段唯一性（json格式）
        :return bool: 查询成功返回查询结果， 查询失败False
        """
        if data is None:
            data = {}
        response = self.api_sdk.View(formid, data).encode('utf-8')
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return res["Result"]['Result']
        else:
            return False

    def delete_kd_data(self, formid: str, data=None):
        """
        删除金蝶数据
        :param formid: 编号
        :param data: 需要删除字段的条件，字段唯一性（json格式）
        :return bool: 删除成功True， 删除失败False
        """
        if data is None:
            data = {}
        response = self.api_sdk.Delete(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return True
        else:
            return False

    def submit_kd_data(self, formid: str, data=None):
        """
        提交金蝶数据
        :param formid: 编号
        :param data: 需要删除字段的条件，字段唯一性
        :return bool: 提交成功True， 提交失败False
        """
        if data is None:
            data = {}
        response = self.api_sdk.Submit(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return True
        else:
            return False

    def audit_kd_data(self, formid: str, data=None):
        """
        审核金蝶数据
        :param formid: 调用金蝶的编号
        :param data: 需要审核的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.Audit(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return True
        else:
            return False

    def unaudit_kd_data(self, formid: str, data=None):
        """
        反审核金蝶数据
        :param formid: 调用金蝶的编号
        :param data: 需要反审核的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.UnAudit(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return True
        else:
            return False

    def execute_bill_query(self, data=None):
        """
        单据查询
        :param data: 单据查询的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.ExecuteBillQuery(data)
        res = json.loads(response)
        if len(res) > 0:
            return response
        else:
            return False

    def group_save_kd_data(self, formid: str, data=None):
        """
        分组保存
        :param formid: 调用金蝶的编号
        :param data: 需要分组保存的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.GroupSave(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return True
        else:
            return False

    def query_group_info(self, data=None):
        """
        分组信息查询
        :param data: 需要分组查询的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.QueryGroupInfo(data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return response
        else:
            return False

    def push_kd_data(self, formid: str, data=None):
        """
        下推金蝶数据
        :param formid: 调用金蝶的编号
        :param data: 需要分组保存的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.Push(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return response
        else:
            return False

    def allocate_kd_data(self, formid: str, data=None):
        """
        分配金蝶数据
        :param formid: 调用金蝶的编号
        :param data: 需要分组保存的数据（json格式）
        """
        if data is None:
            data = {}
        response = self.api_sdk.Allocate(formid, data)
        res = json.loads(response)
        if res["Result"]["ResponseStatus"]["IsSuccess"]:
            return response
        else:
            return False
