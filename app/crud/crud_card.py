# from app.models import Card, User
from sqlalchemy.orm import Session
from app.data import engine


def add_card(user: User, card: Card):
    card.id = app.utils.util_id.generate_id()

    with Session(engine) as session:
        session.add(Card(**card.__dict__))
        session.commit()

    return card
