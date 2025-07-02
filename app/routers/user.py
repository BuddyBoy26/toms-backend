from fastapi import APIRouter, Depends
from ..routers.auth import get_current_user

from .. import schemas

router = APIRouter(tags=["users"])

@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current=Depends(get_current_user)):
    print("Current user:", current)
    return current