from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from sqlmodel import Session

from app import crud, deps
from app.error_models.user_errors import FileError
from app.models import User, UserBase, UserUpdate
from app.models.msg import Msg

router = APIRouter()


@router.get("", response_model=list[User])
def get_users(
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    return crud.user.get_multi(db)


@router.post("/profile/avatar", response_model=Msg, status_code=201)
def add_avatar(
    logged_user: User = Depends(deps.get_current_user),
    file: UploadFile = File(...),
) -> Msg | HTTPException:
    try:
        return crud.user.add_avatar(user=logged_user, file=file)
    except FileError as err:
        raise HTTPException(status_code=400, detail=err.args[0])


@router.delete("/profile/avatar", status_code=204)
def delete_avatar(
    logged_user: User = Depends(deps.get_current_user),
):
    try:
        return crud.user.delete_avatar(logged_user)
    except FileError as err:
        raise HTTPException(status_code=404, detail=err.args[0])


@router.get("/profile", response_model=User)
def profile_info(logged_user: User = Depends(deps.get_current_user)):
    return logged_user


@router.put("/profile", response_model=User)
def update_profile(
    edit: UserUpdate,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    return crud.user.update(db=db, db_obj=logged_user, obj_in=edit)


@router.get("/{identifier}", response_model=UserBase)
def get_user(
    identifier: str,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    """
    Returns a User model from username, email or id search
    """
    user = crud.user.get(db, identifier)

    if not user:
        raise HTTPException(status_code=404)
    return user


@router.post("/{identifier}/friends", response_model=UserBase)
def add_friend(
    id: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if user != logged_user:
        raise HTTPException(status_code=403, detail="Cannot add friends to other users")

    result = crud.user.add_friend(user=user, db=db, friend=id)
    if not result:
        raise HTTPException(
            status_code=409, detail="User is already in your contact list"
        )

    return result


@router.get("/{identifier}/friends", response_model=List[UserBase])
def get_friends(
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if user != logged_user:
        raise HTTPException(status_code=403, detail="Cannot view other user's friends")
    friend_list = user.friends

    return friend_list


@router.delete("/{identifier}/friends", status_code=204)
def remove_friend(
    id: str,
    user: User = Depends(deps.get_user_from_path),
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if user != logged_user:
        raise HTTPException(
            status_code=403, detail="Cannot remove friends from other users"
        )

    result = crud.user.remove_friend(user=user, db=db, friend=id)
    if not result:
        raise HTTPException(
            status_code=404, detail="The user is not in your friend list"
        )

    return Response(status_code=204)
