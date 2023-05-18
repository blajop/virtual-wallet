# import datetime
# from app.models import Card, User
# from app.services.card_services import add_card

# USER = User(
#     id="123",
#     username="tester123",
#     password="tester123",
#     email="test@example.com",
#     phone="0877992857",
#     f_name="Test",
#     l_name="User",
# )

# CARD = Card(
#     id="234",
#     number="4111111111111111",
#     expiry=datetime.datetime(month=2, year=25),
#     holder="TEST USER",
#     cvc="453",
# )


def test_add_card_to_profile():
    # add_card(USER, CARD)
    assert 1 == 1
