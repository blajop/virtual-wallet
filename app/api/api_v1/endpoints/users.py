from datetime import timedelta
from typing import Annotated
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Response,
    Security,
)
from app.core import security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.crud import crud_mail, crud_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
import app
from app.api import deps

router = APIRouter(prefix="/users", tags=["01. API / Users"])

# admin may toggle the write access of a user even irrespective of his confirming or not the email


@router.get("/")  # , response_model=User
def get_users():
    return app.crud.get_users()


@router.post("/login")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return security.get_token(form_data)


@router.get("/profile")  # , response_model=User
def profile_info(current_user: Annotated[User, Depends(deps.get_current_user)]):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="You must be logged in to see your profile"
        )
    return current_user.__dict__


@router.post("/signup")
def sign_up_user(
    current_user: Annotated[User, Depends(deps.get_current_user)],
    new_user: UserRegistration,
    background_tasks: BackgroundTasks,
):
    if current_user:
        raise HTTPException(
            status_code=403, detail="You should be logged out in order to register"
        )
    registered_user = crud_user.register_user(new_user)
    generated_id = registered_user.id
    background_tasks.add_task(
        crud_mail.send_email,
        new_user,
        crud_mail.registration_mail(new_user, generated_id),
    )
    return JSONResponse(
        content={
            "registered_user": jsonable_encoder(registered_user),
            "msg": "Link for email verification has been sent to your declared email",
        }
    )


# @users_router.get("/{search_param}")
# def get_user(search_param: str):
#     user = user_services.search(search_param)
#     if not user:
#         return Response(status_code=404)
#     return user


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
