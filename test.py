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


# from app.utils import util_id

# print(util_id.generate_id())
# print(util_id.datetime_from_id(7055597939821920257))
