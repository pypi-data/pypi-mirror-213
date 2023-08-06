# _*_ coding:utf-8 _*_
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from loguru import logger
import pandas as pd
import chardet
from Crypto.Cipher import AES
import base64
import hashlib

BLOCK_SIZE = 16  # Bytes


class DateTool:
    """
    日期相关的使用方法
    1、获取当前日期和指定间隔月的时间：get_month_delta_date
    2、获取两个日期之间的 时间列表：get_date_list
    3、获取两个日期之间，指定间隔时间的日期列表：get_date_cycle_list

    """

    @classmethod
    def get_month_delta_date(cls, month_delta=1):
        """
        获取查询时间,起止时间
        默认查询上月数据
        :param month_delta: 间隔月数，少一月为1. 多一月为负一
        :return: ("20230101","20230201")
        """
        last_month_today = date.today() - relativedelta(months=month_delta)
        start_date = date(last_month_today.year, last_month_today.month, 1).strftime("%Y%m%d")
        this_month_today = date.today() - relativedelta(months=month_delta - 1)
        end_date = date(this_month_today.year, this_month_today.month, 1).strftime("%Y%m%d")
        return start_date, end_date

    @classmethod
    def get_date_list(cls, begin_date: str, end_date: str) -> list:
        """
        获取起始时间内每天的日期列表
        :param begin_date: 开始日期
        :param end_date: 结束日期
        :return list:日期列表
        """
        # 前闭后闭
        date_list = []
        start_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
        end_date = datetime.datetime.strptime(end_date, "%Y%m%d")
        while start_date <= end_date:
            date_str = start_date.strftime("%Y%m%d 00:00:00")
            date_list.append(date_str)
            start_date += datetime.timedelta(days=1)
        return date_list

    @classmethod
    def get_date_cycle_list(cls, start_date: str, end_date: str, cycle: int) -> list:
        """
        获取日期列表
        :param start_date: 开始时间
        :param end_date: 结束时间
        :param cycle: 查询的时间
        :return list: 返回日期列表
        """
        date_list = []
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        while True:
            date = {}
            middle_date = start_date + datetime.timedelta(days=cycle)
            # 结束时间
            if middle_date >= end_date:
                date["start"] = start_date
                date["end"] = end_date
                date_list.append(date)
                break
            else:
                date["start"] = start_date
                date["end"] = middle_date
                date_list.append(date)
                start_date = middle_date
        return date_list


class TableTool:
    """
    python 读取、写入excel数据工具包
    """

    @classmethod
    def load_excel_data(cls, file_type: str, file_path: str, sheet=None, skiprows: int = 0):
        """
        :param file_type: 文件类型 ：
        :param file_path: 文件路径
        :param sheet: 子表名称
        :param
        :return: 数据列表
        """
        with open(file_path, 'rb') as f:
            data = chardet.detect(f.read())
            encoding = data['encoding']
        try:
            if file_type == 'excel':
                df = pd.read_excel(file_path, sheet, skiprows=skiprows)
            elif file_type == 'csv':
                df = pd.read_csv(file_path, encoding=encoding, skiprows=skiprows)
            else:
                logger.error(f"{file_type} 文件类型错误。参数为：excel、csv")
                return
        except Exception as e:
            logger.error(f'error file:{e.__traceback__.tb_frame.f_globals["__file__"]}')
            logger.error(f'error line:{e.__traceback__.tb_lineno}')
            logger.error(f'error message:{e.args}')
            return
            # 将nan转化为None
        df.fillna('None', inplace=True)
        # 获取整个工作表数据
        data_all = df.values.tolist()
        return data_all


class EncryptTool:
    """
    加密工具包
    """

    @classmethod
    def do_pad(cls, text):
        return text + (BLOCK_SIZE - len(text) % BLOCK_SIZE) * \
               chr(BLOCK_SIZE - len(text) % BLOCK_SIZE)

    @classmethod
    def aes_encrypt(cls, key, data):
        """
        AES的ECB模式加密方法
        :param key: 密钥
        :param data:被加密字符串（明文）
        :return:密文
        """
        key = key.encode('utf-8')
        # 字符串补位
        data = cls.do_pad(data)
        cipher = AES.new(key, AES.MODE_ECB)
        # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
        result = cipher.encrypt(data.encode())
        encode_str = base64.b64encode(result)
        enc_text = encode_str.decode('utf-8')
        return enc_text

    @classmethod
    def md5_encrypt(cls, text: str):
        md = hashlib.md5()
        md.update(text.encode('utf-8'))
        return md.hexdigest()
