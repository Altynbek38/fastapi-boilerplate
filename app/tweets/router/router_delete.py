from fastapi import Depends, Response
from ..service import Service, get_service
from . import router
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


@router.delete("/shanyraks/{id}", status_code=200)
def delete_tweet(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    svc.repository.delete_tweets_by_id(id, jwt_data.user_id)

    return Response(status_code=200)
