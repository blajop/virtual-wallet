from __future__ import annotations
from typing import Optional
from fastapi import Response, UploadFile
from sqlmodel import Session, or_, select

from app import utils
from app.core import security
from app.crud.base import CRUDBase
from app.error_models import DataTakenError
from app.error_models.user_errors import FileError
from app.models import User, UserCreate, UserUpdate, Scope, Msg
from app.models.user import UserSettings

import os
from PIL import Image


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(
        self, db: Session, new_user: UserCreate, referrer: User | None
    ) -> User | DataTakenError:
        if not self.user_data_taken(db, user=new_user):
            # Create the user object
            user_orm = User.from_orm(new_user)
            user_orm.id = utils.util_id.generate_id()
            user_orm.password = security.get_password_hash(user_orm.password)
            scope = db.scalar(select(Scope).filter(Scope.id == 2))
            user_orm.scopes.append(scope)

            db.add(user_orm)
            db.commit()
            db.refresh(user_orm)

            # Generate the user settings
            settings_id = utils.util_id.generate_id()
            settings = UserSettings(
                id=settings_id,
                user_id=user_orm.id,
            )

            user_orm.user_settings_obj = settings

        db.add(user_orm)
        db.commit()
        db.refresh(user_orm)

        if referrer:
            if referrer.user_settings_obj.referrals_left > 0:
                referrer.user_settings_obj.referrals_left - 1

                referrer.user_settings_obj.default_wallet_obj.balance + 20
                user_orm.user_settings_obj.default_wallet_obj + 20

        return user_orm

    def get_multi(self, db: Session, identifier: str | None) -> Optional[User]:
        if not identifier:
            return db.exec(select(User)).unique().all()

        search_query = f"%{identifier}%"

        return (
            db.scalars(
                select(self.model).where(
                    or_(
                        self.model.username.ilike(search_query),
                        self.model.f_name.ilike(search_query),
                        self.model.l_name.ilike(search_query),
                        self.model.email.ilike(search_query),
                        self.model.phone.ilike(search_query),
                    )
                )
            )
            .unique()
            .all()
        )

    def get(self, db: Session, identifier: str) -> Optional[User]:
        return db.scalars(
            select(self.model).where(
                or_(
                    self.model.id == identifier,
                    self.model.username == identifier,
                    self.model.email == identifier,
                    self.model.phone == identifier,
                )
            )
        ).first()

    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        update_data = obj_in

        if update_data.password:
            update_data.password = security.get_password_hash(update_data.password)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def confirm_email(self, db: Session, *, db_obj: User):
        db_obj.user_settings_obj.email_confirmed = True
        db.add(db_obj)
        db.commit()

        return Msg(msg="You successfully verified your email")

    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get(db, identifier=username)
        if not user:
            return None
        if not security.verify_password(password, user.password):
            return None
        return user

    def is_admin(self, user: User) -> bool:
        return "admin" in [sc.scope for sc in user.scopes]

    def user_data_taken(self, db: Session, *, user: UserCreate):
        result = db.scalar(select(User).filter(User.username == user.username))
        if result:
            raise DataTakenError("Username is already taken")

        result = db.scalar(select(User).filter(User.email == user.email))
        if result:
            raise DataTakenError("Email is already taken")

        result = db.scalar(select(User).filter(User.phone == user.phone))
        if result:
            raise DataTakenError("Phone number is already taken")

        return False

    def username_taken(self, db: Session, *, username: str):
        result = db.scalar(select(User).filter(User.username == username))
        if result:
            raise DataTakenError("Username is already taken")
        return False

    def email_taken(self, db: Session, *, email: str):
        result = db.scalar(select(User).filter(User.email == email))
        if result:
            raise DataTakenError("Email is already taken")
        return False

    def phone_taken(self, db: Session, *, phone: str):
        result = db.scalar(select(User).filter(User.phone == phone))
        if result:
            raise DataTakenError("Phone is already taken")
        return False

    def refer_friend(self, *, user: User, email: str, db: Session):
        if self.get(db, identifier=email):
            return Response(status_code=400, content="User is already registered")

        utils.util_mail.send_refferal_email(email_to=email, refferer=user)

        return Response(status_code=200)

    def add_friend(self, *, user: User, db: Session, friend: str):
        friend: User = self.get(db=db, identifier=friend)

        if friend in user.friends:
            return None

        user.friends.append(friend)

        db.add(user)
        db.commit()
        db.refresh(user)

        return friend

    def remove_friend(self, *, user: User, db: Session, friend: str):
        friend: User = self.get(db=db, identifier=friend)

        if friend not in user.friends:
            return None

        user.friends.remove(friend)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def add_avatar(self, *, user: User, file: UploadFile) -> Msg | FileError:
        cwd = os.getcwd()
        try:
            with Image.open(file.file, mode="r") as img:
                size = min(img.size)

                left = (img.width - size) // 2
                top = 0
                right = left + size
                bottom = size
                cropped_img = img.crop((left, top, right, bottom))

                resized_img = cropped_img.resize((600, 600))
                resized_img.save(
                    f"app/static/avatars/{user.id}.png",
                    format="PNG",
                )
            return Msg(msg="Successfully uploaded avatar!")
        except OSError as err:
            raise FileError("Cannot convert and upload file")

    def delete_avatar(self, user: User) -> Msg | FileError:
        cwd = os.getcwd()
        exp_file_path = os.path.join(cwd, f"app/static/avatars/{user.id}.jpg")
        if not os.path.exists(exp_file_path):
            raise FileError("There is no uploaded avatar.")

        os.remove(exp_file_path)

        return Msg(msg="Successfully deleted avatar!")


user = CRUDUser(User)
