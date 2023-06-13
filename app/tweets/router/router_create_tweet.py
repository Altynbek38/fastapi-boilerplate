from fastapi import Depends, Response, HTTPException
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateTweetRequest(AppModel):
    user_id = str
    content: str
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str


@router.post("/shanyraks/")
def create_tweet(
    input: CreateTweetRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    user_id = jwt_data.user_id
    input_dict = input.dict()
    input_dict['user_id'] = user_id
    try:
        svc.repository.create_tweet(input_dict)
        return Response(status_code=200)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to insert data")

