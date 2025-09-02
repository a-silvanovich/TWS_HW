from datetime import datetime
from sqlalchemy import create_engine, Integer, String, select, ForeignKey, func, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship

engine = create_engine('sqlite:///shop.db', echo=False)
session_maker = sessionmaker(bind=engine, autocommit=False)

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    orders: Mapped[list["Order"]] = relationship("Order", lazy="select", back_populates="products")

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    points: Mapped[int] = mapped_column(Integer)

    tickets: Mapped[list["Ticket"]] = relationship("Ticket", lazy="select", back_populates="users")
    orders: Mapped[list["Order"]] = relationship("Order", lazy="select", back_populates="users")

    @staticmethod
    def is_exist(username: str) -> bool:
        with session_maker() as session:
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                return False
            else:
                return True

    def orders_list(self) -> list:
        orders_list = []
        with (session_maker() as session):
            query = select(Order.order_date, Order.count, Product.cost, Product.name).outerjoin(Order.products)
            query = query.where(Order.user_id == self.id)
            orders = session.execute(query).all()
            for i in orders:
                orders_list.append(i)
            return orders_list


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    available: Mapped[bool] = mapped_column(Boolean)
    user: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="RESTRICT"))

    users: Mapped["User"] = relationship("User", lazy="select", back_populates="tickets")

    @staticmethod
    def valid_ticket(uuid: str) -> bool:
        with session_maker() as session:
            check = session.query(Ticket).filter(Ticket.uuid == uuid).first()
            if check is None:
                return False
            else:
                query = select(Ticket.available).where(Ticket.uuid == uuid)
                result = session.execute(query).fetchone()[0]
                if result:
                    return True
                else:
                    return False

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="RESTRICT"))
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    order_date: Mapped[datetime] = mapped_column(server_default=func.now())

    users: Mapped["User"] = relationship("User", lazy="select", back_populates="orders")
    products: Mapped["Product"] = relationship("Product", lazy="select", back_populates="orders")