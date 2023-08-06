"""Application Group APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import List, Union, Optional, Tuple

from cai.api.error import BotException

from cai.client import GroupMember, GroupMessage, pkg_builder
from cai.client import Group as group_t
from cai.client.message_service.decoders import TroopMessageDecoder
from cai.client.pkg_builder import build_recall_group_msg_pkg
from cai.pb.msf.msg.svc import PbMsgWithDrawResp, PbGetGroupMsgResp

from .base import BaseAPI


class Group(BaseAPI):
    async def get_group(
        self, group_id: int, cache: bool = True
    ) -> Optional[group_t]:
        """Get Group.

        This function wraps the :meth:`~cai.session.session.Session.get_group`
        method of the session.

        Args:
            group_id (int): Group id.
            cache (bool, optional):  Use cached friend group list. Defaults to True.

        Returns:
            Group: Group object.
            None: Group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self._executor("get_group", group_id, cache)

    async def get_group_list(self, cache: bool = True) -> List[group_t]:
        """Get account group list.

        This function wraps the :meth:`~cai.session.session.Session.get_group_list`
        method of the session.

        Args:
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List[Group]: Group list.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupListException: Get group list returned non-zero ret code.
        """
        return await self._executor("get_group_list", cache)

    async def get_group_member_list(
        self, group: Union[int, group_t], cache: bool = True
    ) -> Optional[List[GroupMember]]:
        """Get account group member list.

        This function wraps the :meth:`~cai.session.session.Session.get_group_member_list`
        method of the session.

        Args:
            group (Union[int, Group]): Group id or group object want to get members.
            cache (bool, optional): Use cached group list. Defaults to True.

        Returns:
            List[GroupMember]: Group member list.
            None: Group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get group list failed.
            GroupMemberListException: Get group member list returned non-zero ret code.
        """
        return await self._executor("get_group_member_list", group, cache)

    async def set_group_admin(self, group: int, uin: int, is_admin: bool):
        await self.session.send_unipkg_and_wait(
            "OidbSvc.0x55c_1",
            pkg_builder.build_set_admin_pkg(
                target_uin=uin,
                group=group,
                is_admin=is_admin
            )
        )

    async def mute_member(self, group: int, uin: int, duration: int):
        await self.session.send_unipkg_and_wait(
            "OidbSvc.0x570_8",
            pkg_builder.build_mute_member_pkg(
                target_uin=uin,
                group=group,
                duration=duration
            )
        )

    async def send_group_nudge(self, group: int, uin: int):
        await self.session.send_unipkg_and_wait(
            "OidbSvc.0xed3",
            pkg_builder.build_send_nudge_pkg(
                target_uin=uin,
                group=group
            )
        )

    async def recall_group_msg(self, group: int, msg: Tuple[int, int, int]):
        ret = PbMsgWithDrawResp.FromString(
            (
                await self.session.send_unipkg_and_wait(
                    "PbMessageSvc.PbMsgWithDraw",
                    build_recall_group_msg_pkg(
                        group,
                        msg_list=[msg]
                    ).SerializeToString()
                )
            ).data
        ).group_with_draw[0]

        if ret.result:
            raise BotException(ret.result, ret.errmsg)

    async def get_group_msg(
        self,
        group_code: int,
        begin_seq: int,
        end_seq: int,
        filter_recall_msg=True
    ) -> List[GroupMessage]:
        ret = PbGetGroupMsgResp.FromString(
            (
                await self.session.send_unipkg_and_wait(
                    "MessageSvc.PbGetGroupMsg",
                    pkg_builder.build_get_group_msg_req(
                        group_code,
                        begin_seq,
                        end_seq
                    ).SerializeToString()
                )
            ).data
        )
        if ret.result:
            raise BotException(ret.result, ret.errmsg)

        return [*(
            TroopMessageDecoder.decode(msg) for msg in ret.msg
            if filter_recall_msg and msg.head.time
        )]


__all__ = ["Group"]
