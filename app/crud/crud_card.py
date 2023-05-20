from sqlalchemy.orm import Session
from app.data import engine
from app.models.card import Card, CardRegister
from app.models.user import User
from app import utils


def add_card(user: User, new_card: CardRegister):
    card_orm = Card.from_orm(new_card)
    card_orm.id = utils.util_id.generate_id()
    with Session(engine) as session:
        session.add(card_orm)
        session.commit()
        session.refresh(card_orm)
    return card_orm
