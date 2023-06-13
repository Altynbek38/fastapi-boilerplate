from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from fastapi import Depends, HTTPException

from app.utils import AppModel

from ..service import Service, get_service
from . import router


class Update(AppModel):
    content: str
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str




@router.patch("/shanyraks/{id}", status_code=200)
def update_my_tweets(id: str, data: Update, svc: Service = Depends(get_service), jwt_data: JWTData = Depends(parse_jwt_user_data),):
    try:
        svc.repository.update_tweet(id, jwt_data.user_id ,data.dict())
        return {"message": "User data updated successfully"}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update user data")

