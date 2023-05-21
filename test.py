# from time import sleep
# from currencies import Currency
# from app.helpers.snowflake_ids import datetime_from_id, generate_id

# from app.models import User, UserExtended

# currency = Currency("BGN")
# print(currency.get_money_format("13"))


# print(currency.get_money_format(13.99))


# print(currency.get_money_format("13,2313,33"))


# from snowflake import SnowflakeGenerator, Snowflake

# flake = next(SnowflakeGenerator(5))
# sleep(5)
# flake2 = next(SnowflakeGenerator(2))

# sf = Snowflake.parse(flake)
# print(sf)
# sf2 = Snowflake.parse(flake2)

# print(sf.datetime)
# print(sf2.datetime)

# from app.services.mail_services import send_email, registration_mail

# user = UserExtended(
#     id=7064605652767784961,
#     username="stanimmmmm",
#     email="milchev.st@gmail.com",
#     phone="0877001859",
#     f_name="Stanislav",
#     l_name="Milchev",
# )

# data = {"subject": "Alo ne", "body": "Testing mailing au"}

# print(send_email(user, registration_mail(user)))


# id = generate_id()
# print(id)
# print(datetime_from_id(id))


# from app.helpers import currency_exchange

# amount_in_BGN = 47.30

# all_rates = currency_exchange.get_all_rates()
# rate = currency_exchange.get_rate(all_rates, "BGN", "CNY")
# amount_in_CNY = currency_exchange.exchange(rate, amount_in_BGN)


# currency = Currency("CNY")
# print(currency.get_money_format(f"{amount_in_CNY:.2f}"))

# from app.utils import util_mail

# util_mail.send_test_email("vray1@abv.bg")

# import app

# print(a := app.utils.util_id.generate_id())
# print(app.utils.util_id.datetime_from_id(a))


from typing import List, Optional

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine


class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )
    hero_id: Optional[int] = Field(
        default=None, foreign_key="hero.id", primary_key=True
    )


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heroes: List["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    teams: List[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")

        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_z_force, team_preventers],
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            teams=[team_preventers],
        )
        hero_spider_boy = Hero(
            name="Spider-Boy", secret_name="Pedro Parqueador", teams=[team_preventers]
        )
        session.add(hero_deadpond)
        session.add(hero_rusty_man)
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        print("Deadpond:", hero_deadpond)
        print("Deadpond teams:", hero_deadpond.teams)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man Teams:", hero_rusty_man.teams)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy Teams:", hero_spider_boy.teams)


def main():
    create_db_and_tables()
    create_heroes()


if __name__ == "__main__":
    main()
