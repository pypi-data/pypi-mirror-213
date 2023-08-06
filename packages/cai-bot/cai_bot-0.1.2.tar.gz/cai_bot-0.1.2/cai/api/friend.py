"""Application Friend APIs.

:Copyright: Copyright (C) 2021-2021  cscs181
:License: AGPL-3.0 or later. See `LICENSE`_ for detail.

.. _LICENSE:
    https://github.com/cscs181/CAI/blob/master/LICENSE
"""

from typing import List, Optional, Tuple

from cai.client import FriendGroup
from cai.client import Friend as friend_t

from .base import BaseAPI
from .error import BotException
from ..client.pkg_builder import build_recall_private_msg_pkg
from ..pb.msf.msg.svc import PbMsgWithDrawResp


class Friend(BaseAPI):
    async def get_friend(
        self, friend_uin: int, cache: bool = True
    ) -> Optional[friend_t]:
        """Get account friend.

        This function wraps the :meth:`~cai.session.session.Session.get_friend`
        method of the session.

        Args:
            friend_uin (int): Friend account uin.
            cache (bool, optional):  Use cached friend list. Defaults to True.

        Returns:
            Friend: Friend object.
            None: Friend not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self.session.get_friend(friend_uin, cache)

    async def get_friend_list(self, cache: bool = True) -> List[friend_t]:
        """Get account friend list.

        This function wraps the :meth:`~cai.session.session.Session.get_friend_list`
        method of the session.

        Args:
            cache (bool, optional):  Use cached friend list. Defaults to True.

        Returns:
            List of :obj:`~cai.session.models.Friend`

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self._executor("get_friend_list", cache)

    async def get_friend_group(
        self, group_id: int, cache: bool = True
    ) -> Optional[FriendGroup]:
        """Get Friend Group.

        This function wraps the :meth:`~cai.session.session.Session.get_friend_group`
        method of the session.

        Args:
            group_id (int): Friend group id.
            cache (bool, optional):  Use cached friend group list. Defaults to True.

        Returns:
            FriendGroup: Friend group object.
            None: Friend group not exists.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend list failed.
            FriendListException: Get friend list returned non-zero ret code.
        """
        return await self._executor("get_friend_group", group_id, cache)

    async def get_friend_group_list(
        self, cache: bool = True
    ) -> List[FriendGroup]:
        """Get account friend group list.

        This function wraps the :meth:`~cai.session.session.Session.get_friend_group_list`
        method of the session.

        Args:
            cache (bool, optional):  Use cached friend group list. Defaults to True.

        Returns:
            List[FriendGroup]: Friend group list.

        Raises:
            RuntimeError: Error response type got. This should not happen.
            ApiResponseError: Get friend group list failed.
            FriendListException: Get friend group list returned non-zero ret code.
        """
        return await self._executor("get_friend_group_list", cache)

    async def recall_friend_msg(self, uin: int, msg: Tuple[int, int, int]):
        ret = PbMsgWithDrawResp.FromString(
            (
                await self.session.send_unipkg_and_wait(
                    "PbMessageSvc.PbMsgWithDraw",
                    build_recall_private_msg_pkg(
                        self.session.uin,
                        uin,
                        msg_list=[msg]
                    ).SerializeToString()
                )
            ).data
        ).c2c_with_draw[0]

        if ret.result not in (2, 3):
            raise BotException(ret.result, ret.errmsg)


__all__ = ["Friend"]
