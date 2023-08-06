"""MessageSvc message models.

This module is used to define message models.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

import abc
from enum import IntEnum
from dataclasses import dataclass
from typing import List, Sequence, Union, Optional

from cai.pb.im.msg.msg_body import Ptt


class PokeType(IntEnum):
    ChuoYiChuo = 0
    BiXin = 2
    DianZan = 3
    XinSui = 4
    SixSixSix = 5
    FangDaZhao = 6


class Element(abc.ABC):
    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError


@dataclass
class ForwardNode:
    from_uin: int
    nickname: str
    send_time: int
    message: Sequence["Element"]


@dataclass
class ForwardMessage(Element):
    from_group: int
    res_id: str
    file_name: str
    nodes: List[ForwardNode]
    brief: Optional[str] = "[聊天记录]"

    def add_node(self, from_uin: int, nickname: str, send_time: int, message: Sequence["Element"]):
        self.nodes.append(
            ForwardNode(
                from_uin,
                nickname,
                send_time,
                message
            )
        )

    @property
    def type(self):
        return "forward_message"


@dataclass
class ReplyElement(Element):
    seq: int
    time: int
    sender: int
    message: List[Element]
    troop_name: Optional[str] = None

    @property
    def type(self) -> str:
        return "reply"


@dataclass
class TextElement(Element):
    content: str

    @property
    def type(self) -> str:
        return "text"


@dataclass
class FaceElement(Element):
    id: int

    @property
    def type(self) -> str:
        return "face"


@dataclass
class SmallEmojiElement(Element):
    id: int
    text: str
    # byte: bytes

    @property
    def type(self) -> str:
        return "small_emoji"


@dataclass
class AtAllElement(Element):
    @property
    def type(self) -> str:
        return "at_all"


@dataclass
class ImageElement(Element):
    filename: str
    size: int
    width: int
    height: int
    md5: bytes
    id: Optional[int] = 0
    url: Optional[str] = None
    filetype: Optional[int] = 1000
    is_emoji: Optional[bool] = False

    @property
    def type(self) -> str:
        return "image"

    def to_flash(self) -> "FlashImageElement":
        return FlashImageElement(
            filename=self.filename,
            filetype=self.filetype,
            size=self.size,
            width=self.width,
            height=self.height,
            md5=self.md5,
            id=self.id,
            url=self.url,
        )


@dataclass
class FlashImageElement(ImageElement):
    @property
    def type(self) -> str:
        return "flash_image"


@dataclass
class VoiceElement(Element):
    file_name: str
    file_type: int
    file_id: int
    from_uin: int
    md5: bytes
    size: int
    group_file_key: bytes
    url: Optional[str] = None
    time: int = 0

    @property
    def type(self) -> str:
        return "voice"

    @property
    def _pb_reserve(self) -> bytes:
        return bytes([8, 0, 40, 0, 56, 0])

    def _to_ptt(self) -> Ptt:
        return Ptt(
            file_type=self.file_type,
            src_uin=self.from_uin,
            file_md5=self.md5,
            file_name=self.file_name.encode(),
            file_size=self.size,
            pb_reserve=self._pb_reserve,
            valid=True,
        )


@dataclass
class PokeElement(Element):
    id: Union[int, PokeType] = 0
    name: str = ""
    strength: int = 0
    double_hit: int = 0

    @property
    def type(self) -> str:
        return "poke"


@dataclass
class AtElement(Element):
    target: int
    display: Optional[str] = ""

    @property
    def type(self) -> str:
        return "at"


@dataclass
class RichMsgElement(Element):
    """
    service_id:
      case -1:
        json
      case 0:
        light_app
      default:
        xml
    """

    content: bytes
    service_id: Optional[int] = -2

    @property
    def type(self) -> str:
        return "rich_msg"


@dataclass
class ShakeElement(Element):
    stype: int = 0
    uin: int = 0

    @property
    def type(self) -> str:
        return "shake"


@dataclass
class CustomDataElement(Element):
    data: bytes

    @property
    def type(self) -> str:
        return "custom_daata"


@dataclass
class GroupFileElement(Element):
    name: str
    size: int
    path: str
    md5: bytes

    @property
    def type(self) -> str:
        return "group_file"


@dataclass
class VideoElement(Element):
    file_name: str
    file_md5: bytes
    file_uuid: bytes
    file_size: int
    file_time: int  # sec
    source: str  # camera or
    thumb_size: int
    thumb_md5: bytes

    @property
    def type(self) -> str:
        return "video"
