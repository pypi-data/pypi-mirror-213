# _*_ coding: utf-8 _*_
# @Time : 2023/5/19
# @Author : 杨洋
# @Email ： yangyang@doocn.com
# @File : DigiCore
# @Desc :
import subprocess

from loguru import logger

# 查看已安装的包列表
import pkg_resources

installed_packages = [pkg.key for pkg in pkg_resources.working_set]

if 'kingdee.cdp.webapi.sdk' not in installed_packages:
    try:
        subprocess.call(['pip', 'install', '../kingdee.cdp.webapi.sdk-8.0.3-py3-none-any.whl'])
    except Exception as e:
        logger.error('金蝶安装包安装失败！')
