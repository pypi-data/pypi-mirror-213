from typing import List, Tuple, Sequence

from cai.pb.im.cs.cmd0x388 import RspBody, GetPttUrlRsp
from cai.pb.highway.ptt_center import RspBody as VideoUpRsp

from .utils import itoa
from .models import UploadResponse, ImageUploadResponse


def decode_upload_image_resp(data: bytes) -> ImageUploadResponse:
    pkg = decode_d388_rsp(data).tryup_img_rsp[0]
    if pkg.result != 0:
        return ImageUploadResponse(
            resultCode=pkg.result, message=pkg.fail_msg.decode()
        )

    if pkg.file_exit:
        if pkg.img_info:
            info = pkg.img_info
            # fuck: pkg.fileId != pkg.fileid
            return ImageUploadResponse(
                isExists=True,
                fileId=pkg.fileid,
                hasMetaData=True,
                fileType=info.file_type,
                width=info.file_width,
                height=info.file_height,
            )
        else:
            return ImageUploadResponse(isExists=True, fileId=pkg.fileid)
    return ImageUploadResponse(
        isExists=False,
        fileId=pkg.fileid,
        uploadAddr=parse_addr(pkg.up_ip, pkg.up_port),
        uploadKey=pkg.up_ukey,
    )


def parse_addr(ip_list: Sequence[int], port_list: Sequence[int]) -> List[Tuple[str, int]]:
    return [(itoa(a), p) for a, p in zip(ip_list, port_list)]


def decode_upload_ptt_resp(data: bytes) -> UploadResponse:
    pkg = decode_d388_rsp(data).tryup_ptt_rsp[0]
    if pkg.result != 0:
        return UploadResponse(
            resultCode=pkg.result, message=pkg.fail_msg.decode()
        )

    if pkg.file_exit:
        return UploadResponse(isExists=True, fileId=pkg.fileid)
    return UploadResponse(
        isExists=False,
        uploadAddr=[(itoa(a), p) for a, p in zip(pkg.up_ip, pkg.up_port)],
        uploadKey=pkg.up_ukey,
    )


def decode_get_ptt_url_rsp(data: bytes) -> GetPttUrlRsp:
    pkg = decode_d388_rsp(data).getptt_url_rsp[0]
    if pkg.result != 0:
        raise ConnectionError(pkg.result, pkg.fail_msg)
    return pkg


def decode_d388_rsp(data: bytes) -> RspBody:
    return RspBody.FromString(data)


def decode_video_upload_resp(data: bytes) -> VideoUpRsp:
    return VideoUpRsp.FromString(data)
