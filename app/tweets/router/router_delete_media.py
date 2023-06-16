from fastapi import Depends, UploadFile
from typing import List
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.delete("/shanyraks/{id}/media")
def delete_files(
    url: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    svc.repository.delete_media(id, jwt_data.user_id)
    svc.s3_service.delete_file(url)

    return {"msg": files}
