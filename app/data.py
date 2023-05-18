import os
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

engine = sqlalchemy.create_engine(os.getenv("DB_ENGINE"))

# base_orm = declarative_base()

# class NewTableORM(base_orm):
#     __tablename__ = "new_table"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     kur = Column(Integer)

# class AddressORM(base_orm):
#     __tablename__ = "address"
#     idaddress = Column(Integer, primary_key=True)
#     address = Column(String)
#     user = Column(Integer, ForeignKey("new_table.id"))

# class Address(BaseModel):
#     idaddress : int
#     address : str
#     user :int
#     class Config:
#         orm_mode = True

# class NewTable(BaseModel):
#     id: int | None
#     name: str
#     kur: int
#     address: Address | None
#     class Config:
#         orm_mode = True


# with Session(engine) as session:
#     orm = NewTableORM(name='44T', kur=25)
#     pyd = NewTable.from_orm(orm)
#     print(pyd)
#     print(orm)
#     session.add(orm)
#     session.commit()

# with Session(engine) as session:
#     result = session.execute(select(NewTableORM, AddressORM).join_from(NewTableORM, AddressORM, isouter=False))
#     for row in result:
#         user = NewTable.from_orm(row[0])
#         addr = Address.from_orm(row[1])
#         user.address = addr
#         print(user)
#         print(addr)
# print(result)
# print(NewTable.from_orm(result))

# result = select(NewTableORM).where(NewTableORM.name == "44T")
# print(result)
