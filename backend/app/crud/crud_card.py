from typing import List, Optional
from sqlmodel import Session, or_, select
from app.crud.base import CRUDBase
from app.error_models import CardDataError, CardNotFoundError
from app.models import Card, CardBase, CardCreate, CardShow, User, Msg
from app.models.card import Card
from app.utils import util_id, util_crypt


class CRUDCard(CRUDBase[Card, CardBase, CardCreate]):
    # Called with user arg from the router, internally used with 2 args.
    def get(
        self,
        db: Session,
        card_identifier: str,
        user: Optional[User] = None,
        admin_r: bool = False,
    ) -> Card | None:
        found_card: Card = db.exec(
            select(Card).filter(
                or_(
                    Card.number == util_crypt.encrypt(card_identifier),
                    Card.id == card_identifier,
                )
            )
        ).first()

        if not found_card:
            return None

        found_card.number = util_crypt.decrypt(found_card.number)
        found_card.cvc = util_crypt.decrypt(found_card.cvc)

        # for internal code reuse
        if (not user) and (not admin_r):
            return found_card

        if admin_r or (user in found_card.users):
            return found_card

        return None

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        user: Optional[User] = None,
        admin_r: bool = False,
    ) -> List[Card]:
        if admin_r:
            result = super().get_multi(db, skip=skip, limit=limit)
        else:
            result = (
                db.exec(
                    select(Card)
                    .offset(skip)
                    .limit(limit)
                    .filter(Card.id.in_(c.id for c in user.cards))
                )
                .unique()
                .all()
            )
        for card in result:
            card.number = util_crypt.decrypt(card.number)
            card.cvc = util_crypt.decrypt(card.cvc)

        return result

    def get_by_owner(self, db: Session, owner: User):
        result = db.exec(select(Card).where(Card.users.contains(owner))).unique().all()
        for card in result:
            card.number = util_crypt.decrypt(card.number)
            card.cvc = util_crypt.decrypt(card.cvc)

        return result

    def add_card(
        self, db: Session, user: User, new_card: CardCreate
    ) -> Card | Msg | CardDataError:
        card_orm = Card(
            number=util_crypt.encrypt(new_card.number),
            expiry=new_card.expiry.datetime_,
            holder=new_card.holder,
            cvc=util_crypt.encrypt(new_card.cvc),
        )
        if found_card := self.get(db, new_card.number):
            # real-world logic for card verification by banks should be included otherwise
            if not all(
                (
                    found_card.expiry == card_orm.expiry,
                    found_card.holder == card_orm.holder,
                    found_card.cvc == new_card.cvc,
                )
            ):
                raise CardDataError(
                    "This card # already exists with different credentials"
                )
            if user in found_card.users:
                raise CardDataError("You already have this card")
            found_card.number = util_crypt.encrypt(found_card.number)
            found_card.cvc = util_crypt.encrypt(found_card.cvc)
            card_orm = found_card
        else:
            card_orm.id = util_id.generate_id()

        card_orm.users.append(user)

        if found_card:
            db.add(card_orm)
        db.commit()

        return CardShow(
            number=util_crypt.decrypt(card_orm.number),
            expiry=card_orm.expiry.strftime("%m/%y"),
            holder=card_orm.holder,
        )

    def deregister_card(self, db: Session, card_identifier: str, user: User):
        """
        Removes a card attached to the account of the passed user.
        If other users have registered this card also,
        the card remains but is detached from the passed user account.
        """

        if not (found_card := self.get(db, card_identifier)):
            raise CardNotFoundError("There is no such card")
        if user not in found_card.users:
            raise CardNotFoundError("There is no such card within your access")
        if len(found_card.users) > 1:
            found_card.users.remove(user)
            found_card.number = util_crypt.encrypt(found_card.number)
            found_card.cvc = util_crypt.encrypt(found_card.cvc)
            db.commit()
        else:
            found_card.users.clear()
            db.delete(found_card)
            db.commit()

    def remove(self, db: Session, card_identifier: str):
        if not (found_card := self.get(db, card_identifier)):
            raise CardNotFoundError("There is no such card")

        found_card.users.clear()
        db.delete(found_card)
        db.commit()


card = CRUDCard(Card)
