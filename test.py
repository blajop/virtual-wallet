from time import sleep
from currencies import Currency

# currency = Currency("BGN")
# print(currency.get_money_format("13"))


# print(currency.get_money_format(13.99))


# print(currency.get_money_format("13,2313,33"))


from snowflake import SnowflakeGenerator, Snowflake

flake = next(SnowflakeGenerator(5))
sleep(5)
flake2 = next(SnowflakeGenerator(2))

sf = Snowflake.parse(flake)
print(sf)
sf2 = Snowflake.parse(flake2)

print(sf.datetime)
print(sf2.datetime)
