import uuid

from models import *

def goods() -> None:
    with session_maker() as session:
        print(f"{'ID':5} {'Стоимость':<10} {'Количество':<12} Название")
        print("="*54)
        products = session.query(Product).all()
        for product in products:
            print(f"{product.id:<5} {product.cost:<10} {product.quantity:<12} {product.name}")

def sign_up() -> None:
    with session_maker() as session:
        username = input("Create your username: ")
        password = input("Create your password: ")
        user = User(username=username, password=password, points=0)
        session.add(user)
        session.commit()
        session.refresh(user)
    print(f"User = {username} = is created")

def sign_in() -> str | None:
    username = input("Enter your username: ")
    if User.is_exist(username):
        password = input("Enter your password: ")
        with session_maker() as session:
            query = select(User.password).where(User.username == username)
            result = session.execute(query).fetchone()[0]
            if password == result:
                return username
            else:
                print("Wrong password")
                return None
    else:
        print("User does not exist")
        return None

def profile(user_current, id_current):
    with session_maker() as session:
        query = select(User.points).where(User.username == user_current)
        points = session.execute(query).fetchone()[0]
        user = session.get(User, id_current)

        print(f"""=== {user_current} ===
Поинтов: {points}
Заказы:""")
        print("-"*54)
        print(f"{'Дата':<20} {'Кол-во':<7} {'Сумма':<7} {'Название'}")
        for i in User.orders_list(user):
            print(f"{str(i[0]):<20} {i[1]:<7} {i[2]*i[1]:<7} {i[3]}")

def use_ticket(uuid: str, user_id) -> None:
    with session_maker() as session:
        if Ticket.valid_ticket(uuid):
            user = session.get(User, user_id)
            user.points += 20
            session.commit()
            session.refresh(user)

            query = select(Ticket.id).where(Ticket.uuid == uuid)
            ticket_id = session.execute(query).fetchone()[0]
            ticket = session.get(Ticket, ticket_id)
            ticket.available = False
            session.commit()
            session.refresh(ticket)
            query = select(User.points).where(User.id == user_id)
            points = session.execute(query).fetchone()[0]
            print(f"""Вы успешно обменяли тикет на 20 поинтов!
Теперь у вас {points} поинтов""")
        else:
            print("Ticket does not exist or was used")

def buy(product_id, buying_quantity, user_id) -> None:
    with session_maker() as session:
        query = select(Product.quantity, Product.cost).where(Product.id == product_id)
        result = session.execute(query).fetchall()
        if result != [] and result[0] != 0:
            buying_cost = result[0][1]
            total_cost = buying_cost * buying_quantity
            user = session.get(User, user_id)
            if user.points >= total_cost:
                user.points -= total_cost
                session.commit()
                session.refresh(user)

                oder = Order(user_id=user_id, product_id=product_id ,count=buying_quantity)
                session.add(oder)
                session.commit()
                session.refresh(oder)
            else:
                print("Not enough points")
        else:
            print("Purchase failed")

#================ СЛУЖЕБНЫЕ =========================================================

def tickets():
    with session_maker() as session:
        print(f"{'=== Tickets available ===':^48}")
        print(f"{'id':3} {'available':<10} {'user':5} {'uuid':30}")
        print("="*54)
        tickets = session.query(Ticket).limit(5).all()
        for ticket in tickets:
            print(f"{ticket.id:<3} {ticket.available:<10} {ticket.user:<5} {ticket.uuid:<30}")

def show_users():
    with session_maker() as session:
        print(f"{'id':3} {'username':15} {'password':<15} {'points':5}")
        print("="*54)
        users = session.query(User).all()
        for user in users:
            print(f"{user.id:<3} {user.username:<15} {user.password:<15} {user.points:<5}")

def add_tickets():
    for i in range(10):
        with session_maker() as session:
            ticket = Ticket(uuid=str(uuid.uuid4()), available=True, user=0)
            session.add(ticket)
            session.commit()
            session.refresh(ticket)

def add_product(cost, quantity, name):
    with session_maker() as session:
        product = Product(cost=cost, quantity=quantity, name=name)
        session.add(product)
        session.commit()
        session.refresh(product)
    return product