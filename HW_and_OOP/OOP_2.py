""" Задание 1 ======================================================="""
from copy import deepcopy
from random import random


class GameCharacter:
    def __init__(self, name: str, __hp: int, level: int):
        self.name = name
        self.__hp = __hp
        self.level = level

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, value: int):
        self.__hp = 100 if value > 100 else value

    def _level_up(self) -> None:
        self.level += 1

    def attack(self, other_character: 'GameCharacter') -> None:
        other_character.__hp -= 10

    @classmethod
    def create_character(cls, name: str) -> 'GameCharacter':
        return cls(name, 100, 1)

    @staticmethod
    def compare_character(character1: 'GameCharacter', character2: 'GameCharacter') -> 'GameCharacter':
        if character1.level >= character2.level:
            return character1
        elif character1.level < character2.level:
            return character2


# ch_1 = GameCharacter.create_character("Moonknight")
# ch_2 = GameCharacter.create_character("Skywalker")
# ch_1.attack(ch_2)
# print(ch_2.hp)
# ch_1._level_up()
# print(ch_1.level)
# print(GameCharacter.compare_character(ch_1, ch_2).name)
# ch_1.hp += 20
# print(ch_1.hp)

""" Задание 2 ======================================================="""


class Store:
    def __init__(self, name: str, products: list[dict]):
        self.name = name
        self.products = products

    def add_product(self, name: str, price: int, quantity: int) -> None:
        product = {'name': name, 'price': price, 'quantity': quantity}
        self.products.append(product)

    def remove_product(self, name: str) -> None:
        for product in self.products:
            if product['name'] == name:
                self.products.remove(product)

    def update_price(self, name: str, new_price: int) -> None:
        for product in self.products:
            if product['name'] == name:
                product['price'] = new_price

    def sell_products(self, name: str, quantity: int) -> None:
        for product in self.products:
            if product['name'] == name:
                if product['quantity'] >= quantity:
                    product['quantity'] -= quantity
                else:
                    print("Not enough quantity")

    def get_inventory(self) -> list[dict]:
        return self.products

    def find_most_expensive(self) -> dict:
        result = self.products[0]
        for product in self.products:
            if product['price'] > result['price']:
                result = product
        return result

    def find_cheapest(self) -> dict:
        result = self.products[0]
        for product in self.products:
            if product['price'] < result['price']:
                result = product
        return result


# store_1 = Store("Store 1", [])
# print(store_1.get_inventory())
# store_1.add_product("Pen", 20, 5)
# store_1.add_product("Pencil", 30, 9)
# store_1.add_product("Notebook", 200, 2)
# print(store_1.get_inventory())
# store_1.update_price("Pen", 25)
# print(store_1.get_inventory())
# print(store_1.find_most_expensive())
# print(store_1.find_cheapest())
# store_1.remove_product("Pencil")
# print(store_1.get_inventory())
# store_1.sell_products("Notebook", 5)
# store_1.sell_products("Pen", 4)
# print(store_1.get_inventory())

""" Задание 3 ======================================================="""


class Book:
    def __init__(self, name: str, author: str, publication: int, status: bool = True):
        self.name = name
        self.author = author
        self.publication = publication
        self.status = status

    def info(self) -> None:
        return print(
            f"Name: {self.name}\nAuthor: {self.author}\nYear of publication: {self.publication}\nAvailability: {self.status}")

    def mark_as_taken(self) -> None:
        self.status = False

    def mark_as_returned(self) -> None:
        self.status = True


class Library:
    def __init__(self, name: str, books: list = []):
        self.name = name
        self.books = books

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def remove_book(self, book: Book) -> None:
        self.books.remove(book)

    def find_by_author(self, author: str) -> list[Book]:
        result = []
        for book in self.books:
            if book.author == author:
                result.append(book)
        return result

    def find_by_year(self, year: int) -> list[Book]:
        result = []
        for book in self.books:
            if book.publication == year:
                result.append(book)
        return result

    def available_books(self) -> list[Book]:
        result = []
        for book in self.books:
            if book.status:
                result.append(book)
        return result

    def taken_books(self) -> list[Book]:
        result = []
        for book in self.books:
            if not book.status:
                result.append(book)
        return result


# book_1 = Book("Book 1", "Author 1", 2007)
# book_1.info()
# book_1.mark_as_taken()
# book_1.info()
# book_2 = Book("Book 2", "Author 2", 2007)
# book_3 = Book("Book 3", "Author 1", 2010)
# lib_1 = Library("Library 1")
# lib_1.add_book(book_1)
# lib_1.add_book(book_2)
# lib_1.add_book(book_3)
# print(lib_1.books)
# print(lib_1.available_books())
# print(lib_1.taken_books())
# print(lib_1.find_by_year(2007))
# print(lib_1.find_by_author("Author 1"))
# lib_1.remove_book(book_1)
# print(lib_1.books)

""" Задание 4 ======================================================="""


class Wallet:
    def __init__(self, id: int, owner: str, __balance: int):
        self.id = id
        self.owner = owner
        self.__balance = __balance

    def deposit(self, amount: int) -> None:
        if amount > 0:
            self.__balance += amount
            self.__apply_bonus(amount)

    def withdraw(self, amount: int) -> None:
        if self.__balance >= amount:
            self.__balance -= amount
        else:
            print("Not enough money")

    def transfer_to(self, other: 'Wallet', amount: int) -> None:
        if self.__balance >= amount > 0:
            self.__balance -= amount
            other.__balance += amount
        else:
            print("Not enough money")

    def __apply_bonus(self, amount: int) -> None:
        self.__balance += int(0.01 * amount)

    @property
    def balance(self):
        return self.__balance

    @staticmethod
    def info(self):
        return print(f"ID: {self.id}\nOwner: {self.owner}\nBalance: {self.balance}")


# w1 = Wallet(1, "user_1", 100)
# w2 = Wallet(2, "user_2", 200)
# Wallet.info(w1)
# w1.deposit(200)
# Wallet.info(w1)
# w1.withdraw(305)
# w1.withdraw(55)
# Wallet.info(w1)
# w1.transfer_to(w2, 250)
# w1.transfer_to(w2, 200)
# Wallet.info(w1)
# Wallet.info(w2)

""" Задание 5 ======================================================= """


class Order:
    def __init__(self, id: int, products: list[dict], status: str):
        self.id = id
        self.products = products
        self.status = status

    def calculate_total(self):
        total = 0
        for product in self.products:
            total += product['price'] * product['quantity']
        return total

    def add_item(self, name, price, quantity):
        self.products.append({'name': name, 'price': price, 'quantity': quantity})

    def remove_item(self, name):
        for product in self.products:
            if product['name'] == name:
                self.products.remove(product)

    def change_status(self, status: str) -> None:
        self.status = status

    def __str__(self):
        return f"{'=' * 20}\nID: {self.id}\nStatus: {self.status}\nProducts: {self.products}\n{'=' * 20}"


class OrderSystem:
    def __init__(self, orders: list[Order]):
        self.orders = orders

    def create_order(self, id: int, products: list[dict], status: str) -> None:
        self.orders.append(Order(id, products, status))

    def get_order_by_id(self, id: int) -> Order | None:
        for order in self.orders:
            if order.id == id:
                return order

    def get_orders_by_status(self, status: str) -> list[Order]:
        orders = []
        for order in self.orders:
            if order.status.lower() == status.lower():
                orders.append(order)
        return orders

    def get_total_revenue(self):
        total = 0
        for order in self.orders:
            if order.status.lower() == "завершен":
                total += order.calculate_total()
        return total


# order1 = Order(1, [], "новый")
# print(order1)
# order1.add_item("pen", 100, 2)
# order1.add_item("pencil", 150, 7)
# print(order1)
# print(order1.calculate_total())
# order1.remove_item("pen")
# order1.change_status("Завершен")
# print(order1)
# sys1 = OrderSystem([order1])
# sys1.create_order(2, [], "новый")
# print(sys1.get_order_by_id(2))
# print(sys1.get_total_revenue())
# for order in sys1.get_orders_by_status("НоВЫй"):
#     print(order)

""" Задание 6 ======================================================= """


class Car:
    def __init__(self, brand, model, year, fuel, milage):
        self.brand = brand
        self.model = model
        self.year = year
        self.fuel = fuel
        self.milage = milage

    def drive(self, km):
        if self.__check_fuel(km):
            self.fuel -= km * 0.1
            self.milage += km

    def refuel(self, liters):
        self.fuel += liters

    def info(self):
        return f"{'Brand':>10} : {self.brand}\n{'Model':>10} : {self.model}\n{'Year':>10} : {self.year}\n{'Fuel':>10} : {self.fuel}\n{'Milage':>10} : {self.milage}\n"

    def __check_fuel(self, km):
        if km * 0.1 <= self.fuel:
            return True
        else:
            return False

    @staticmethod
    def age(car):
        return 2025 - car.year

# car1 = Car("Mitsubishi", "Colt", 2012, 10, 50000)
# print(car1.info())
# print(Car.age(car1))
# car1.drive(250)
# print(car1.info())
# car1.drive(58)
# car1.refuel(7)
# print(car1.info())

""" Задание 7 ======================================================= """
class Inventory:
    def __init__(self, items: list[dict]):
        self.items = items

    def add_item(self, name: str, weight: int, value: int) -> None:
        self.items.append({'name': name, 'weight': weight, 'value': value})

    def remove_item(self, name: str) -> None:
        for item in self.items:
            if item['name'] == name:
                self.items.remove(item)

    def get_total_weight(self) -> int:
        total = 0
        for item in self.items:
            total += item['weight']
        return total

    def get_total_value(self) -> int:
        total = 0
        for item in self.items:
            total += item['value']
        return total

    def find_heaviest(self) -> dict:
        if len(self.items) != 0:
            result = self.items[0]
            for item in self.items:
                if item['weight'] > result['weight']:
                    result = item
            return result

    def find_most_valuable(self) -> dict:
        if len(self.items) != 0:
            result = self.items[0]
            for item in self.items:
                if item['value'] > result['value']:
                    result = item
            return result

    def sort_by_value(self) -> list[dict]:
        return sorted(self.items, key=lambda item: item['value'], reverse=False)

    def sort_by_weight(self) -> list[dict]:
        return sorted(self.items, key=lambda item: item['weight'], reverse=False)

# inv1 = Inventory([])
# inv1.add_item("Sword", 15, 340)
# inv1.add_item("Axe", 20, 410)
# inv1.add_item("Staff", 12, 555)
# print(inv1.get_total_weight())
# print(inv1.get_total_value())
# print(inv1.find_heaviest())
# print(inv1.find_most_valuable())
# print(inv1.sort_by_value())
# print(inv1.sort_by_weight())
# inv1.remove_item("Axe")
# print(inv1.items)

""" Задание 8 ======================================================= """
class Gym:
    def __init__(self, name: str, clients: list[dict]):
        self.name = name
        self.clients = clients

    def add_client(self, name: str, age: int) -> None:
        self.clients.append({'name': name, 'age': age, 'membership': False})

    def remove_client(self, name: str) -> None:
        for client in self.clients:
            if client['name'] == name:
                self.clients.remove(client)

    def activate_membership(self, name: str) ->None:
        for client in self.clients:
            if client['name'] == name:
                client['membership'] = True

    def deactivate_membership(self, name: str) -> None:
        for client in self.clients:
            if client['name'] == name:
                client['membership'] = False

    def get_active_clients(self) -> list[dict]:
        result = []
        for client in self.clients:
            if client['membership']:
                result.append(client)
        return result

    def find_youngest_client(self) -> dict | None:
        if len(self.clients) != 0:
            result = self.clients[0]
            for client in self.clients:
                if client['age'] < result['age']:
                    result = client
            return result

    def find_oldest_client(self) -> dict | None:
        if len(self.clients) != 0:
            result = self.clients[0]
            for client in self.clients:
                if client['age'] > result['age']:
                    result = client
            return result

    def average_age(self) -> float:
        total_age = sum(client['age'] for client in self.clients)
        return round(total_age / len(self.clients),1) if len(self.clients) > 0 else 0

# gym1 = Gym("Bro", [])
# print(gym1.find_youngest_client())
# print(gym1.find_oldest_client())
# print(gym1.average_age())
# print(gym1.get_active_clients())
# gym1.add_client("ivan", 33)
# gym1.add_client("vasiliy", 28)
# gym1.add_client("kseniya", 21)
# print(gym1.find_youngest_client())
# print(gym1.find_oldest_client())
# print(gym1.average_age())
# gym1.activate_membership("ivan")
# gym1.activate_membership("kseniya")
# print(gym1.get_active_clients())
# gym1.remove_client("ivan")
# print(gym1.clients)

""" Задание 9 ======================================================= """
class Playlist:
    def __init__(self, name: str, tracks: list[dict]):
        self.name = name
        self.tracks = tracks

    def add_track(self, name, atrist, duration) -> None:
        self.tracks.append({'name': name, 'atrist': atrist, 'duration': duration})

    def remove_track(self, name: str) -> None:
        for track in self.tracks:
            if track['name'] == name:
                self.tracks.remove(track)

    def total_duration(self) -> int:
        result = 0
        for track in self.tracks:
            result += track['duration']
        return result

    def find_by_artist(self, artist: str) -> list[dict]:
        result = []
        for track in self.tracks:
            if track['atrist'] == artist:
                result.append(track)
        return result

    def longest_track(self) -> dict:
        if len(self.tracks) != 0:
            result = self.tracks[0]
            for track in self.tracks:
                if track['duration'] > result['duration']:
                    result = track
            return result

    def shortest_track(self) -> dict:
        if len(self.tracks) != 0:
            result = self.tracks[0]
            for track in self.tracks:
                if track['duration'] < result['duration']:
                    result = track
            return result

    def shuffle(self):
        track_list = deepcopy(list(self.tracks))
        random.shuffle(track_list)
        return track_list

    def sort_by_duration(self) -> list[dict]:
        return sorted(self.tracks, key=lambda track: track['duration'], reverse=False)

# pl1= Playlist("Number 1", [])
# print(pl1.total_duration())
# print(pl1.longest_track())
# print(pl1.shortest_track())
# print(pl1.find_by_artist("lady gaga"))
# pl1.add_track("song 1", "artist 1", 123)
# pl1.add_track("song 2", "artist 2", 456)
# pl1.add_track("song 3", "artist 1", 245)
# print(pl1.total_duration())
# print(pl1.longest_track())
# print(pl1.shortest_track())
# print(pl1.find_by_artist("artist 1"))
# print(pl1.sort_by_duration())
# pl1.remove_track("song 3")
# print(pl1.tracks)

""" Задание 9 ======================================================= """
class Student:
    def __init__(self, name: str, grades: list[int]):
        self.name = name
        self.grades = grades

    def add_grade(self, grade: int) -> None:
        self.grades.append(grade)

    def average_grade(self) -> float:
        total_grades = sum(self.grades)
        return round(total_grades / len(self.grades), 1) if len(self.grades) > 0 else 0

    def info(self):
        return f"Student: {self.name:<10} === Grades: {self.grades}"

class StudyGroup:
    def __init__(self, name: str, students: list[Student]):
        self.name = name
        self.students = students

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def remove_student(self, name: str) -> None:
        for student in self.students:
            if student.name == name:
                self.students.remove(student)

    def find_best_student(self) -> Student:
        if len(self.students) != 0:
            result = self.students[0]
            for student in self.students:
                if student.average_grade() > result.average_grade():
                    result = student
            return result

    def group_average(self) -> float:
        result = 0
        for student in self.students:
            result += student.average_grade()
        return round(result / len(self.students), 1) if len(self.students) > 0 else 0

    def list_students(self) -> None:
        for student in self.students:
            print(student.info())

# group1 = StudyGroup("Group 1", [])
# group1.list_students()
# print(group1.find_best_student())
# print(group1.group_average())
# group1.add_student(Student("Student 1", [8, 7, 9]))
# group1.add_student(Student("Student 2", [5, 7, 7]))
# group1.add_student(Student("Student 3", [9, 9, 10]))
# group1.students[0].add_grade(7)
# group1.list_students()
# print(group1.find_best_student().info())
# print(group1.group_average())
# group1.remove_student("Student 1")
# group1.list_students()