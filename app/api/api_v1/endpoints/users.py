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
from app.api import deps
from app.models.user import User, UserCreate
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


@router.get("/{identifier}", response_model=User)
def get_user(identifier: str, db: Session = Depends(deps.get_db)):
    """
    Returns a User model from username, email or id search
    """
    user = app.crud.user.get(db, identifier)
    if not user:
        return Response(status_code=404)
    return user


@router.post("/signup")
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

    registered_user = crud.user.create(db, new_user)

    background_tasks.add_task(
        util_mail.send_new_account_email,
        registered_user.email,
        registered_user.username,
    )

    return JSONResponse(
        content={
            "user": jsonable_encoder(registered_user),
            "msg": "Link for email verification has been sent to your declared email",
        }
    )


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
