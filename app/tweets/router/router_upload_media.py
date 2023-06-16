from fastapi import Depends, UploadFile
from typing import List
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


@router.post("/shanyraks/{id}/media")
def upload_files(
    id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    print("HELLO")
    result = []
    for file in files:
        url = svc.s3_service.upload_file(file.file, file.filename)
        result.append(url)
    print("LOOOOOH")
    svc.repository.upload_media(id, jwt_data.user_id, result)

    return {"msg": files}
