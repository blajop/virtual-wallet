from fastapi import HTTPException
from sqlmodel import Session, or_, select
from app import crud
from app.crud.base import CRUDBase
from app.error_models.card_errors import CardDataError
from app.models.card import Card, CardBase, CardCreate
from app.models.user import User
from app.models.msg import Msg
from app.utils import util_id
from sqlalchemy import exc as sqlExc


class CRUDCard(CRUDBase[Card, CardBase, CardCreate]):
    def get(self, db: Session, card_identifier: str, user: User) -> Card | None:
        found_card = db.exec(
            select(Card).filter(
                or_(
                    Card.number == card_identifier,
                    Card.id == card_identifier,
                )
            )
        ).first()
        if found_card and (user in found_card.users or crud.user.is_admin(user)):
            return found_card

    def add_card(
        self, db: Session, user: User, new_card: CardCreate
    ) -> Card | Msg | CardDataError:
        card_orm = Card(
            number=new_card.number,
            expiry=new_card.expiry.datetime_,
            holder=new_card.holder,
            cvc=new_card.cvc,
        )
        if found_card := self.get(db, card_orm.number):
            # real-world logic for card verification by banks should be included otherwise
            if not all(
                (
                    found_card.expiry == card_orm.expiry,
                    found_card.holder == card_orm.holder,
                    found_card.cvc == card_orm.cvc,
                )
            ):
                raise CardDataError(
                    "This card # already exists with different credentials"
                )
            if user in found_card.users:
                return Msg(msg="You already have this card")
            card_orm = found_card
        else:
            card_orm.id = util_id.generate_id()

        card_orm.users.append(user)
        db.add(card_orm)
        db.commit()
        db.refresh(card_orm)

        return card_orm


card = CRUDCard(Card)
