from app.models import Card, CardORM, UserExtended
from app.helpers import snowflake_ids as sf
from sqlalchemy.orm import Session
from app.data import engine


def add_card(user: UserExtended, card: Card):
    card.id = sf.generate_id()

    with Session(engine) as session:
        session.add(CardORM(**card.__dict__))
        session.commit()

    return card
