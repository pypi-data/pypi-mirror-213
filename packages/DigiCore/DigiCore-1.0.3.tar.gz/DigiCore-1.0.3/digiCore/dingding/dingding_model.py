# _*_ coding:utf-8 _*_
from typing import Optional

from pydantic import BaseModel


class AtMobile(BaseModel):
    atMobiles: Optional[list] = []
    isAtAll: Optional[bool] = False


class TextMsg(BaseModel):
    project_title: str
    subserver: str
    text: str


class Text(BaseModel):
    """
    文本消息结构
    """
    msgtype: Optional[str] = "text"
    text: Optional[dict] = {}
    at: Optional[dict] = AtMobile.construct()


class MarkdownMsg(BaseModel):
    title: Optional[str] = " "
    text: Optional[str] = ""


class Markdown(BaseModel):
    msgtype: Optional[str] = 'markdown'
    markdown: Optional[dict] = MarkdownMsg.construct()
    at: Optional[dict] = AtMobile.construct()


class LinkMsg(BaseModel):
    text: Optional[str] = ""
    title: Optional[str] = ""
    picUrl: Optional[str] = ""
    messageUrl: Optional[str] = ""


class Link(BaseModel):
    msgtype: Optional[str] = 'link'
    link: Optional[dict] = LinkMsg.construct()

