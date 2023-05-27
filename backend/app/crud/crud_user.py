from __future__ import annotations
from typing import Optional
from fastapi import File, HTTPException, Response, UploadFile
from sqlmodel import Session, or_, select

from app import utils
from app.core import security
from app.crud.base import CRUDBase
from app.error_models import DataTakenError
from app.error_models.user_errors import FileError
from app.models import User, UserBase, UserCreate, UserUpdate, Scope, Msg
from app.models.user import UserSettings

import os
from PIL import Image


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def create(
        self, db: Session, new_user: UserCreate, referrer: User | None
    ) -> User | DataTakenError:
        """
        Registers a new user.

        Arguments:
            db: Session
            new_user: UserCreate model
        Returns:
            User model
        Raises:
            DataTakenError: Username/Email/Phone number already taken
        """
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
        # check referrer for referrals left. deduct if available and send both money
        # seperate in another func and call it here
        if referrer:
            if referrer.user_settings_obj.referrals_left > 0:
                referrer.user_settings_obj.referrals_left - 1
                # get the currency of main wallet
                # figure out what do if no wallets/no main wallet.
                # referrer should be asked to create a wallet when he send a referral link
                # just store money in the user account? maybe start with a default wallet?
                #
                # perform the transaction
                referrer.user_settings_obj.default_wallet_obj.balance + 20
                # a default wallet needs to be created upon registration if we choose that approach
                user_orm.user_settings_obj.default_wallet_obj + 20

        return user_orm

    def get(self, db: Session, identifier: str) -> Optional[User]:
        return db.scalars(
            select(self.model).where(
                or_(
                    self.model.id == identifier,
                    self.model.username == identifier,
                    self.model.email == identifier,
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

    def refer_friend(self, *, user: User, email: str, db: Session):
        # check if email in system
        if self.get(db, identifier=email):
            return Response(status_code=400, content="User is already registered")

        # send email with invite link
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
                # Calculate the size of the square
                size = min(img.size)

                # Crop the image to a square
                left = (img.width - size) // 2
                top = 0
                right = left + size
                bottom = size
                cropped_img = img.crop((left, top, right, bottom))

                # Resize the img
                resized_img = cropped_img.resize((600, 600))

                resized_img.save(
                    os.path.join(cwd, f"app/static/avatars/{user.id}.jpg"),
                    format="JPEG",
                )
            return Msg(msg="Successfully uploaded avatar!")
        except OSError as err:
            print(err)
            raise FileError("Cannot convert and upload file")


user = CRUDUser(User)
