from fastapi import Depends, HTTPException, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router
from ...utils import AppModel


class UpdateCommentRequest(AppModel):
    content: str


@router.patch("shanyraks/{id:str}/comments")
def update_comment(
    comment_id: str,
    request: UpdateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    user_id = jwt_data.user_id
    success = svc.comment_repository.update_comment_by_id(
        comment_id=comment_id, user_id=user_id, data=request.dict()
    )
    if not success:
        raise HTTPException(status_code=404, detail="Could not update")
    return Response(status_code=200)
