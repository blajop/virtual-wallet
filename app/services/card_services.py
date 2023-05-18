from app.models import Card, CardORM, UserExtended, User
from app.helpers import snowflake_ids as sf
from sqlalchemy.orm import Session
from app.data import engine


def add_card(user: User, card: Card):
    card.id = sf.generate_id()

    with Session(engine) as session:
        session.add(Card(**card.__dict__))
        session.commit()

    return card
