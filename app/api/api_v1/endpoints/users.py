from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
)
from sqlmodel import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app import crud
import app
from app import utils
from app.api import deps
from app.error_models.user_errors import DataTakenError
from app.models.user import User, UserBase, UserCreate
from app.utils import util_mail

router = APIRouter()


@router.get("", response_model=list[User])
def get_users(db: Session = Depends(deps.get_db)):
    return crud.user.get_multi(db)


@router.get("/profile", response_model=User)
def profile_info(logged_user: User = Depends(deps.get_current_user)):
    if not logged_user:
        raise HTTPException(
            status_code=401, detail="You must be logged in to see your profile"
        )
    return logged_user


@router.get("/{identifier}", response_model=UserBase)
def get_user(identifier: str, db: Session = Depends(deps.get_db)):
    """
    Returns a User model from username, email or id search
    """
    user = crud.user.get(db, identifier)

    if not user:
        raise HTTPException(status_code=404)
    return user


@router.post("/signup", response_model=UserBase)
def sign_up_user(
    new_user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    logged_user: User = Depends(deps.get_current_user),
):
    if logged_user:
        raise HTTPException(
            status_code=403, detail="You should be logged out in order to register"
        )
    try:
        registered_user = crud.user.create(db, new_user)
    except DataTakenError as err:
        raise HTTPException(status_code=409, detail=err.args[0])

    background_tasks.add_task(
        util_mail.send_new_account_email,
        registered_user.email,
        registered_user.username,
    )

    return registered_user


@router.get("/verify/{token}")
def verify_email(token, db: Session = Depends(deps.get_db)):
    user_email = util_mail.verify_email_link_token(token)
    user = crud.user.get(db, user_email)
    if not user:
        raise HTTPException(status_code=404, detail="Token user not found")
    return crud.user.confirm_email(db, db_obj=user)


#################


# @users_router.put("/password-change")
# def change_password(
#     password_update: PasswordUpdateModel,
#     current_user: Annotated[
#         UserPermissionsSchema, Security(auth.get_current_user, scopes=["write"])
#     ],
# ):
#     return user_services.update_password(current_user, password_update)


# @users_router.get("/verify/{vrfy_tkn}")
# async def verify_email_(vrfy_tkn: str = None):
#     if vrfy_tkn is None:
#         raise HTTPException(status_code=400)
#     user_services.verify_email(vrfy_tkn)

#     return RedirectResponse("/")


# @users_router.get("/verify")
# async def request_verify_email(
#     background_tasks: BackgroundTasks,
#     current_user: Annotated[UserPermissionsSchema, Security(auth.get_current_user)],
# ):
#     if not current_user:
#         raise HTTPException(status_code=401)
#     background_tasks.add_task(auth.send_email_verify, current_user)
#     return {
#         "msg": "Email sent successfully! The verification link is valid for 25 mins"
#     }


# @users_router.get("/privileges")
# async def privileged_users(
#     current_user: Annotated[
#         UserPermissionsSchema, Security(auth.get_current_user, scopes=["admin"])
#     ]
# ):
#     if not current_user:
#         raise HTTPException(status_code=401)
#     # if not current_user.is_admin:
#     #     raise HTTPException(status_code=403, detail='Admin endpoint')

#     return user_services.get_users_with_privileges()


# @users_router.put("/{id}/toggle_write_perm")
# def toggle_write_permissions(
#     subj_user_id: int,
#     current_user: Annotated[
#         UserPermissionsSchema, Security(auth.get_current_user, scopes=["admin"])
#     ],
# ):
#     if not current_user:
#         raise HTTPException(
#             status_code=401,
#             detail="You should be logged in as admin to toggle write permissions",
#         )

#     subject_user = user_services.get_user_by_id(subj_user_id)

#     return user_services.toggle_write_perm(subject_user)
