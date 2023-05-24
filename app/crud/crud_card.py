from sqlmodel import Session, or_, select
from app import crud
from app.crud.base import CRUDBase
from app.error_models import CardDataError, CardNotFoundError
from app.models import Card, CardBase, CardCreate, CardShow, User, Msg
from app.utils import util_id, util_crypt


class CRUDCard(CRUDBase[Card, CardBase, CardCreate]):
    # Called with user arg from the router, internally used with 2 args.
    def get(self, db: Session, card_identifier: str, user: User = None) -> Card | None:
        """
        Gets a card available to the passed user (registered for his account or any card for user admin).
        Note: The output is a Card object with plain text number and cvc,
        so before updating it in the DB, they should be encrypted back.

        Arguments:
            db: Session
            user: User model
        Returns:
            Card model

        """
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
        if not user:
            return found_card

        if user in found_card.users or crud.user.is_admin(user):
            return found_card

    def add_card(
        self, db: Session, user: User, new_card: CardCreate
    ) -> Card | Msg | CardDataError:
        """
        Registers a card attached to the account of the passed user.

        Arguments:
            db: Session
            user: User model
        Returns:
            CardShow model
        Raises:
            CardDataError

        """
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
        # db.refresh(card_orm) # breaks the session of the tests and not needed in code for now
        return CardShow(
            number=util_crypt.decrypt(card_orm.number),
            expiry=card_orm.expiry.strftime("%m/%y"),
            holder=card_orm.holder,
        )

    def remove(self, db: Session, card_identifier: str, user: User):
        """
        Removes a card attached to the account of the passed user.
        If the other users have registered this card also,
        the card remains but is detached from the passed user account.
        - If the admin removes a card he is using together with other people,
        it is detached from his account only.
        - If the admin removes a card he is not using, the card is
        removed from the DB and detached from all connected accounts.
        Arguments:
            db: Session
            card_identifier: str : id or number of the card
            user: User model
        Returns:
            None
        Raises:
            CardNotFoundError

        """
        found_card = self.get(db, card_identifier)
        if not found_card:
            raise CardNotFoundError("There is no such card")
        if crud.user.is_admin(user) and user not in found_card.users:
            found_card.users.clear()
            db.delete(found_card)
            db.commit()
        else:
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


card = CRUDCard(Card)
