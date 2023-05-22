from fastapi import HTTPException
from sqlmodel import Session, or_, select
from app import crud
from app.crud.base import CRUDBase
from app.models.card import Card
from app.models.transaction import Transaction, TransactionBase, TransactionCreate
from app.models.user import User
from app.models.msg import Msg
from app.models.wallet import Wallet
from app.utils import util_id, util_crypt
from sqlalchemy import exc as sqlExc


class CRUDTransaction(CRUDBase[Transaction, TransactionBase, TransactionCreate]):
    def get(self, db: Session, id: str, user: User):
        found_transaction = super().get(db, id)

        if not found_transaction:
            return None

        sender_item: Wallet | Card = (
            found_transaction.wallet_sen_obj
            if found_transaction.wallet_sen_obj
            else found_transaction.card_sen_obj
        )
        receiver_wallet = found_transaction.wallet_rec_obj

        if (
            crud.user.is_admin(user)
            or (user in sender_item)
            or (user in receiver_wallet)
        ):
            return found_transaction
        return None

    # def get(self, db: Session, id: str) -> Optional[ModelType]:
    #     return db.exec(select(self.model).where(self.model.id == id)).first()

    # def get_multi(
    #     self, db: Session, *, skip: int = 0, limit: int = 100
    # ) -> List[ModelType]:
    #     return db.exec(select(self.model).offset(skip).limit(limit)).unique().all()


transaction = CRUDTransaction(Transaction)
